# TCM Contabilidad IA

Fuente unica de verdad para la creacion de cuentas contables (chart of accounts) de Kondor K+/K+TP, usando Claude Code sobre un estandar versionado y validado automaticamente.

Para las instrucciones completas que sigue Claude, ver AGENTS.md. Este README es solo el punto de entrada rapido.

## Estructura

  AGENTS.md                      Reglas duras y mapa del proyecto
  CLAUDE.md                      Importa @AGENTS.md
  CODEOWNERS                     Quien aprueba cambios a cada carpeta
  .gitattributes                 Fin de linea protegido para los fixtures de prueba
  .gitignore                     contexto/ y Account/ no se versionan (datos sensibles/locales)
  requirements.txt               Dependencias de Python (jsonschema, openpyxl)

  .claude/
    settings.json                 Permisos (deny/ask) de Claude Code en este repo
    skills/arnes-*/                9 skills del estandar de arnes de TCM

  .github/workflows/
    validar-generador-cuentas.yml  Gate de CI: corre las pruebas en cada Pull Request

  contexto/                      Documentacion cruda de Kondor/Finastra - SOLO LECTURA, NO se versiona

  vault-patrones/                Estandar confirmado y reutilizable
    kondor/cuentas/
      estructura-cuenta.md          Campos, formato, XML de salida
      naturaleza-cuentas.md         Deudora/acreedora por tipo (sin fuente confirmada aun)
      catalogo-proyectos.md         Proyectos/entidades confirmados
      glosario-prompts.md           Prompts recomendados para pedirle cuentas a Claude
      guia-replicar-entorno.md      Como configurar este repo en un equipo nuevo
    candidatos/
      enums-pendientes.md           Valores y preguntas sin confirmar todavia
    inventario-contexto.md         Evidencia de regresion contra la macro original

  vault-proyecto-rd-unica/
    proyecto.md                    Datos del proyecto RD_UNICA

  herramientas/
    generar_cuenta_xml.py          El generador: valida y crea los .xml
    tests/
      test_generador_cuentas.py     Pruebas de regresion automaticas
      fixtures/macro/                11 casos reales (anonimizados) exportados por la macro

  schemas/
    cuenta.schema.json              JSON Schema del estandar
    catalogo_proyectos.json         Proyectos validos, formato que lee el script

  Account/                       Los .xml generados (no versionado)
  reportes/                      Reporte Excel consolidado (no versionado)

  memoria/
    decisiones.md                  Decisiones de arquitectura, con su motivo
    lecciones.md                   Problemas tecnicos y su solucion
    revision-arnes-2026-09-30.md   Revision externa que definio el plan de adecuacion al arnes
    sesiones/                      (vacio - sin hooks de sesion todavia)

## Como usarlo

1. Clona el repo (ver vault-patrones/kondor/cuentas/guia-replicar-entorno.md para el detalle completo).
2. Abre VS Code en la carpeta del repo, abre una terminal integrada y escribe claude.
3. Pide, en lenguaje natural, que cree una o varias cuentas (ver vault-patrones/kondor/cuentas/glosario-prompts.md para ejemplos).
4. El .xml generado queda en Account/; copialo manualmente a la ruta real de carga de Kondor.

## Gobernanza

- Rama main protegida: todo cambio pasa por Pull Request.
- herramientas/, schemas/, vault-patrones/kondor/cuentas/ y los workflows tienen un gate de CI obligatorio (25 pruebas automaticas).
- CODEOWNERS define quien aprueba cada carpeta - hoy hay un solo owner, limitacion conocida y registrada en memoria/decisiones.md.
- El consultor opera git y Kondor; Claude nunca ejecuta git, SQL, ni carga nada directamente a Kondor.

## Estado del proyecto (ver memoria/decisiones.md para el detalle completo)

- Generador probado: 25 pruebas automaticas, incluyendo 11 casos reales exportados por la macro original, verificados byte a byte.
- Un solo proyecto confirmado: RD_UNICA.
- Enums (AccountType/ValuationType/InputMode) con un solo valor confirmado cada uno.
- Control de duplicados contra Kondor: pendiente - la carga pasa por la interfaz de K+TP, no por SQL directo, y falta confirmar como verificarlo (ver memoria/decisiones.md, 2026-10-01).