from __future__ import annotations

import json
import math
import os
import tempfile
from pathlib import Path

# Keep plotting caches out of the repo and out of unwritable home paths.
TMP_CACHE_ROOT = Path(tempfile.gettempdir()) / "predictions-ground-coastline-cache"
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
CONSTRAINTS_PATH = REPO_ROOT / "data" / "ground_coordinate_constraints.json"


def local_land_path() -> Path:
    return Path.home() / ".local" / "share" / "cartopy" / "shapefiles" / "natural_earth" / "physical" / "ne_50m_land.shp"


def region_output_paths(region: str) -> dict[str, Path]:
    slug = region.lower()
    return {
        "scaffold_json": REPO_ROOT / "docs" / "data" / f"{slug}_ground_scaffold.json",
        "coastline_png": REPO_ROOT / "docs" / "assets" / f"{slug}_scaffold_coastline.png",
    }


def load_payload() -> dict:
    return json.loads(CONSTRAINTS_PATH.read_text())


def load_scaffold_points(scaffold_path: Path) -> dict[str, np.ndarray]:
    payload = json.loads(scaffold_path.read_text())
    # The scaffold plots use the math solve's raw y-axis. For coastline review
    # we flip that axis so the preview is north-up and easier to inspect.
    return {
        row["city"]: np.array([row["x_rel_km"], -row["y_rel_km"]], dtype=float)
        for row in payload["cities"]
    }


def source_projection(lon_e: float, lat_deg: float, lon0: float, lat0: float) -> np.ndarray:
    x_km = (lon_e - lon0) * math.cos(math.radians(lat0)) * 111.32
    y_km = (lat_deg - lat0) * 111.32
    return np.array([x_km, y_km], dtype=float)


def control_points(scaffold_points: dict[str, np.ndarray], anchor_lon_lat: dict[str, list[float]], lon0: float, lat0: float) -> tuple[np.ndarray, np.ndarray]:
    source_points = []
    destination_points = []

    for city, lon_lat in anchor_lon_lat.items():
        if city not in scaffold_points:
            continue
        lon_e, lat_deg = lon_lat
        source_points.append(source_projection(lon_e, lat_deg, lon0, lat0))
        destination_points.append(scaffold_points[city])

    source_array = np.array(source_points, dtype=float)
    destination_array = np.array(destination_points, dtype=float)
    source_x = source_array[:, 0]
    source_y = source_array[:, 1]
    dest_x = destination_array[:, 0]
    dest_y = destination_array[:, 1]

    source_margin = 700.0
    dest_margin = 800.0
    source_corners = np.array(
        [
            [min(source_x) - source_margin, min(source_y) - source_margin],
            [min(source_x) - source_margin, max(source_y) + source_margin],
            [max(source_x) + source_margin, min(source_y) - source_margin],
            [max(source_x) + source_margin, max(source_y) + source_margin]
        ],
        dtype=float,
    )
    destination_corners = np.array(
        [
            [min(dest_x) - dest_margin, min(dest_y) - dest_margin],
            [min(dest_x) - dest_margin, max(dest_y) + dest_margin],
            [max(dest_x) + dest_margin, min(dest_y) - dest_margin],
            [max(dest_x) + dest_margin, max(dest_y) + dest_margin]
        ],
        dtype=float,
    )

    return (
        np.vstack([source_array, source_corners]),
        np.vstack([destination_array, destination_corners]),
    )


def build_rbf_warp(source_points: np.ndarray, destination_points: np.ndarray) -> tuple[Rbf, Rbf]:
    source_x = source_points[:, 0]
    source_y = source_points[:, 1]
    destination_x = destination_points[:, 0]
    destination_y = destination_points[:, 1]

    x_warp = Rbf(source_x, source_y, destination_x, function="thin_plate", smooth=50000.0)
    y_warp = Rbf(source_x, source_y, destination_y, function="thin_plate", smooth=50000.0)
    return x_warp, y_warp


def warp_points(points: np.ndarray, x_warp: Rbf, y_warp: Rbf) -> np.ndarray:
    return np.column_stack([x_warp(points[:, 0], points[:, 1]), y_warp(points[:, 0], points[:, 1])])


def region_polygons(region_meta: dict) -> list[np.ndarray]:
    bbox = region_meta["visualization"]["coast_bbox"]
    min_area = region_meta["visualization"].get("min_polygon_area", 0.1)
    reader = shpreader.Reader(local_land_path())
    polygons = []

    for geometry in reader.geometries():
        pieces = geometry.geoms if isinstance(geometry, MultiPolygon) else [geometry]
        for polygon in pieces:
            centroid = polygon.centroid
            if not (bbox["lon_min"] <= centroid.x <= bbox["lon_max"] and bbox["lat_min"] <= centroid.y <= bbox["lat_max"]):
                continue
            if polygon.area < min_area:
                continue
            polygons.append(np.asarray(polygon.exterior.coords, dtype=float))

    return polygons


def render_region(region: str, payload: dict) -> None:
    region_meta = payload["regions"][region]
    if "visualization" not in region_meta:
        return

    paths = region_output_paths(region)
    if not paths["scaffold_json"].exists():
        return

    scaffold_points = load_scaffold_points(paths["scaffold_json"])
    viz = region_meta["visualization"]
    lon0 = viz["projection_center"]["lon0"]
    lat0 = viz["projection_center"]["lat0"]
    source_points, destination_points = control_points(scaffold_points, viz["anchor_lon_lat"], lon0, lat0)
    x_warp, y_warp = build_rbf_warp(source_points, destination_points)
    coastline_polygons = region_polygons(region_meta)

    warped_polygons = []
    for polygon in coastline_polygons:
        source_xy = np.array(
            [source_projection(lon_e, lat_deg, lon0, lat0) for lon_e, lat_deg in polygon],
            dtype=float,
        )
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
        ax.text(point[0] + 18, point[1] + 12, city, color="#e2e8f0", fontsize=8.0, zorder=5)

    ax.set_title(f"{region_meta['title']} Coastline Warp", color="#e2e8f0", fontsize=13, pad=12)
    ax.text(
        0.5,
        1.01,
        "Real land outline from Natural Earth, warped by scaffold anchors. Provisional regional asset only.",
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
    paths["coastline_png"].parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(paths["coastline_png"], bbox_inches="tight")
    plt.close(fig)

    print(f"Wrote {paths['coastline_png']}")


def main() -> None:
    payload = load_payload()
    for region in payload["regions"]:
        render_region(region, payload)


if __name__ == "__main__":
    main()
