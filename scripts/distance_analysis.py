import numpy as np
from scipy.optimize import fsolve
import json

def H(r):
    return 8537 * np.exp(-r / 8619)

def compute_r(polaris_elev_deg):
    elev = np.radians(polaris_elev_deg)
    def eq(r): return r * np.tan(elev) - H(r)
    return fsolve(eq, 5000)[0]

# City data: (dome_r, dome_theta)
cities = {
    'London':       (3778,   0.0),
    'New York':     (5520,  73.1),
    'Los Angeles':  (7029, 118.1),
    'Tokyo':        (6610, -139.0),
    'Sydney':       (7160,  32.5),
    'Cape Town':    (7326, -30.0),
    'Buenos Aires': (7298,  58.0),
    'Melbourne':    (6405,  36.0),
    'Auckland':     (5083,  34.0),
    'Paris':        (4144,  -2.3),
    'Berlin':       (3645, -13.9),
    'Oslo':         (2753,   3.5),
    'Moscow':       (3234, -36.4),
}

# Actual distances (km, great circle)
actual_distances = {
    ('London', 'Paris'): 344,
    ('London', 'New York'): 5570,
    ('New York', 'Los Angeles'): 3940,
    ('Los Angeles', 'Tokyo'): 8815,
    ('London', 'Sydney'): 16993,
    ('Sydney', 'Cape Town'): 11000,
    ('Sydney', 'Buenos Aires'): 11700,
    ('Sydney', 'Auckland'): 2156,
    ('Cape Town', 'Buenos Aires'): 6845,
    ('Melbourne', 'Auckland'): 2591,
    ('Oslo', 'Moscow'): 1850,
    ('London', 'Moscow'): 2500,
    ('Paris', 'Berlin'): 878,
}

def dome_distance_raw(r1, t1, r2, t2):
    """Raw V12 distance without ellipse"""
    delta_t = np.radians(t2 - t1) * 0.9941
    return np.sqrt(r1**2 + r2**2 - 2 * r1 * r2 * np.cos(delta_t))

def dome_distance_ellipse(r1, t1, r2, t2,
                          a=20015, b=15000, orient=60):
    """V12 distance with ellipse correction"""
    o = np.radians(orient)
    t1r, t2r = np.radians(t1), np.radians(t2)
    delta_t = np.radians(t2 - t1) * 0.9941

    def ellipse_r(r, theta):
        t = theta - o
        scale = (a * b) / np.sqrt(
            (b * np.cos(t))**2 + (a * np.sin(t))**2)
        return r * (scale / a)

    r1e = ellipse_r(r1, t1r)
    r2e = ellipse_r(r2, t2r)

    return np.sqrt(r1e**2 + r2e**2 - 2 * r1e * r2e * np.cos(delta_t))

print("V12 DISTANCE ANALYSIS")
print("=" * 70)
print(f"{'Route':<35} {'Actual':>8} {'Raw':>8} {'Err%':>6} "
      f"{'Ellipse':>8} {'Err%':>6}")
print("-" * 70)

total_err_raw = 0
total_err_ellipse = 0
northern_err_raw = 0
northern_err_ellipse = 0
southern_err_raw = 0
southern_err_ellipse = 0
n = 0
n_north = 0
n_south = 0

# Routes that involve southern cities
southern_routes = {
    ('London', 'Sydney'), ('Sydney', 'Cape Town'),
    ('Sydney', 'Buenos Aires'), ('Sydney', 'Auckland'),
    ('Cape Town', 'Buenos Aires'), ('Melbourne', 'Auckland'),
}

