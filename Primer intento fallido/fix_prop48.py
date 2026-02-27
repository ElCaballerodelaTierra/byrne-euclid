
import os

file_path = r'c:\Users\cavn\Documents\Repositorios\byrne-euclid\Los Elementos -  Euclides & Byrne\byrne-es-latex.tex'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Prop XLVIII proof is roughly from line 3763 to 3777
# Line 3763 is index 3762
start_idx = 3762
end_idx = 3777

new_proof = [
    '\\begin{center}\n',
    'Dibuja $\\drawUnitLine{AD} \\perp \\drawUnitLine{AB}$ e $= \\drawUnitLine{AC}$ \\byref{prop:I.XI,prop:I.III}\\\\\n',
    'y dibuja \\drawUnitLine{BD} también.\n',
    '\n',
    'Como $\\drawUnitLine{AD} = \\drawUnitLine{AC}$ \\byref{\\constref}\\\\\n',
    '$\\drawUnitLine{AD}^2 = \\drawUnitLine{AC}^2$;\n',
    '\n',
    '$\\therefore \\drawUnitLine{AD}^2 + \\drawUnitLine{AB}^2 = \\drawUnitLine{AC}^2 + \\drawUnitLine{AB}^2$\n',
    '\n',
    'pero $\\drawUnitLine{AD}^2 + \\drawUnitLine{AB}^2 = \\drawUnitLine{BD}^2$ \\byref{prop:I.XLVII},\\\\\n',
    'y $\\drawUnitLine{AC}^2 + \\drawUnitLine{AB}^2 = \\drawUnitLine{BC}^2$ \\byref{\\hypref}\n',
    '\n',
    '$\\therefore \\drawUnitLine{BD}^2 = \\drawUnitLine{BC}^2$,\n',
    '\n',
    '$\\therefore \\drawUnitLine{BD} = \\drawUnitLine{BC}$;\n',
    '\n',
    'y $\\therefore \\drawAngle{DAB} = \\drawAngle{BAC}$ \\byref{prop:I.VIII},\n',
    '\n',
    'consecuentemente \\drawAngle{BAC} es un ángulo recto.\n',
    '\n',
    'Q. E. D.\n',
    '\\end{center}\n'
]

# Double check
if '\\begin{center}' in lines[3762]:
    lines[3762:3777] = new_proof
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Success")
else:
    print(f"Mismatch! Line 3763: {repr(lines[3762])}")
