from __future__ import annotations

import csv
import json
import math
import os
import tempfile
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


REPO_ROOT = Path(__file__).resolve().parents[1]
CONSTRAINTS_PATH = REPO_ROOT / "data" / "ground_coordinate_constraints.json"
JSON_OUTPUT_PATH = REPO_ROOT / "docs" / "data" / "australia_ground_scaffold.json"
CSV_OUTPUT_PATH = REPO_ROOT / "docs" / "data" / "australia_ground_scaffold.csv"
PNG_OUTPUT_PATH = REPO_ROOT / "docs" / "assets" / "australia_ground_scaffold.png"

for output_path in (JSON_OUTPUT_PATH, CSV_OUTPUT_PATH, PNG_OUTPUT_PATH):
    output_path.parent.mkdir(parents=True, exist_ok=True)


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


def load_constraints() -> dict:
    return json.loads(CONSTRAINTS_PATH.read_text())


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
            )
        )
    return constraints


def dense_distance_matrix(cities: list[str], constraints: list[Constraint]) -> np.ndarray:
    # This scaffold intentionally mirrors the user's road-MDS method:
    # use the dense Australia road matrix as the relative-geometry solve layer,
    # while keeping rail values as validation-only upper-bound checks.
    index = {city: idx for idx, city in enumerate(cities)}
    distance_matrix = np.zeros((len(cities), len(cities)), dtype=float)

    for constraint in constraints:
        if constraint.solver_role != "core":
            continue
        if constraint.mode != "road":
            continue
        i = index[constraint.a]
        j = index[constraint.b]
        distance_matrix[i, j] = constraint.distance_km
        distance_matrix[j, i] = constraint.distance_km

    if np.any(distance_matrix == 0.0) and len(cities) > 1:
        missing = np.argwhere((distance_matrix == 0.0) & (~np.eye(len(cities), dtype=bool)))
        if len(missing) > 0:
            pairs = ", ".join(f"{cities[i]}-{cities[j]}" for i, j in missing[:6])
            raise ValueError(f"Dense road matrix is incomplete; missing pairs include: {pairs}")

    return distance_matrix


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


def measured_counts(constraints: list[Constraint]) -> tuple[int, int]:
    measured = sum(1 for item in constraints if item.solver_role == "core" and not item.estimated and item.mode == "road")
    estimated = sum(1 for item in constraints if item.solver_role == "core" and item.estimated and item.mode == "road")
    return measured, estimated


def validation_rows(cities: list[str], coords: np.ndarray, constraints: list[Constraint]) -> list[dict]:
    index = {city: idx for idx, city in enumerate(cities)}
    rows = []

    for constraint in constraints:
        if constraint.solver_role != "validation":
            continue
        i = index[constraint.a]
        j = index[constraint.b]
        direct_km = float(np.linalg.norm(coords[i] - coords[j]))
        rows.append(
            {
                "a": constraint.a,
                "b": constraint.b,
                "mode": constraint.mode,
                "tier": constraint.tier,
                "observed_path_km": round(constraint.distance_km, 1),
                "scaffold_direct_km": round(direct_km, 1),
                "gap_km": round(constraint.distance_km - direct_km, 1),
                "note": constraint.note,
            }
        )

    return rows


def write_json(
    payload: dict,
    cities: list[str],
    coords: np.ndarray,
    eigenvalues: np.ndarray,
    constraints: list[Constraint],
) -> None:
    measured, estimated = measured_counts(constraints)
    rows = []

    for city, (x_value, y_value) in zip(cities, coords):
        rows.append(
            {
                "city": city,
                "x_rel_km": round(float(x_value), 1),
                "y_rel_km": round(float(y_value), 1),
            }
        )

    output = {
        "version": payload["version"],
        "title": "Australia Ground Scaffold",
        "status": "provisional",
        "method": "classical MDS on the dense Australia road matrix from session working notes",
        "anti_circular_note": "The solve itself does not consume GPS/WGS84 coordinates. Absolute SH theta/r remain unresolved under OPEN-016.",
        "frame_note": payload["regions"]["australia"]["display_note"],
        "core_road_constraints": {
            "measured_count": measured,
            "estimated_count": estimated,
        },
        "eigenvalues": [round(float(value), 3) for value in eigenvalues[:4]],
        "cities": rows,
        "validation_edges": validation_rows(cities, coords, constraints),
    }
    JSON_OUTPUT_PATH.write_text(json.dumps(output, indent=2))


