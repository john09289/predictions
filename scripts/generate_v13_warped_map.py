from __future__ import annotations

import html
import math
import re
from dataclasses import dataclass
from pathlib import Path

import cartopy.io.shapereader as shpreader
import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path as MplPath
from scipy.interpolate import CubicSpline
from scipy.spatial import Delaunay
from shapely.geometry import LineString, MultiLineString, MultiPolygon, Polygon


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = REPO_ROOT / "docs" / "assets" / "homepage-warped-map.png"
COORDINATES_PATH = REPO_ROOT / "docs" / "coordinates.html"
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# Homepage display constants.
NP_X = 282.0
NP_Y = 310.0

# The homepage keeps the site's established "horizontal ovoid" silhouette.
# This is a display frame, not a new derivation. The control points below are
# used only to shape the final rendered map on the homepage.
MAIN_BOUNDARY_CONTROL = np.array(
    [
        (170, 310),
        (176, 228),
        (214, 156),
        (286, 126),
        (372, 92),
        (493, 108),
        (556, 186),
        (611, 255),
        (610, 369),
        (556, 440),
        (496, 518),
        (374, 544),
        (290, 506),
        (218, 474),
        (178, 398),
        (170, 310),
    ],
    dtype=float,
)

BEYOND_BOUNDARY_CONTROL = np.array(
    [
        (154, 310),
        (160, 220),
        (202, 142),
        (284, 108),
        (380, 70),
        (518, 90),
        (590, 176),
        (651, 252),
        (650, 372),
        (589, 452),
        (519, 539),
        (384, 567),
        (286, 525),
        (206, 490),
        (160, 408),
        (154, 310),
    ],
    dtype=float,
)

# The source map starts from a standard north-pole azimuthal-equidistant style
# disc. We then warp that disc into the homepage ovoid with V13 city anchors.
SOURCE_RADIUS = 252.0
SOURCE_CENTER = np.array([0.0, 0.0], dtype=float)

# Synthetic lattice controls keep the warp smooth. Exact city anchors from
# docs/coordinates.html then locally pull the real coastlines into the V13 map.
CONTROL_FRACTIONS = (0.18, 0.34, 0.50, 0.68, 0.84, 1.00)
CONTROL_ANGLES_DEG = tuple(range(0, 360, 15))

# Only a few continent labels are needed on the homepage. They are transformed
# with the exact same warp as the land polygons so they stay visually honest.
LABEL_POINTS = [
    ("Africa", 21.0, 4.0, -12.0, 18.0),
    ("Asia", 96.0, 44.0, 14.0, 10.0),
    ("Australia", 136.0, -25.0, 22.0, 4.0),
]


def smooth_closed_curve(control_points: np.ndarray, samples: int = 720) -> np.ndarray:
    # The user correctly called out that the earlier boundary read like a hexagon.
    # We keep the same control vertices, but draw and sample them as a periodic
    # spline so the ice wall reads like a continuous ovoid instead of a faceted
    # polygon.
    base = np.asarray(control_points, dtype=float)
    deltas = np.diff(base, axis=0)
    distances = np.sqrt((deltas**2).sum(axis=1))
    t = np.concatenate([[0.0], np.cumsum(distances)])
    x_spline = CubicSpline(t, base[:, 0], bc_type="periodic")
    y_spline = CubicSpline(t, base[:, 1], bc_type="periodic")
    sample_t = np.linspace(0.0, t[-1], samples, endpoint=False)
    curve = np.column_stack([x_spline(sample_t), y_spline(sample_t)])
    return np.vstack([curve, curve[0]])


MAIN_BOUNDARY = smooth_closed_curve(MAIN_BOUNDARY_CONTROL)
BEYOND_BOUNDARY = smooth_closed_curve(BEYOND_BOUNDARY_CONTROL)


@dataclass(frozen=True)
class CityAnchor:
    city: str
    lat: float
    lon_e: float
    theta_deg: float
    x_km: float
    y_km: float
    hemisphere: str


def local_shapefile(*parts: str) -> Path:
    return Path.home() / ".local" / "share" / "cartopy" / "shapefiles" / "natural_earth" / Path(*parts)


def load_map_geoms():
    land_path = local_shapefile("physical", "ne_50m_land.shp")
    coast_path = local_shapefile("physical", "ne_110m_coastline.shp")
    borders_path = local_shapefile("cultural", "ne_110m_admin_0_boundary_lines_land.shp")
    return (
        list(shpreader.Reader(land_path).geometries()),
        list(shpreader.Reader(coast_path).geometries()),
        list(shpreader.Reader(borders_path).geometries()),
    )


