import re
import os
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

latex_file = r"c:\Users\Generation\Desktop\Los Elementos -  Euclides & Byrne\byrne-euclid-master\byrne-en-latex.tex"
html_dir = r"c:\Users\Generation\Desktop\Los Elementos -  Euclides & Byrne\Euclides - c82"

with open(latex_file, 'r', encoding='utf-8') as f:
    latex_content = f.read()

# Split latex blocks
blocks = []
current_block = []
latex_lines = latex_content.splitlines(True)
for line in latex_lines:
    if re.match(r'\\start(definition|postulate|axiom|problem|theorem){.*?}\\label{(def|post|ax|prop):', line):
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

def extract_latex_macros(latex_text):
    # remove purely structural \begin{center} and \end{center} etc
    # To extract graphical macros properly
    # \offsetPicture{...}{...}
    text = re.sub(r'\\defineNewPicture(\[.*?\])?\{.*?\}', '', latex_text, flags=re.DOTALL)
    
    # regex for macros
    macros = []
    # match patterns like \drawUnitLine{AB} or \offsetPicture{15pt}{0pt}{\drawFromCurrentPicture{...}}
    # We will use a regex that matches balanced braces for \macro{...} up to 3 levels deep
    ptrn = re.compile(r'\\(drawUnitLine|offsetPicture|drawAngle|drawLine|triangle[A-Z]{3}|drawFromCurrentPicture|pointA|pointB|pointC|drawSquareLine|drawParallelogram|drawTwoRightAngles|drawRectangleLine|drawCrossCrosslet|circleA|circleB|circleC|semicircle|polygon|square|rhombus|rhomboid|oblong|trapezium)(?:\[[^\]]*\])*(\{([^{}]*|\{[^{}]*\})*\})?')
    
    def repl_graphic(m):
        macros.append(m.group(0))
        return " [G_MACRO] "
        
    text_g = ptrn.sub(repl_graphic, text)
    # Sometimes it misses some because of nesting, so let's do one more pass
    text_g = ptrn.sub(repl_graphic, text_g)
    
    refs = []
    def repl_ref(m):
        refs.append(m.group(0))
        return " [R_MACRO] "
    
    text_r = re.sub(r'\\byref\{.*?\}', repl_ref, text_g)
    return len(macros), len(refs)

book_indices = []
for i, block in enumerate(blocks):
    if re.search(r'\\start.*?\\label{.*?:I\.', block):
        book_indices.append(i)

# Parse HTML
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

print(f"Book 1: LaTeX found {len(book_indices)}, HTML found {len(items_html)}")

for i in range(len(book_indices)):
    latex_idx = book_indices[i]
    latex_str = blocks[latex_idx]
    html_item = items_html[i]
    
    l_g, l_r = extract_latex_macros(latex_str)
    
    h_g = 0
    h_r = 0
    for t in html_item:
        spans = t.find_all('span', class_=lambda c: c and ('fs' in c or 'fs-text' in c))
        h_g += len(spans)
        text = str(t)
        # count references
        # Sometimes refs are inside parens like ( Postulado 1 ) or pr. 4.
        # This is harder to count strictly via regex, but let's just count (.*) roughly that look like refs.
        h_r += len(re.findall(r'\(\s*(Postulado|Definici[oó]n|Axioma|Proposici[oó]n|pr\.|post\.|def\.|ax\.).*?\)', text, re.IGNORECASE))
        
    print(f"Item {i+1}: LaTeX[G:{l_g}, R:{l_r}] | HTML[G:{h_g}, R:{h_r}]")

