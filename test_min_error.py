import math

cities = {
    "North Pole": (89.99, 0.0),
    "Reykjavik": (64.10, 13.93),
    "Anchorage": (61.20, 22.80),
    "Oslo": (59.90, 12.23),
    "Stockholm": (59.33, 12.07),
    "Moscow": (55.75, 9.57),
    "London": (51.50, 12.00),
    "Warsaw": (52.20, 10.60),
    "Berlin": (52.50, 11.07),
    "Paris": (48.90, 11.85),
    "Chicago": (41.88, 17.80),
    "Istanbul": (41.01, 9.47),
    "Madrid": (40.42, 12.47),
    "New York": (40.71, 16.87),
    "Denver": (39.73, 19.13),
    "Chapel Hill NC": (36.18, 17.25),
    "Tokyo": (35.70, 2.73),
    "Los Angeles": (34.05, 19.87),
    "Cairo": (30.10, 9.87),
    "Baghdad": (33.30, 8.47),
    "Miami": (25.80, 17.27),
    "Mexico City": (19.43, 18.60),
    "Mumbai": (19.08, 6.20),
    "Hong Kong": (22.32, 3.80)
}

dist_pairs = [
    ("London", "New York", 5570),
    ("New York", "Los Angeles", 3935),
    ("London", "Paris", 344),
    ("Tokyo", "Los Angeles", 8815),
    ("London", "Moscow", 2500),
    ("Denver", "Chapel Hill NC", 2378),
    ("Reykjavik", "London", 1890),
    ("Miami", "New York", 1757),
    ("Stockholm", "Oslo", 416)
]

print("=== BEST CASE SCENARIO (H perfectly hugging Sun at 5733) ===")
# If H must be >= 5733, the smallest r happens when H = 5733.
# Let's see what happens if we force H = max(5733, 8537 * exp(-r / 8619))
# Actually, the simplest curve to test is H = max(5733, 8537 * exp(-r / 8619)).
def calc_r_hmin(lat):
    if lat == 90: return 1
    tan_lat = math.tan(math.radians(lat))
    # the ideal r for V50.6:
    for mid in range(1, 25000):
        h = max(5733.0, 8537 * math.exp(-mid / 8619))
        if mid * tan_lat >= h:
            return mid
    return 25000

coords = {}
for city, (lat, noon) in cities.items():
    r = calc_r_hmin(lat)
    # theta
    theta = (noon - 13.0) * 15.0  # approximate
    coords[city] = (r * math.cos(math.radians(theta)), r * math.sin(math.radians(theta)))

errors = []
for c1, c2, real_d in dist_pairs:
    x1, y1 = coords[c1]
    x2, y2 = coords[c2]
    calc_d = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    err = abs(calc_d - real_d) / real_d * 100
    errors.append(err)
    print(f"{c1} to {c2}: Real {real_d} | Calc {calc_d:.0f} | Err {err:.1f}%")

print(f"Mean Error: {sum(errors)/len(errors):.1f}%")

