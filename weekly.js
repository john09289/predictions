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
      "description": "African cell minimum < 21,795 nT by 2026-03-13",
      "week": "2026-03-06 to 2026-03-13",
      "registered": "2026-03-07T11:35:00.000000",
      "prediction": {
        "value": 21795,
        "unit": "nT",
        "uncertainty": 30
      },
      "mechanism": "Aetheric rim degradation accelerating African lobe",
      "data_source": "CHAOS-7",
      "status": "pending",
      "sha256": "48ebb89f8ed7a1deb4d36c86fdd7fe2b157c341817c8835c542bc6d23333e8c4",
      "point_prediction": {
        "value": 21795,
        "uncertainty": 30,
        "range": [
          21765,
          21825
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
      "description": "Current deviation from 120 E longitude > -18 (i.e. still accelerating)",
      "week": "2026-03-06 to 2026-03-13",
      "registered": "2026-03-07T11:35:00.000000",
      "prediction": {
        "value": -18.0,
        "unit": "degrees",
        "uncertainty": 0.5
      },
      "mechanism": "Precession vortex convergence",
      "data_source": "NOAA NP.xy",
      "status": "pending",
      "sha256": "efd5a9eb4fffdb96507c5dddbf87d0d60e3460db7b2b1509368efd9d9c4dd68f",
      "point_prediction": {
        "value": -18.0,
        "uncertainty": 0.5,
        "range": [
          -18.5,
          -17.5
        ],
        "confidence": "1-sigma"
      }
    },
    {
      "id": "W011",
      "title": "Field Decay Rate Confirmation",
      "description": "IGRF/CHAOS-7 global dipole moment decreased >=28 nT since March 2025",
      "week": "2026-03-06 to 2026-03-13",
      "registered": "2026-03-07T11:35:00.000000",
      "prediction": {
        "value": -28.0,
        "unit": "nT/year",
        "uncertainty": 3.0
      },
      "mechanism": "Aetheric medium degradation",
      "data_source": "INTERMAGNET annual",
      "status": "pending",
      "sha256": "299cd65ec436a027997cdb4a6e761a51a3b5bf9479bf88ec4fc792b8cbc26b3b",
      "point_prediction": {
        "value": -28.0,
        "uncertainty": 3.0,
        "range": [
          -31.0,
          -25.0
        ],
        "confidence": "1-sigma"
      }
    },
    {
      "id": "W012",
      "title": "SAA Separation 2026 Check",
      "description": "SAA cell longitude separation = 51.5 degrees as of March 2026",
      "week": "2026-03-06 to 2026-03-13",
      "registered": "2026-03-07T11:35:00.000000",
      "prediction": {
        "value": 51.5,
        "unit": "degrees",
        "uncertainty": 1.5
      },
      "mechanism": "Exponential aetheric field separation",
      "data_source": "CHAOS-7",
      "status": "pending",
      "sha256": "b50343fe0c88ce600926e9694bcae155a95e6e5815af6da6325bc3c590bfc511",
      "point_prediction": {
        "value": 51.5,
        "uncertainty": 1.5,
        "range": [
          50.0,
          53.0
        ],
        "confidence": "1-sigma"
      }
    },
    {
      "id": "W013",
      "title": "Schumann 7.83 Hz Anomaly Persistence",
      "description": "Measured Schumann fundamental remains 7.83 Hz this week",
      "week": "2026-03-06 to 2026-03-13",
      "registered": "2026-03-07T11:35:00.000000",
      "prediction": {
        "value": 7.83,
        "unit": "Hz",
        "uncertainty": 0.3
      },
      "mechanism": "Aetheric damping of resonant cavity",
      "data_source": "Tomsk/HeartMath Schumann monitors",
      "status": "pending",
      "sha256": "ae70df0babca8289657768af9274cf4f455851e0efad7997f7f15d71ccc8a1fc",
      "point_prediction": {
        "value": 7.83,
        "uncertainty": 0.3,
        "range": [
          7.53,
          8.13
        ],
        "confidence": "1-sigma"
      }
    },
    {
      "id": "W014",
      "title": "Crepuscular Ray Divergence Angle",
      "description": "Crepuscular rays photographed this week show divergence angles >0.5 degrees",
      "week": "2026-03-06 to 2026-03-13",
      "registered": "2026-03-07T11:35:00.000000",
      "prediction": {
        "value": 0.5,
        "unit": "degrees",
        "uncertainty": 0.1
      },
      "mechanism": "Local compact sun geometry",
      "data_source": "Any clear sky photography",
      "status": "pending",
      "sha256": "f0688bb58008728cdf4d253c228ea60fa832c005d6c120086353f9ac9ac810c1",
      "point_prediction": {
        "value": 0.5,
        "uncertainty": 0.1,
        "range": [
          0.4,
          0.6
        ],
        "confidence": "1-sigma"
      }
    },
    {
      "id": "W015",
      "title": "Lunar Phase Magnetic Correlation",
      "description": "INTERMAGNET stations show Z component 0.5-2.0 nT shift correlated with full moon March 11 2026",
      "week": "2026-03-06 to 2026-03-13",
      "registered": "2026-03-07T11:35:00.000000",
      "prediction": {
        "value": 1.25,
        "unit": "nT",
        "uncertainty": 0.75
      },
      "mechanism": "Lunar aetheric pressure modulation",
      "data_source": "INTERMAGNET",
      "status": "pending",
      "sha256": "5ae53feed6017c4f4c3316052970eec4ef7973cabbd72417a919d7218acc4363",
      "point_prediction": {
        "value": 1.25,
        "uncertainty": 0.75,
        "range": [
          0.5,
          2.0
        ],
        "confidence": "1-sigma"
      }
    },
    {
      "id": "W016",
      "title": "W004 Baseline Recalibration",
      "description": "Recalibrated quiet-day baseline = -6.5 to -7.5 nT",
      "week": "2026-03-06 to 2026-03-13",
      "registered": "2026-03-07T11:35:00.000000",
      "prediction": {
        "value": -7.0,
        "unit": "nT",
        "uncertainty": 0.5
      },
      "mechanism": "Formula self-correction from empirical overshoot",
      "data_source": "W004 observed data",
      "status": "pending",
      "sha256": "fe44b89e6310d8d827ca68d48a4bf9d49a2b90a7d4c532657c53b84986e648d2",
      "point_prediction": {
        "value": -7.0,
        "uncertainty": 0.5,
        "range": [
          -7.5,
          -6.5
        ],
        "confidence": "1-sigma"
      }
    }
  ]
};