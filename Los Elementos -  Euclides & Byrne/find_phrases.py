import re
import os

latex_file = r"c:\Users\Generation\Desktop\Los Elementos -  Euclides & Byrne\byrne-euclid-master\byrne-en-latex.tex"

with open(latex_file, 'r', encoding='utf-8') as f:
    text = f.read()

# remove pictures
text = re.sub(r'\\defineNewPicture(\[.*?\])?\{.*?\}', '', text, flags=re.DOTALL)

# split by macros
# macros are anything starting with \ and having {}
parts = re.split(r'(\\[a-zA-Z]+(?:\[[^\]]*\])*\{[^{}]*\}|\\[a-zA-Z]+|\$)', text)

phrases = {}
for p in parts:
    if p and not p.startswith('\\') and not p == '$':
        # clean
        clean = p.strip()
        # ignore pure punctuation
        if re.search(r'[a-zA-Z]', clean):
            phrases[clean] = phrases.get(clean, 0) + 1

# output top 100 most frequent phrases
import json
sorted_phrases = sorted(phrases.items(), key=lambda kv: kv[1], reverse=True)
print("Total unique English text chunks:", len(sorted_phrases))
for k, v in sorted_phrases[:50]:
    print(f"{v}: {repr(k)}")

