import re

prompt_file = '/Users/nicholashughes/.gemini/antigravity/scratch/astro_observations/predictions/eclipse_v12_predictions.txt'
# Based on the user's paste, they have an onboarding text. Let's see if there's a file for it.
import glob
files = glob.glob('/Users/nicholashughes/.gemini/antigravity/scratch/astro_observations/predictions/*.txt')
print("Text files:", files)
