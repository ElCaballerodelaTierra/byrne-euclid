
import os
import re

file_path = r'c:\Users\cavn\Documents\Repositorios\byrne-euclid\Los Elementos -  Euclides & Byrne\byrne-es-latex.tex'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Prop XLIV Fixed Content
prop_44_fixed = r"""\problem{A}{}{ una línea recta dada (\drawUnitLine{EG}) para aplicar un paralelogramo igual a un triángulo dado (\drawPolygon[middle][polygonJKL]{JKL}), y teniendo un ángulo igual a un ángulo rectilíneo dado (\drawAngle{N}).}

\begin{center}
Haz $\drawPolygon[middle][polygonAHEF]{AHEF} = \polygonJKL$ con $\drawAngle{F} = \drawAngle{N}$ \byref{prop:I.XLII}\\
y teniendo uno de sus lados \drawUnitLine{FE} limítrofe y en continuación de \drawUnitLine{EG}.

Prolonga \drawUnitLine{AH} hasta que se encuentre con $\drawUnitLine{BG} \parallel \drawUnitLine{HE}$;\\
dibuja \drawUnitLine{BE} prolóngala hasta que se encuentre con \drawUnitLine{AF} continuada;\\
dibuja $\drawUnitLine{CD} \parallel \drawUnitLine{FE,EG}$ encontrándose con \drawUnitLine{BG} prolongada y prolonga \drawUnitLine{HE}.

$\polygonAHEF = \drawPolygon[middle][polygonEGDI]{EGDI}$ \byref{prop:I.XLIII}\\
pero $\polygonAHEF = \polygonJKL$ \byref{\constref}

$\therefore \polygonEGDI = \polygonJKL$;

y $\drawAngle{F} = \drawAngle{E} = \drawAngle{I} = \drawAngle{N}$ \byref{prop:I.XXIX,\constref}.

Q. E. D.
\end{center}"""

# Prop XLV Fixed Content
prop_45_fixed = r"""\problem{P}{ara}{ construir un paralelogramo igual a una figura rectilínea dada (\drawPolygon[middle][polygonABCDE]{ABC,ACD,ADE}) y que tenga un ángulo igual a un ángulo rectilíneo dado (\drawAngle{O}).}

\begin{center}
Dibuja \drawUnitLine{AC} y \drawUnitLine{AD}, dividiendo la figura rectilínea en triángulos.

Construye el paralelogramo $\drawPolygon[bottom][polygonFGIH]{FGIH} = \polygonABC$ \byref{prop:I.XLII}\\
teniendo $\drawAngle{I} = \drawAngle{O}$;\\
para $\polygonACD$ aplica el paralelogramo $\drawPolygon[bottom][polygonGJKI]{GJKI} = \polygonACD$ \byref{prop:I.XLIV}\\
teniendo $\drawAngle{K} = \drawAngle{O}$;\\
y para $\polygonADE$ aplica el paralelogramo $\drawPolygon[bottom][polygonJLMK]{JLMK} = \polygonADE$ \byref{prop:I.XLIV}\\
teniendo $\drawAngle{M} = \drawAngle{O}$.

Entonces $\drawPolygon[bottom][polygonFHLM]{FGIH,GJKI,JLMK}$ es un paralelogramo \byref{prop:I.XXIX,prop:I.XIV,prop:I.XXX}\\
teniendo $\drawAngle{M} = \drawAngle{O}$ y es igual a la figura rectilínea dada.

Q. E. D.
\end{center}"""

# Replacement for Prop 44
pattern_44 = re.escape(r"\problem{A}{}{ una línea recta dada (\drawUnitLine{EG})") + r".*?" + re.escape(r"\end{center}")
content = re.sub(pattern_44, lambda m: prop_44_fixed, content, flags=re.DOTALL)

# Replacement for Prop 45
pattern_45 = re.escape(r"\problem{P}{ara}{ construir un paralelogramo igual a una figura rectilínea dada (\drawAngle{O})") + r".*?" + re.escape(r"\end{center}")
content = re.sub(pattern_45, lambda m: prop_45_fixed, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Proactive fixes applied for Props 44 and 45.")
