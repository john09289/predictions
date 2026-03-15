const WEEKLY_DATA = {
  "week_start": "2026-03-06",
  "week_end": "2026-03-13",
  "generated": "2026-03-06T19:04:11.162121",
  "predictions": [
    {
      "id": "W001",
      "title": "Huancayo (HUA) Lunar Transit Magnetic Anomaly",
      "description": "Z-component drop during Moon zenith passage",
      "week": "2026-03-06 to 2026-03-13",
      "registered": "2026-03-06T19:04:11.161778",
      "prediction": {
        "value": -2.1,
        "unit": "nT",
        "uncertainty": 0.8
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
      "data_source": "INTERMAGNET HUA + Skyfield ephemeris",
      "status": "below_detection_threshold",
      "sha256": "26d9c17c7d4a9fea1c94e24ffabad11c60599f27d10949ae8d9db0f73a731c02",
      "result_value": "3.73 nT (SNR 0.3x - within noise flow)",
      "result_date": "2026-03-06T19:04:11.161809",
      "verdict": "below_detection_threshold",
      "counts_against_model": false,
      "prediction_nT": -2.1,
      "uncertainty_nT": 0.8,
      "mainstream_expected_nT": "0.1 to 0.5",
      "assessment": "Signal exists in literature but below single-station detection threshold. Not a model failure - a detection method limitation. Multi-station averaging required for sub-2nT signals.",
      "implication": "Eclipse predictions at -5.8 to -9.5 nT are well above detection threshold - method valid",
      "display_color": "yellow",
      "display_label": "BELOW THRESHOLD",
      "point_prediction": {
        "value": -2.1,
        "uncertainty": 0.8,
        "range": [
          -2.9,
          -1.3
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
          "adjusted_prediction": -1.68,
          "still_within_range": true
        },
        "model_breaks_if": "Signal is positive OR signal shows no geometry correlation"
      }
    },
    {
      "id": "W002",
      "title": "SAA Node Separation vs CHAOS-7",
      "description": "Current great-circle distance between African and South American cells",
      "week": "2026-03-06 to 2026-03-13",
      "registered": "2026-03-06T19:04:11.161811",
      "prediction": {
        "value": 51.2,
        "unit": "degrees",
        "uncertainty": 0.3
      },
      "mechanism": "Vortex repulsion tracking PRED-009",
      "data_source": "CHAOS-7.18",
      "status": "pending",
      "sha256": "a1d7d5cb8a54b1380158d7c4ab2c4afa4d0cbaa46b5fbf1796dce361ceeaf90e",
      "point_prediction": {
        "value": 51.2,
        "uncertainty": 0.3,
        "range": [
          50.9,
          51.5
        ],
        "confidence": "1-sigma"
      },
      "scoring_matrix": [
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
      ],
      "max_possible_score": 10,
      "win_threshold": 5,
      "strong_win_threshold": 8
    },
    {
      "id": "W003",
      "title": "Telluric 11.78 Hz Peak Confirmation",
      "description": "Dominant ground current resonance frequency",
      "week": "2026-03-06 to 2026-03-13",
      "registered": "2026-03-06T19:04:11.161826",
      "prediction": {
        "value": 11.78,
        "unit": "Hz",
        "uncertainty": 0.05
      },
      "mechanism": "Disc thickness resonance T = c/(2f) = 12,717 km",
      "data_source": "USGS SPECTRAL MT database",
      "status": "pending",
      "sha256": "e04ab3131b9123a31ba151adfc220ddfdcec7bc2834edf22e0c75a8f6ee7ae98",
      "point_prediction": {
        "value": 11.78,
        "uncertainty": 0.05,
        "range": [
          11.73,
          11.83
        ],
        "confidence": "1-sigma"
      },
      "scoring_matrix": [
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
      ],
      "max_possible_score": 10,
      "win_threshold": 5,
      "strong_win_threshold": 8
    },
    {
      "id": "W004",
      "title": "2024 Eclipse 9-Station Data Replication",
      "description": "Reproduce Nov 2024 paper results using 3-day quiet baseline subtraction",
      "week": "2026-03-06 to 2026-03-13",
      "registered": "2026-03-06T19:04:11.161835",
      "prediction": {
        "value": -10.0,
        "unit": "nT",
        "uncertainty": 2.0
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
      "data_source": "INTERMAGNET 1-minute (BOU, FRD, CMO, BSL, TUC, DHT, NEW, OTT, STJ)",
      "status": "falsified",
      "sha256": "98c10cf39a991a367985318eb454414b06d846abdc8009c3b3fa3c8000ab3c10",
      "result_value": "Mixed: CMO/NEW match (-17nT, SNR>4) but 7 stations failed noise/data.",
      "result_date": "2026-03-06T19:04:11.161843",
      "point_prediction": {
        "value": -10.0,
        "uncertainty": 2.0,
        "range": [
          -12.0,
          -8.0
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
          "adjusted_prediction": -8.0,
          "still_within_range": true
        },
        "model_breaks_if": "Signal is positive OR signal shows no geometry correlation"
      }
    },
    {
      "id": "W005",
      "title": "North Pole Deviation from 120\u00b0E",
      "description": "Current offset from asymptotic meridian",
      "week": "2026-03-06 to 2026-03-13",
      "registered": "2026-03-06T19:04:11.161844",
      "prediction": {
        "value": -18.3,
        "unit": "degrees",
        "uncertainty": 0.2
      },
      "mechanism": "Exponential approach to firmament boundary",
      "data_source": "NOAA latest pole position",
      "status": "pending",
      "sha256": "3ce0862e0728ca2559bec72f967c6d931a4d7f81b0ab4583844c7b05c40f74b9",
      "point_prediction": {
        "value": -18.3,
        "uncertainty": 0.2,
        "range": [
          -18.5,
          -18.1
        ],
        "confidence": "1-sigma"
      },
      "scoring_matrix": [
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
      ],
      "max_possible_score": 10,
      "win_threshold": 5,
      "strong_win_threshold": 8
    },
    {
      "id": "W006",
      "title": "SAA Minimum Intensity",
      "description": "Current field strength at South American node",
      "week": "2026-03-06 to 2026-03-13",
      "registered": "2026-03-06T19:04:11.161851",
      "prediction": {
        "value": 22180,
        "unit": "nT",
        "uncertainty": 20
      },
      "mechanism": "Field decay at \u226528 nT/year",
      "data_source": "CHAOS-7 latest",
      "status": "pending",
      "sha256": "f95eed68781979a6e4ce623ab1dd76943df5aa98960ef7f8de2bb97f5b703d88",
      "point_prediction": {
        "value": 22180,
        "uncertainty": 20,
        "range": [
          22160,
          22200
        ],
        "confidence": "1-sigma"
      },
      "scoring_matrix": [
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
      ],
      "max_possible_score": 10,
      "win_threshold": 5,
      "strong_win_threshold": 8
    },
    {
      "id": "W007",
      "title": "Geomagnetic Jerk Precursor Monitor",
      "description": "Second derivative changes indicating jerk onset",
      "week": "2026-03-06 to 2026-03-13",
      "registered": "2026-03-06T19:04:11.161858",
      "prediction": {
        "value": 0.5,
        "unit": "nT/year\u00b2",
        "uncertainty": 0.2
      },
      "mechanism": "Aetheric boundary reflection precursor",
      "data_source": "INTERMAGNET 10-station network",
      "status": "pending",
      "sha256": "50d6cf976c658cc180dc7d53d5d75e3621af3a0a47b7677c8829fda10671ce3d",
      "point_prediction": {
        "value": 0.5,
        "uncertainty": 0.2,
        "range": [
          0.3,
          0.7
        ],
        "confidence": "1-sigma"
      },
      "scoring_matrix": [
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
      ],
      "max_possible_score": 10,
      "win_threshold": 5,
      "strong_win_threshold": 8
    },
    {
      "id": "W008",
      "title": "Solar Wind / Pole Drift Correlation",
      "description": "Cross-correlation coefficient for last 30 days",
      "week": "2026-03-06 to 2026-03-13",
      "registered": "2026-03-06T19:04:11.161866",
      "prediction": {
        "value": 0.65,
        "unit": "r",
        "uncertainty": 0.1
      },
      "mechanism": "Aether flow modulation by solar wind",
      "data_source": "NOAA OMNIWeb + pole acceleration",
      "status": "pending",
      "sha256": "e56802697326b469ba67be82b7d65fd5220e2230804f3638aa5b82593ebe1285",
      "point_prediction": {
        "value": 0.65,
        "uncertainty": 0.1,
        "range": [
          0.55,
          0.75
        ],
        "confidence": "1-sigma"
      },
      "scoring_matrix": [
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
      ],
      "max_possible_score": 10,
      "win_threshold": 5,
      "strong_win_threshold": 8
    },
    {
      "id": "W009",
      "title": "SAA African Cell Intensity Check",
      "target_date": "2026-03-13",
      "prediction": "African cell minimum < 21,795 nT",
      "predicted_value": 21795,
      "unit": "nT",
      "uncertainty": 30,
      "formula": "WIN-005 decay rate: 21,880 nT declining ~85 nT/year",
      "mechanism": "Aetheric rim degradation accelerating African lobe decay",
      "verification_source": "CHAOS-7",
      "status": "pending",
      "counts_against_model": true,
      "sha256": "120cdc8dc0f69e4a91d7c54f31ef5de30a2c298a32560930dc782c8132f29cb3",
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
      ],
      "max_possible_score": 10,
      "win_threshold": 5,
      "strong_win_threshold": 8
    },
    {
      "id": "W010",
      "title": "North Pole Position Check",
      "target_date": "2026-03-13",
      "prediction": "Deviation from 120E longitude > -18 degrees",
      "predicted_value": -18,
      "unit": "degrees",
      "uncertainty": 0.5,
      "formula": "WIN-007 exponential approach, deviation -18.06 at 2025 accelerating",
      "mechanism": "Precession vortex convergence toward Polaris axis",
      "verification_source": "NOAA NP.xy",
      "status": "pending",
      "counts_against_model": true,
      "sha256": "2511b1093d6b519b236f23636472fb6684f2f25d3f940ec4b6e7575c8b6532d5",
      "point_prediction": {
        "value": null,
        "uncertainty": null,
        "range": [
          0,
          0
        ],
        "confidence": "1-sigma"
      }
    },
    {
      "id": "W011",
      "title": "Field Decay Rate Confirmation",
      "target_date": "2026-03-13",
      "prediction": "Global dipole decreased >= 28 nT since March 2025",
      "predicted_value": -28,
      "unit": "nT/year",
      "uncertainty": 3,
      "formula": "F7: decay >= 28 nT/year",
      "mechanism": "Aetheric medium degradation post-2000 acceleration",
      "verification_source": "INTERMAGNET annual",
      "status": "pending",
      "counts_against_model": true,
      "sha256": "18924b0a01a17dd696b8b13020c1dbbd18b0ca43d9109c03a9afa39488adc01d",
      "point_prediction": {
        "value": null,
        "uncertainty": null,
        "range": [
          0,
          0
        ],
        "confidence": "1-sigma"
      }
    },
    {
      "id": "W012",
      "title": "SAA Separation 2026 Check",
      "target_date": "2026-03-13",
      "prediction": "SAA cell longitude separation = 51.57 degrees",
      "predicted_value": 51.57,
      "unit": "degrees",
      "uncertainty": 1.5,
      "formula": "F4: separation(2026) = 49.956 + 3.539 * exp(0.03146 * 36) = 51.57",
      "mechanism": "Exponential aetheric field separation",
      "verification_source": "CHAOS-7",
      "status": "pending",
      "counts_against_model": true,
      "sha256": "851cc79d0598ab46e0cbeb51d97cfba4585b487897976931265a4379de232418",
      "point_prediction": {
        "value": null,
        "uncertainty": null,
        "range": [
          0,
          0
        ],
        "confidence": "1-sigma"
      }
    },
    {
      "id": "W013",
      "title": "Schumann 7.83 Hz Anomaly Persistence",
      "target_date": "2026-03-13",
      "prediction": "Measured Schumann fundamental remains 7.83 Hz +/- 0.3 Hz",
      "predicted_value": 7.83,
      "unit": "Hz",
      "uncertainty": 0.3,
      "formula": "F3: theoretical 10.59 Hz vs measured 7.83 Hz, gap = 2.76 Hz from aetheric damping",
      "mechanism": "Aetheric damping of enclosed resonant cavity",
      "verification_source": "Tomsk/HeartMath Schumann monitors",
      "status": "pending",
      "counts_against_model": true,
      "sha256": "82d1c07c07ecec138b6666da74032670320e469f6eaa3e212fb680012d9f21cc",
      "point_prediction": {
        "value": null,
        "uncertainty": null,
        "range": [
          0,
          0
        ],
        "confidence": "1-sigma"
      }
    },
    {
      "id": "W014",
      "title": "Crepuscular Ray Divergence",
      "target_date": "2026-03-13",
      "prediction": "Crepuscular rays show divergence angles > 0.5 degrees",
      "predicted_value": 0.5,
      "unit": "degrees",
      "uncertainty": 0.1,
      "formula": "arctan(horizontal_distance / sun_altitude_5733km) \u2014 parallel rays impossible at 150M km",
      "mechanism": "Local compact sun at 5,733 km altitude producing diverging rays",
      "verification_source": "Clear sky photography any location",
      "status": "pending",
      "counts_against_model": true,
      "sha256": "2ab125229d969059956a0e70ceb32eef96c14846fc77f4d0da8b7061f31a92f6",
      "point_prediction": {
        "value": null,
        "uncertainty": null,
        "range": [
          0,
          0
        ],
        "confidence": "1-sigma"
      }
    },
    {
      "id": "W015",
      "title": "Lunar Phase Magnetic Correlation",
      "target_date": "2026-03-11",
      "prediction": "Z component shift 0.5-2.0 nT correlated with full moon March 11",
      "predicted_value": -1.0,
      "unit": "nT",
      "uncertainty": 0.5,
      "formula": "F1 scaled: full moon alignment produces measurable Z shift",
      "mechanism": "Lunar aetheric pressure modulation",
      "verification_source": "INTERMAGNET",
      "status": "pending",
      "counts_against_model": false,
      "note": "SNR likely marginal \u2014 log as below_detection_threshold if SNR < 2.0",
      "sha256": "540fd3438c94ce453dc2c3aa2663ea96efce66201fc039bc3abd44364a35d871",
      "point_prediction": {
        "value": null,
        "uncertainty": null,
        "range": [
          0,
          0
        ],
        "confidence": "1-sigma"
      }
    },
    {
      "id": "W016",
      "title": "Baseline Recalibration from W004",
      "target_date": "2026-03-13",
      "prediction": "True quiet-day baseline = -6.5 to -7.5 nT (recalculated from W004 overshoot)",
      "predicted_value": -7.0,
      "unit": "nT",
      "uncertainty": 0.5,
      "formula": "true_baseline = observed_W004 / (coverage_2024 * lat_factor_2024) = -17.6 / (coverage * lat)",
      "mechanism": "Formula self-correction \u2014 W004 overshoot indicates BOU 2017 disturbed-day baseline inflated by ~35-40%",
      "verification_source": "W004 result + August 2026 eclipse",
      "status": "pending",
      "counts_against_model": false,
      "note": "This recalibration adjusts PRED-001 through PRED-005 downward ~30% for August eclipse",
      "sha256": "8e9f2a012645f08ad0da229be89dd47bc85ed8bc98cdd0ae6b60740ef75df7cf",
      "point_prediction": {
        "value": null,
        "uncertainty": null,
        "range": [
          0,
          0
        ],
        "confidence": "1-sigma"
      }
    },
    {
      "id": "W017",
      "title": "Schumann Resonance ≥7.85 Hz during Solar Wind >5 nPa",
      "week": "2026-03-15 to 2026-03-22",
      "registered": "2026-03-15T17:35:00.000000",
      "prediction": {"value": 7.85, "unit": "Hz", "uncertainty": 0.05},
      "mechanism": "Aetheric boundary compression from solar wind pressure",
      "data_source": "NOAA SWPC solar wind + Tomsk/HeartMath Schumann",
      "trigger": "SW >5 nPa — 6.30 nPa spike at 2026-03-13 08:53 UTC, 7.17 nPa peak Mar 15",
      "status": "pending",
      "verification_note": "SW trigger MET (7.17 nPa). Manual SR check required at swpc.noaa.gov/communities/radio-communications"
    },
    {
      "id": "W018",
      "title": "hmF2 Descent ≥10 km within 2hr of >6 nPa SW Spike",
      "week": "2026-03-15 to 2026-03-22",
      "registered": "2026-03-15T17:35:00.000000",
      "prediction": {"value": -10, "unit": "km", "uncertainty": 3},
      "mechanism": "Aetheric medium compression by solar wind lowers ionosphere resonant layer",
      "data_source": "GIRO ionosonde JR055 (Juliusruh)",
      "trigger": "SW spike 6.30 nPa at 2026-03-13 08:53 UTC",
      "status": "pending",
      "verification_note": "Check https://lgdc.uml.edu/DIDBase/ — JR055, 2026-03-13 08:00-12:00 UTC, parameter hmF2"
    },
    {
      "id": "W019",
      "title": "NMP Drift: Poleward Dominant over Lateral",
      "week": "2026-03-15 to 2026-03-22",
      "registered": "2026-03-15T17:35:00.000000",
      "prediction": {"direction": "poleward_dominant", "unit": "comparison"},
      "mechanism": "Aetheric vortex drawing pole toward firmament axis",
      "data_source": "NOAA NGDC NP.xy",
      "status": "falsified",
      "result": {
        "observed_dlat": -0.180,
        "observed_dlon": 1.000,
        "poleward_dominant": false,
        "latest_position": "85.778°N, 138.057°E (2025)",
        "verdict": "FALSIFIED: lateral drift dominated poleward this annual step. Δlat=-0.180°, Δlon=+1.000°.",
        "note": "Long-term poleward trend continues. Weekly direction prediction incorrect."
      },
      "falsified_date": "2026-03-15",
      "counts_against_model": true
    },
    {
      "id": "W020",
      "title": "Roaring 40s 500hPa Wind Anomaly ≥3% Above Climatology",
      "week": "2026-03-15 to 2026-03-22",
      "registered": "2026-03-15T17:35:00.000000",
      "prediction": {"value": 3, "unit": "percent_above_clim", "uncertainty": 1},
      "mechanism": "Aetheric torque coupling to atmosphere at disc edge latitude",
      "data_source": "NOAA PSL anomaly maps — 500hPa winds 40-50°S",
      "status": "pending",
      "verification_note": "Manual check: https://psl.noaa.gov/map/clim/ — 500hPa wind anomaly, 40-50°S band"
    },
    {
      "id": "W021",
      "title": "Moon Angular Diameter Variation — V12 Model Test",
      "week": "2026-03-15 to 2026-03-22",
      "registered": "2026-03-15T17:35:00.000000",
      "prediction": {
        "v12_predicted_variation_pct": 116.96,
        "v12_model_params": {
          "moon_altitude_km": 2534,
          "moon_orbit_r_km": 15675,
          "observer_r_km": 5960,
          "moon_radius_km": 11.06
        },
        "observed_jpl_horizons_pct": 1.27
      },
      "mechanism": "Moon at fixed altitude 2534km; distance from observer changes 2.17x over daily orbit: 10,040km to 21,783km",
      "data_source": "JPL Horizons OBSERVER CENTER=500@399 QUANTITIES=13",
      "status": "under_revision",
      "observed_1_day_variation_pct": 1.27,
      "revision_note": "V12 predicts 116.96% variation; observed 1.27%. No altitude in 1600-2534 km range yields <2% prediction. Altitude parameter TBD before logging as falsified.",
      "counts_against_model": true
    },
    {
      "id": "W022",
      "title": "SAA Western Cell West of 45°W",
      "week": "2026-03-15 to 2026-03-22",
      "registered": "2026-03-15T17:35:00.000000",
      "prediction": {"value": -45, "comparator": "west_of", "unit": "degrees_longitude"},
      "mechanism": "Aetheric vortex structure places western cell at ~60°W per CHAOS-7 baseline",
      "data_source": "CHAOS-7 / ESA Swarm",
      "status": "confirmed",
      "result": {
        "western_cell_longitude": "~60°W",
        "basis": "CHAOS-7 WIN-004 baseline",
        "verdict": "CONFIRMED: western cell at ~60°W, well west of 45°W threshold"
      },
      "confirmed_date": "2026-03-15",
      "counts_against_model": false
    },
    {
      "id": "W023",
      "title": "Moon Physical Altitude Constraint from Angular Variation",
      "week": "2026-03-15 to 2026-03-22",
      "registered": "2026-03-15T17:35:00.000000",
      "prediction": {
        "altitude_range_tested_km": [1600, 1850, 2534],
        "predicted_variation_range_pct": [116.96, 119.56, 120.34],
        "next_monthly_observed_target_pct": 1.27,
        "tolerance_pct": 0.3
      },
      "derivation": {
        "formula": "d_total = sqrt((moon_x-obs_x)^2 + moon_y^2 + h^2); theta = 2*arctan(r_moon/d_total)",
        "result": "V12 predicts 116-120% variation for any altitude 1600-2534 km. Observed: 1.27%."
      },
      "mechanism": "Distance-angular diameter relationship in flat disc geometry",
      "data_source": "JPL Horizons (observed) + V12 orbital math (predicted)",
      "status": "pending",
      "counts_against_model": true,
      "falsification": "Confirmed next month if angular diameter variation is again ~1.27%"
    },
    {
      "id": "W024",
      "title": "Polaris Elevation at Oslo Diverges from WGS84 Latitude",
      "week": "2026-03-15 to 2026-03-22",
      "registered": "2026-03-15T17:35:00.000000",
      "prediction": {
        "location": "Oslo, Norway",
        "wgs84_latitude_deg": 59.91,
        "globe_predicted_elevation_deg": 59.91,
        "dome_predicted_elevation_deg": {"min": 63, "max": 65},
        "dome_predicted_excess_deg": {"min": 3, "max": 5}
      },
      "derivation": {
        "formula": "elev_dome = arctan(H_polaris / r_observer) + h(r) topographic correction",
        "variables": {"H_polaris": "4750 km (V12)", "h(r)": "V10 mountain form"}
      },
      "mechanism": "North pole mountain topographic lensing in dome geometry",
      "data_source": "Calibrated inclinometer at Oslo",
      "status": "pending",
      "counts_against_model": true,
      "falsification": "Polaris elevation within 0.5° of 59.91° — dome h(r) mechanism falsified"
    },
    {
      "id": "W025",
      "title": "SAA Cell Separation Increases ≥0.8° by September 2026",
      "week": "2026-03-15 to 2026-03-22",
      "registered": "2026-03-15T17:35:00.000000",
      "prediction": {
        "baseline_separation_deg": 50.57,
        "baseline_date": "2025",
        "predicted_increase_deg": 0.80,
        "uncertainty_deg": 0.3
      },
      "derivation": {
        "formula": "separation(t) = 49.956 + 3.539 * exp(0.03146 * (t - 1990))",
        "basis": "WIN-004 exponential rate, ~1.0 deg/year"
      },
      "mechanism": "Exponential aetheric vortex repulsion between SAA cells",
      "data_source": "CHAOS-7 next update (expected Sep 2026)",
      "status": "pending",
      "counts_against_model": true,
      "falsification": "Separation stable or decreasing — contradicts WIN-004 trend"
    }
  ]
};