import math

# Baseline coords (V50.6) mapped accurately to WGS84
cities_old_r = {
    "London": 3778,
    "New York": 5520,
    "Los Angeles": 7029,
    "Tokyo": 6610,
    "Moscow": 3234,
    "Sydney": 7160,
    "Cape Town": 7326,
    "Buenos Aires": 7298
}

def test_curve(name, H_func):
    """
    Test a curve where H_func is a function of r.
    Because the user insists on dynamical solving (r * tan(polaris) = H_func(r)),
    we have to compare what the *new* solved r would be for each city
    against the baseline (old) r that gave the 5.2% accuracy map.
    
    If the new solved r matches the old r, the map accuracy is maintained.
    """
    print(f"\n=== Testing {name} ===")
    errors = []
    
    for city, old_r in cities_old_r.items():
        # What was the elevation angle in the old model?
        # old_H = 8537 * exp(-old_r / 8619)
        old_H = 8537 * math.exp(-old_r / 8619)
        tan_elev = old_H / old_r
        
        # Now find the NEW r that satisfies: new_r * tan_elev = H_func(new_r)
        low, high = 1, 30000
        for _ in range(100):
            mid = (low + high) / 2
            try:
                if mid * tan_elev < H_func(mid):
                    low = mid
                else:
                    high = mid
            except ValueError:
                high = mid
                
        new_r = low
        err = abs(new_r - old_r) / old_r * 100
        errors.append(err)
        
        h_actual = H_func(new_r)
        
        print(f"{city:12}: Old r={old_r:4.0f} | New r={new_r:5.0f} (Err {err:5.1f}%) | H={h_actual:4.0f}")
        
    print(f"Mean Radial Stretching Error: {sum(errors)/len(errors):.1f}%")
    
    # Check max height
    h_max = H_func(1)
    print(f"H max (at r=0): {h_max:.0f} km")
    
    # Check sun clearance (sun is at r ~ 10,000 for equator, but 5733 high)
    # Actually, worst clearance is ~ Chapel Hill/LA
    h_la = H_func(7029)
    print(f"H at Los Angeles (r=7000): {h_la:.0f} km (Must be > 5733)")

test_curve("Parabola (H_0=8537, R=20015)", lambda r: 8537 * (1 - (r/20015)**2) if (1 - (r/20015)**2) > 0 else 0)
test_curve("Ellipse (H_0=8537, R=20015)", lambda r: 8537 * math.sqrt(max(0, 1 - (r/20015)**2)))
test_curve("Flattened Exponential (H_0=8537)", lambda r: 8537 * math.exp(-(r/20000)**2))
test_curve("V50.6 Baseline", lambda r: 8537 * math.exp(-r/8619))

