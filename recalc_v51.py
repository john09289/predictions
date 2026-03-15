import math

north_cities = [
    ("North Pole", 89.99, 0.00, -180.0),
    ("Reykjavik", 64.10, 13.93, +28.9),
    ("Anchorage", 61.20, 22.80, +162.0),
    ("Oslo", 59.90, 12.23, +3.5),
    ("Stockholm", 59.33, 12.07, +1.1),
    ("Moscow", 55.75, 9.57, -36.4),
    ("London", 51.50, 12.00, +0.0),
    ("Warsaw", 52.20, 10.60, -21.0),
    ("Berlin", 52.50, 11.07, -13.9),
    ("Paris", 48.90, 11.85, -2.3),
    ("Chicago", 41.88, 17.80, +87.0),
    ("Istanbul", 41.01, 9.47, -37.9),
    ("Madrid", 40.42, 12.47, +7.1),
    ("New York", 40.71, 16.87, +73.1),
    ("Denver", 39.73, 19.13, +106.9),
    ("Chapel Hill NC", 36.18, 17.25, +78.8),
    ("Tokyo", 35.70, 2.73, -139.0),
    ("Los Angeles", 34.05, 19.87, +118.1),
    ("Cairo", 30.10, 9.87, -32.0),
    ("Baghdad", 33.30, 8.47, -52.9),
    ("Miami", 25.80, 17.27, +79.0),
    ("Mexico City", 19.43, 18.60, +99.0),
    ("Mumbai", 19.08, 6.20, -87.0),
    ("Hong Kong", 22.32, 3.80, -123.0)
]

south_cities = [
    ("Sydney", 33.0, 14.17, "33.6S", 33.6),
    ("Cape Town", 33.6, 10.00, "33.0S", 33.0),
    ("Buenos Aires", 33.5, 15.87, "33.1S", 33.1),
    ("Santiago", 37.0, 16.87, "29.6S", 29.6),
    ("Melbourne", 30.0, 14.40, "36.6S", 36.6),
    ("Auckland", 23.5, 14.27, "43.1S", 43.1),
    ("Johannesburg", 42.0, 9.73, "24.6S", 24.6),
    ("Perth", 38.0, 12.13, "28.6S", 28.6)
]

H0 = 9572.0
Redge = 20015.0

def calc_r_x_y(angle_deg, theta_deg):
    angle_rad = math.radians(angle_deg)
    tan_a = math.tan(angle_rad)
    ratio = H0 / Redge
    r = H0 / math.sqrt(tan_a**2 + ratio**2)
    
    theta_rad = math.radians(theta_deg)
    x = r * math.cos(theta_rad)
    y = r * math.sin(theta_rad)
    return round(r), int(round(x)), int(round(y))

out_coord_n = []
for name, polaris, noon_utc, theta in north_cities:
    r, x, y = calc_r_x_y(polaris, theta)
    if name == "North Pole": r = 1
    out_coord_n.append(f"  <tr><td>{name}</td><td>{polaris:.2f}</td><td>{noon_utc:.2f}</td><td>{r:,}</td><td>{theta:+.1f}</td><td>{x:,}</td><td>{y:,}</td></tr>")

out_coord_s = []
for name, noon_alt, noon_utc, lat_str, lat_val in south_cities:
    theta = (noon_utc - 12.0) * 15.0
    r, x, y = calc_r_x_y(lat_val, theta)
    out_coord_s.append(f"  <tr><td>{name}</td><td>{noon_alt:.1f}&deg;</td><td>{noon_utc:.2f}</td><td>{lat_str}</td><td>{r:,}</td><td>{theta:+.1f}</td><td>{x:,}</td><td>{y:,}</td></tr>")

out_ct_n = []
for name, polaris, noon_utc, theta in north_cities:
    r, x, y = calc_r_x_y(polaris, theta)
    if name == "North Pole": r = 1
    out_ct_n.append(f"<tr><td>{name}</td><td>{polaris:.2f}</td><td>{noon_utc:.2f}</td><td>{r}</td><td>{theta:+.1f}</td><td>{x}</td><td>{y}</td></tr>")

out_ct_s = []
for name, noon_alt, noon_utc, lat_str, lat_val in south_cities:
    theta = (noon_utc - 12.0) * 15.0
    r, x, y = calc_r_x_y(lat_val, theta)
    out_ct_s.append(f"<tr><td>{name}</td><td>{noon_alt:.1f}</td><td>{noon_utc:.2f}</td><td>{lat_str}</td><td>{r}</td><td>{theta:+.1f}</td><td>{x}</td><td>{y}</td></tr>")

with open('v51_rows_coord.txt', 'w') as f:
    f.write("\n".join(out_coord_n))
    f.write("\n=====\n")
    f.write("\n".join(out_coord_s))

with open('v51_rows_context.txt', 'w') as f:
    f.write("\n".join(out_ct_n))
    f.write("\n=====\n")
    f.write("\n".join(out_ct_s))
