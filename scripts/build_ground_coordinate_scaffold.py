from __future__ import annotations

import csv
import json
import math
import os
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

# Keep Matplotlib and font caches out of the repo and out of unwritable home
# directories. This avoids noisy warnings during repeated scaffold rebuilds.
TMP_CACHE_ROOT = Path(tempfile.gettempdir()) / "predictions-ground-scaffold-cache"
TMP_CACHE_ROOT.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(TMP_CACHE_ROOT / "mplconfig"))
os.environ.setdefault("XDG_CACHE_HOME", str(TMP_CACHE_ROOT / "xdg-cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


REPO_ROOT = Path(__file__).resolve().parents[1]
CONSTRAINTS_PATH = REPO_ROOT / "data" / "ground_coordinate_constraints.json"

MODE_COLORS = {
    "road": "#38bdf8",
    "rail": "#34d399",
    "ferry": "#c084fc",
    "ship": "#22d3ee",
}
VALIDATION_COLOR = "#f59e0b"


@dataclass(frozen=True)
class Constraint:
    a: str
    b: str
    distance_km: float
    mode: str
    tier: str
    estimated: bool
    solver_role: str
    note: str
    source_type: str | None = None
    source_url: str | None = None


def load_constraints() -> dict:
    return json.loads(CONSTRAINTS_PATH.read_text())


def region_output_paths(region: str) -> dict[str, Path]:
    slug = region.lower()
    return {
        "json": REPO_ROOT / "docs" / "data" / f"{slug}_ground_scaffold.json",
        "csv": REPO_ROOT / "docs" / "data" / f"{slug}_ground_scaffold.csv",
        "png": REPO_ROOT / "docs" / "assets" / f"{slug}_ground_scaffold.png",
    }


def region_cities(payload: dict, region: str) -> list[str]:
    return [entry["city"] for entry in payload["cities"] if entry["region"] == region]


def region_constraints(payload: dict, region: str) -> list[Constraint]:
    allowed = set(region_cities(payload, region))
    constraints = []
    for entry in payload["constraints"]:
        if entry["a"] not in allowed or entry["b"] not in allowed:
            continue
        constraints.append(
            Constraint(
                a=entry["a"],
                b=entry["b"],
                distance_km=float(entry["distance_km"]),
                mode=entry["mode"],
                tier=entry["tier"],
                estimated=bool(entry["estimated"]),
                solver_role=entry["solver_role"],
                note=entry["note"],
                source_type=entry.get("source_type"),
                source_url=entry.get("source_url"),
            )
        )
    return constraints


def core_constraints(constraints: list[Constraint]) -> list[Constraint]:
    return [constraint for constraint in constraints if constraint.solver_role == "core"]


def validation_constraints(constraints: list[Constraint]) -> list[Constraint]:
    return [constraint for constraint in constraints if constraint.solver_role == "validation"]


def solve_distance_matrix(cities: list[str], constraints: list[Constraint]) -> np.ndarray:
    # The regional scaffolds are solved from graph distances, not from globe
    # coordinates. Australia happens to have a dense surface-distance matrix,
    # while corridor regions like New Zealand are naturally sparse trunks with
    # a few branches. Converting the core graph to all-pairs shortest-path
    # distances lets both kinds of regions share one non-circular solver.
    index = {city: idx for idx, city in enumerate(cities)}
    n = len(cities)
    matrix = np.full((n, n), np.inf, dtype=float)
    np.fill_diagonal(matrix, 0.0)

    for constraint in core_constraints(constraints):
        i = index[constraint.a]
        j = index[constraint.b]
        matrix[i, j] = min(matrix[i, j], constraint.distance_km)
        matrix[j, i] = min(matrix[j, i], constraint.distance_km)

    for k in range(n):
        matrix = np.minimum(matrix, matrix[:, [k]] + matrix[[k], :])

    if not np.all(np.isfinite(matrix)):
        missing = np.argwhere(~np.isfinite(matrix))
        unresolved = [
            f"{cities[i]}-{cities[j]}"
            for i, j in missing
            if i < j
        ]
        preview = ", ".join(unresolved[:6]) if unresolved else "unknown pairs"
        raise ValueError(f"Core graph is disconnected for region solve; unresolved pairs include: {preview}")

    return matrix


def classical_mds(distance_matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    n = len(distance_matrix)
    centering = np.eye(n) - np.ones((n, n)) / n
    gram = -0.5 * centering @ (distance_matrix ** 2) @ centering
    eigenvalues, eigenvectors = np.linalg.eigh(gram)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    coords = eigenvectors[:, :2] @ np.diag(np.sqrt(np.maximum(eigenvalues[:2], 0.0)))
    return coords, eigenvalues


def shift_to_origin(cities: list[str], coords: np.ndarray, origin_city: str) -> np.ndarray:
    origin = coords[cities.index(origin_city)]
    return coords - origin


def core_counts(constraints: list[Constraint]) -> dict:
    measured = [item for item in core_constraints(constraints) if not item.estimated]
    estimated = [item for item in core_constraints(constraints) if item.estimated]

    return {
        "measured_count": len(measured),
        "estimated_count": len(estimated),
        "measured_by_mode": dict(sorted(Counter(item.mode for item in measured).items())),
        "estimated_by_mode": dict(sorted(Counter(item.mode for item in estimated).items())),
    }


def validation_rows(cities: list[str], coords: np.ndarray, constraints: list[Constraint]) -> list[dict]:
    index = {city: idx for idx, city in enumerate(cities)}
    rows = []

    for constraint in validation_constraints(constraints):
        i = index[constraint.a]
        j = index[constraint.b]
        direct_km = float(np.linalg.norm(coords[i] - coords[j]))
        rows.append(
            {
                "a": constraint.a,
                "b": constraint.b,
                "mode": constraint.mode,
                "tier": constraint.tier,
                "observed_path_km": round(constraint.distance_km, 2),
                "scaffold_direct_km": round(direct_km, 2),
                "gap_km": round(constraint.distance_km - direct_km, 2),
                "note": constraint.note,
                "source_url": constraint.source_url,
            }
        )

    return rows


def write_json(
    payload: dict,
    region: str,
    cities: list[str],
    coords: np.ndarray,
    eigenvalues: np.ndarray,
    constraints: list[Constraint],
    output_path: Path,
) -> None:
    meta = payload["regions"][region]
    city_rows = []

    for city, (x_value, y_value) in zip(cities, coords):
        city_rows.append(
            {
                "city": city,
                "x_rel_km": round(float(x_value), 2),
                "y_rel_km": round(float(y_value), 2),
            }
        )

    output = {
        "version": payload["version"],
        "region": region,
        "title": meta.get("title", f"{region.replace('_', ' ').title()} Ground Scaffold"),
        "status": meta.get("status", "provisional"),
        "method": meta.get("method_note", "classical MDS on all-pairs shortest-path distances built from core surface constraints"),
        "anti_circular_note": meta.get(
            "anti_circular_note",
            "The solve itself does not consume GPS/WGS84 coordinates. Absolute inter-region theta/r locking remains separate work.",
        ),
        "frame_note": meta["display_note"],
        "origin_city": meta["origin_city"],
        "core_constraint_summary": core_counts(constraints),
        "eigenvalues": [round(float(value), 3) for value in eigenvalues[:4]],
        "cities": city_rows,
        "validation_edges": validation_rows(cities, coords, constraints),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2))


def write_csv(cities: list[str], coords: np.ndarray, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["city", "x_rel_km", "y_rel_km"])
        for city, (x_value, y_value) in zip(cities, coords):
            writer.writerow([city, round(float(x_value), 2), round(float(y_value), 2)])


def edge_style(constraint: Constraint) -> tuple[str, float, tuple[int, int] | str]:
    color = MODE_COLORS.get(constraint.mode, "#38bdf8")
    alpha = 0.45 if constraint.estimated else 0.78
    linestyle: tuple[int, int] | str = (0, (3, 3)) if constraint.estimated else "solid"
    return color, alpha, linestyle


def render_plot(region: str, payload: dict, cities: list[str], coords: np.ndarray, constraints: list[Constraint], output_path: Path) -> None:
    meta = payload["regions"][region]
    fig, ax = plt.subplots(figsize=(7.4, 5.6), dpi=180)
    fig.patch.set_facecolor("#071121")
    ax.set_facecolor("#071121")

    city_index = {city: idx for idx, city in enumerate(cities)}
    legend_handles: list[Line2D] = []
    seen_labels: set[str] = set()

    for constraint in core_constraints(constraints):
        i = city_index[constraint.a]
        j = city_index[constraint.b]
        x_vals = [coords[i, 0], coords[j, 0]]
        y_vals = [coords[i, 1], coords[j, 1]]
        color, alpha, linestyle = edge_style(constraint)
        ax.plot(x_vals, y_vals, color=color, alpha=alpha, linewidth=1.35, linestyle=linestyle, zorder=1)

        label = f"{constraint.mode} core edge"
        if constraint.estimated:
            label = f"estimated {constraint.mode} edge"
        if label not in seen_labels:
            legend_handles.append(Line2D([0], [0], color=color, linewidth=1.4, linestyle=linestyle, label=label))
            seen_labels.add(label)

    if validation_constraints(constraints):
        for constraint in validation_constraints(constraints):
            i = city_index[constraint.a]
            j = city_index[constraint.b]
            x_vals = [coords[i, 0], coords[j, 0]]
            y_vals = [coords[i, 1], coords[j, 1]]
            ax.plot(
                x_vals,
                y_vals,
                color=VALIDATION_COLOR,
                alpha=0.58,
                linewidth=1.0,
                linestyle=(0, (6, 4)),
                zorder=1,
            )
        legend_handles.append(
            Line2D([0], [0], color=VALIDATION_COLOR, linewidth=1.0, linestyle=(0, (6, 4)), label="validation edge")
        )

    point_color = "#f8fafc"
    accent_color = "#60a5fa"
    ax.scatter(coords[:, 0], coords[:, 1], s=34, color=point_color, edgecolors=accent_color, linewidths=0.8, zorder=3)

    for city, (x_value, y_value) in zip(cities, coords):
        ax.text(x_value + 24, y_value + 18, city, color="#e2e8f0", fontsize=8.4, zorder=4)

    ax.set_title(meta.get("title", f"{region.replace('_', ' ').title()} Ground Scaffold"), color="#e2e8f0", fontsize=13, pad=12)
    ax.text(
        0.5,
        1.01,
        meta["display_note"],
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        color="#94a3b8",
        fontsize=8.1,
    )
    ax.set_xlabel("relative x (km)", color="#94a3b8")
    ax.set_ylabel("relative y (km)", color="#94a3b8")
    ax.tick_params(colors="#94a3b8", labelsize=8)
    ax.grid(color="#1e293b", linewidth=0.6, alpha=0.7)

    for spine in ax.spines.values():
        spine.set_color("#334155")

    if legend_handles:
        ax.legend(
            handles=legend_handles,
            loc="lower right",
            facecolor="#071121",
            edgecolor="#334155",
            labelcolor="#cbd5e1",
            fontsize=8,
        )

    ax.set_aspect("equal", adjustable="box")
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def build_region(payload: dict, region: str) -> None:
    cities = region_cities(payload, region)
    if not cities:
        return

    constraints = region_constraints(payload, region)
    meta = payload["regions"][region]
    distance_matrix = solve_distance_matrix(cities, constraints)
    coords, eigenvalues = classical_mds(distance_matrix)
    coords = shift_to_origin(cities, coords, origin_city=meta["origin_city"])

    output_paths = region_output_paths(region)
    write_json(payload, region, cities, coords, eigenvalues, constraints, output_paths["json"])
    write_csv(cities, coords, output_paths["csv"])
    render_plot(region, payload, cities, coords, constraints, output_paths["png"])

    counts = core_counts(constraints)
    print(f"{meta.get('title', region)} generated")
    print(f"Core measured edges: {counts['measured_count']}")
    print(f"Core estimated edges: {counts['estimated_count']}")
    print(f"JSON: {output_paths['json']}")
    print(f"CSV:  {output_paths['csv']}")
    print(f"PNG:  {output_paths['png']}")


def main() -> None:
    payload = load_constraints()
    for region in payload["regions"]:
        build_region(payload, region)


if __name__ == "__main__":
    main()
