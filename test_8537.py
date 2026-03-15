import math

cities = {
    "Stockholm": (59.33, 12.07),
    "Oslo": (59.90, 12.23),
    "London": (51.50, 12.00),
    "New York": (40.71, 16.87),
    "Cape Town": (-33.9, 18.4),
    "Buenos Aires": (-34.6, -58.4)
}

dist_pairs = [
    ("Stockholm", "Oslo", 416),
    ("London", "New York", 5570),
    ("Cape Town", "Buenos Aires", 6860)
]

def map_error(H_func):
    errors = []
    coords = {}
    for city, (lat, lon) in cities.items():
        if lat == 90: r = 1
        else:
            tan_lat = math.tan(math.radians(lat))
            # Binary search
            low, high = 1, 30000
            for _ in range(100):
                mid = (low + high) / 2
                h = H_func(abs(lat), mid)
                if mid * tan_lat < h:
                    low = mid
                else:
                    high = mid
            r = low
        theta = lon # approx
        coords[city] = (r * math.cos(math.radians(theta)), r * math.sin(math.radians(theta)))
        
    for c1, c2, real_d in dist_pairs:
        x1, y1 = coords[c1]
        x2, y2 = coords[c2]
        calc_d = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        errors.append(abs(calc_d - real_d) / real_d)
        print(f"{c1} to {c2}: Real {real_d} | Calc {calc_d:.0f} | Err {errors[-1]*100:.1f}%")
    print(f"Mean Error: {sum(errors)/len(errors)*100:.1f}%\n")

print("=== V50.6 Baseline ===")
map_error(lambda lat, r: 8537 * math.exp(-r/8619))

print("=== Ellipse H0=8537 R=20015 ===")
map_error(lambda lat, r: 8537 * math.sqrt(max(0, 1 - (r/20015)**2)))

print("=== Parabola H0=8537 R=20015 ===")
map_error(lambda lat, r: 8537 * (1 - (r/20015)**2))
