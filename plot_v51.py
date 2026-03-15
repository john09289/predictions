import numpy as np
import matplotlib.pyplot as plt

r = np.linspace(0, 20015, 500)

# V50.6 Exponential Curve
h_50 = 8537 * np.exp(-r/8619)

# V51 Elliptical Dome Curve (True Dome)
H0 = 9572 # Schumann resonance height
R_edge = 20015 # Ice wall radius
h_51 = H0 * np.sqrt(1 - (r/R_edge)**2)

# Sun and Moon fixed altitudes
sun_h = 5733
moon_h = 2534

fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

ax.plot(r, h_50, label="V50.6 (Exponential)", color='red', linestyle='--', linewidth=2)
ax.plot(r, h_51, label="V51 (True Elliptical Dome)", color='#39ff14', linewidth=3)

# Sun line
ax.axhline(sun_h, color='#ffcc00', linestyle=':', linewidth=2, label="Sun Altitude (5,733 km)")
# Moon line
ax.axhline(moon_h, color='#cce6ff', linestyle=':', linewidth=2, label="Moon Altitude (2,534 km)")

# Fill area from 0 to 20015 (ground)
ax.fill_between(r, 0, h_51, color='#39ff14', alpha=0.1)

# Annotations
ax.annotate('Collision Point V50.6!', xy=(3500, 5733), xytext=(4000, 7000),
            arrowprops=dict(facecolor='red', shrink=0.05),
            color='white', fontweight='bold')

ax.annotate('Geometric Clearance V51', xy=(10000, 5733), xytext=(8000, 8000),
            arrowprops=dict(facecolor='#39ff14', shrink=0.05),
            color='white', fontweight='bold')

# Formatting
ax.set_title("V50.6 vs V51 Firmament Curvature $H(r)$", color='white', pad=20, fontsize=16)
ax.set_xlabel("r: Distance from North Pole (km)", color='white', fontsize=12)
ax.set_ylabel("H: Altitude (km)", color='white', fontsize=12)
ax.grid(True, color='#30363d', linestyle='-', linewidth=0.5)
ax.tick_params(colors='white')
ax.spines['bottom'].set_color('#30363d')
ax.spines['left'].set_color('#30363d')

plt.legend(facecolor='#0d1117', edgecolor='#30363d', labelcolor='white', fontsize=11)
plt.tight_layout()

plt.savefig("v51_firmament_profile.png", dpi=300, facecolor=fig.get_facecolor())
print("Saved v51_firmament_profile.png")
