# Prueba de regresión sobre el corpus

## Qué demuestra
Que las herramientas entienden y reproducen **todo** lo que el corpus contiene: ningún elemento se pierde al pasar de un
entregable real a la ficha y de la ficha al entregable.

## Procedimiento
1. Listar los ejemplos del corpus que son entregables completos (no piezas auxiliares). Guardar la lista en el script: el
   conjunto no cambia entre mediciones sin que se registre.
2. Para cada ejemplo:
   1. `desde-extraccion <ejemplo> --ficha <tmp>/ficha.yaml`
   2. `generar <tmp>/ficha.yaml --salida <tmp>/salida --forzar`
   3. `comparar <tmp>/salida/<objeto> <ejemplo>`
3. Contar: sin diferencias / total. Listar los que difieren con la primera diferencia de cada uno.
4. Escribir el resultado en la decisión que registra el cambio de herramientas: "N de N, método: <script>, fecha".

Todo en una carpeta temporal fuera del vault y de `contexto/`.

## Script de referencia (Python, biblioteca estándar)

```python
#!/usr/bin/env python3
"""Prueba de regresión: desde-extracción → generar --forzar → comparar, sobre todo el corpus."""
import subprocess, sys, tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CORPUS = RAIZ / "contexto" / "ejemplos"
PATRON = "*.<ext>"        # AJUSTAR: extensión del entregable (piloto: "*.sql")
EXCLUIR = ()              # AJUSTAR: prefijos de piezas auxiliares que no son el entregable (piloto: ("PRC_", "TBL_"))

def correr(*args):
    return subprocess.run([sys.executable, *args], cwd=RAIZ, capture_output=True, text=True)

ejemplos = sorted(p for p in CORPUS.rglob(PATRON) if not p.name.startswith(EXCLUIR))
ok, fallas = 0, []
with tempfile.TemporaryDirectory() as tmp:
    for i, ej in enumerate(ejemplos):
        d = Path(tmp) / str(i)
        d.mkdir()
        ficha = d / "ficha.yaml"
        r1 = correr("herramientas/ficha.py", "desde-extraccion", str(ej), "--ficha", str(ficha))
        r2 = correr("herramientas/ficha.py", "generar", str(ficha), "--salida", str(d / "salida"), "--forzar")
        salidas = list((d / "salida").glob(PATRON))
        r3 = correr("herramientas/leer.py", "comparar", str(salidas[0]), str(ej)) if salidas else None
        if r1.returncode == 0 and r2.returncode == 0 and r3 and r3.returncode == 0:
            ok += 1
        else:
            detalle = (r3.stdout if r3 else r2.stderr or r1.stderr).strip().splitlines()[:1]
            fallas.append((ej.relative_to(RAIZ), detalle))
print(f"Regresión: {ok} de {len(ejemplos)} sin diferencias")
for ruta, det in fallas:
    print(f"  {ruta}: {det}")
sys.exit(0 if not fallas else 1)
```

## Trampas de la medición
- **Opciones distintas entre mediciones.** Sin `--forzar`, los ejemplos que no pasan las reglas internas (más estrictas que el
  sistema) se cortan y bajan el conteo sin que el generador haya cambiado.
- **Archivo equivocado.** Si un ejemplo tiene varios archivos (el entregable y piezas auxiliares), comparar el que corresponde.
- **Duplicados.** Si un ejemplo se agrega también en `evidencias/`, decidir si cuenta una o dos veces y dejarlo escrito.
- **Reportar el número sin el método.** Un número sin el método no se puede comparar con el siguiente.
