import os

docs_dir = '/Users/nicholashughes/.gemini/antigravity/scratch/astro_observations/predictions/docs'

for filename in os.listdir(docs_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(docs_dir, filename)
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Replace global V50.6 with V51
        new_content = content.replace('V50.6', 'V51')
        new_content = new_content.replace('Version 50.6', 'Version 51')
        
        # We wrote some specific custom V51 text earlier, just doing global catches
        
        if content != new_content:
            with open(filepath, 'w') as f:
                f.write(new_content)
            print(f"Updated {filename}")

# Also check api/master.json if it exists to update the version string!
import json
api_file = os.path.join(docs_dir, '../api/master.json')
if os.path.exists(api_file):
    with open(api_file, 'r') as f:
        data = json.load(f)
    if 'version' in data:
        data['version'] = 'V51'
    if 'model_parameters' in data and 'H_curve' in data['model_parameters']:
        data['model_parameters']['H_curve'] = '9572 * sqrt(1 - (r/20015)^2)'
    with open(api_file, 'w') as f:
        json.dump(data, f, indent=2)
    print("Updated master.json")