def polygon_to_patch(coords: np.ndarray, **kwargs):
    if len(coords) < 3:
        return None
    return mpatches.PathPatch(MplPath(coords, closed=True), **kwargs)


def ray_polygon_distance(theta_rad: float, polygon: np.ndarray, origin: tuple[float, float]) -> float:
    ox, oy = origin
    dx, dy = math.cos(theta_rad), math.sin(theta_rad)
    best_t = None

    for idx in range(len(polygon) - 1):
        x1, y1 = polygon[idx]
        x2, y2 = polygon[idx + 1]
        sx, sy = x2 - x1, y2 - y1

        det = dx * (-sy) - dy * (-sx)
        if abs(det) < 1e-9:
            continue

        bx, by = x1 - ox, y1 - oy
        t = (bx * (-sy) - by * (-sx)) / det
        u = (dx * by - dy * bx) / det

        if t >= 0 and 0 <= u <= 1:
            if best_t is None or t < best_t:
                best_t = t

    return best_t if best_t is not None else 0.0


def boundary_radius(theta_rad: float) -> float:
    return ray_polygon_distance(theta_rad, MAIN_BOUNDARY, (NP_X, NP_Y))


def boundary_point(theta_rad: float, fraction: float = 1.0) -> np.ndarray:
    radius = fraction * boundary_radius(theta_rad)
    return np.array([NP_X + radius * math.cos(theta_rad), NP_Y + radius * math.sin(theta_rad)], dtype=float)


def clean_numeric(value: str) -> float:
    text = html.unescape(value)
    text = text.replace("&minus;", "-").replace("−", "-").replace(",", "").strip()
    return float(text)


def extract_table(html_text: str, heading: str) -> str:
    section = html_text.split(heading, 1)[1]
    return re.search(r"<table>(.*?)</table>", section, re.S).group(1)


def extract_cells(row_html: str) -> list[str]:
    cells = re.findall(r"<t[dh]>(.*?)</t[dh]>", row_html, re.S)
    return [html.unescape(re.sub(r"<.*?>", "", cell)).strip() for cell in cells]


def parse_anchor_table(table_html: str, hemisphere: str) -> list[CityAnchor]:
    anchors = []
    for row_html in re.findall(r"<tr>(.*?)</tr>", table_html, re.S):
        cells = extract_cells(row_html)
        if not cells or cells[0] == "City":
            continue

        if hemisphere == "NH" and len(cells) == 7:
            city, lat, lon_e, _r, theta_deg, x_km, y_km = cells
            lat_value = clean_numeric(lat)
        elif hemisphere == "SH" and len(cells) == 8:
            city, lat, lon_e, _r_nh, _r_sh, theta_deg, x_km, y_km = cells
            lat_value = -clean_numeric(lat)
        else:
            continue

        anchors.append(
            CityAnchor(
                city=city,
                lat=lat_value,
                lon_e=clean_numeric(lon_e),
                theta_deg=clean_numeric(theta_deg),
                x_km=clean_numeric(x_km),
                y_km=clean_numeric(y_km),
                hemisphere=hemisphere,
            )
        )

    return anchors


def load_v13_anchors() -> list[CityAnchor]:
    html_text = COORDINATES_PATH.read_text()
    nh_table = extract_table(html_text, "<h2>Northern Hemisphere City Coordinates (V13)</h2>")
    sh_table = extract_table(html_text, "<h2>Southern Hemisphere City Coordinates (V13 Two-Zone)</h2>")
    anchors = parse_anchor_table(nh_table, "NH") + parse_anchor_table(sh_table, "SH")
    return [anchor for anchor in anchors if anchor.city != "North Pole"]


def source_disc_point(lon_e: float, lat_deg: float) -> np.ndarray:
    # Standard north-pole disc source map. This keeps the country outlines
    # recognizable before the V13 warp is applied.
    theta = math.radians(-lon_e)
    rho = SOURCE_RADIUS * ((90.0 - lat_deg) / 180.0)
    return SOURCE_CENTER + np.array([rho * math.cos(theta), rho * math.sin(theta)], dtype=float)


def rotation_to_broad_side(anchors: list[CityAnchor]) -> float:
    # Rotate the published V13 city cloud so NH cities bias toward the narrow
    # side and SH cities spread toward the broad side. This is a display choice
    # for the homepage image, not a change to the repo's underlying x,y math.
    nh_points = np.array([[anchor.x_km, anchor.y_km] for anchor in anchors if anchor.hemisphere == "NH"], dtype=float)
    sh_points = np.array([[anchor.x_km, anchor.y_km] for anchor in anchors if anchor.hemisphere == "SH"], dtype=float)
    vector = sh_points.mean(axis=0) - nh_points.mean(axis=0)
    return -math.atan2(vector[1], vector[0])


