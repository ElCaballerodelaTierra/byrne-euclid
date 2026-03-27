<# 
    Compilar y reordenar el índice de Byrne-Euclid
    
    Este script:
    1. Compila el documento LaTeX con lualatex (2 veces para resolver referencias)
    2. Reordena las páginas del PDF para mover el índice al principio
    
    Uso:
        .\compilar.ps1                    # Compilación completa (2 pasadas + reordenar)
        .\compilar.ps1 -SoloReordenar     # Solo reordena (si ya compilaste)
        .\compilar.ps1 -PaginasPrevias 2 -PaginasIndice 5
#>

param(
    [switch]$SoloReordenar,
    [int]$PaginasPrevias = 2,
    [int]$PaginasIndice = 5,
    [string]$Archivo = "byrne-es-traduccion-primer-libro"
)

$ErrorActionPreference = "Stop"

$python = "C:\Users\Generation\AppData\Local\Python\bin\python.exe"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Compilacion de Byrne-Euclid (Libro 1 - Espanol)" -ForegroundColor Cyan  
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

if (-not $SoloReordenar) {
    # Primera compilación
    Write-Host "[1/3] Primera compilacion con lualatex..." -ForegroundColor Yellow
    & lualatex --interaction=nonstopmode "$Archivo.tex"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  Advertencia: lualatex retorno codigo $LASTEXITCODE" -ForegroundColor DarkYellow
    }
    Write-Host "  Primera pasada completada." -ForegroundColor Green
    Write-Host ""

    # Segunda compilación (resolver referencias)
    Write-Host "[2/3] Segunda compilacion (resolver referencias)..." -ForegroundColor Yellow
    & lualatex --interaction=nonstopmode "$Archivo.tex"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  Advertencia: lualatex retorno codigo $LASTEXITCODE" -ForegroundColor DarkYellow
    }
    Write-Host "  Segunda pasada completada." -ForegroundColor Green
    Write-Host ""
}

# Reordenar páginas
Write-Host "[3/3] Reordenando paginas del indice..." -ForegroundColor Yellow
& $python reordenar_indice.py "$Archivo.pdf" -o "${Archivo}_final.pdf" --paginas-previas $PaginasPrevias --paginas-indice $PaginasIndice
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Error al reordenar el PDF." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  Compilacion completada!" -ForegroundColor Green
Write-Host "  PDF original:    $Archivo.pdf" -ForegroundColor White
Write-Host "  PDF con indice:  ${Archivo}_final.pdf" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
