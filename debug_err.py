import math

H = lambda r: 8537 * math.exp(-r / 8619)

bou_r = 5715
h_bou = H(bou_r)
fsf_b = h_bou / bou_r

print(f"BOU FSF base: {fsf_b:.6f}")

spt_r = 5600
spt_lat_f = 0.80
spt_cov = 0.94
pred_spt = -10.9 * spt_cov * spt_lat_f
print(f"SPT prediction calculation: -10.9 * {spt_cov} * {spt_lat_f} = {pred_spt:.3f}")

snk_lat_f = 0.75
snk_cov = 0.70
pred_snk = -10.9 * snk_cov * snk_lat_f
print(f"SNK prediction calculation: -10.9 * {snk_cov} * {snk_lat_f} = {pred_snk:.3f}")

# Wait, the prompt lists the target predictions as:
# SPT: -8.3 nT
# SNK: -5.8 nT
# Let's check -10.9 * 0.94 * 0.81 for SPT (maybe lat_factor is 0.81 like EBR?)
print(f"SPT with lat=0.81: {-10.9 * 0.94 * 0.81:.3f}")
