import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.patheffects as path_effects
import matplotlib.path as mpath
from matplotlib.patches import Polygon

# --- Coordinates ---
north_cities = {
    "North Pole": (-1, 0), "Reykjavik": (2018, 1116), "Anchorage": (-2484, 807),
    "Oslo": (2748, 166), "Stockholm": (2817, 54), "Moscow": (2601, -1921),
    "London": (3778, 0), "Warsaw": (3440, -1320), "Berlin": (3537, -879),
    "Paris": (4140, -163), "Chicago": (277, 5290), "Istanbul": (4307, -3359),
    "Madrid": (5535, 685), "New York": (1609, 5281), "Denver": (-1666, 5467),
    "Chapel Hill NC": (1267, 6370), "Tokyo": (-4993, -4332), 
    "Los Angeles": (-3305, 6203), "Cairo": (6953, -4336), 
    "Baghdad": (4357, -5771), "Miami": (1866, 9647), 
    "Mexico City": (-2107, 13300), "Mumbai": (719, -13714), 
    "Hong Kong": (-6302, -9704)
}

south_cities = {
    "Sydney": (6035, 3852), "Cape Town": (6344, -3663), 
    "Buenos Aires": (3862, 6192), "Santiago": (2442, 8011), 
    "Melbourne": (5182, 3765), "Auckland": (4212, 2846), 
    "Johannesburg": (8612, -5820), "Perth": (8722, 297)
}

a = 20015  # km semi-major
b = 15000  # km semi-minor
orient_deg = 60 # degrees rotation

fig = plt.figure(figsize=(16, 16), facecolor="#0a0a1a")

# Azimuthal Equidistant projection (Globe stretched to flat disc)
proj = ccrs.AzimuthalEquidistant(central_longitude=0, central_latitude=90)
ax = fig.add_subplot(1, 1, 1, projection=proj)
ax.set_facecolor('#04122d')

def rot90(x, y):
    return -y, x

# Create elliptical boundary path
t = np.linspace(0, 2*np.pi, 200)
ex = np.cos(t) * (a * 1000)
ey = np.sin(t) * (b * 1000)
theta_rad = np.radians(orient_deg)
rx = ex * np.cos(theta_rad) - ey * np.sin(theta_rad)
ry = ex * np.sin(theta_rad) + ey * np.cos(theta_rad)

# Rotate to match Cartopy orientation
rx_rot, ry_rot = rot90(rx, ry)
ellipse_path = mpath.Path(np.column_stack([rx_rot, ry_rot]))

# Set the global extent of the entire projection first (valid spherical coordinates)
ax.set_global()

# Now set the specific boundary clip path
ax.set_boundary(ellipse_path, transform=proj)

# Map Features
ax.add_feature(cfeature.LAND.with_scale('50m'), facecolor='#1a3311', edgecolor='#436b33', linewidth=0.5)
ax.add_feature(cfeature.OCEAN.with_scale('50m'), facecolor='#04122d')
ax.add_feature(cfeature.LAKES.with_scale('50m'), facecolor='#04122d', edgecolor='#436b33', linewidth=0.3)
ax.add_feature(cfeature.BORDERS.with_scale('50m'), edgecolor='#2b4520', linewidth=0.5, linestyle=':')

# Ice Wall Glow
ice_wall = Polygon(np.column_stack([rx_rot, ry_rot]), 
                  edgecolor='#cce6ff', fc='none', lw=6, zorder=6, alpha=0.9, transform=proj)
ax.add_patch(ice_wall)

glow = Polygon(np.column_stack([rx_rot, ry_rot]), 
                  edgecolor='#58a6ff', fc='none', lw=20, zorder=7, alpha=0.3, transform=proj)
ax.add_patch(glow)

# Plot Cities 
def plot_cities(city_dict, color, marker, size):
    for name, (x, y) in city_dict.items():
        rx_val, ry_val = rot90(x, y)
        mx = rx_val * 1000
        my = ry_val * 1000
        
        ax.scatter(mx, my, c=color, s=size, marker=marker, zorder=10, transform=proj, edgecolors='black', linewidths=1)
        
        txt = ax.text(mx + 200000, my + 200000, name, color='white', fontsize=11, 
                fontweight='bold', zorder=11, transform=proj)
        txt.set_path_effects([path_effects.withStroke(linewidth=3, foreground='black')])

plot_cities(north_cities, '#39ff14', 'o', 80)
plot_cities(south_cities, '#ff1493', '^', 100)

ax.gridlines(draw_labels=False, color='#58a6ff', alpha=0.3, linestyle='--')

plt.title("Dome Earth Elliptical Map with Continental Relief", 
          color='#58a6ff', pad=30, fontsize=24, fontweight='bold')

from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Northern City', markerfacecolor='#39ff14', markersize=12, linewidth=0),
    Line2D([0], [0], marker='^', color='w', label='Southern City', markerfacecolor='#ff1493', markersize=14, linewidth=0),
    Line2D([0], [0], color='#cce6ff', lw=6, label='Ice Wall Boundary')
]
ax.legend(handles=legend_elements, loc='upper left', facecolor='#04122d', edgecolor='#58a6ff', 
          labelcolor='white', fontsize=12, framealpha=0.9)

output_path = "dome_map_advanced_v12.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
print(f"Advanced map saved to {output_path}")