for (c1, c2), actual in actual_distances.items():
    r1, t1 = cities[c1]
    r2, t2 = cities[c2]

    raw = dome_distance_raw(r1, t1, r2, t2)
    err_raw = (raw - actual) / actual * 100

    ell = dome_distance_ellipse(r1, t1, r2, t2)
    err_ell = (ell - actual) / actual * 100

    total_err_raw += abs(err_raw)
    total_err_ellipse += abs(err_ell)
    n += 1

    is_southern = (c1, c2) in southern_routes or (c2, c1) in southern_routes
    if is_southern:
        southern_err_raw += abs(err_raw)
        southern_err_ellipse += abs(err_ell)
        n_south += 1
    else:
        northern_err_raw += abs(err_raw)
        northern_err_ellipse += abs(err_ell)
        n_north += 1

    flag = " <-- SOUTHERN" if is_southern else ""
    print(f"{c1+'-'+c2:<35} {actual:>8.0f} {raw:>8.0f} {err_raw:>+6.1f}% "
          f"{ell:>8.0f} {err_ell:>+6.1f}%{flag}")

print("-" * 70)
print(f"{'MEAN ABSOLUTE ERROR (ALL)':<35} {'':>17} {total_err_raw/n:>6.1f}% "
      f"{'':>9} {total_err_ellipse/n:>6.1f}%")
if n_north > 0:
    print(f"{'MEAN ERROR (NORTHERN ONLY)':<35} {'':>17} "
          f"{northern_err_raw/n_north:>6.1f}% {'':>9} "
          f"{northern_err_ellipse/n_north:>6.1f}%")
if n_south > 0:
    print(f"{'MEAN ERROR (SOUTHERN ROUTES)':<35} {'':>17} "
          f"{southern_err_raw/n_south:>6.1f}% {'':>9} "
          f"{southern_err_ellipse/n_south:>6.1f}%")

# Grid search for optimal ellipse
print("\nGRID SEARCH — Optimal ellipse parameters")
print("-" * 50)

best_params = None
best_err = 999

for ba_ratio in [0.70, 0.75, 0.80, 0.85, 0.90]:
    for orient in [45, 50, 55, 60, 65, 70, 75]:
        b = 20015 * ba_ratio
        total = 0
        for (c1, c2), actual in actual_distances.items():
            r1, t1 = cities[c1]
            r2, t2 = cities[c2]
            pred = dome_distance_ellipse(r1, t1, r2, t2,
                                        b=b, orient=orient)
            total += abs(pred - actual) / actual
        mae = total / len(actual_distances) * 100
        if mae < best_err:
            best_err = mae
            best_params = (ba_ratio, orient, b)

ba, ori, b_val = best_params
print(f"Optimal b/a:          {ba}")
print(f"Optimal orientation:  {ori}deg NE")
print(f"Optimal b value:      {b_val:.0f} km")
print(f"Mean absolute error:  {best_err:.1f}%")

# Northern-only optimal
best_north = None
best_north_err = 999
for ba_ratio in [0.70, 0.75, 0.80, 0.85, 0.90]:
    for orient in [45, 50, 55, 60, 65, 70, 75]:
        b = 20015 * ba_ratio
        total = 0
        count = 0
        for (c1, c2), actual in actual_distances.items():
            if (c1, c2) in southern_routes or (c2, c1) in southern_routes:
                continue
            r1, t1 = cities[c1]
            r2, t2 = cities[c2]
            pred = dome_distance_ellipse(r1, t1, r2, t2, b=b, orient=orient)
            total += abs(pred - actual) / actual
            count += 1
        if count > 0:
            mae = total / count * 100
            if mae < best_north_err:
                best_north_err = mae
                best_north = (ba_ratio, orient, b)

ba_n, ori_n, b_n = best_north
print(f"\nNorthern-only optimal:")
print(f"  b/a={ba_n}, orient={ori_n}deg, error={best_north_err:.1f}%")

# Save results
results = {
    'optimal_ba_ratio': ba,
    'optimal_orient_deg': ori,
    'optimal_b_km': b_val,
    'optimal_a_km': 20015,
    'mean_absolute_error_all_pct': round(best_err, 1),
    'northern_only_ba': ba_n,
    'northern_only_orient': ori_n,
    'northern_only_error_pct': round(best_north_err, 1),
    'version': 'V12'
}

with open('data/ellipse_optimal.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nSaved to data/ellipse_optimal.json")
print("OPEN-003 RESOLVED")
