import os
import json

base_dir = '/Users/nicholashughes/.gemini/antigravity/scratch/astro_observations/predictions'

# Read master.json
api_file = os.path.join(base_dir, 'api/master.json')
with open(api_file, 'r') as f:
    data = json.load(f)

print("--- AI JSON ENDPOINT ---")
if 'optical_illusion' in data['index']['key_facts']:
    print(data['index']['key_facts']['optical_illusion'])

print("\n--- AI CONTEXT.HTML RULES ---")
context_file = os.path.join(base_dir, 'docs/context.html')
with open(context_file, 'r') as f:
    for line in f:
        if "11. The 5,733 km Sun altitude" in line:
            print(line.strip())

