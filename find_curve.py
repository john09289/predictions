import math

cities = {
    # lat, lon
    "London": (51.50, -0.12),
    "New York": (40.71, -74.00),
    "Los Angeles": (34.05, -118.24),
    "Tokyo": (35.67, 139.65),
    "Moscow": (55.75, 37.61),
    "Cape Town": (-33.92, 18.42),
    "Buenos Aires": (-34.60, -58.38),
    "Sydney": (-33.86, 151.20)
}

# Real WGS84 distances
real_dist = {
    ("London", "New York"): 5570,
    ("New York", "Los Angeles"): 3935,
    ("Tokyo", "Los Angeles"): 8815,
    ("London", "Moscow"): 2500,
    ("Sydney", "Los Angeles"): 12050,
    ("Cape Town", "Buenos Aires"): 6860
}

# V50.6 baseline R calculation
def calc_r_v506(lat):
    # numerical solve for r * tan(lat) = 8537 * exp(-r / 8619)
    # or for south: the south formula was different in V9... but let's just use north for now
    pass

def wgs_dist(c1, c2):
    return real_dist[(c1, c2)]

print("Required H(lat) to maintain perfect WGS84 map radius (r = (90-lat)*111.1):")
for lat in range(80, -10, -10):
    r = (90 - lat) * 111.1
    tan_lat = math.tan(math.radians(lat))
    if lat == 0:
        continue
    h_req = r * tan_lat
    print(f"Lat {lat:2d}: r = {r:5.0f} km, Required H = {h_req:5.0f} km")

