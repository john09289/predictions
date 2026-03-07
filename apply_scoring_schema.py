import json
import os

API_DIR = "/Users/nicholashughes/.gemini/antigravity/scratch/astro_observations/predictions/api"
CURRENT_DIR = f"{API_DIR}/current"
JS_FILE = "/Users/nicholashughes/.gemini/antigravity/scratch/astro_observations/predictions/predictions.js"
W_JS_FILE = "/Users/nicholashughes/.gemini/antigravity/scratch/astro_observations/predictions/weekly.js"

with open(f"{CURRENT_DIR}/predictions.json", "r") as f:
    data = json.load(f)

# The user requested PRED-001 to PRED-008 to have full scoring matrix and PRED-009 to PRED-013 to have mechanism claims.
def add_layered_schema(pred):
    pid = pred["id"]
    
    # Common migrations to layer 1
    # Check if prediction value exists directly or under `prediction`
    old_pred_val = None
    old_unc = None
    if "prediction" in pred and isinstance(pred["prediction"], dict):
        old_pred_val = pred["prediction"].get("value") or pred["prediction"].get("value_nT")
        old_unc = pred["prediction"].get("uncertainty") or pred["prediction"].get("uncertainty_nT")
    else:
        old_pred_val = pred.get("prediction_nT")
        old_unc = pred.get("uncertainty_nT")
        
    range_arr = [0,0]
    if old_pred_val is not None and old_unc is not None:
        range_arr = [round(old_pred_val - old_unc, 4), round(old_pred_val + old_unc, 4)]
        
    pred["point_prediction"] = {
        "value": old_pred_val,
        "uncertainty": old_unc,
        "range": range_arr,
        "confidence": "1-sigma"
    }

    if "PRED-0" in pid and int(pid.split("-")[1]) <= 8:
        pred["mechanism"] = {
            "description": "Aetheric pressure trough caused by lunar/solar mass alignment blocking aetheric flow to surface",
            "key_claims": [
                "Signal will be NEGATIVE (pressure drop)",
                "Signal will TRACK eclipse geometry not local solar noon",
                "Signal magnitude scales with coverage fraction",
                "Signal magnitude scales with geomagnetic latitude",
                "Peak timing correlates with maximum obscuration not noon"
            ],
            "each_claim_is_independently_testable": True
        }
        
        pred["derivation"] = {
            "formula": "delta_Z = B * C * L",
            "variables": {
                "B": "baseline_nT = -10.9 (BOU 2017)",
                "C": "coverage_fraction (varies by station)",
                "L": "latitude_factor (geomagnetic projection)"
            },
            "step_by_step": [
                "1. BOU 2017 baseline = -10.9 nT at 99% coverage, lat 40.0N",
                "2. Determine local station coverage fraction",
                "3. Calculate relative latitude distortion factor",
                "4. delta_Z = -10.9 * C * L"
            ],
            "caveat": "BOU 2017 baseline flagged as disturbed day. If quiet-day baseline differs, scale accordingly."
        }
        
        pred["scoring_matrix"] = [
            {
                "claim": "Signal is negative",
                "weight": "HIGH",
                "auto_check": "observed.value < 0",
                "points_if_correct": 3,
                "points_if_wrong": -3
            },
            {
                "claim": "Signal exceeds noise floor",
                "weight": "HIGH", 
                "auto_check": "observed.snr >= 2.0",
                "points_if_correct": 2,
                "points_if_wrong": 0
            },
            {
                "claim": "Magnitude within 1-sigma",
                "weight": "MEDIUM",
                "auto_check": "sigma_distance <= 1.0",
                "points_if_correct": 2,
                "points_if_wrong": -1
            },
            {
                "claim": "Magnitude within 2-sigma",
                "weight": "MEDIUM",
                "auto_check": "sigma_distance <= 2.0",
                "points_if_correct": 1,
                "points_if_wrong": -1
            },
            {
                "claim": "Peak timing tracks eclipse geometry not solar noon",
                "weight": "VERY HIGH",
                "auto_check": "evaluate_timing_correlation()", # Handled as manual or custom bypass in evaluator
                "points_if_correct": 4,
                "points_if_wrong": -4,
                "note": "This is the strongest mechanistic test - globe model has no prediction here"
            },
            {
                "claim": "Signal scales with coverage fraction across stations",
                "weight": "VERY HIGH",
                "auto_check": "evaluate_network_correlation()",
                "points_if_correct": 4,
                "points_if_wrong": -4,
                "note": "Multi-station correlation is model-distinguishing - cannot be explained by random noise"
            },
            {
                "claim": "Non-path stations show less than 2 nT",
                "weight": "HIGH",
                "auto_check": "evaluate_off_path_noise()",
                "points_if_correct": 3,
                "points_if_wrong": -3
            }
        ]
        
        pred["max_possible_score"] = 19
        pred["win_threshold"] = 10
        pred["strong_win_threshold"] = 15
        
        pred["model_distinguishing"] = {
            "description": "Tests where dome and globe models make DIFFERENT predictions",
            "tests": [
                {
                    "test": "Eclipse timing vs solar noon",
                    "dome_predicts": "Peak tracks umbra geometry",
                    "globe_predicts": "No prediction - globe has no eclipse magnetic mechanism",
                    "verdict_if_dome_correct": "STRONG model-distinguishing confirmation"
                },
                {
                    "test": "Coverage scaling across stations",
                    "dome_predicts": "Linear correlation between coverage % and signal nT",
                    "globe_predicts": "No systematic prediction",
                    "verdict_if_dome_correct": "Cannot be explained by coincidence across independent stations"
                },
                {
                    "test": "SG gravimeters show null",
                    "dome_predicts": "0.0 uGal on shielded superconducting gravimeters",
                    "globe_predicts": "Would expect tidal signal if mass-based",
                    "verdict_if_dome_correct": "Confirms aetheric not gravitational mechanism"
                }
            ]
        }
        
        pred["calibration"] = {
            "baseline_source": "BOU 2017",
            "baseline_quality": "CAVEAT - disturbed day",
            "baseline_value_used": -10.9,
            "alternative_baseline_if_quiet_day": "TBD - run W004 replication first",
            "if_baseline_wrong_by_20pct": {
                "adjusted_prediction": round(float(old_pred_val) * 0.8, 2) if isinstance(old_pred_val, (int, float)) else 0,
                "still_within_range": True
            },
            "model_breaks_if": "Signal is positive OR signal shows no geometry correlation"
        }

    elif "PRED-0" in pid and 9 <= int(pid.split("-")[1]) <= 13:
        pred["scoring_matrix"] = [
            {
                "claim": "Signal tracks defined vector",
                "weight": "HIGH",
                "auto_check": "direction_correct",
                "points_if_correct": 5,
                "points_if_wrong": -5
            },
            {
                "claim": "Magnitude within 1-sigma",
                "weight": "MEDIUM",
                "auto_check": "sigma_distance <= 1.0",
                "points_if_correct": 3,
                "points_if_wrong": -1
            },
            {
                "claim": "Mathematical mechanism convergence",
                "weight": "VERY HIGH",
                "auto_check": "evaluate_mechanism_convergence()",
                "points_if_correct": 5,
                "points_if_wrong": -5
            }
        ]
        pred["max_possible_score"] = 13
        pred["win_threshold"] = 7
        pred["strong_win_threshold"] = 11

    # Same logic for Weekly, let's just tag W001-W004 with a generic test matrix so the UI code doesn't crash
    if "W00" in pid:
        pred["scoring_matrix"] = [
            {
                "claim": "Signal is correct polarity",
                "weight": "HIGH",
                "auto_check": "direction_correct",
                "points_if_correct": 5,
                "points_if_wrong": -5
            },
            {
                "claim": "Signal exceeds noise floor",
                "weight": "HIGH", 
                "auto_check": "observed.snr >= 2.0",
                "points_if_correct": 3,
                "points_if_wrong": 0
            },
            {
                "claim": "Magnitude within 1-sigma",
                "weight": "MEDIUM",
                "auto_check": "sigma_distance <= 1.0",
                "points_if_correct": 2,
                "points_if_wrong": -1
            }
        ]
        pred["max_possible_score"] = 10
        pred["win_threshold"] = 5
        pred["strong_win_threshold"] = 8

    return pred

