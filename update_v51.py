import os
import json

docs_dir = '/Users/nicholashughes/.gemini/antigravity/scratch/astro_observations/predictions/docs'

# 1. Update master.json to V51 with the new H(r) curve equation
api_file = os.path.join(docs_dir, '../api/master.json')
if os.path.exists(api_file):
    with open(api_file, 'r') as f:
        data = json.load(f)
    
    data['index']['current_version'] = '51.0'
    data['scorecard']['version'] = '51.0'
    if 'model_parameters' in data and 'H_curve' in data['model_parameters']:
        data['model_parameters']['H_curve'] = '8537 * sqrt(1 - (r/20015)^2)'
    
    # Optional: we can add an optical caveat
    data['index']['key_facts']['optical_illusion'] = "5,733 km Sun altitude is an electromagnetic optical illusion; physical firmament drops to 4,200 km at mid-latitudes."
        
    with open(api_file, 'w') as f:
        json.dump(data, f, indent=2)

# 2. Update all HTML files
for filename in os.listdir(docs_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(docs_dir, filename)
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Replace global V50.6 strings
        content = content.replace('V50.6', 'V51')
        content = content.replace('Version 50.6', 'Version 51')
        
        # Replace the old exponential formula with the new ellipse
        content = content.replace('8537 * exp(-r / 8619)', '8537 * sqrt(1 - (r/20015)^2)')
        content = content.replace('8537 × exp(−r/8619)', '8537 × sqrt(1 - (r/20015)²)')
        content = content.replace('8537&times;e<sup>&minus;r/8619</sup>', '8537&times;&radic;(1&minus;(r/20015)&sup2;)')
        
        # Ensure we write back
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {filename}")

