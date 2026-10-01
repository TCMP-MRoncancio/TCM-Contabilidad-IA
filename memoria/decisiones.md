# Decisiones

- 2026-09: se descarta el nucleo generico multi-area (registro/organizacion.yaml) como base de este proyecto. Se adopta en su lugar el patron de vault-patrones / vault-proyecto-* / contexto / memoria, adaptado de un piloto de Custom Windows (CW), pero sin el concepto de tickets por ahora.
- 2026-09: las cuentas se generan siempre validadas contra schema + catalogo de proyectos + catalogo de enums; nunca se sobrescribe un .xml existente sin --forzar explicito.
- 2026-09: se adopta el plan de adecuacion al estandar de arnes TCM segun memoria/revision-arnes-2026-09-30.md; se ejecuta por bloques con aprobacion del consultor.
- 2026-09: se agregan denies de Bash (redireccion de shell) contra contexto/, ademas de Edit/Write. RIESGO ACEPTADO: no cubre toda forma posible de escritura por shell (ej. python -c, tee, cp); la defensa robusta seria restringir Bash a lista blanca estricta, pendiente de evaluar en un bloque posterior.
- 2026-09-30: se confirmo con 11 casos reales exportados por la macro que el fin de linea correcto es CRLF, no LF. Se cambio herramientas/generar_cuenta_xml.py de newline='\n' a newline='\r\n'. Con el cambio, los 11 casos reales coinciden byte a byte. Ver vault-patrones/inventario-contexto.md.
- 2026-10-01: contexto/ no se versiona (contiene datos de produccion del cargador). El Excel queda solo en local. Motivo: revision externa de la v2.
- 2026-10-01: PASO A, prueba de permisos confirmada en vivo (sesion nueva de Claude Code):
  a) /permissions lista correctamente las 15 reglas deny y las 8 ask de settings.json.
  b) deny sobre contexto/ confirmado con mensaje de sistema ("File is in a directory that
     is denied by your permission settings"), no por decision de Claude. Lectura (Read)
     SI esta permitida en contexto/ -- el deny solo cubre escritura, consistente con la
     regla de "solo lectura" (se puede leer, no se puede escribir).
  c) ask sobre herramientas/ confirmado: el consultor vio un prompt de confirmacion antes
     de que se aplicara la edicion de prueba (revertida despues de confirmar el comportamiento).
  PASO A cerrado.
- 2026-10-01: PASO C (control contra Kondor) no se puede construir como consultas SQL directas:
  la carga no se hace por insercion directa a columnas, pasa por la interfaz de K+TP, cuyo
  esquema interno de base de datos no se conoce y no deberia asumirse. Pendiente de investigar
  con soporte/administracion de Kondor: (1) si K+TP tiene pantalla de busqueda de cuentas
  existentes, (2) si hay reporte/export de cuentas cargadas, (3) si existe una vista SQL de
  solo lectura soportada por el proveedor. Hasta tener respuesta, el control de duplicados y
  la verificacion post-carga siguen siendo manuales (revision visual/exportes), como ya se
  habia decidido el 2026-09-30.