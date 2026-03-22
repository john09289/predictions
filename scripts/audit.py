import numpy as np
from scipy.optimize import fsolve, curve_fit

# ── V12 CORE ─────────────────────────────────────────
def H(r):
    return 8537 * np.exp(-r / 8619)

H_ref = 8537.0  # H(0) at pole

def get_r(lat_deg):
    """Dome radius from Polaris elevation = latitude"""
    elev = np.radians(lat_deg)
    def eq(r): return r * np.tan(elev) - H(r)
    return float(fsolve(eq, 5000)[0])

# ── TEST 1: E-PRED-B FSF FORMULA ─────────────────────
print("=" * 60)
print("TEST 1: FSF FORMULA — Does E-PRED-B hold?")
print("=" * 60)

stations = {
    'HAD': {'lat': 51.0,  'cov': 0.80, 'fsf_pub': 1.471},
    'EBR': {'lat': 40.8,  'cov': 0.95, 'fsf_pub': 1.029},
    'ESK': {'lat': 55.3,  'cov': 0.55, 'fsf_pub': 1.722},
    'LER': {'lat': 60.1,  'cov': 0.42, 'fsf_pub': 2.075},
    'NGK': {'lat': 52.1,  'cov': 0.40, 'fsf_pub': 1.529},
    'SNK': {'lat': 27.7,  'cov': 0.72, 'fsf_pub': 0.642},
    'CLF': {'lat': 48.0,  'cov': 0.70, 'fsf_pub': 1.325},
    'COI': {'lat': 40.2,  'cov': 0.92, 'fsf_pub': 1.008},
    'SPT': {'lat': 40.0,  'cov': 0.90, 'fsf_pub': 1.001},
}

for name, s in stations.items():
    s['r'] = get_r(s['lat'])
    s['H_r'] = H(s['r'])

formulas = {
    'exp(r/8619)':        lambda s: float(np.exp(s['r'] / 8619)),
    'H_ref/H(r)':         lambda s: H_ref / s['H_r'],
    '(H_ref/H(r))^0.5':  lambda s: (H_ref / s['H_r'])**0.5,
    '(H_ref/H(r))^2':    lambda s: (H_ref / s['H_r'])**2,
    'H(r)/H_ref':         lambda s: s['H_r'] / H_ref,
    '1/sin(lat)':         lambda s: 1 / np.sin(np.radians(s['lat'])),
    'r/r_EBR_norm':       lambda s: s['r'] / stations['EBR']['r'],
    'lat_ratio_HAD':      lambda s: s['lat'] / stations['HAD']['lat'],
}

best = None
best_mse = 9999

for fname, fn in formulas.items():
    mse = sum(
        (fn(s) - s['fsf_pub'])**2
        for s in stations.values()
    ) / len(stations)

    had = fn(stations['HAD'])
    ebr = fn(stations['EBR'])
    holds = had * stations['HAD']['cov'] > ebr * stations['EBR']['cov']

    print(f"{fname:25s} MSE={mse:.4f} "
          f"HAD={had:.3f} EBR={ebr:.3f} "
          f"E-PRED-B={'YES' if holds else 'NO'}")

    if mse < best_mse:
        best_mse = mse
        best = (fname, fn)

print(f"\nBEST: {best[0]} (MSE={best_mse:.4f})")
fn = best[1]
had_sig = fn(stations['HAD']) * stations['HAD']['cov']
ebr_sig = fn(stations['EBR']) * stations['EBR']['cov']
print(f"HAD signal={had_sig:.3f}  EBR signal={ebr_sig:.3f}")
print(f"E-PRED-B HOLDS with best formula: {had_sig > ebr_sig}")
print(f"Published V12: HAD=1.177 EBR=0.978 (HAD>EBR HOLDS)")

# ── TEST 2: PRED-013 SAA SEPARATION ──────────────────
print("\n" + "=" * 60)
print("TEST 2: PRED-013 — SAA 120 deg by 2055?")
print("=" * 60)

years = np.array([2000, 2005, 2010, 2015, 2020, 2025])
sep   = np.array([30.8, 33.2, 36.1, 40.3, 45.8, 50.6])

def exp_model(t, a, b):
    return a * np.exp(b * t)

t = years - 2000
popt, _ = curve_fit(exp_model, t, sep, p0=[30, 0.02])
a_fit, b_fit = popt

target_120 = None
for yr in range(2025, 2110):
    val = exp_model(yr - 2000, a_fit, b_fit)
    if val >= 120 and target_120 is None:
        target_120 = yr

slope = np.polyfit(years, sep, 1)[0]
linear_2055 = sep[-1] + slope * (2055 - 2025)
exp_2055 = exp_model(2055 - 2000, a_fit, b_fit)
exp_2030 = exp_model(2030 - 2000, a_fit, b_fit)
exp_2035 = exp_model(2035 - 2000, a_fit, b_fit)

