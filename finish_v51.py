import os
import json

docs_dir = '/Users/nicholashughes/.gemini/antigravity/scratch/astro_observations/predictions/docs'

# Fix context.html
ctx_file = os.path.join(docs_dir, 'context.html')
with open(ctx_file, 'r') as f:
    text = f.read()
text = text.replace('8537 × exp(−r / 8619)', '8537 × sqrt(1 - (r/20015)²)')
text = text.replace('8537×exp(−r/8619)', '8537×sqrt(1-(r/20015)²)')
with open(ctx_file, 'w') as f:
    f.write(text)

# Fix master.json
api_file = os.path.join(docs_dir, '../api/master.json')
with open(api_file, 'r') as f:
    data = json.load(f)

if 'optical_illusion' in data['index']['key_facts']:
    del data['index']['key_facts']['optical_illusion']

with open(api_file, 'w') as f:
    json.dump(data, f, indent=2)

