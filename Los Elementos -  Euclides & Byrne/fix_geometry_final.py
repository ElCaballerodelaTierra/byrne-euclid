
import os
import re

file_path = r'c:\Users\cavn\Documents\Repositorios\byrne-euclid\Los Elementos -  Euclides & Byrne\byrne-es-latex.tex'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Prop XLVII Fixed Content
prop_47_fixed = r"""\problem{E}{n}{ un triángulo rectángulo (\drawPolygon[middle][polygonABC]{ABC}) el cuadrado de la hipotenusa (\drawUnitLine{BC}) es igual a la suma de los cuadrados de los lados (\drawUnitLine{AC} y \drawUnitLine{AB}).}

\begin{center}
Sobre \drawUnitLine{BC}, \drawUnitLine{AC} y \drawUnitLine{AB} describe cuadrados (\drawPolygon[middle][polygonBHKC]{BHKC}, \drawPolygon[middle][polygonACFG]{ACFG} y \drawPolygon[middle][polygonABED]{ABED}) \byref{prop:I.XLVI}.

Dibuja $\drawUnitLine{AK} \parallel \drawUnitLine{BH,CK}$ \byref{prop:I.XXXI}; dibuja \drawUnitLine{BF} y \drawUnitLine{AH}.

$\drawAngle{HBC} = \drawAngle{ABD}$ (const.)\\
a cada uno agrega $\drawAngle{ABC} \therefore \drawAngle{HBA} = \drawAngle{CBD}$ \byref{ax:I.II};\\
$\drawUnitLine{AB} = \drawUnitLine{BD}$ y $\drawUnitLine{HB} = \drawUnitLine{BC}$ (const.)\\
$\therefore \drawPolygon[middle][polygonHBA]{HBA} = \drawPolygon[middle][polygonCBD]{CBD}$ \byref{prop:I.IV};

$\drawPolygon[middle][polygonBLJK]{BLJK} = 2 \times \polygonHBA$ \byref{prop:I.XLI}\\
y $\polygonABED = 2 \times \polygonCBD$ \byref{prop:I.XLI}

$\therefore \polygonBLJK = \polygonABED$ \byref{ax:I.II}.

De la misma manera, dibujando \drawUnitLine{BG} y \drawUnitLine{CH}, se puede demostrar que\\
$\drawPolygon[middle][polygonCLJK]{CLJK} = \polygonACFG$

$\therefore \polygonBHKC = \polygonABED + \polygonACFG$ \byref{ax:I.II}.

Q. E. D.
\end{center}"""

# Prop XLVIII Fixed Content
prop_48_fixed = r"""\problem{S}{i}{ en un triángulo (\drawPolygon[middle][polygonABC]{ABC}) el cuadrado de uno de sus lados (\drawSizedLine{BC}) es igual a los cuadrados de sus otros dos lados (\drawUnitLine{AC} y \drawUnitLine{AB}), el ángulo incluido por estos dos lados es un ángulo recto.}

\begin{center}
Dibuja \drawUnitLine{AD} $\perp$ \drawUnitLine{AC} \byref{prop:I.XI}\\
y haz \drawUnitLine{AD} = \drawUnitLine{AB} \byref{prop:I.III}\\
y dibuja \drawUnitLine{CD}.

$\therefore \drawUnitLine{CD}^{2} = \drawUnitLine{AC}^{2} + \drawUnitLine{AD}^{2}$ \byref{prop:I.XLVII}\\
por lo tanto $\drawUnitLine{CD}^{2} = \drawUnitLine{AC}^{2} + \drawUnitLine{AB}^{2}$ \byref{\constref}\\
pero $\drawUnitLine{BC}^{2} = \drawUnitLine{AC}^{2} + \drawUnitLine{AB}^{2}$ \byref{\hypref}\\
$\therefore \drawUnitLine{CD}^{2} = \drawUnitLine{BC}^{2}$ y $\therefore \drawUnitLine{CD} = \drawUnitLine{BC}$.\\
$\therefore \drawAngle{A} = \drawAngle{CAB}$ \byref{prop:I.VIII}\\
pero $\drawAngle{A}$ es un ángulo recto (const.) $\therefore \drawAngle{CAB}$ es un ángulo recto.

Q. E. D.
\end{center}"""

# Replacement for Prop 47
pattern_47 = re.escape(r"\problem{E}{n}{ un triángulo rectángulo \drawLine[bottom][triangleABC]{CA,BC,AB}") + r".*?" + re.escape(r"\end{center}")
# Wait, I need to match the actual problem text which I saw in line 3694
pattern_47 = re.escape(r"\problem{E}{n}{ un triángulo rectángulo \drawLine[bottom][triangleABC]{CA,BC,AB} el cuadrado de la hipotenusa \drawUnitLine{BC} es igual a la suma de los cuadrados de los lados, (\drawUnitLine{CA} y \drawUnitLine{AB}).}") + r".*?" + re.escape(r"\end{center}")
content = re.sub(pattern_47, lambda m: prop_47_fixed, content, flags=re.DOTALL)

# Replacement for Prop 48
# I'll rely on the \problem line which I saw in my thought process (re-verify XLVIII problem line)
pattern_48 = re.escape(r"\problem{S}{i}{ en un triángulo (\drawPolygon[middle][polygonABC]{ABC}) el cuadrado de uno de sus lados (\drawSizedLine{BC}) es igual a los cuadrados de sus otros dos lados (\drawUnitLine{AC} y \drawUnitLine{AB}), el ángulo incluido por estos dos lados es un ángulo recto.}") + r".*?" + re.escape(r"\end{center}")
content = re.sub(pattern_48, lambda m: prop_48_fixed, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Final proactive fixes applied for Props 47 and 48.")
