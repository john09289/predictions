# Dome Cosmological Model — Falsifiable Prediction Registry

**Live site:** https://john09289.github.io/predictions
**Wins:** 56 confirmed | 4 refined | 93.3% accuracy
**Version:** V50.10 / Coordinate System V13
**Last updated:** 2026-03-29

---

## What This Is

A falsifiable, cryptographically timestamped registry of predictions derived from the Dome Cosmological Model (ECM) — a disc-shaped earth enclosed by a conductive copper/bronze firmament filled with an exponentially varying aetheric medium. Every prediction is registered before the confirming data arrives. Git timestamps and Bitcoin blockchain anchors (OpenTimestamps) prove predictions predate confirmations.

The model derives from two inputs: the original Hebrew texts of Genesis/Job/Deuteronomy, and raw empirical data (INTERMAGNET, NOAA, CHAOS-7, Tomsk SR network). No globe-model assumptions.

---

## V13 Architecture Summary

**Disc geometry:** Egg-shaped (horizontal ovoid, Hildegard model). North Pole at the narrow tip. Southern ice wall at the wide outer edge.

**Two-zone coordinate system:**
- NH inner zone: r = 0 (N. Pole) → 14,105 km (coord. boundary)
- SH outer zone: r = 14,105 → ~28,210 km (ice wall)
- Angular coordinate: θ = −lon_E (derivable from sundial + clock, no GPS)

**Single governing scale length:** λ_g = 8,619 km governs 6 independent domains: geomagnetics, gravity, Schumann resonance, SAA separation, NMP drift, and solar elevation.

**Tesla aetheric distance formula:** d = √(NS² + EW²) / n(r_avg), where n(r) = 1 + 0.271 × (H₀/H(r) − 1)

**H(r) = 8537 × exp(−r / 8619) km** — firmament height curve. At ice wall (r=20,015 km): H=837 km, n=3.49.

---

## Scorecard

| Category | Count |
|----------|-------|
| Confirmed wins | **56** |
| Refined (narrow window or formula bug) | **4** |
| Accuracy | **93.3%** |
| Prospective (predicted before data) | 10 |

---

## Selected Wins

| ID | Prediction | Result |
|----|------------|--------|
| WIN-001 | Tesla disc resonance 11.787 Hz | Exact match. US Patent 787412. |
| WIN-004 | SAA exponential cell separation | CHAOS-7 confirms 30.8°→50.6°, exponential. |
| WIN-007 | NP post-1990 exponential acceleration | NOAA confirms phase transition. Globe has no mechanism. |
| WIN-012 | Magnetic-gravity coupling κ=1.67 nT/µGal | BOU+Mohe two independent events. |
| WIN-026 | Sun altitude 5,733 km | Zero free-parameter triangulation. |
| WIN-029 | Schumann requires hard conductive ceiling | H=c/(4×7.83)=9,572 km. Zero fitted parameters. |
| WIN-034 | Firmament = cast copper/bronze | Job 37:18 + Deut 28:23. Schumann confirms. |
| WIN-056 | Solar elevation from H(r) alone | θ=90°−φ_obs+φ_sun. Zero free parameters. 6th λ_g domain. |
| WIN-057 | Two-zone disc topology (cross-equatorial RMSE 6.2%) | Circle gives 64.3%, egg gives 7.7% on same routes. |
| WIN-058 | θ=−lon_E coordinate unification | Corrected Sydney: −151.2°, not +32.5°. |

Full list: https://john09289.github.io/predictions/wins.html

---

## Eclipse Predictions — Aug 12 2026

Condition: Kp < 2 on eclipse day (quiet-day condition, WIN-010).
Monitor from Aug 9.

| Station | Predicted signal | Globe prediction |
|---------|-----------------|-----------------|
| HAD Hartland | −21.5 nT | 0.0 nT |
| EBR Ebro Spain | −17.7 nT | 0.0 nT |

Correction factor 1.672 = κ (PRED-KAPPA-001). If κ = eclipse factor, this is structural.

---

## Active Open Problems

| ID | Problem |
|----|---------|
| OPEN-012 | Finsler parameter lock — SYD-EZE currently −8.4%, target <5% |
| OPEN-014 | Southern Ocean aetheric flow direction (Perth↔BA needed) |
| OPEN-015 | Near-equatorial cities break two-zone formula (Singapore r > r_eq) |
| OPEN-016 | SH city r coordinate verification from Category 1 ground data |

---

## Category 1 Data Methodology

**Tier 1 (clean):** Pre-GPS rail surveys, mechanical odometers, pre-1960 surveys, ship logs by speed, Polaris+sundial
**Tier 2:** Post-GPS rail from original construction records
**Tier 3:** Modern road distances, coastal charts (caution)
**Tier 4 — REJECT:** GPS coordinates, WGS84, Google Maps, satellite-derived (circular — assumes globe)

**Australian Tier 1 rail anchors:**
- Indian Pacific Sydney→Perth: 4,352 km (1.324× globe great-circle, surveyed 1912–1917)
- XPT Sydney→Melbourne: 966 km (1.366× globe great-circle)

---

## How to Verify Any Prediction

1. Clone the repo: `git clone https://github.com/John09289/predictions`
2. Find any prediction in `docs/predictions.html`
3. Take its SHA256 hash from the page or `docs/data/prediction_hashes.json`
4. Check the git commit timestamp — it must predate the measurement date
5. Bitcoin anchor for eclipse predictions: OpenTimestamps 2026-03-06

Anyone can clone, fork, build on it. The timestamps are permanent.

---

## Verify SHA256

```bash
echo -n "PREDICTION TEXT" | sha256sum
# compare to docs/data/prediction_hashes.json
```

---

## For AI Onboarding

```
Fetch https://john09289.github.io/predictions/model.html and load ecm-dome skill, then continue dome work V13
```

Use Claude Code with local agent mode + skills for full context without token waste.
