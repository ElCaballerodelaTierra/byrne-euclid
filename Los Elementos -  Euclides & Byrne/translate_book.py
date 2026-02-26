import re
import os
import sys
from bs4 import BeautifulSoup

# Ensure correct print encoding on Windows
sys.stdout.reconfigure(encoding='utf-8')

latex_file = r"c:\Users\Generation\Desktop\Los Elementos -  Euclides & Byrne\byrne-euclid-master\byrne-en-latex.tex"
html_dir = r"c:\Users\Generation\Desktop\Los Elementos -  Euclides & Byrne\Euclides - c82"

# --- 1. Parse LaTeX Blocks ---
with open(latex_file, 'r', encoding='utf-8') as f:
    latex_content = f.read()

# Since we want to modify the file in place, we can split it by \start...
# But to be safe, let's use a regex that captures the blocks.
# We will just split the entire content by regex finding \startdefinition, \startproblem, etc.
# Actually, iterating through the lines is better to keep exact whitespace.

blocks = []
current_block = []
latex_lines = latex_content.splitlines(True)
for line in latex_lines:
    if re.match(r'\\start(definition|postulate|axiom|problem|theorem){.*?}?\\label{(def|post|ax|prop):', line):
        if current_block:
            blocks.append("".join(current_block))
        current_block = [line]
    elif re.match(r'\\part{', line) or re.match(r'\\chapter\*{', line):
        if current_block:
            blocks.append("".join(current_block))
        current_block = [line]
    else:
        current_block.append(line)

if current_block:
    blocks.append("".join(current_block))

# Find the indices of Book 1 items
book1_indices = []
for i, block in enumerate(blocks):
    if re.match(r'\\start(definition|postulate|axiom|problem|theorem){.*?}\\label{(def|post|ax|prop):I\.', block):
        book1_indices.append(i)

print(f"Found {len(book1_indices)} Book 1 items in LaTeX.")

# --- 2. Parse HTML Blocks ---
with open(os.path.join(html_dir, r"01 Libro 1\Libro I - Euclides de Byrne.html"), 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')
items_html = []
current_item = []

for tag in soup.find_all(['h2', 'h3', 'p', 'div']):
    if tag.name == 'div' and tag.get('class') != ['problem-title']:
        continue
    text = tag.get_text(separator=' ', strip=True)
    if not text:
        continue
    if tag.name in ['h2', 'h3'] and re.match(r'^(Proposición\s+[IVXL]+|Prop\.|[IVXL]+\.)', text):
        if current_item:
            items_html.append(current_item)
        current_item = [tag]
        continue
    if current_item and tag.name in ['p', 'div'] and (not tag.parent or tag.parent.name != 'figure'):
        current_item.append(tag)

if current_item:
    items_html.append(current_item)

print(f"Found {len(items_html)} Book 1 items in HTML.")

if len(book1_indices) != len(items_html):
    print("MISMATCH IN COUNT!")

# Now process the first 5 as a test
for i in range(5):
    html_tags = items_html[i]
    latex_idx = book1_indices[i]
    latex_str = blocks[latex_idx]
    
    # Let's extract the raw Spanish text nicely
    spanish_texts = []
    for t in html_tags:
        # Instead of replacing, we can just get text
        spanish_texts.append(t.get_text(separator=' ', strip=True))
        
    print(f"\n--- ITEM {i+1} ---")
    print("SPANISH:")
    for text in spanish_texts:
        print(text)
    
    print("\nENGLISH (Snippet):")
    # Clean up latex slightly to show just the center block
    m = re.search(r'\\begin{center}(.*?)\\end{center}', latex_str, re.DOTALL)
    if m:
        print(m.group(1).strip())
    else:
        print(latex_str[:200])

