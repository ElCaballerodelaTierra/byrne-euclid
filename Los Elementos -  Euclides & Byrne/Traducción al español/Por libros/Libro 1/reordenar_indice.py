"""
Reordena las páginas del PDF compilado para mover el índice
(que se genera al final) justo después de la portada y créditos.

Uso:
    python reordenar_indice.py [archivo.pdf] [--paginas-previas N] [--paginas-indice M]

El script:
1. Lee el PDF compilado
2. Detecta automáticamente las páginas del índice (las últimas M páginas)
3. Las reinserta después de las primeras N páginas (portada + créditos)
4. Guarda el resultado como un nuevo PDF

Por defecto:
- N = 2 (portada + créditos)
- M = 5 (5 páginas de índice: 1 de secciones + 4 de proposiciones)
"""

import argparse
import sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("Error: pypdf no está instalado. Ejecuta: pip install pypdf")
    sys.exit(1)


def reordenar_pdf(
    archivo_entrada: str,
    archivo_salida: str,
    paginas_previas: int = 2,
    paginas_indice: int = 5,
):
    """
    Reordena un PDF moviendo las últimas `paginas_indice` páginas
    para insertarlas después de las primeras `paginas_previas` páginas.

    Ejemplo con un PDF de 71 páginas, previas=2, indice=5:
      Original:  [1, 2, 3, 4, ..., 66, 67, 68, 69, 70, 71]
                  ^^^^^                  ^^^^^^^^^^^^^^^^^^^^
                  portada+créditos       índice (5 páginas)

      Resultado: [1, 2, 67, 68, 69, 70, 71, 3, 4, ..., 66]
                  ^^^^^  ^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^
                  portada  índice (movido)     contenido
    """
    reader = PdfReader(archivo_entrada)
    writer = PdfWriter()
    total_paginas = len(reader.pages)

    print(f"  PDF de entrada: {archivo_entrada}")
    print(f"  Total de páginas: {total_paginas}")
    print(f"  Páginas previas (portada+créditos): {paginas_previas}")
    print(f"  Páginas del índice (al final): {paginas_indice}")

    if paginas_previas + paginas_indice > total_paginas:
        print("Error: La suma de páginas previas + índice excede el total de páginas.")
        sys.exit(1)

    inicio_indice = total_paginas - paginas_indice

    # Sección 1: Portada y créditos (páginas 0..previas-1)
    # Sección 2: Índice (últimas M páginas)
    # Sección 3: Contenido (páginas previas..inicio_indice-1)

    orden = []

    # 1. Páginas previas
    for i in range(paginas_previas):
        orden.append(i)

    # 2. Páginas del índice
    for i in range(inicio_indice, total_paginas):
        orden.append(i)

    # 3. Contenido
    for i in range(paginas_previas, inicio_indice):
        orden.append(i)

    print(f"\n  Nuevo orden de páginas (PDF, base 1):")
    print(f"    Portada+créditos: {[x+1 for x in orden[:paginas_previas]]}")
    print(f"    Índice:           {[x+1 for x in orden[paginas_previas:paginas_previas+paginas_indice]]}")
    print(f"    Contenido:        [{orden[paginas_previas+paginas_indice]+1} ... {orden[-1]+1}]")

    for i in orden:
        writer.add_page(reader.pages[i])

    writer.write(archivo_salida)
    print(f"\n  ✓ PDF reordenado guardado en: {archivo_salida}")
    print(f"    Total de páginas: {len(orden)}")


def main():
    parser = argparse.ArgumentParser(
        description="Reordena las páginas del PDF para mover el índice al principio."
    )
    parser.add_argument(
        "archivo",
        nargs="?",
        default="byrne-es-traduccion-primer-libro.pdf",
        help="Archivo PDF de entrada (default: byrne-es-traduccion-primer-libro.pdf)",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Archivo PDF de salida (default: [nombre]_con_indice.pdf)",
    )
    parser.add_argument(
        "--paginas-previas",
        type=int,
        default=2,
        help="Número de páginas antes del índice: portada + créditos (default: 2)",
    )
    parser.add_argument(
        "--paginas-indice",
        type=int,
        default=5,
        help="Número de páginas del índice al final del PDF (default: 5)",
    )

    args = parser.parse_args()

    archivo_entrada = Path(args.archivo)
    if not archivo_entrada.exists():
        print(f"Error: No se encontró el archivo '{archivo_entrada}'")
        sys.exit(1)

    if args.output:
        archivo_salida = args.output
    else:
        archivo_salida = str(archivo_entrada.stem) + "_con_indice.pdf"

    print("=" * 60)
    print("  Reordenamiento del índice de Byrne-Euclid")
    print("=" * 60)

    reordenar_pdf(
        str(archivo_entrada),
        archivo_salida,
        args.paginas_previas,
        args.paginas_indice,
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
