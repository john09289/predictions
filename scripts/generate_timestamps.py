import hashlib
import json
from datetime import datetime

predictions = {
    'PRED-R001': {
        'desc': 'SAA separation >=57 deg by 2030',
        'formula': 'sep(t)=30.8*exp(0.0208*(year-2000))',
        'threshold': '57 degrees',
        'test_date': '2030',
        'registered': '2026-03-21'
    },
    'PRED-R002': {
        'desc': 'SAA African cell <=21750 nT by 2028',
        'formula': '21880-(3*75)=21655',
        'threshold': '21750 nT',
        'test_date': '2028',
        'registered': '2026-03-21'
    },
    'PRED-R003': {
        'desc': 'NMP reaches 141-146E by 2031',
        'formula': '139.3+(6*0.48)=142.2',
        'threshold': '141-146E longitude',
        'test_date': '2031',
        'registered': '2026-03-21'
    },
    'PRED-R004': {
        'desc': 'NMP longitudinal ratio >=2.0x through 2028',
        'formula': 'abs(lon_rate/lat_rate)>=2.0',
        'threshold': '2.0x minimum',
        'test_date': '2028',
        'registered': '2026-03-21'
    },
    'PRED-R005': {
        'desc': 'Aug 12 2026 eclipse SR shift -0.005 to -0.015 Hz',
        'formula': 'cavity_height_perturbation -> SR_shift',
        'threshold': '>0.004 Hz shift',
        'test_date': '2026-08-12',
        'registered': '2026-03-21'
    },
    'PRED-R006': {
        'desc': 'G3+ storms elevate SR +0.008 to +0.022 Hz',
        'formula': 'dome_compression -> cavity_height_decrease',
        'threshold': '>0.008 Hz per G3+ event',
        'test_date': 'ongoing',
        'registered': '2026-03-21'
    },
    'WIN-042': {
        'desc': 'Field decay confirmed: Tsumeb 77 nT/yr, 2.8x threshold',
        'basis': 'PRED-012 promoted',
        'data': 'INTERMAGNET 2024-2025',
        'registered': '2026-03-21'
    },
    'WIN-043': {
        'desc': 'NMP longitudinal dominance 2.26x confirmed',
        'data': 'NOAA NP.xy 2020-2025',
        'lat_rate': '-16.4 km/yr',
        'lon_rate': '-37.1 km/yr',
        'registered': '2026-03-21'
    },
}

print("PREDICTION HASHES — V50.7 (2026-03-21)")
print("=" * 56)

hashes = {}
for pid, data in predictions.items():
    content = json.dumps(data, sort_keys=True)
    sha = hashlib.sha256(content.encode()).hexdigest()
    hashes[pid] = sha
    print(f"{pid}: {sha[:20]}...")

with open('data/prediction_hashes.json', 'w') as f:
    json.dump({
        'generated': datetime.now().isoformat(),
        'version': 'V50.7',
        'hashes': hashes,
        'full_data': predictions
    }, f, indent=2)

print("\nSaved to data/prediction_hashes.json")
print("Git commit SHA = cryptographic timestamp proof")
print("All predictions registered 2026-03-21")
