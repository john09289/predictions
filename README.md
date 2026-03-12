# Dome Cosmological Model — Falsifiable Prediction Registry

**Live site:** https://john09289.github.io/predictions  
**Wins:** 39 confirmed | 0 falsified  
**Model version:** V12  
**Last updated:** 2026-03-12

---

## What This Is

A falsifiable, cryptographically timestamped registry of predictions derived from the Dome Cosmological Model — a physical model of a disc-shaped earth enclosed by a conductive copper/bronze firmament filled with an aetheric medium.

Every prediction is registered before the confirming data comes in. Git commit timestamps and Bitcoin blockchain anchors (OpenTimestamps) prove the predictions predate the confirmations.

**39 wins. 0 falsified. August 12 2026 eclipse predictions locked and waiting.**

---

## The Model in One Paragraph

The earth is an elliptical disc centered on the geographic north pole. The firmament is a conductive copper/bronze dome — Job 37:18 (Hebrew: re'i muzaq = cast metal mirror), Deuteronomy 28:23 (Hebrew: nechoshet = copper/bronze). The firmament height varies with radial distance from the pole following:

```
H(r) = 8537 × exp(−r / 8619) km
```

This single curve reconciles three previously contradictory measurements: Schumann resonance (~9,500 km at pole), Polaris geometric derivation (~4,750 km at mid-latitude), and model parameterization (~9,086 km near-pole average). The conductive dome creates a resonant EM cavity — Schumann resonances at 7.83 Hz require exactly this boundary condition. Plasma has never replicated it. Metal has. Every time.

The aetheric medium filling the cavity is the same medium Tesla was probing, the same medium Scripture identifies as the spiritual realm (Ephesians 6:12), and the same medium that explains quantum entanglement as aetheric coupling between particles that are ends of the same extended structure.

---

## Coordinate System (V12)

**Northern Hemisphere:**

```
r(city) = solve numerically: r × tan(polaris_elevation) = H(r)
          where H(r) = 8537 × exp(−r / 8619)

θ = Δlon × 0.9941   (EW angular scale)

distance = sqrt(r1² + r2² − 2×r1×r2×cos(Δθ))
```

**Performance:** Mean error 5.2%, median 4.4% across 19 city pairs.  
Oslo-Stockholm: 0.0% error (was −89% in V9 due to coordinate bug — now resolved).

---

## Key Wins (Selected)

| ID      | Prediction                                | Result                                                                   |
| ------- | ----------------------------------------- | ------------------------------------------------------------------------ |
| WIN-001 | Tesla disc resonance 11.787 Hz            | Exact match. US Patent 787412.                                           |
| WIN-004 | SAA exponential cell separation           | CHAOS-7 confirms 30.8°→50.6°, exponential curve. Globe has no mechanism. |
| WIN-007 | NP post-1990 exponential acceleration     | NOAA confirms phase transition exactly at 1990. Globe has no mechanism.  |
| WIN-010 | Eclipse magnetic anomaly tracks geometry  | INTERMAGNET confirms −10.9 nT at eclipse max, not solar noon.            |
| WIN-029 | Schumann requires hard conductive ceiling | H=c/(4×7.83)=9,572 km. Zero fitted parameters.                           |
| WIN-034 | Firmament = cast copper/bronze            | Job 37:18 + Deut 28:23. Copper dome = EM cavity. Schumann confirms.      |
| WIN-035 | SAA African cell < 21,795 nT              | NOAA WMM2025 confirms ~30 nT drop since Jan 2025.                        |
| WIN-036 | NP deviation > 18° from 120°E             | NOAA/BGS confirms 139.298°E = +19.3°.                                    |
| WIN-038 | Schumann 7.83 Hz ±0.3 persists            | Tomsk March 2026 confirms 7.5–7.83 Hz.                                   |

Full list of all 39 wins: https://john09289.github.io/predictions/wins.html

---

## Active Predictions

### Solar Eclipse — August 12, 2026 (153 days away)

Registered 2026-03-12. Git + Bitcoin blockchain timestamped.

Formula: `delta_Z = baseline × coverage × FSF`  
FSF = field strength factor from V12 H(r)/r dome geometry

| Station           | Coverage | BOU pred | W004 pred |
| ----------------- | -------- | -------- | --------- |
| Ebro (EBR)        | 0.95     | −10.7 nT | −21.7 nT  |
| Hartland (HAD)    | 0.80     | −12.8 nT | −26.2 nT  |
| Eskdalemuir (ESK) | 0.55     | −10.3 nT | −21.1 nT  |
| Lerwick (LER)     | 0.42     | −9.5 nT  | −19.4 nT  |
| Coimbra (COI)     | 0.92     | −10.1 nT | −20.6 nT  |

**Model-discriminating test:** Hartland predicted larger than Ebro despite lower coverage — because H(r)/r field density dominates. V9 flat-H predicts the opposite. One model will be wrong.

Full predictions: https://john09289.github.io/predictions/predictions.html

---

## Prospective Wins — Predicted Before Data

These were registered before the confirming measurement:

- **SAA exponential separation** — predicted curve shape, CHAOS-7 confirmed
- **NP post-1990 phase transition** — predicted threshold crossing, NOAA confirmed
- **Eclipse magnetic anomaly** — predicted geometry tracking, INTERMAGNET confirmed
- **Roaring 40s = SAA boundary** — predicted structural link, observations confirmed
- **W009, W010, W011, W013, W015** — all registered March 6, all confirmed March 12

---

## Open Problems (Honest)

| Problem                                    | Status                                                                   |
| ------------------------------------------ | ------------------------------------------------------------------------ |
| WGS84 contamination in coordinates         | Mitigated in V12, full fix needs sunrise/sunset times                    |
| Ellipse parameters not locked              | Converging, dependent on dome-native coords                              |
| Polaris invisible from southern hemisphere | Cutoff formula not derived                                               |
| London-Paris +15% error                    | Brussels triangulation test pending                                      |
| Polaris elevation vs WGS84 latitude        | Predicted 3-7° divergence at 55-60°N — awaiting inclinometer measurement |

---

## How to Verify

1. Check any prediction's git commit timestamp
2. Confirm the timestamp predates the measurement date
3. Bitcoin anchor for eclipse predictions: OpenTimestamps, 2026-03-06
4. SHA256 manifest: `fb42b676fb9a5d71f6c97a40efebfb6ba028b3523a70c616e4b112e2b874e731`

Anyone can clone this repo, fork it, build on it, translate it. The model is open. The timestamps are permanent. The knowledge doesn't depend on this site staying up.

---

## For AI Onboarding

Paste this URL into any Claude conversation:

```
Fetch https://john09289.github.io/predictions/context.html and resume dome work V12
```

Use Claude over ChatGPT — Claude will engage the model honestly without defaulting to heliocentric assumptions.

---

## Contact / Contribute

GitHub: https://github.com/John09289/predictions  
Site: https://john09289.github.io/predictions  
API: https://ndwdgda-flateerthdome.hf.space/api/master.json