def rotate_xy(points: np.ndarray, angle_rad: float) -> np.ndarray:
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    rot = np.array([[cos_a, -sin_a], [sin_a, cos_a]], dtype=float)
    return points @ rot.T


def display_scale(rotated_xy: np.ndarray) -> float:
    # Fit the rotated V13 anchors into the homepage ovoid with a margin so the
    # countries do not visually bleed into the ice wall.
    scales = []
    for x_km, y_km in rotated_xy:
        r_km = math.hypot(x_km, y_km)
        if r_km < 1e-9:
            continue
        theta = math.atan2(y_km, x_km)
        # Extra inset keeps SH land, especially Australia, visually inside the
        # rim instead of kissing the ice wall in the homepage render.
        scales.append(0.82 * boundary_radius(theta) / r_km)
    return min(scales)


def model_target_lookup(anchors: list[CityAnchor]) -> dict[str, np.ndarray]:
    rotation = rotation_to_broad_side(anchors)
    rotated = rotate_xy(np.array([[anchor.x_km, anchor.y_km] for anchor in anchors], dtype=float), rotation)
    scale = display_scale(rotated)

    lookup = {}
    for anchor, point in zip(anchors, rotated, strict=True):
        lookup[anchor.city] = np.array([NP_X + scale * point[0], NP_Y + scale * point[1]], dtype=float)
    return lookup


def add_or_replace_control(source_points: list[np.ndarray], target_points: list[np.ndarray], source: np.ndarray, target: np.ndarray, tolerance: float = 2.5):
    for idx, existing in enumerate(source_points):
        if np.linalg.norm(existing - source) <= tolerance:
            source_points[idx] = source
            target_points[idx] = target
            return
    source_points.append(source)
    target_points.append(target)


def build_control_mesh(anchors: list[CityAnchor]) -> tuple[np.ndarray, np.ndarray]:
    target_lookup = model_target_lookup(anchors)
    rotation = rotation_to_broad_side(anchors)

    source_points: list[np.ndarray] = [SOURCE_CENTER.copy()]
    target_points: list[np.ndarray] = [np.array([NP_X, NP_Y], dtype=float)]

    # Base lattice: a smooth circle-to-ovoid warp that preserves recognizable
    # country shapes even before city anchors locally correct the geometry.
    for fraction in CONTROL_FRACTIONS:
        for angle_deg in CONTROL_ANGLES_DEG:
            theta_src = math.radians(angle_deg)
            theta_dst = theta_src + rotation
            source = SOURCE_CENTER + SOURCE_RADIUS * fraction * np.array([math.cos(theta_src), math.sin(theta_src)], dtype=float)
            target = boundary_point(theta_dst, fraction=fraction)
            add_or_replace_control(source_points, target_points, source, target, tolerance=1.5)

    # Exact published V13 city coordinates override nearby lattice nodes.
    for anchor in anchors:
        source = source_disc_point(anchor.lon_e, anchor.lat)
        target = target_lookup[anchor.city]
        add_or_replace_control(source_points, target_points, source, target, tolerance=6.0)

    return np.array(source_points, dtype=float), np.array(target_points, dtype=float)


class PiecewiseAffineWarp:
    def __init__(self, source_points: np.ndarray, target_points: np.ndarray):
        self.source_points = source_points
        self.target_points = target_points
        self.triangulation = Delaunay(source_points)

    def transform_points(self, points: np.ndarray) -> np.ndarray:
        simplices = self.triangulation.find_simplex(points)
        transformed = np.empty((len(points), 2), dtype=float)

        for idx, simplex in enumerate(simplices):
            point = points[idx]
            if simplex == -1:
                theta = math.atan2(point[1], point[0])
                radius = np.linalg.norm(point)
                fraction = 0.0 if SOURCE_RADIUS == 0 else np.clip(radius / SOURCE_RADIUS, 0.0, 1.0)
                transformed[idx] = boundary_point(theta, fraction=fraction)
                continue

            matrix = self.triangulation.transform[simplex]
            bary = matrix[:2] @ (point - matrix[2])
            weights = np.array([bary[0], bary[1], 1.0 - bary.sum()], dtype=float)
            vertices = self.triangulation.simplices[simplex]
            transformed[idx] = weights @ self.target_points[vertices]

        return transformed


def geometry_is_antarctica(geom) -> bool:
    _minx, miny, _maxx, maxy = geom.bounds
    return maxy < -55 or miny < -88


