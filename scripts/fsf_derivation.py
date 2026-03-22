import numpy as np
from scipy.optimize import fsolve

# V12 H(r) formula
def H(r):
    return 8537 * np.exp(-r / 8619)

H_ref = H(0)  # = 8537 km (pole)

def compute_r(polaris_elev_deg):
    elev = np.radians(polaris_elev_deg)
    def eq(r):
        return r * np.tan(elev) - H(r)
    r_sol = fsolve(eq, 5000)[0]
    return r_sol

# Station elevations (Polaris ~ latitude)
stations = {
    'HAD': {'lat': 51.0, 'coverage': 0.80, 'fsf_published': 1.471},
    'EBR': {'lat': 40.8, 'coverage': 0.95, 'fsf_published': 1.029},
    'SPT': {'lat': 40.0, 'coverage': 0.90, 'fsf_published': 1.001},
    'ESK': {'lat': 55.3, 'coverage': 0.55, 'fsf_published': 1.722},
    'LER': {'lat': 60.1, 'coverage': 0.42, 'fsf_published': 2.075},
    'NGK': {'lat': 52.1, 'coverage': 0.40, 'fsf_published': 1.529},
    'SNK': {'lat': 27.7, 'coverage': 0.72, 'fsf_published': 0.642},
    'CLF': {'lat': 48.0, 'coverage': 0.70, 'fsf_published': 1.325},
    'COI': {'lat': 40.2, 'coverage': 0.92, 'fsf_published': 1.008},
}

print("=" * 60)
print("FSF DERIVATION — Finding formula that matches published")
print("=" * 60)

# Compute r and H(r) for each station
for name, s in stations.items():
    r = compute_r(s['lat'])
    h = H(r)
    s['r'] = r
    s['h_r'] = h
    print(f"{name}: lat={s['lat']}° r={r:.0f}km H(r)={h:.0f}km")

print()
print("Testing FSF formulas:")
print("-" * 60)

# Formula candidates
formulas = {
    'A: H(r)/H_ref':
        lambda s: s['h_r'] / H_ref,
    'B: H_ref/H(r)':
        lambda s: H_ref / s['h_r'],
    'C: (H_ref/H(r))^0.5':
        lambda s: (H_ref / s['h_r'])**0.5,
    'D: (H_ref/H(r))^1.5':
        lambda s: (H_ref / s['h_r'])**1.5,
    'E: exp(r/8619)':
        lambda s: np.exp(s['r'] / 8619),
    'F: r/H(r) normalized':
        lambda s: (s['r'] / s['h_r']) /
                  (compute_r(51.0) / H(compute_r(51.0))),
    'G: 1/cos(lat)':
        lambda s: 1 / np.cos(np.radians(s['lat'])),
    'H: sin(lat)/sin(51)':
        lambda s: np.sin(np.radians(s['lat'])) /
                  np.sin(np.radians(51.0)),
    'I: field_gradient |dH/dr|':
        lambda s: abs(-8537 / 8619 * np.exp(-s['r'] / 8619)) /
                  abs(-8537 / 8619),
}

# For each formula, compute MSE vs published FSF
best_formula = None
best_mse = 999

for fname, ffunc in formulas.items():
    computed = {}
    mse = 0
    for name, s in stations.items():
        val = ffunc(s)
        computed[name] = val
        mse += (val - s['fsf_published'])**2
    mse /= len(stations)

    had_vs_ebr = "HAD>EBR ✓" if computed['HAD'] > computed['EBR'] \
                 else "HAD<EBR ✗"

    print(f"\n{fname}")
    print(f"  MSE: {mse:.4f} | {had_vs_ebr}")
    print(f"  HAD={computed['HAD']:.3f} "
          f"(pub={stations['HAD']['fsf_published']})")
    print(f"  EBR={computed['EBR']:.3f} "
          f"(pub={stations['EBR']['fsf_published']})")
    print(f"  LER={computed['LER']:.3f} "
          f"(pub={stations['LER']['fsf_published']})")

    if mse < best_mse:
        best_mse = mse
        best_formula = fname

print()
print("=" * 60)
print(f"BEST FORMULA: {best_formula}")
print(f"MSE: {best_mse:.4f}")
print("=" * 60)

# Now test if best formula makes E-PRED-B hold
print()
print("E-PRED-B FINAL STATUS:")
had_fsf = formulas[best_formula](stations['HAD'])
ebr_fsf = formulas[best_formula](stations['EBR'])
had_signal = stations['HAD']['coverage'] * had_fsf
ebr_signal = stations['EBR']['coverage'] * ebr_fsf
print(f"HAD: coverage={stations['HAD']['coverage']} "
      f"x FSF={had_fsf:.3f} = {had_signal:.3f}")
print(f"EBR: coverage={stations['EBR']['coverage']} "
      f"x FSF={ebr_fsf:.3f} = {ebr_signal:.3f}")
if had_signal > ebr_signal:
    print("E-PRED-B: HOLDS ✓ — HAD beats EBR")
else:
    print("E-PRED-B: FAILS ✗ — EBR beats HAD")
    print("Need additional latitude coupling term")

print()
print("PUBLISHED V12 RESULTS (eclipse_v12_predictions.txt):")
print("HAD: coverage=0.80 x FSF=1.471 = 1.177")
print("EBR: coverage=0.95 x FSF=1.029 = 0.978")
print("Published E-PRED-B: HOLDS (HAD 1.177 > EBR 0.978)")
