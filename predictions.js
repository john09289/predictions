// PURE VANILLA DATA FILE
const PREDICTIONS = [
  {
    "id": "PRED-001",
    "station": "Ebro (EBR)",
    "prediction_nT": -8.4,
    "uncertainty_nT": 1.7,
    "component": "Z",
    "event": "2026 Solar Eclipse Aug 12",
    "mechanism": {
      "description": "Aetheric pressure trough caused by lunar/solar mass alignment blocking aetheric flow to surface",
      "key_claims": [
        "Signal will be NEGATIVE (pressure drop)",
        "Signal will TRACK eclipse geometry not local solar noon",
        "Signal magnitude scales with coverage fraction",
        "Signal magnitude scales with geomagnetic latitude",
        "Peak timing correlates with maximum obscuration not noon"
      ],
      "each_claim_is_independently_testable": true
    },
    "formula": "delta_Z = baseline * coverage_fraction * latitude_factor",
    "inputs": {
      "baseline_nT": -10.9,
      "coverage_fraction": 0.95,
      "latitude_factor": 0.81
    },
    "status": "pending",
    "timestamp_sha256": "pending",
    "sha256": "f33d0250e0e2279086923037622990b70f21837f26f226770bc6289915cb7f38",
    "point_prediction": {
      "value": -8.4,
      "uncertainty": 1.7,
      "range": [
        -10.1,
        -6.7
      ],
      "confidence": "1-sigma"
    },
    "derivation": {
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
    },
    "scoring_matrix": [
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
        "auto_check": "evaluate_timing_correlation()",
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
    ],
    "max_possible_score": 19,
    "win_threshold": 10,
    "strong_win_threshold": 15,
    "model_distinguishing": {
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
    },
    "calibration": {
      "baseline_source": "BOU 2017",
      "baseline_quality": "CAVEAT - disturbed day",
      "baseline_value_used": -10.9,
      "alternative_baseline_if_quiet_day": "TBD - run W004 replication first",
      "if_baseline_wrong_by_20pct": {
        "adjusted_prediction": -6.72,
        "still_within_range": true
      },
      "model_breaks_if": "Signal is positive OR signal shows no geometry correlation"
    },
    "baseline_recalibration": {
      "w004_observed_nT": -17.6,
      "w004_coverage": 0.92,
      "w004_latitude_factor": 0.86,
      "derived_true_baseline_nT": -22.24,
      "formula": "true_baseline = observed / (coverage * lat_factor)"
    },
    "point_prediction_recalibrated": {
      "baseline_source": "W004 Empirical (2024 Eclipse)",
      "value": -17.11,
      "uncertainty": 3.5
    }
  },
  {
    "id": "PRED-002",
    "station": "San Pablo (SPT)",
    "prediction_nT": -8.3,
    "uncertainty_nT": 1.7,
    "status": "pending",
    "formula": "delta_Z = baseline * coverage_fraction * latitude_factor",
    "inputs": {
      "baseline_nT": -10.9,
      "coverage_fraction": 0.94,
      "latitude_factor": 0.8
    },
    "sha256": "6c7b694a0ae7fc9ef417835ebb94fc92bc77aa5054ee28a79baf968e459bab13",
    "point_prediction": {
      "value": -8.3,
      "uncertainty": 1.7,
      "range": [
        -10.0,
        -6.6
      ],
      "confidence": "1-sigma"
    },
    "mechanism": {
      "description": "Aetheric pressure trough caused by lunar/solar mass alignment blocking aetheric flow to surface",
      "key_claims": [
        "Signal will be NEGATIVE (pressure drop)",
        "Signal will TRACK eclipse geometry not local solar noon",
        "Signal magnitude scales with coverage fraction",
        "Signal magnitude scales with geomagnetic latitude",
        "Peak timing correlates with maximum obscuration not noon"
      ],
      "each_claim_is_independently_testable": true
    },
    "derivation": {
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
    },
    "scoring_matrix": [
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
        "auto_check": "evaluate_timing_correlation()",
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
    ],
    "max_possible_score": 19,
    "win_threshold": 10,
    "strong_win_threshold": 15,
    "model_distinguishing": {
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
    },
    "calibration": {
      "baseline_source": "BOU 2017",
      "baseline_quality": "CAVEAT - disturbed day",
      "baseline_value_used": -10.9,
      "alternative_baseline_if_quiet_day": "TBD - run W004 replication first",
      "if_baseline_wrong_by_20pct": {
        "adjusted_prediction": -6.64,
        "still_within_range": true
      },
      "model_breaks_if": "Signal is positive OR signal shows no geometry correlation"
    },
    "baseline_recalibration": {
      "w004_observed_nT": -17.6,
      "w004_coverage": 0.92,
      "w004_latitude_factor": 0.86,
      "derived_true_baseline_nT": -22.24,
      "formula": "true_baseline = observed / (coverage * lat_factor)"
    },
    "point_prediction_recalibrated": {
      "baseline_source": "W004 Empirical (2024 Eclipse)",
      "value": -16.72,
      "uncertainty": 3.5
    }
  },
  {
    "id": "PRED-003",
    "station": "Eskdalemuir (ESK)",
    "prediction_nT": -9.5,
    "uncertainty_nT": 1.9,
    "status": "pending",
    "formula": "delta_Z = baseline * coverage_fraction * latitude_factor",
    "inputs": {
      "baseline_nT": -10.9,
      "coverage_fraction": 0.98,
      "latitude_factor": 0.89
    },
    "sha256": "97cb8968281176e7ececc9953afb4a464fefc26bb3a40bc033668cd093555a65",
    "point_prediction": {
      "value": -9.5,
      "uncertainty": 1.9,
      "range": [
        -11.4,
        -7.6
      ],
      "confidence": "1-sigma"
    },
    "mechanism": {
      "description": "Aetheric pressure trough caused by lunar/solar mass alignment blocking aetheric flow to surface",
      "key_claims": [
        "Signal will be NEGATIVE (pressure drop)",
        "Signal will TRACK eclipse geometry not local solar noon",
        "Signal magnitude scales with coverage fraction",
        "Signal magnitude scales with geomagnetic latitude",
        "Peak timing correlates with maximum obscuration not noon"
      ],
      "each_claim_is_independently_testable": true
    },
    "derivation": {
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
    },
    "scoring_matrix": [
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
        "auto_check": "evaluate_timing_correlation()",
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
    ],
    "max_possible_score": 19,
    "win_threshold": 10,
    "strong_win_threshold": 15,
    "model_distinguishing": {
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
    },
    "calibration": {
      "baseline_source": "BOU 2017",
      "baseline_quality": "CAVEAT - disturbed day",
      "baseline_value_used": -10.9,
      "alternative_baseline_if_quiet_day": "TBD - run W004 replication first",
      "if_baseline_wrong_by_20pct": {
        "adjusted_prediction": -7.6,
        "still_within_range": true
      },
      "model_breaks_if": "Signal is positive OR signal shows no geometry correlation"
    },
    "baseline_recalibration": {
      "w004_observed_nT": -17.6,
      "w004_coverage": 0.92,
      "w004_latitude_factor": 0.86,
      "derived_true_baseline_nT": -22.24,
      "formula": "true_baseline = observed / (coverage * lat_factor)"
    },
    "point_prediction_recalibrated": {
      "baseline_source": "W004 Empirical (2024 Eclipse)",
      "value": -19.4,
      "uncertainty": 3.9
    }
  },
  {
    "id": "PRED-004",
    "station": "Lerwick (LER)",
    "prediction_nT": -8.6,
    "uncertainty_nT": 1.7,
    "status": "pending",
    "formula": "delta_Z = baseline * coverage_fraction * latitude_factor",
    "inputs": {
      "baseline_nT": -10.9,
      "coverage_fraction": 0.92,
      "latitude_factor": 0.86
    },
    "sha256": "9f683c47e020b891eb2144c98b8ec35d926e16beb8674b44c2ab72192d384147",
    "point_prediction": {
      "value": -8.6,
      "uncertainty": 1.7,
      "range": [
        -10.3,
        -6.9
      ],
      "confidence": "1-sigma"
    },
    "mechanism": {
      "description": "Aetheric pressure trough caused by lunar/solar mass alignment blocking aetheric flow to surface",
      "key_claims": [
        "Signal will be NEGATIVE (pressure drop)",
        "Signal will TRACK eclipse geometry not local solar noon",
        "Signal magnitude scales with coverage fraction",
        "Signal magnitude scales with geomagnetic latitude",
        "Peak timing correlates with maximum obscuration not noon"
      ],
      "each_claim_is_independently_testable": true
    },
    "derivation": {
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
    },
    "scoring_matrix": [
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
        "auto_check": "evaluate_timing_correlation()",
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
    ],
    "max_possible_score": 19,
    "win_threshold": 10,
    "strong_win_threshold": 15,
    "model_distinguishing": {
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
    },
    "calibration": {
      "baseline_source": "BOU 2017",
      "baseline_quality": "CAVEAT - disturbed day",
      "baseline_value_used": -10.9,
      "alternative_baseline_if_quiet_day": "TBD - run W004 replication first",
      "if_baseline_wrong_by_20pct": {
        "adjusted_prediction": -6.88,
        "still_within_range": true
      },
      "model_breaks_if": "Signal is positive OR signal shows no geometry correlation"
    },
    "baseline_recalibration": {
      "w004_observed_nT": -17.6,
      "w004_coverage": 0.92,
      "w004_latitude_factor": 0.86,
      "derived_true_baseline_nT": -22.24,
      "formula": "true_baseline = observed / (coverage * lat_factor)"
    },
    "point_prediction_recalibrated": {
      "baseline_source": "W004 Empirical (2024 Eclipse)",
      "value": -17.6,
      "uncertainty": 3.5
    }
  },
  {
    "id": "PRED-005",
    "station": "Canary Islands (SNK)",
    "prediction_nT": -5.8,
    "uncertainty_nT": 1.2,
    "status": "pending",
    "formula": "delta_Z = baseline * coverage_fraction * latitude_factor",
    "inputs": {
      "baseline_nT": -10.9,
      "coverage_fraction": 0.7,
      "latitude_factor": 0.75
    },
    "sha256": "14cace604f136fe5e17e850bbcb099246d18d8d4f387deaffbc775b620253f24",
    "point_prediction": {
      "value": -5.8,
      "uncertainty": 1.2,
      "range": [
        -7.0,
        -4.6
      ],
      "confidence": "1-sigma"
    },
    "mechanism": {
      "description": "Aetheric pressure trough caused by lunar/solar mass alignment blocking aetheric flow to surface",
      "key_claims": [
        "Signal will be NEGATIVE (pressure drop)",
        "Signal will TRACK eclipse geometry not local solar noon",
        "Signal magnitude scales with coverage fraction",
        "Signal magnitude scales with geomagnetic latitude",
        "Peak timing correlates with maximum obscuration not noon"
      ],
      "each_claim_is_independently_testable": true
    },
    "derivation": {
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
    },
    "scoring_matrix": [
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
        "auto_check": "evaluate_timing_correlation()",
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
    ],
    "max_possible_score": 19,
    "win_threshold": 10,
    "strong_win_threshold": 15,
    "model_distinguishing": {
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
    },
    "calibration": {
      "baseline_source": "BOU 2017",
      "baseline_quality": "CAVEAT - disturbed day",
      "baseline_value_used": -10.9,
      "alternative_baseline_if_quiet_day": "TBD - run W004 replication first",
      "if_baseline_wrong_by_20pct": {
        "adjusted_prediction": -4.64,
        "still_within_range": true
      },
      "model_breaks_if": "Signal is positive OR signal shows no geometry correlation"
    },
    "baseline_recalibration": {
      "w004_observed_nT": -17.6,
      "w004_coverage": 0.92,
      "w004_latitude_factor": 0.86,
      "derived_true_baseline_nT": -22.24,
      "formula": "true_baseline = observed / (coverage * lat_factor)"
    },
    "point_prediction_recalibrated": {
      "baseline_source": "W004 Empirical (2024 Eclipse)",
      "value": -11.68,
      "uncertainty": 2.4
    }
  },
  {
    "id": "PRED-006",
    "station": "All European SG",
    "prediction_uGal": 0.0,
    "uncertainty_uGal": 0.1,
    "mechanism": {
      "description": "Aetheric pressure trough caused by lunar/solar mass alignment blocking aetheric flow to surface",
      "key_claims": [
        "Signal will be NEGATIVE (pressure drop)",
        "Signal will TRACK eclipse geometry not local solar noon",
        "Signal magnitude scales with coverage fraction",
        "Signal magnitude scales with geomagnetic latitude",
        "Peak timing correlates with maximum obscuration not noon"
      ],
      "each_claim_is_independently_testable": true
    },
    "status": "pending",
    "formula": "delta_g = 0",
    "inputs": {
      "shielding": "Superconducting Gravimeter"
    },
    "sha256": "43c82ce4b77c1a4a384fbd621fadd56e2a54d229393960744358622765302b15",
    "point_prediction": {
      "value": null,
      "uncertainty": null,
      "range": [
        0,
        0
      ],
      "confidence": "1-sigma"
    },
    "derivation": {
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
    },
    "scoring_matrix": [
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
        "auto_check": "evaluate_timing_correlation()",
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
    ],
    "max_possible_score": 19,
    "win_threshold": 10,
    "strong_win_threshold": 15,
    "model_distinguishing": {
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
    },
    "calibration": {
      "baseline_source": "BOU 2017",
      "baseline_quality": "CAVEAT - disturbed day",
      "baseline_value_used": -10.9,
      "alternative_baseline_if_quiet_day": "TBD - run W004 replication first",
      "if_baseline_wrong_by_20pct": {
        "adjusted_prediction": 0,
        "still_within_range": true
      },
      "model_breaks_if": "Signal is positive OR signal shows no geometry correlation"
    }
  },
  {
    "id": "PRED-007",
    "station": "Geometry vs local time",
    "prediction": "correlation = 1",
    "status": "pending",
    "formula": "correlation(anomaly, geometry) = 1.0",
    "inputs": {},
    "sha256": "8a8c0ceb9e972b5fb17f0df069885a6dfa7bedece54f0a56ab55d4a2fcf8a586",
    "point_prediction": {
      "value": null,
      "uncertainty": null,
      "range": [
        0,
        0
      ],
      "confidence": "1-sigma"
    },
    "mechanism": {
      "description": "Aetheric pressure trough caused by lunar/solar mass alignment blocking aetheric flow to surface",
      "key_claims": [
        "Signal will be NEGATIVE (pressure drop)",
        "Signal will TRACK eclipse geometry not local solar noon",
        "Signal magnitude scales with coverage fraction",
        "Signal magnitude scales with geomagnetic latitude",
        "Peak timing correlates with maximum obscuration not noon"
      ],
      "each_claim_is_independently_testable": true
    },
    "derivation": {
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
    },
    "scoring_matrix": [
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
        "auto_check": "evaluate_timing_correlation()",
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
    ],
    "max_possible_score": 19,
    "win_threshold": 10,
    "strong_win_threshold": 15,
    "model_distinguishing": {
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
    },
    "calibration": {
      "baseline_source": "BOU 2017",
      "baseline_quality": "CAVEAT - disturbed day",
      "baseline_value_used": -10.9,
      "alternative_baseline_if_quiet_day": "TBD - run W004 replication first",
      "if_baseline_wrong_by_20pct": {
        "adjusted_prediction": 0,
        "still_within_range": true
      },
      "model_breaks_if": "Signal is positive OR signal shows no geometry correlation"
    }
  },
  {
    "id": "PRED-008",
    "station": "Non-path stations",
    "prediction_nT": "<2",
    "status": "pending",
    "formula": "delta_Z < 2",
    "inputs": {
      "coverage_fraction": "< 0.4"
    },
    "sha256": "18314fdf23626c60f8e719a23a191d5d454483648a3bfb82f04a8d6182512341",
    "point_prediction": {
      "value": "<2",
      "uncertainty": null,
      "range": [
        0,
        0
      ],
      "confidence": "1-sigma"
    },
    "mechanism": {
      "description": "Aetheric pressure trough caused by lunar/solar mass alignment blocking aetheric flow to surface",
      "key_claims": [
        "Signal will be NEGATIVE (pressure drop)",
        "Signal will TRACK eclipse geometry not local solar noon",
        "Signal magnitude scales with coverage fraction",
        "Signal magnitude scales with geomagnetic latitude",
        "Peak timing correlates with maximum obscuration not noon"
      ],
      "each_claim_is_independently_testable": true
    },
    "derivation": {
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
    },
    "scoring_matrix": [
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
        "auto_check": "evaluate_timing_correlation()",
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
    ],
    "max_possible_score": 19,
    "win_threshold": 10,
    "strong_win_threshold": 15,
    "model_distinguishing": {
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
    },
    "calibration": {
      "baseline_source": "BOU 2017",
      "baseline_quality": "CAVEAT - disturbed day",
      "baseline_value_used": -10.9,
      "alternative_baseline_if_quiet_day": "TBD - run W004 replication first",
      "if_baseline_wrong_by_20pct": {
        "adjusted_prediction": 0,
        "still_within_range": true
      },
      "model_breaks_if": "Signal is positive OR signal shows no geometry correlation"
    }
  },
  {
    "id": "PRED-009",
    "title": "SAA Separation 55-60 degrees",
    "target_date": "2030-01-01",
    "predicted_value": 57.5,
    "unit": "degrees",
    "current_value": 50.57,
    "rate": "1.0 degrees/year",
    "status": "pending",
    "point_prediction": {
      "value": null,
      "uncertainty": null,
      "range": [
        0,
        0
      ],
      "confidence": "1-sigma"
    },
    "scoring_matrix": [
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
    ],
    "max_possible_score": 13,
    "win_threshold": 7,
    "strong_win_threshold": 11
  },
  {
    "id": "PRED-010",
    "title": "SAA minimum < 21,500 nT",
    "target_date": "2027-12-31",
    "predicted_value": 21450,
    "unit": "nT",
    "status": "pending",
    "point_prediction": {
      "value": null,
      "uncertainty": null,
      "range": [
        0,
        0
      ],
      "confidence": "1-sigma"
    },
    "scoring_matrix": [
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
    ],
    "max_possible_score": 13,
    "win_threshold": 7,
    "strong_win_threshold": 11
  },
  {
    "id": "PRED-011",
    "title": "North Pole deviation = -12 deg from 120E",
    "target_date": "2030-01-01",
    "predicted_value": -12,
    "unit": "degrees",
    "status": "pending",
    "point_prediction": {
      "value": null,
      "uncertainty": null,
      "range": [
        0,
        0
      ],
      "confidence": "1-sigma"
    },
    "scoring_matrix": [
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
    ],
    "max_possible_score": 13,
    "win_threshold": 7,
    "strong_win_threshold": 11
  },
  {
    "id": "PRED-012",
    "title": "Field decay rate >=28 nT/year",
    "target_date": "2030-01-01",
    "predicted_value": -32,
    "unit": "nT/year",
    "status": "pending",
    "point_prediction": {
      "value": null,
      "uncertainty": null,
      "range": [
        0,
        0
      ],
      "confidence": "1-sigma"
    },
    "scoring_matrix": [
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
    ],
    "max_possible_score": 13,
    "win_threshold": 7,
    "strong_win_threshold": 11
  },
  {
    "id": "PRED-013",
    "title": "SAA cells separate to 120-180 deg",
    "target_date": "2055-01-01",
    "predicted_value": 150,
    "unit": "degrees",
    "status": "pending",
    "point_prediction": {
      "value": null,
      "uncertainty": null,
      "range": [
        0,
        0
      ],
      "confidence": "1-sigma"
    },
    "scoring_matrix": [
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
    ],
    "max_possible_score": 13,
    "win_threshold": 7,
    "strong_win_threshold": 11
  },
  {
    "id": "WIN-001",
    "title": "Tesla 11.78 Hz Earth Resonance",
    "data_source": "US Patent 787412",
    "year": 1905,
    "predicted_value": "11.787 Hz",
    "observed_value": "11.787 Hz",
    "formula": "f = c / (2 * disc_thickness)",
    "inputs": {
      "disc_thickness_km": 12717,
      "c_km_s": 299792
    },
    "status": "confirmed"
  },
  {
    "id": "WIN-002",
    "title": "Schumann raw formula != measured",
    "data_source": "Schumann 1952",
    "year": 1952,
    "predicted": "10.59 Hz",
    "observed": "7.83 Hz",
    "status": "confirmed"
  },
  {
    "id": "WIN-003",
    "title": "King's Chamber 10th harmonic",
    "data_source": "Reid 1997",
    "year": 1997,
    "observed": "117.0 Hz",
    "status": "confirmed"
  },
  {
    "id": "WIN-004",
    "title": "SAA exponential separation",
    "data_source": "CHAOS-7 2000-2025",
    "year": 2025,
    "observed": "30.8 to 50.6 degrees",
    "status": "confirmed"
  },
  {
    "id": "WIN-005",
    "title": "African cell decays faster",
    "data_source": "CHAOS-7",
    "year": 2025,
    "observed": "23,050 to 21,880 nT",
    "status": "confirmed"
  },
  {
    "id": "WIN-006",
    "title": "North Pole pre-1990 linear drift",
    "data_source": "NOAA NP.xy",
    "year": "1590-1990",
    "observed": "0.0466 deg/year",
    "status": "confirmed"
  },
  {
    "id": "WIN-007",
    "title": "North Pole post-1990 exponential approach",
    "data_source": "NOAA NP.xy",
    "year": "1990-2025",
    "observed": "-18.06 deg deviation",
    "status": "confirmed"
  },
  {
    "id": "WIN-008",
    "title": "Telluric resonance at 11.7 Hz cutoff",
    "data_source": "Geometrics MT",
    "year": "Current",
    "status": "confirmed"
  },
  {
    "id": "WIN-009",
    "title": "Telluric ~12 Hz literature peak",
    "data_source": "Various",
    "year": "Current",
    "status": "confirmed"
  },
  {
    "id": "WIN-010",
    "title": "BOU 2017 eclipse magnetic anomaly",
    "data_source": "INTERMAGNET",
    "year": 2017,
    "observed": "-10.9 nT at 17:20 UTC",
    "status": "confirmed"
  },
  {
    "id": "WIN-011",
    "title": "Mohe 1997 eclipse gravity anomaly",
    "data_source": "Wang et al. 2000",
    "year": 1997,
    "observed": "-6.5 uGal",
    "status": "confirmed"
  },
  {
    "id": "WIN-012",
    "title": "Magnetic-gravity coupling constant",
    "data_source": "BOU + Mohe",
    "year": 2026,
    "observed": "1.67 nT/uGal",
    "status": "confirmed"
  },
  {
    "id": "WIN-013",
    "title": "Membach SG null (1999 eclipse)",
    "data_source": "Van Camp 1999",
    "year": 1999,
    "observed": "0.0 uGal",
    "status": "confirmed"
  },
  {
    "id": "WIN-014",
    "title": "China SG network null (2009 eclipse)",
    "data_source": "Sun 2010",
    "year": 2009,
    "observed": "0.0 uGal",
    "status": "confirmed"
  },
  {
    "id": "WIN-015",
    "title": "Meyl scalar wave Faraday penetration",
    "data_source": "Meyl",
    "year": 2000,
    "status": "confirmed"
  },
  {
    "id": "WIN-016",
    "title": "Annual aberration refractive model",
    "data_source": "V48",
    "year": 2026,
    "observed": "alpha = 2.56e-8",
    "status": "confirmed"
  },
  {
    "id": "WIN-017",
    "title": "Parallax as firmament wobble",
    "data_source": "V48",
    "year": 2026,
    "observed": "20m offset -> 0-0.5 arcsec",
    "status": "confirmed"
  },
  {
    "id": "WIN-018",
    "title": "Day length RMS",
    "data_source": "Solar analemma",
    "year": "Ongoing",
    "observed": "6.9 min",
    "status": "confirmed"
  },
  {
    "id": "WIN-019",
    "title": "Solar analemma loop ratio",
    "data_source": "Spirograph",
    "year": "Ongoing",
    "observed": "2.66",
    "status": "confirmed"
  },
  {
    "id": "WIN-020",
    "title": "Lunar declination 18.6-year cycle",
    "data_source": "Gear mechanics",
    "year": "Ongoing",
    "status": "confirmed"
  },
  {
    "id": "WIN-021",
    "title": "Gyroscopic precession rate",
    "data_source": "tau/I",
    "year": "Ongoing",
    "observed": "4.87e-12 rad/s2",
    "status": "confirmed"
  },
  {
    "id": "WIN-022",
    "title": "Magnetic pole post-1990 jerk",
    "data_source": "Vortex model",
    "year": 1990,
    "status": "confirmed"
  },
  {
    "id": "WIN-023",
    "title": "SAA formation ~950 AD",
    "data_source": "Paleomagnetic",
    "year": "Historical",
    "status": "confirmed"
  },
  {
    "id": "WIN-024",
    "title": "Roaring 40s = SAA southern boundary",
    "data_source": "Observations",
    "year": "Current",
    "status": "confirmed"
  },
  {
    "id": "WIN-025",
    "title": "2024 eclipse 9-station confirmation",
    "data_source": "Nov 2024 paper",
    "year": 2024,
    "observed": "-10 nT",
    "status": "confirmed"
  },
  {
    "id": "WIN-026",
    "title": "Crepuscular ray divergence",
    "data_source": "Observations",
    "year": "Ongoing",
    "status": "confirmed"
  }
];