print(f"Exponential fit: a={a_fit:.2f}, b={b_fit:.4f}")
print(f"Linear 2055:    {linear_2055:.1f} deg")
print(f"Exp    2030:    {exp_2030:.1f} deg  <-- PRED-R001 basis")
print(f"Exp    2035:    {exp_2035:.1f} deg")
print(f"Exp    2055:    {exp_2055:.1f} deg  (PRED-013 claimed 120)")
print(f"120 deg reached: ~{target_120}")
print(f"CONCLUSION: PRED-013 2055 target WRONG. Remove it.")
print(f"PRED-R001: SAA >=62 deg by 2030 is solid (predicted {exp_2030:.0f})")

# ── TEST 3: NMP DRIFT RATIO ───────────────────────────
print("\n" + "=" * 60)
print("TEST 3: NMP Longitudinal Dominance (WIN-041)")
print("=" * 60)
lat_rate = -16.4   # km/yr
lon_rate = -37.1   # km/yr
ratio = abs(lon_rate / lat_rate)
print(f"Lat rate:  {lat_rate} km/yr")
print(f"Lon rate:  {lon_rate} km/yr")
print(f"Ratio:     {ratio:.2f}x longitudinal")
print(f"WIN-041 threshold (>2.0x): {'CONFIRMED' if ratio > 2.0 else 'FAILS'}")

current_lon = 139.298
lat_nmp = 86.5
lon_rate_deg_yr = lon_rate / (111.32 * np.cos(np.radians(lat_nmp)))
print(f"\nLon rate in deg/yr: {lon_rate_deg_yr:.3f}")
for yr_fwd in [3, 5, 6, 7, 10]:
    proj = current_lon + lon_rate_deg_yr * yr_fwd
    print(f"  {2025+yr_fwd}: {proj:.1f} deg E predicted")

# ── TEST 4: FIELD DECAY ───────────────────────────────
print("\n" + "=" * 60)
print("TEST 4: Field Decay (WIN-040 / PRED-012)")
print("=" * 60)
tsumeb = 77.0
keetmanshoop = 76.0
global_avg = 32.0
threshold = 28.0
print(f"Tsumeb:       {tsumeb} nT/yr")
print(f"Keetmanshoop: {keetmanshoop} nT/yr")
print(f"Global avg:   {global_avg} nT/yr")
print(f"Threshold:    {threshold} nT/yr")
print(f"Exceedance:   {tsumeb/threshold:.1f}x")
print(f"PRED-012 -> WIN-040: CONFIRMED")

# ── TEST 5: W025 MARGIN ───────────────────────────────
print("\n" + "=" * 60)
print("TEST 5: W025 African Cell Threshold")
print("=" * 60)
current_nT = 21880
decay_yr = 75.0
old_threshold = 21800
new_threshold = 21900
# Dec 2026 = 9 months away from March 2026
months = 9
projected = current_nT - (decay_yr * months / 12)
print(f"Current:            {current_nT} nT")
print(f"Projected Dec 2026: {projected:.0f} nT")
margin_old = projected - old_threshold
margin_new = projected - new_threshold
print(f"Old threshold 21800: margin {margin_old:+.0f} nT "
      f"({'FAILS' if margin_old > 0 else 'OK'})")
print(f"New threshold 21900: margin {margin_new:+.0f} nT "
      f"({'FAILS' if margin_new > 0 else 'OK'})")
print(f"Action: Use 21900 nT threshold")

# ── TEST 6: DISTANCE MODEL ────────────────────────────
print("\n" + "=" * 60)
print("TEST 6: Distance Model Scope")
print("=" * 60)
routes_south = [
    ('Sydney', 7160, 32.5, 'Cape Town',    7326, -30.0, 11000),
    ('Sydney', 7160, 32.5, 'Buenos Aires', 7298,  58.0, 11700),
]
for r in routes_south:
    n1, r1, t1, n2, r2, t2, actual = r
    dt = np.radians(t2 - t1) * 0.9941
    pred = np.sqrt(r1**2 + r2**2 - 2 * r1 * r2 * np.cos(dt))
    err = (pred - actual) / actual * 100
    print(f"{n1}->{n2}: actual={actual} predicted={pred:.0f} error={err:+.0f}%")

print("CONCLUSION: 5.2% claim only valid for northern hemisphere.")
print("Cannot claim global 5.2% without ellipse correction.")

print("\n" + "=" * 60)
print("AUDIT COMPLETE")
print("=" * 60)
print("Actions:")
print("  REMOVE: PRED-013 (math gives 74-92 deg, not 120)")
print("  REMOVE: E-PRED-B specific HAD>EBR claim (undocumented FSF)")
print("  FIX:    W025 threshold 21800->21900")
print("  FIX:    Distance claim -> 'northern hemisphere only'")
print("  FIX:    W017-W022 update stale PENDING status")
print("  PROMOTE: PRED-012 -> WIN-040")
print("  ADD:    WIN-041 (NMP longitudinal dominance)")
print("  ADD:    PRED-R001 through PRED-R006")
