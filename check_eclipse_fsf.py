import math

r_bou = 5715 # Denver
r_had = 3778 # Hartland
r_ebr = 5577 # Ebro

def calc_fsf(name, r, H_func):
    h = H_func(r)
    h_b = H_func(r_bou)
    fsf = (h / r) / (h_b / r_bou)
    return fsf

def test_curve(name, H_func):
    print(f"\n=== {name} ===")
    fsf_had = calc_fsf("HAD", r_had, H_func)
    fsf_ebr = calc_fsf("EBR", r_ebr, H_func)
    print(f"BOU FSF: 1.000")
    print(f"HAD FSF: {fsf_had:.3f} (Coverage 0.80 -> Signal proxy: {fsf_had * 0.80:.3f})")
    print(f"EBR FSF: {fsf_ebr:.3f} (Coverage 0.95 -> Signal proxy: {fsf_ebr * 0.95:.3f})")
    if (fsf_had * 0.80) > (fsf_ebr * 0.95):
        print("✅ HAD beats EBR (Prediction maintained)")
    else:
        print("❌ EBR beats HAD (PREDICTION BROKEN)")
        
    # Check Sun clearance at equator (~ 10,000 km)
    h_eq = H_func(10000)
    print(f"H at Equator (r=10000): {h_eq:.0f} km")
    if h_eq > 5733:
        print("✅ Clears the Sun")
    else:
        print("❌ Crashes into the Sun")

test_curve("V50.6 Exponential (Baseline)", lambda r: 8537 * math.exp(-r/8619))
test_curve("Ellipse H0=8537, R=20015", lambda r: 8537 * math.sqrt(1 - (r/20015)**2))
test_curve("Parabola H0=8537, R=20015", lambda r: 8537 * (1 - (r/20015)**2))

