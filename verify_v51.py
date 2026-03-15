import math

# City coordinates calculated for V51 (x, y)
cities = {
    "Reykjavik": (3964, 2188),
    "London": (7116, 0),
    "New York": (2827, 9304),
    "Los Angeles": (-5446, 10199),
    "Tokyo": (-8369, -7275),
    "Sydney": (9856, 6291),
    "Cape Town": (10278, -5934),
    "Buenos Aires": (6265, 10046),
    "Moscow": (4988, -3677),
    "Paris": (7700, -309),
    "Anchorage": (-4840, 1573)
}

# Approximate real-world distances (WGS84) in km
real_dist = {
    ("London", "New York"): 5570,
    ("New York", "Los Angeles"): 3935,
    ("London", "Paris"): 344,
    ("Tokyo", "Los Angeles"): 8815,
    ("London", "Moscow"): 2500,
    ("Sydney", "Los Angeles"): 12050,
    ("Cape Town", "Buenos Aires"): 6860
}

print("=== V51 Distance Verification ===")
errors = []
for (c1, c2), true_d in real_dist.items():
    x1, y1 = cities[c1]
    x2, y2 = cities[c2]
    
    # Distance formula in the V51 model: straight line Euclidean distance
    calc_d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    err = abs(calc_d - true_d) / true_d * 100
    errors.append(err)
    print(f"{c1:12} to {c2:12} : Real {true_d:5d} km | V51 {calc_d:5.0f} km | Error: {err:5.1f}%")

print(f"\nMean Error against sample: {sum(errors)/len(errors):.1f}%")

# Verifying Sun Clearance
print("\n=== Sun Clearance Verification ===")
H0 = 9572.0
Redge = 20015.0

def H(r):
    return H0 * math.sqrt(1 - (r/Redge)**2)

sun_alt = 5733.0
print(f"Sun altitude: {sun_alt} km")
print(f"H(0) North Pole: {H(0):.0f} km")
print(f"H(10954) Chapel Hill: {H(10954):.0f} km")
print(f"H(15000) Equatorial: {H(15000):.0f} km")
r_intersect = Redge * math.sqrt(1 - (sun_alt/H0)**2)
print(f"Sun intersects firmament at r = {r_intersect:.0f} km")

# Let's check the maximum r in our cities
max_r_city_name = ""
max_r_city_val = 0
for name, (x, y) in cities.items():
    r = math.sqrt(x**2 + y**2)
    if r > max_r_city_val:
        max_r_city_val = r
        max_r_city_name = name

print(f"Furthest city in test set is {max_r_city_name} at r={max_r_city_val:.0f} km")
if max_r_city_val > r_intersect:
    print("WARNING: Sun collision exists over habitable areas!")
else:
    print("SUCCESS: Firmament remains above Sun over all habitable areas.")

