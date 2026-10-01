# Revisión del arnés contra el estándar TCM (2026-09-30)

## Se conserva
Generador determinista con validaciones; reglas duras de AGENTS.md; tabla "Dónde se anota qué";
pruebas de sincronía .md vs código; CI en cada PR; candidatos y marcas [CONFIRMAR]; decisiones y lecciones.

## Verificado ejecutando (copia fuera del repo)
- Los 14 tests pasan.
- settings.json con BOM: falla en parsers JSON estrictos; los permisos podrían no cargarse.
- Se acepta un campo extra pese a additionalProperties:false.
- Account_Name "   " (solo espacios) genera cuenta.
- Account_Name de más de 300 caracteres genera cuenta (sin largo máximo).
- Account_ShortName numérico (no texto) provoca AttributeError.
- Lote con número repetido: genera la primera cuenta y rechaza la segunda (lote a medias).
- write_text sin newline: en Windows escribe CRLF; no está verificado que Kondor lo acepte.

## Riesgos
1. Cargar en Kondor una cuenta ya existente: el control de duplicados solo mira Account/ local.
2. Permisos ignorados o inexistentes (solo allow; BOM).
3. XML aceptado por el script y rechazado o mal cargado por Kondor.
4. "Idéntico a la macro" sin evidencia en el repo.
5. CODEOWNERS apunta a rutas inexistentes y tiene un solo owner.
6. Datos de proyectos de clientes dentro del repo del estándar.

## Plan
Bloque 1 seguridad; 2 generador; 3 evidencia contra la macro; 4 control contra Kondor;
5 orden del repo; 6 ciclo y memoria. Un bloque por sesión, con aprobación escrita del consultor.
## Revisión de la v2 (2026-10-01)
- Bloques 1 y 2 aprobados. 21 tests pasan. settings.json carga sin error.
- Validado: CRLF confirmado contra 11 XML reales de la macro, coincidencia byte a byte.
- La prueba de 621 registros compara contra una reconstrucción del formato, no contra salida real de
  la macro; la evidencia válida son los 11 casos reales.
- Riesgo nuevo: contexto/ no está en .gitignore y el Excel de la macro tiene datos de producción.
- Pendiente: prueba de /permissions, fixture versionado de los 11 casos, bloques 4, 5 y 6.
- Menores del generador: elemento no-objeto en el lote provoca AttributeError; acepta espacios al
  inicio/fin del nombre; cada --forzar pisa el .bak anterior; lote vacío termina con éxito;
  docstring de escribir_cuenta dice newline='\n'; requirements.txt sin versiones fijas.