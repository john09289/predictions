from __future__ import annotations

import json
import math
import os
import tempfile
from pathlib import Path

# Keep plotting caches out of the repo and out of unwritable home paths.
TMP_CACHE_ROOT = Path(tempfile.gettempdir()) / "predictions-australia-coastline-cache"
TMP_CACHE_ROOT.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(TMP_CACHE_ROOT / "mplconfig"))
os.environ.setdefault("XDG_CACHE_HOME", str(TMP_CACHE_ROOT / "xdg-cache"))

import cartopy.io.shapereader as shpreader
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon as PolygonPatch
from scipy.interpolate import Rbf
from shapely.geometry import MultiPolygon


REPO_ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD_PATH = REPO_ROOT / "docs" / "data" / "australia_ground_scaffold.json"
OUTPUT_PATH = REPO_ROOT / "docs" / "assets" / "australia_scaffold_coastline.png"
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

LAT0 = -27.0
LON0 = 134.0
LON_MIN = 111.0
LON_MAX = 155.5
LAT_MIN = -45.5
LAT_MAX = -10.0

# These city positions are used only as local warp anchors. The source side is a
# standard lon/lat projection of the real outline. The destination side is the
# Australia scaffold generated from surface-distance constraints.
CITY_LON_LAT = {
    "Sydney": (151.2, -33.9),
    "Melbourne": (145.0, -37.8),
    "Brisbane": (153.0, -27.5),
    "Adelaide": (138.6, -34.9),
    "Perth": (115.9, -31.9),
    "Darwin": (130.8, -12.5),
    "Cairns": (145.8, -16.9),
}


def local_land_path() -> Path:
    return Path.home() / ".local" / "share" / "cartopy" / "shapefiles" / "natural_earth" / "physical" / "ne_50m_land.shp"


def source_projection(lon_e: float, lat_deg: float) -> np.ndarray:
    x_km = (lon_e - LON0) * math.cos(math.radians(LAT0)) * 111.32
    y_km = (lat_deg - LAT0) * 111.32
    return np.array([x_km, y_km], dtype=float)


def load_scaffold_points() -> dict[str, np.ndarray]:
    payload = json.loads(SCAFFOLD_PATH.read_text())
    # The scaffold image currently uses negative y for northward movement. Flip
    # that here so the coastline render is north-up and easier to inspect.
    return {
        row["city"]: np.array([row["x_rel_km"], -row["y_rel_km"]], dtype=float)
        for row in payload["cities"]
    }