def write_csv(cities: list[str], coords: np.ndarray) -> None:
    with CSV_OUTPUT_PATH.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["city", "x_rel_km", "y_rel_km"])
        for city, (x_value, y_value) in zip(cities, coords):
            writer.writerow([city, round(float(x_value), 1), round(float(y_value), 1)])


def render_plot(cities: list[str], coords: np.ndarray, constraints: list[Constraint]) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 5.4), dpi=180)
    fig.patch.set_facecolor("#071121")
    ax.set_facecolor("#071121")

    city_index = {city: idx for idx, city in enumerate(cities)}

    for constraint in constraints:
        if constraint.solver_role != "core" or constraint.mode != "road":
            continue
        i = city_index[constraint.a]
        j = city_index[constraint.b]
        x_vals = [coords[i, 0], coords[j, 0]]
        y_vals = [coords[i, 1], coords[j, 1]]
        color = "#94a3b8" if constraint.estimated else "#38bdf8"
        alpha = 0.45 if constraint.estimated else 0.75
        linestyle = (0, (3, 3)) if constraint.estimated else "solid"
        ax.plot(x_vals, y_vals, color=color, alpha=alpha, linewidth=1.2, linestyle=linestyle, zorder=1)

    for constraint in constraints:
        if constraint.solver_role != "validation":
            continue
        i = city_index[constraint.a]
        j = city_index[constraint.b]
        x_vals = [coords[i, 0], coords[j, 0]]
        y_vals = [coords[i, 1], coords[j, 1]]
        ax.plot(x_vals, y_vals, color="#f59e0b", alpha=0.55, linewidth=1.0, linestyle=(0, (6, 4)), zorder=1)

    point_color = "#f8fafc"
    accent_color = "#60a5fa"
    ax.scatter(coords[:, 0], coords[:, 1], s=34, color=point_color, edgecolors=accent_color, linewidths=0.8, zorder=3)

    for city, (x_value, y_value) in zip(cities, coords):
        ax.text(x_value + 65, y_value + 40, city, color="#e2e8f0", fontsize=8.5, zorder=4)

    ax.set_title("Australia Surface-Distance Scaffold (Provisional)", color="#e2e8f0", fontsize=13, pad=12)
    ax.text(
        0.5,
        1.01,
        "Sydney is origin. Orientation is arbitrary; this is a relative solve, not a north-up map.",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        color="#94a3b8",
        fontsize=8.2,
    )
    ax.set_xlabel("relative x (km)", color="#94a3b8")
    ax.set_ylabel("relative y (km)", color="#94a3b8")
    ax.tick_params(colors="#94a3b8", labelsize=8)
    ax.grid(color="#1e293b", linewidth=0.6, alpha=0.7)

    for spine in ax.spines.values():
        spine.set_color("#334155")

    legend_handles = [
        plt.Line2D([0], [0], color="#38bdf8", linewidth=1.6, label="measured road edge"),
        plt.Line2D([0], [0], color="#94a3b8", linewidth=1.2, linestyle=(0, (3, 3)), label="estimated road cross-link"),
        plt.Line2D([0], [0], color="#f59e0b", linewidth=1.0, linestyle=(0, (6, 4)), label="rail validation edge"),
    ]
    ax.legend(handles=legend_handles, loc="lower right", facecolor="#071121", edgecolor="#334155", labelcolor="#cbd5e1", fontsize=8)

    fig.tight_layout()
    fig.savefig(PNG_OUTPUT_PATH, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    payload = load_constraints()
    cities = region_cities(payload, "australia")
    constraints = region_constraints(payload, "australia")
    distance_matrix = dense_distance_matrix(cities, constraints)
    coords, eigenvalues = classical_mds(distance_matrix)
    coords = shift_to_origin(cities, coords, origin_city="Sydney")

    write_json(payload, cities, coords, eigenvalues, constraints)
    write_csv(cities, coords)
    render_plot(cities, coords, constraints)

    measured, estimated = measured_counts(constraints)
    print("Australia scaffold generated")
    print(f"Core measured road edges: {measured}")
    print(f"Core estimated road edges: {estimated}")
    print(f"JSON: {JSON_OUTPUT_PATH}")
    print(f"CSV:  {CSV_OUTPUT_PATH}")
    print(f"PNG:  {PNG_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
