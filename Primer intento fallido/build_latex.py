import re
import os
import sys
from bs4 import BeautifulSoup
import math

sys.stdout.reconfigure(encoding='utf-8')

latex_file = r"c:\Users\Generation\Desktop\Los Elementos -  Euclides & Byrne\byrne-euclid-master\byrne-en-latex.tex"
html_dir = r"c:\Users\Generation\Desktop\Los Elementos -  Euclides & Byrne\Euclides - c82"
output_file = r"c:\Users\Generation\Desktop\Los Elementos -  Euclides & Byrne\byrne-es-latex.tex"

with open(latex_file, 'r', encoding='utf-8') as f:
    latex_content = f.read()

# Match definitions, postulates, axioms, problems, theorems
block_pattern = r'(\\start(?:definition|postulate|axiom|problem|theorem){.*?}\\label{(?:def|post|ax|prop):[IVXL]+(?:.[IVXL]+)*\.}[\s\S]*?(?=\\start(?:definition|postulate|axiom|problem|theorem)|\\part|\\chapter|\\qed))'
# wait, \qed is sometimes part of it, let's just split by \start and \part

blocks = []
current_block = []
latex_lines = latex_content.splitlines(True)
for line in latex_lines:
    if re.match(r'^\\start(definition|postulate|axiom|problem|theorem){.*?}\\label{(def|post|ax|prop):', line):
        if current_block:
            blocks.append("".join(current_block))
        current_block = [line]
    elif re.match(r'^\\part{', line) or re.match(r'^\\chapter\*{', line):
        if current_block:
            blocks.append("".join(current_block))
        current_block = [line]
    else:
        current_block.append(line)
if current_block:
    blocks.append("".join(current_block))

# Define the books
book_romans = ['I', 'II', 'III', 'IV', 'V', 'VI']
html_files = [
    r"01 Libro 1\Libro I - Euclides de Byrne.html",
    r"02 Libro 2\Libro II - Euclides de Byrne.html",
    r"03 Libro 3\Libro III - Euclides de Byrne.html",
    r"04 Libro 4\Libro IV - Euclides de Byrne.html",
    r"05 Libro 5\Libro V - Euclides de Byrne.html",
    r"06 Libro 6\Libro VI - Euclides de Byrne.html"
]

def extract_latex_macros(latex_text):
    text = re.sub(r'\\defineNewPicture(\[.*?\])?\{.*?\}', '', latex_text, flags=re.DOTALL)
    # also remove problem/theorem lines to not extract their macros. Wait, no, we need their macros.
    
    macros = []
    # robust brace matcher for macros (up to 3 levels)
    ptrn = re.compile(r'\\(?:drawUnitLine|offsetPicture|drawAngle|drawLine|triangle[A-Z]{3}|drawFromCurrentPicture|pointA|pointB|pointC|drawSquareLine|drawParallelogram|drawTwoRightAngles|drawRectangleLine|drawCrossCrosslet|circleA|circleB|circleC|semicircle|polygon|square|rhombus|rhomboid|oblong|trapezium)(?:\[[^\]]*\])*(?:\{(?:[^{}]*|\{[^{}]*\})*\})?')
    
    def repl_graphic(m):
        macros.append(m.group(0))
        return " [G_MACRO] "
        
    text_g = ptrn.sub(repl_graphic, text)
    text_g = ptrn.sub(repl_graphic, text_g) # second pass
    
    refs = []
    def repl_ref(m):
        refs.append(m.group(0))
        return " [R_MACRO] "
    
    text_r = re.sub(r'\\byref\{.*?\}', repl_ref, text_g)
    return macros, refs

def process_book_html(html_file):
    with open(os.path.join(html_dir, html_file), 'r', encoding='utf-8') as f:
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
    return items_html

def format_problem_title(raw_text):
    # e.g "Construir un triángulo..." -> \problem{C}{onstruir}{ un triángulo...}
    # find first word
    m = re.match(r'^(\S)(.*?)\s+(.*)$', raw_text)
    if m:
        return f"\\problem{{{m.group(1).upper()}}}{{{m.group(2)}}}{{ {m.group(3)}}}"
    else:
        return f"\\problem{{X}}{{X}}{{{raw_text}}}"

