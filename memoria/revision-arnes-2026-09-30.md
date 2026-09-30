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