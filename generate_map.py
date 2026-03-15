import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

# --- Extracted Data from coordinates.html ---

# Northern Hemisphere (x, y) coordinates in km
north_cities = {
    "North Pole": (-1, 0),
    "Reykjavik": (2018, 1116),
    "Anchorage": (-2484, 807),
    "Oslo": (2748, 166),
    "Stockholm": (2817, 54),
    "Moscow": (2601, -1921),
    "London": (3778, 0),
    "Warsaw": (3440, -1320),
    "Berlin": (3537, -879),
    "Paris": (4140, -163),
    "Chicago": (277, 5290),
    "Istanbul": (4307, -3359),
    "Madrid": (5535, 685),
    "New York": (1609, 5281),
    "Denver": (-1666, 5467),
    "Chapel Hill NC": (1267, 6370),
    "Tokyo": (-4993, -4332),
    "Los Angeles": (-3305, 6203),
    "Cairo": (6953, -4336),
    "Baghdad": (4357, -5771),
    "Miami": (1866, 9647),
    "Mexico City": (-2107, 13300),
    "Mumbai": (719, -13714),
    "Hong Kong": (-6302, -9704)
}

# Southern Hemisphere (x, y) coordinates
south_cities = {
    "Sydney": (6035, 3852),
    "Cape Town": (6344, -3663),
    "Buenos Aires": (3862, 6192),
    "Santiago": (2442, 8011),
    "Melbourne": (5182, 3765),
    "Auckland": (4212, 2846),
    "Johannesburg": (8612, -5820),
    "Perth": (8722, 297)
}

# --- Ellipse Geometry Params (from V12/V9 notes) ---
# a = semi-major axis, b = semi-minor axis
a = 20015  # km
b = 15000  # km
orient_deg = 60 # degrees rotation

fig, ax = plt.subplots(figsize=(14, 14))
ax.set_facecolor('#0d1117')
fig.patch.set_facecolor('#0d1117')

# Draw the Outer Ellipse (Ice Wall / Firmament boundary)
ellipse = Ellipse(xy=(0, 0), width=a*2, height=b*2, angle=orient_deg, 
                  edgecolor='#58a6ff', fc='none', lw=2, linestyle='--', alpha=0.7)
ax.add_patch(ellipse)

# Draw axes for orientation
ax.axhline(0, color='#30363d', lw=1, zorder=1)
ax.axvline(0, color='#30363d', lw=1, zorder=1)

# Plot Northern Cities
nx = [coords[0] for coords in north_cities.values()]
ny = [coords[1] for coords in north_cities.values()]
ax.scatter(nx, ny, c='#238636', s=40, zorder=5, label="North")

for city, (x, y) in north_cities.items():
    ax.annotate(city, (x, y), xytext=(5, 5), textcoords="offset points", 
                color='#c9d1d9', fontsize=9)

# Plot Southern Cities
sx = [coords[0] for coords in south_cities.values()]
sy = [coords[1] for coords in south_cities.values()]
ax.scatter(sx, sy, c='#d29922', s=50, marker='^', zorder=5, label="South")

for city, (x, y) in south_cities.items():
    ax.annotate(city, (x, y), xytext=(5, -12), textcoords="offset points", 
                color='#d29922', fontsize=9)

# North Pole Marker
ax.scatter([0], [0], c='white', s=80, marker='*', zorder=10)

# Formatting
ax.set_title("Dome Earth Cosmological Map (V12 Coordinates)", color='white', pad=20, fontsize=16)
ax.set_aspect('equal', 'box')
ax.set_xlim(-a*1.2, a*1.2)
ax.set_ylim(-a*1.2, a*1.2)
ax.grid(True, color='#21262d', linestyle='-', linewidth=0.5)

# Styling ticks
ax.tick_params(colors='#8b949e')
for spine in ax.spines.values():
    spine.set_color('#30363d')

plt.tight_layout()
output_path = "dome_map_v12.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
print(f"Map successfully generated and saved to {output_path}")