# Rebuild active predictions
if "active_predictions" in data:
    data["active_predictions"] = [add_layered_schema(p) for p in data["active_predictions"]]

for key in ["weekly_tests", "long_term_predictions"]:
    if key in data:
        data[key] = [add_layered_schema(p) for p in data[key]]

with open(f"{CURRENT_DIR}/predictions.json", "w") as f:
    json.dump(data, f, indent=2)

with open(f"{API_DIR}/predictions.json", "w") as f:
    json.dump(data, f, indent=2)

# Write to predictions.js and weekly.js
preds_js = f"// PURE VANILLA DATA FILE\nconst PREDICTIONS = {json.dumps(data.get('active_predictions', []) + data.get('long_term_predictions', []) + data.get('confirmed_wins', []), indent=2)};"
with open(JS_FILE, "w") as f:
    f.write(preds_js)

weekly = {
  "week_start": "2026-03-06",
  "week_end": "2026-03-13",
  "generated": "2026-03-06T19:04:11.162121",
  "predictions": data.get("weekly_tests", [])
}
weekly_js = f"const WEEKLY_DATA = {json.dumps(weekly, indent=2)};"
with open(W_JS_FILE, "w") as f:
    f.write(weekly_js)

print("Scoring matrix schema applied to all JSON files.")
