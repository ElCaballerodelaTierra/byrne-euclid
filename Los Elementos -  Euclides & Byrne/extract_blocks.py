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

def process_book(book_num, html_file):
    book_indices = []
    for i, block in enumerate(blocks):
        # find \label{def:I. or prop:IV.
        # roman numerals matching book_num
        roman = ['I', 'II', 'III', 'IV', 'V', 'VI'][book_num-1]
        pattern = r'\\start.*?\\label{.*?:' + roman + r'\.'
        if re.search(pattern, block):
            book_indices.append(i)
            
    # Parse HTML
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
        
    print(f"Book {book_num}: LaTeX found {len(book_indices)}, HTML found {len(items_html)}")
    
    # Test macro mapping for Proposition 1 (which is the 51st item in Book 1 usually: 35 defs + 3 post + 12 ax + 1 = 51)
    # Actually just iter all and find the first Prop
    prop_index = None
    for i, item in enumerate(items_html):
        txt = item[0].get_text()
        if "Proposición I" in txt:
            prop_index = i
            break
            
    if prop_index is None: return
    
    print("\n--- Testing alignment for Prop I ---")
    html_item = items_html[prop_index]
    latex_idx = book_indices[prop_index]
    latex_str = blocks[latex_idx]
    
    # 1. Extract HTML macros
    html_text = ""
    for t in html_item:
        # replace span.fs with [MACRO]
        for span in t.find_all('span', class_=lambda c: c and 'fs' in c):
            span.replace_with("[MACRO]")
        for cite in t.find_all(text=re.compile(r'\(\s*(Postulado|Definición|Axioma|Proposición).*?\)')):
             # Wait, finding text node and replacing is tricky in bs4, let's just do it on string
             pass
        html_text += str(t) + "\n"
        
    # strip tags from html_text to see the result
    raw_html = BeautifulSoup(html_text, 'html.parser').get_text(separator=' ', strip=True)
    raw_html = re.sub(r'\(\s*(Postulado|Definición|Axioma|Proposición).*?\)', '[REF]', raw_html)
    print("SPANISH PATTERN:")
    print(raw_html[:500])
    
    # 2. Extract LaTeX macros
    # Remove \defineNewPicture
    latex_no_pic = re.sub(r'\\defineNewPicture(\[.*?\])?\{.*?\}', '', latex_str, flags=re.DOTALL)
    # Replace line, circle, etc macros
    latex_pattern = re.sub(r'\\(drawUnitLine|offsetPicture|drawAngle|drawLine|triangle[A-Z]{3}|drawFromCurrentPicture|pointA|drawSquareLine|drawParallelogram|drawTwoRightAngles|drawRectangleLine|drawCrossCrosslet)\[.*?\]{.*?}', '[MACRO]', latex_no_pic)
    latex_pattern = re.sub(r'\\(drawUnitLine|offsetPicture|drawAngle|drawLine|triangle[A-Z]{3}|drawFromCurrentPicture|pointA|drawSquareLine|drawParallelogram|drawTwoRightAngles|drawRectangleLine|drawCrossCrosslet){.*?}', '[MACRO]', latex_pattern)
    latex_pattern = re.sub(r'\\(drawUnitLine|offsetPicture|drawAngle|drawLine|triangle[A-Z]{3}|drawFromCurrentPicture|pointA|drawSquareLine|drawParallelogram|drawTwoRightAngles|drawRectangleLine|drawCrossCrosslet)', '[MACRO]', latex_pattern)
    
    latex_pattern = re.sub(r'\\byref{.*?}', '[REF]', latex_pattern)
    
    # Just show the center text
    m = re.search(r'\\begin{center}(.*?)\\end{center}', latex_pattern, re.DOTALL)
    if m:
        center_text = m.group(1).strip()
        print("\nENGLISH PATTERN:")
        print(center_text[:500])
        
process_book(1, r"01 Libro 1\Libro I - Euclides de Byrne.html")
process_book(2, r"02 Libro 2\Libro II - Euclides de Byrne.html")
# process_book(3, r"03 Libro 3\Libro III - Euclides de Byrne.html")
