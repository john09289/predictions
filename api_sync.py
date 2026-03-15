import os
import json

api_file = '/Users/nicholashughes/.gemini/antigravity/scratch/astro_observations/predictions/api/master.json'
with open(api_file, 'r') as f:
    content = f.read()

new_content = content.replace('"50.5"', '"51"')
new_content = new_content.replace('"V50.5"', '"V51"')

with open(api_file, 'w') as f:
    f.write(new_content)
print("Updated master.json versioning to 51")
