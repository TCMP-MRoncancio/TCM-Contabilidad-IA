# Especificación de las herramientas

Contrato de línea de comandos de cada herramienta. Los nombres son sugeridos; lo que importa es el comportamiento.

## `leer.py` (lector y validador del entregable)

```
python herramientas/leer.py resumen <archivo>              # estructura legible: secciones, elementos, conteos
python herramientas/leer.py json <archivo>                 # estructura completa en JSON
python herramientas/leer.py validar <archivo> [--formato F] # reglas V01..Vnn; código 1 si hay errores
python herramientas/leer.py comparar <generado> <extraido>  # diferencias elemento por elemento; código 1 si hay
python herramientas/leer.py cobertura <carpeta-corpus> --salida <vault>/<dominio>   # cobertura.md y fragmentos/
python herramientas/leer.py catalogo <carpeta-corpus> --md <vault>/<dominio>/catalogo.md
```

- `validar`: cada regla con id, severidad y remedio. Lista de reglas en el README de herramientas.
- `comparar`: normaliza finales de línea al leer; ignora solo los elementos declarados como "recalculados por el sistema".
  Reporta: elemento, valor generado, valor extraído.
- `cobertura`: no edita fragmentos que no generó (los agregados desde tickets llevan otro nombre).

## `ficha.py` (desde-extracción, validador de ficha y generador)

```
python herramientas/ficha.py validar <ficha.yaml>
python herramientas/ficha.py generar <ficha.yaml> [--salida DIR] [--forzar] [--correccion-dev]
python herramientas/ficha.py desde-extraccion <archivo> --ficha <ficha.yaml>
```

- `validar`: campos obligatorios, límites del sistema, referencias internas, variantes con fragmento, modo, estado. Código 1 si hay errores.
- `generar`:
  - Con `estado: borrador` escribe solo `diseno/diseno.md` (para la aprobación) o, con `--salida`, una vista previa completa en una
    carpeta fuera del vault. `salida/` y `entrega/` solo con `estado: aprobada` (la pone el orquestador tras la aprobación escrita).
  - Escribe `salida/<objeto>.<ext>`, piezas auxiliares, `trazabilidad.md`, `diseno.md` (en `diseno/`) y `entrega/promocion.md`.
  - `modo: nuevo` → guarda al inicio; `modo: existente` → sin guarda.
  - `--correccion-dev` → solo `entrega/<objeto>-CORRECCION-DEV.<ext>`, modo existente, sin guarda, aviso "NO PROMOVER" en la primera línea.
  - `--forzar` → genera aunque `validar` dé errores (solo para la prueba de regresión).
  - No reescribe archivos cuya única diferencia es la fecha del encabezado; lo informa como "sin cambios".
- `desde-extraccion`: todo elemento a un campo o a `extras`; pone `modo: existente` y `estado: borrador`.

## `lint.py` (si el entregable incluye código)

```
python herramientas/lint.py <archivo o carpeta>
```

Reglas numeradas del estándar interno (R01..Rnn), cada una con severidad. Código 1 si hay errores.

## `ticket.py`

Ver la skill `arnes-fases-y-tickets`.

## Garantías que se documentan en `herramientas/README.md`

- Resultado de la prueba de regresión: "reproduce exactamente N de N ejemplos (método, fecha)".
- Qué normaliza el comparador y por qué.
- Qué valida cada regla.
- Que ninguna herramienta se conecta a un ambiente.
- Que todas escriben con final de línea explícito.
