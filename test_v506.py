import math

def get_v506_r(lat_deg):
    if lat_deg == 90: return 1
    lat_rad = math.radians(lat_deg)
    tan_lat = math.tan(lat_rad)
    
    # solve r * tan(lat) = 8537 * exp(-r / 8619)
    # let's do binary search
    low, high = 1, 20000
    for _ in range(100):
        mid = (low + high) / 2
        lhs = mid * tan_lat
        rhs = 8537 * math.exp(-mid / 8619)
        if lhs < rhs:
            low = mid
        else:
            high = mid
    return mid

print("V50.6 r values vs WGS84:")
for lat in range(80, -10, -10):
    if lat == 0: continue
    r = get_v506_r(lat)
    r_wgs = (90 - lat) * 111.1
    h = 8537 * math.exp(-r / 8619)
    print(f"Lat {lat:2d}: r = {r:5.0f} km (WGS: {r_wgs:5.0f}), H = {h:5.0f} km")