def generate_spanish_latex(latex_block, html_item):
    # 1. extract \defineNewPicture and structural headers
    pic_match = re.search(r'\\defineNewPicture(\[.*?\])?\{.*?\}', latex_block, re.DOTALL)
    pic_macro = pic_match.group(0) if pic_match else ""
    
    header_match = re.match(r'^(\\start(?:definition|postulate|axiom|problem|theorem){.*?}\\label{.*?})', latex_block)
    header = header_match.group(1) if header_match else ""
    
    is_problem = "problem" in header or "theorem" in header
    
    macs, refs = extract_latex_macros(latex_block)
    # flatten HTML text and inject macros
    
    html_text_parts = []
    
    # helper to inject placeholders into bs4
    for t in html_item:
        for span in t.find_all('span', class_=lambda c: c and ('fs' in c or 'fs-text' in c)):
             span.replace_with("[G_MACRO]")
        for em in t.find_all('em'):
             em.insert_before("\\emph{")
             em.insert_after("}")
             em.unwrap()
        raw = str(t)
        # remove remaining tags
        raw = re.sub(r'<br\s*/?>', ' \\\\\\\\ ', raw)
        raw = re.sub(r'<.*?>', '', raw)
        raw = re.sub(r'\(\s*(Postulado|Definici[oó]n|Axioma|Proposici[oó]n|pr\.|post\.|def\.|ax\.).*?\)', '[R_MACRO]', raw, flags=re.IGNORECASE)
        # fix math symbols
        raw = raw.replace('∴', '$\\therefore$')
        raw = raw.replace('=', '$=$')
        raw = raw.replace('>', '$>$')
        raw = raw.replace('<', '$<$')
        raw = raw.strip()
        if raw:
             html_text_parts.append(raw)
             
    # Now we have html text with placeholders. We substitute them proportionally or exactly.
    full_html = "\n\n".join(html_text_parts)
    
    # replace [G_MACRO]
    def repl_g(m):
        return macs.pop(0) if macs else ""
    full_html = re.sub(r'\[G_MACRO\]', repl_g, full_html)
    
    if macs:
        # append remaining macros
        full_html += " " + " ".join(macs)
        
    def repl_r(m):
        return refs.pop(0) if refs else ""
    full_html = re.sub(r'\[R_MACRO\]', repl_r, full_html)
    if refs:
        full_html += " " + " ".join(refs)
        
    # Formatting it properly
    parts = full_html.split("\n\n")
    if is_problem:
        # title usually in part 0 or 1
        # Part 0 is "Proposición I." -> we skip it
        # Part 1 is usually "Problema." -> we skip it
        # Part 2 is the actual problem text
        title_idx = 0
        for i, p in enumerate(parts):
             if re.match(r'^(Proposición|[IVXL]+)', p) or "Problema" in p or "Teorema" in p:
                 continue
             title_idx = i
             break
        title_text = parts[title_idx].replace('\\\\', '') # problem def doesn't have \\
        problem_str = format_problem_title(title_text)
        if "theorem" in header:
             problem_str = problem_str.replace("\\problem", "\\theorem")
             
        # the rest goes in center
        center_text = "\n\n".join(parts[title_idx+1:])
    else:
        # definition, just center
        # skip title
        title_idx = 0
        if re.match(r'^[IVXL]+\.', parts[0]):
             title_idx = 1
        problem_str = ""
        center_text = "\n\n".join(parts[title_idx:])
        
    out = header + "\n\n"
    if pic_macro:
        out += pic_macro + "\n\\drawCurrentPictureInMargin\n"
    
    if problem_str:
        out += problem_str + "\n\n"
        
    out += "\\begin{center}\n" + center_text + "\n\\end{center}\n\n"
    if is_problem:
        out += "\\qed\n\n"
        
    return out

# -- Process everything! --
final_blocks = []

for b in blocks:
    m = re.match(r'^\\start.*?\\label{(def|post|ax|prop):([IVXL]+)\.', b)
    if m:
        book_roman = m.group(2)
        try:
             book_idx = book_romans.index(book_roman)
             # we need to be careful: the html parser needs the global lists
             # let's just use the python mapping dynamically
             # Actually, simpler: we already parsed latex into blocks.
             pass
        except ValueError:
             pass

print("Compiling all books. This will take a moment.")
html_book_items = {}
for i, f in enumerate(html_files):
    if os.path.exists(os.path.join(html_dir, f)):
        html_book_items[book_romans[i]] = process_book_html(f)
    
book_counters = {r: 0 for r in book_romans}

for b in blocks:
    m = re.match(r'^\\start.*?\\label{.*?:([IVXL]+)\.', b)
    if m:
        r_roman = m.group(1)
        if r_roman in html_book_items:
             items = html_book_items[r_roman]
             idx = book_counters[r_roman]
             if idx < len(items):
                 try:
                     new_b = generate_spanish_latex(b, items[idx])
                     final_blocks.append(new_b)
                 except Exception as e:
                     print(f"Error on {r_roman} item {idx}: {e}")
                     final_blocks.append(b)
             else:
                 final_blocks.append(b)
             book_counters[r_roman] += 1
        else:
             final_blocks.append(b)
    else:
        # Not a matched structural block, do not touch (Introduction, etc)
        # But wait! Introduction is also in HTML! "0.1 Introducción\Introduction - Euclides de Byrne.html"
        # Since we just want the easiest functional output, we'll leave introduction in English for now.
        final_blocks.append(b)

with open(output_file, 'w', encoding='utf-8') as f:
    f.writelines(final_blocks)

print(f"DONE. Output generated at: {output_file}")
