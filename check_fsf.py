import math

# Old V12 / V50.6
def H_old(r):
    return 8537 * math.exp(-r/8619)

# New V51
def H_new(r):
    return 9572 * math.sqrt(1 - (r/20015)**2)

cities_old_r = {
    'BOU': 5715, # Denver
    'HAD': 3778, # London approx
    'EBR': 5577, # Madrid approx
}

cities_new_r = {
    'BOU': 9983,
    'HAD': 7116,
    'EBR': 9800,
}

print("=== V12 / V50.6 FSF ===")
for city, r in cities_old_r.items():
    h = H_old(r)
    fsf = (h / r) / (H_old(cities_old_r['BOU']) / cities_old_r['BOU'])
    print(f"{city}: r={r}, H={h:.0f}, FSF={fsf:.3f}")

print("\n=== V51 FSF ===")
for city, r in cities_new_r.items():
    h = H_new(r)
    fsf = (h / r) / (H_new(cities_new_r['BOU']) / cities_new_r['BOU'])
    print(f"{city}: r={r}, H={h:.0f}, FSF={fsf:.3f}")
