import re

files = [
    '/Users/nicholashughes/.gemini/antigravity/scratch/astro_observations/predictions/docs/context.html',
    '/Users/nicholashughes/.gemini/antigravity/scratch/astro_observations/predictions/docs/model.html',
    '/Users/nicholashughes/.gemini/antigravity/scratch/astro_observations/predictions/docs/coordinates.html',
    '/Users/nicholashughes/.gemini/antigravity/scratch/astro_observations/predictions/docs/index.html'
]

for fpath in files:
    with open(fpath, 'r') as f:
        content = f.read()

    # 1. Fix the H0 value to 9572 so it matches Schumann again
    content = content.replace('8537 × sqrt(1 - (r/20015)²)', '9572 × sqrt(1 - (r/20015)²)')
    content = content.replace('8537 * sqrt(1 - (r/20015)^2)', '9572 * sqrt(1 - (r/20015)^2)')
    content = content.replace('8537 &times; &radic;(1 &minus; (r/20015)&sup2;)', '9572 &times; &radic;(1 &minus; (r/20015)&sup2;)')
    content = content.replace('8537×sqrt(1-(r/20015)²)', '9572×sqrt(1-(r/20015)²)')

    # 2. Fix contextual errors
    content = content.replace('They all sample the same exponential curve.', 'They all sample the same elliptical dome curve.')
    
    # 3. Specifically fix model.html constants table
    content = content.replace('H at pole (r=0)</td><td>8,537</td><td>km</td><td>H(0) = 8537</td><td>Consistent with', 'H at pole (r=0)</td><td>9,572</td><td>km</td><td>H(0) = 9572</td><td>Matches')
    content = content.replace('H at pole8,537 kmH(0) — consistent', 'H at pole9,572 kmH(0) — matches')
    
    with open(fpath, 'w') as f:
        f.write(content)

