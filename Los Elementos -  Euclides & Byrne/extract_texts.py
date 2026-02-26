import re
import os
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_section_copy = False
        self.in_p = False
        self.in_em = False
        self.in_fs = False
        self.current_paragraph = []
        self.paragraphs = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'div' and attrs_dict.get('class') == 'section-copy':
            self.in_section_copy = True
        
        if not self.in_section_copy:
            return
            
        if tag == 'p':
            self.in_p = True
            self.current_paragraph = []
        elif tag == 'em' and self.in_p:
            self.in_em = True
        elif tag == 'span' and self.in_p:
            classes = attrs_dict.get('class', '')
            if 'fs' in classes:
                self.in_fs = True
                self.current_paragraph.append('[MACRO]')
                
    def handle_endtag(self, tag):
        if not self.in_section_copy:
            return
            
        if tag == 'div':
            # rudimentary handling, assuming no nested divs in section-copy, but that's risky.
            pass
        elif tag == 'p':
            self.in_p = False
            self.paragraphs.append("".join(self.current_paragraph).strip())
        elif tag == 'em' and self.in_p:
            self.in_em = False
        elif tag == 'span' and self.in_p:
            if self.in_fs:
                # Assuming non-nested span containing SVG... wait.
                # span class="fs" contains span class="svg" contains svg.
                # The end tag for span will be called twice.
                pass
                
    def handle_data(self, data):
        if self.in_p:
            if self.in_em:
                self.current_paragraph.append(f'[EM:{data}]')
            elif not self.in_fs:
                # If we are inside an interactive figure span, we ignore its text content 
                # (which is usually things like <title> or empty spaces)
                self.current_paragraph.append(data)
                
html_file = r"c:\Users\Generation\Desktop\Los Elementos -  Euclides & Byrne\Euclides - c82\01 Libro 1\Libro I - Euclides de Byrne.html"

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

extractor = TextExtractor()
extractor.feed(content)

for i in range(15):
    if i < len(extractor.paragraphs):
        print(f"HTML P {i}:", extractor.paragraphs[i])