def control_points(scaffold_points: dict[str, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    source_points = []
    destination_points = []

    for city, (lon_e, lat_deg) in CITY_LON_LAT.items():
        source_points.append(source_projection(lon_e, lat_deg))
        destination_points.append(scaffold_points[city])

    source_x = [point[0] for point in source_points]
    source_y = [point[1] for point in source_points]
    source_margin = 700.0
    source_corners = np.array(
        [
            [min(source_x) - source_margin, min(source_y) - source_margin],
            [min(source_x) - source_margin, max(source_y) + source_margin],
            [max(source_x) + source_margin, min(source_y) - source_margin],
            [max(source_x) + source_margin, max(source_y) + source_margin],
        ],
        dtype=float,
    )

    destination_array = np.array(destination_points, dtype=float)
    dest_x = destination_array[:, 0]
    dest_y = destination_array[:, 1]
    dest_margin = 800.0
    destination_corners = np.array(
        [
            [min(dest_x) - dest_margin, min(dest_y) - dest_margin],
            [min(dest_x) - dest_margin, max(dest_y) + dest_margin],
            [max(dest_x) + dest_margin, min(dest_y) - dest_margin],
            [max(dest_x) + dest_margin, max(dest_y) + dest_margin],
        ],
        dtype=float,
    )

    source_points = np.vstack([np.array(source_points, dtype=float), source_corners])
    destination_points = np.vstack([destination_array, destination_corners])
    return source_points, destination_points


def build_rbf_warp(source_points: np.ndarray, destination_points: np.ndarray) -> tuple[Rbf, Rbf]:
    # A smooth warp keeps the coastline from folding along triangle edges near
    # Darwin and the Gulf. We still anchor to the same scaffold points, but the
    # field between them is interpolated smoothly instead of piecewise-affinely.
    source_x = source_points[:, 0]
    source_y = source_points[:, 1]
    destination_x = destination_points[:, 0]
    destination_y = destination_points[:, 1]

    x_warp = Rbf(source_x, source_y, destination_x, function="thin_plate", smooth=50000.0)
    y_warp = Rbf(source_x, source_y, destination_y, function="thin_plate", smooth=50000.0)
    return x_warp, y_warp


def warp_points(points: np.ndarray, x_warp: Rbf, y_warp: Rbf) -> np.ndarray:
    return np.column_stack([x_warp(points[:, 0], points[:, 1]), y_warp(points[:, 0], points[:, 1])])


def australia_polygons() -> list[np.ndarray]:
    reader = shpreader.Reader(local_land_path())
    polygons = []

    for geometry in reader.geometries():
        if isinstance(geometry, MultiPolygon):
            pieces = geometry.geoms
        else:
            pieces = [geometry]

        for polygon in pieces:
            centroid = polygon.centroid
            if not (LON_MIN <= centroid.x <= LON_MAX and LAT_MIN <= centroid.y <= LAT_MAX):
                continue
            if polygon.area < 0.5:
                continue
            polygons.append(np.asarray(polygon.exterior.coords, dtype=float))

    return polygons


def render() -> None:
    scaffold_points = load_scaffold_points()
    source_points, destination_points = control_points(scaffold_points)
    x_warp, y_warp = build_rbf_warp(source_points, destination_points)
    coastline_polygons = australia_polygons()

    warped_polygons = []
    for polygon in coastline_polygons:
        source_xy = np.array([source_projection(lon_e, lat_deg) for lon_e, lat_deg in polygon], dtype=float)
        warped_polygons.append(warp_points(source_xy, x_warp, y_warp))

    fig, ax = plt.subplots(figsize=(7.4, 5.8), dpi=180)
    fig.patch.set_facecolor("#071121")
    ax.set_facecolor("#071121")

    for polygon in warped_polygons:
        patch = PolygonPatch(
            polygon,
            closed=True,
            facecolor="#1f6f8b",
            edgecolor="#7dd3fc",
            linewidth=1.0,
            alpha=0.95,
            zorder=2,
        )
        ax.add_patch(patch)

    for city, point in scaffold_points.items():
        ax.scatter(point[0], point[1], s=28, color="#f8fafc", edgecolors="#38bdf8", linewidths=0.8, zorder=4)
        ax.text(point[0] + 70, point[1] + 35, city, color="#e2e8f0", fontsize=8.5, zorder=5)

    for a, b in [
        ("Sydney", "Melbourne"),
        ("Sydney", "Brisbane"),
        ("Sydney", "Perth"),
        ("Adelaide", "Perth"),
        ("Adelaide", "Darwin"),
        ("Brisbane", "Cairns"),
    ]:
        start = scaffold_points[a]
        end = scaffold_points[b]
        ax.plot([start[0], end[0]], [start[1], end[1]], color="#38bdf8", linewidth=1.1, alpha=0.55, zorder=1)

    ax.set_title("Australia Coastline Warp From Ground Scaffold", color="#e2e8f0", fontsize=13, pad=12)
    ax.text(
        0.5,
        1.01,
        "Real Australia outline from Natural Earth, warped by scaffold anchors. Provisional regional asset only.",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        color="#94a3b8",
        fontsize=8.2,
    )
    ax.set_xlabel("relative x (km)", color="#94a3b8")
    ax.set_ylabel("relative y (km, north-up)", color="#94a3b8")
    ax.tick_params(colors="#94a3b8", labelsize=8)
    ax.grid(color="#1e293b", linewidth=0.6, alpha=0.65)

    for spine in ax.spines.values():
        spine.set_color("#334155")

    ax.set_aspect("equal", adjustable="box")
    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    render()
    print(f"Wrote {OUTPUT_PATH}")