def draw_geom(ax, geom, warp: PiecewiseAffineWarp, facecolor: str, edgecolor: str, linewidth: float, alpha: float):
    polygons = []
    lines = []
    if isinstance(geom, Polygon):
        polygons = [geom]
    elif isinstance(geom, MultiPolygon):
        polygons = list(geom.geoms)
    elif isinstance(geom, LineString):
        lines = [geom]
    elif isinstance(geom, MultiLineString):
        lines = list(geom.geoms)

    for poly in polygons:
        if geometry_is_antarctica(poly):
            continue
        coords = np.asarray(poly.exterior.coords)[:, :2]
        source_points = np.array([source_disc_point(lon, lat) for lon, lat in coords], dtype=float)
        warped = warp.transform_points(source_points)
        patch = polygon_to_patch(
            warped,
            facecolor=facecolor,
            edgecolor=edgecolor,
            linewidth=linewidth,
            alpha=alpha,
            joinstyle="round",
            capstyle="round",
        )
        if patch is not None:
            ax.add_patch(patch)

    for line in lines:
        if geometry_is_antarctica(line):
            continue
        coords = np.asarray(line.coords)[:, :2]
        source_points = np.array([source_disc_point(lon, lat) for lon, lat in coords], dtype=float)
        warped = warp.transform_points(source_points)
        ax.plot(
            warped[:, 0],
            warped[:, 1],
            color=edgecolor,
            linewidth=linewidth,
            alpha=alpha,
            solid_capstyle="round",
            solid_joinstyle="round",
        )


def make_background(ax):
    ax.set_facecolor("#0f172a")
    ax.add_patch(mpatches.Rectangle((0, 0), 700, 620, facecolor="#0f172a", edgecolor="none"))
    ax.add_patch(
        polygon_to_patch(
            BEYOND_BOUNDARY,
            facecolor="#162235",
            edgecolor="#334155",
            linewidth=1.0,
            alpha=0.65,
            hatch="///",
        )
    )

    main_patch = polygon_to_patch(
        MAIN_BOUNDARY,
        facecolor="#0b2448",
        edgecolor="#60a5fa",
        linewidth=2.6,
        alpha=0.98,
    )
    ax.add_patch(main_patch)

    # These rings are page-reading aids only. They help the eye see scale
    # without drawing a fake geographic equator.
    rotation = rotation_to_broad_side(load_v13_anchors())
    for fraction, color, style, alpha in [
        (0.28, "#1d4ed8", "-", 0.28),
        (0.50, "#2563eb", (0, (4, 5)), 0.28),
        (0.72, "#38bdf8", "-", 0.14),
    ]:
        ring = np.array(
            [
                boundary_point(math.radians(angle_deg) + rotation, fraction=fraction)
                for angle_deg in range(0, 361, 4)
            ],
            dtype=float,
        )
        ax.plot(ring[:, 0], ring[:, 1], color=color, linewidth=0.9, linestyle=style, alpha=alpha)

    ax.text(332, 248, "sun circuit zone", color="#60a5fa", fontsize=7.5, fontstyle="italic", alpha=0.65)
    ax.text(614, 264, "Beyond-Ice", ha="center", color="#6b7280", fontsize=8, fontstyle="italic")
    ax.text(614, 276, "Territory", ha="center", color="#6b7280", fontsize=7.5, fontstyle="italic")
    ax.text(614, 288, "(Byrd 1954)", ha="center", color="#475569", fontsize=7, fontstyle="italic")

    ax.add_patch(mpatches.Circle((NP_X, NP_Y), 7, facecolor="#4fc3f7", edgecolor="none"))
    ax.add_patch(mpatches.Circle((NP_X, NP_Y), 3, facecolor="#e0f2fe", edgecolor="none"))
    ax.text(NP_X, 289, "North Pole", ha="center", color="#bae6fd", fontsize=8.5, fontweight="bold")
    ax.text(507, 506, "Antarctic Ice Wall", ha="center", color="#94a3b8", fontsize=8.5)
    ax.text(507, 519, "broad outer rim / SH side", ha="center", color="#64748b", fontsize=7.5, fontstyle="italic")

    return main_patch


