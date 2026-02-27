
import os

file_path = r'c:\Users\cavn\Documents\Repositorios\byrne-euclid\Los Elementos -  Euclides & Byrne\byrne-es-latex.tex'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_content = [
    'pero $\\polygonABDC = \\mbox{ dos veces } \\polygonBCD$ \\byref{prop:I.XXXIV},\\\\\n',
    'y $\\polygonEFHG = \\mbox{ dos veces } \\polygonEGH$ \\byref{prop:I.XXXIV},\n',
    '\n',
    '$\\therefore \\polygonBCD = \\polygonEGH$ \\byref{ax:I.VII}.\n',
    '\n',
    'Q. E. D.\n',
    '\\end{center}\n'
]

# Looking for the broken section between the success part and the end of the proof.
# Step 142/145 showed the success part ends at line 3157: \drawPolygon...
# The garbage starts after that.

# We will replace from where we see "\byref{prop:I.XXXI}" again down to "\end{center}"
found_start = -1
found_end = -1
for i in range(3150, len(lines)):
    if '\\byref{prop:I.XXXI}' in lines[i] and i > 3155:
        found_start = i
    if '\\end{center}' in lines[i] and i > 3160:
        found_end = i
        break

if found_start != -1 and found_end != -1:
    lines[found_start:found_end+1] = new_content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"Success: Replaced lines {found_start+1} to {found_end+1}")
else:
    print(f"Error: Could not find start ({found_start}) or end ({found_end})")
