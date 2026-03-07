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
      "mechanism": "Aetheric pressure trough from lunar mass",
      "data_source": "INTERMAGNET HUA + Skyfield ephemeris",
      "status": "falsified",
      "sha256": "26d9c17c7d4a9fea1c94e24ffabad11c60599f27d10949ae8d9db0f73a731c02",
      "result_value": "3.73 nT (SNR 0.3x - within noise flow)",
      "result_date": "2026-03-06T19:04:11.161809"
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
      "sha256": "a1d7d5cb8a54b1380158d7c4ab2c4afa4d0cbaa46b5fbf1796dce361ceeaf90e"
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
      "sha256": "e04ab3131b9123a31ba151adfc220ddfdcec7bc2834edf22e0c75a8f6ee7ae98"
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
      "mechanism": "Aetheric Pressure Trough",
      "data_source": "INTERMAGNET 1-minute (BOU, FRD, CMO, BSL, TUC, DHT, NEW, OTT, STJ)",
      "status": "falsified",
      "sha256": "98c10cf39a991a367985318eb454414b06d846abdc8009c3b3fa3c8000ab3c10",
      "result_value": "Mixed: CMO/NEW match (-17nT, SNR>4) but 7 stations failed noise/data.",
      "result_date": "2026-03-06T19:04:11.161843"
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
      "sha256": "3ce0862e0728ca2559bec72f967c6d931a4d7f81b0ab4583844c7b05c40f74b9"
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
      "sha256": "f95eed68781979a6e4ce623ab1dd76943df5aa98960ef7f8de2bb97f5b703d88"
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
      "sha256": "50d6cf976c658cc180dc7d53d5d75e3621af3a0a47b7677c8829fda10671ce3d"
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
      "sha256": "e56802697326b469ba67be82b7d65fd5220e2230804f3638aa5b82593ebe1285"
    }
  ]
};