def draw_currents(ax):
    def arrow(x1, y1, x2, y2, color, width):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=color, lw=width, shrinkA=0, shrinkB=0))

    arrow(246, 331, 298, 304, "#60a5fa", 2.5)
    arrow(255, 344, 305, 319, "#60a5fa", 1.6)
    ax.text(34, 246, "NH ATLANTIC", color="#60a5fa", fontsize=9, fontweight="bold")
    ax.text(34, 259, "ΔS=+0.022 NE • 9 routes", color="#94a3b8", fontsize=7.5)

    arrow(384, 250, 441, 250, "#4ade80", 2.5)
    arrow(381, 266, 436, 266, "#4ade80", 1.6)
    ax.text(524, 242, "NH PACIFIC", color="#4ade80", fontsize=9, fontweight="bold")
    ax.text(524, 254, "ΔS=+0.014 E • 7 routes", color="#94a3b8", fontsize=7.5)

    arrow(512, 418, 516, 455, "#a78bfa", 2.5)
    ax.text(34, 372, "W ATLANTIC", color="#a78bfa", fontsize=9, fontweight="bold")
    ax.text(34, 384, "ΔS=+0.014 S", color="#94a3b8", fontsize=7.5)

    arrow(387, 191, 444, 191, "#22d3ee", 3.0)
    arrow(385, 206, 439, 206, "#22d3ee", 1.8)
    ax.text(526, 411, "SH AUSTRALIAN", color="#22d3ee", fontsize=9, fontweight="bold")
    ax.text(526, 423, "ΔS=+0.028 E • strongest", color="#94a3b8", fontsize=7.5)

    arrow(545, 430, 593, 430, "#22d3ee", 2.0)
    ax.text(34, 433, "S ATLANTIC", color="#22d3ee", fontsize=9, fontweight="bold")
    ax.text(34, 445, "ΔS=+0.012 E", color="#94a3b8", fontsize=7.5)


def add_legend(ax):
    legend_bg = mpatches.FancyBboxPatch(
        (242, 555),
        214,
        33,
        boxstyle="round,pad=0.5,rounding_size=6",
        facecolor="#0b1220",
        edgecolor="#334155",
        linewidth=0.8,
        alpha=0.9,
    )
    ax.add_patch(legend_bg)
    ax.add_patch(mpatches.Rectangle((256, 567), 16, 9, facecolor="#b97831", edgecolor="none"))
    ax.text(278, 575, "country outlines", color="#e5e7eb", fontsize=7.5)
    ax.annotate("", xy=(415, 571), xytext=(395, 571), arrowprops=dict(arrowstyle="-|>", color="#22d3ee", lw=2.2))
    ax.text(423, 575, "current band", color="#e5e7eb", fontsize=7.5)


def add_labels(ax, warp: PiecewiseAffineWarp):
    for label, lon_e, lat_deg, dx, dy in LABEL_POINTS:
        point = warp.transform_points(np.array([source_disc_point(lon_e, lat_deg)], dtype=float))[0]
        ax.text(
            point[0] + dx,
            point[1] + dy,
            label,
            ha="center",
            va="center",
            color="#f1c27b",
            fontsize=8,
            bbox=dict(boxstyle="round,pad=0.14", facecolor="#0f172a", edgecolor="none", alpha=0.40),
        )


def main():
    anchors = load_v13_anchors()
    land_geoms, coast_geoms, border_geoms = load_map_geoms()
    source_points, target_points = build_control_mesh(anchors)
    warp = PiecewiseAffineWarp(source_points, target_points)

    fig, ax = plt.subplots(figsize=(7, 6.2), dpi=180)
    fig.patch.set_facecolor("#0f172a")
    ax.set_xlim(0, 700)
    ax.set_ylim(620, 0)
    ax.set_aspect("equal")
    ax.axis("off")

    main_patch = make_background(ax)
    patch_start = len(ax.patches)
    line_start = len(ax.lines)

    for geom in land_geoms:
        draw_geom(ax, geom, warp, facecolor="#b97831", edgecolor="#6f4211", linewidth=0.20, alpha=0.94)
    for geom in coast_geoms:
        draw_geom(ax, geom, warp, facecolor="none", edgecolor="#6f4211", linewidth=0.45, alpha=0.96)
    for geom in border_geoms:
        draw_geom(ax, geom, warp, facecolor="none", edgecolor="#7f5526", linewidth=0.18, alpha=0.34)

    for patch in ax.patches[patch_start:]:
        patch.set_clip_path(main_patch)
    for line in ax.lines[line_start:]:
        line.set_clip_path(main_patch)

    add_labels(ax, warp)
    draw_currents(ax)
    add_legend(ax)
    ax.text(
        350,
        607,
        "Single Global Eastward Rotation — PRED-CURR-008 — real country outlines warped by V13 city anchors",
        ha="center",
        color="#60a5fa",
        fontsize=8.4,
        fontweight="bold",
    )

    fig.savefig(OUTPUT_PATH, bbox_inches="tight", pad_inches=0, facecolor=fig.get_facecolor())
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
