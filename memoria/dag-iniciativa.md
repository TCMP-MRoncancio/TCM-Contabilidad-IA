# DAG de la iniciativa y del manejo del repositorio

Vista en grafo dirigido aciclico (DAG) de como avanzo la iniciativa y de como se opera el repositorio hoy.
Fuentes: `git log`, `memoria/decisiones.md`, `AGENTS.md`, `CODEOWNERS` y `.github/workflows/validar-generador-cuentas.yml`.
Corte: 2026-11-23.

## 1. Evolucion de la iniciativa (dependencias entre etapas)

Cada flecha significa "esta etapa dependio de la anterior". Entre parentesis, el PR que la llevo a `main`.

```mermaid
flowchart TD
    A["Decision 2026-09: descartar nucleo multi-area<br/>adoptar patron vault-patrones / vault-proyecto / contexto / memoria"]
    B["Reestructura al patron adaptado (PR #2)"]
    C["Corregir rutas obsoletas + reporte consolidado (PR #4)"]
    D["Restaurar validacion de duplicados (PR #3)"]
    E["Gate de CI: pruebas de regresion del generador (PR #5, #6, #7)"]
    F["Verificacion de sincronia .md vs codigo (PR #8)"]
    G["Eliminar catalogo-paises-bonos obsoleto (PR #9)"]
    H["Revision de arnes TCM 2026-09-30<br/>plan por bloques"]
    I["Bloque 1: seguridad por configuracion<br/>deny/ask en settings.json, regla dura 10"]
    J["Bloque 2: validacion jsonschema, lote atomico, --forzar con .bak (PR #10, #11)"]
    K["Bloque 3: evidencia contra la macro<br/>621 registros + 11 casos reales, fix CRLF"]
    L["Paso A: contexto/ fuera de git, permisos probados en vivo"]
    M["Paso B: fixture de 11 casos + 4 correcciones (PR #12)"]
    N["Paso C: control contra Kondor<br/>PAUSADO: no es SQL directo, investigar K+TP (PR #14)"]
    O["Paso D: CODEOWNERS real, README coherente (PR #15)"]
    P["Hook Stop: reporte de tokens por solicitud"]

    A --> B
    B --> C
    B --> D
    C --> E
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J
    J --> K
    K --> L
    L --> M
    M --> N
    M --> O
    O --> P

    Q1["Pendiente: respuesta de soporte Kondor<br/>busqueda, export o vista SQL de solo lectura"]
    Q2["Pendiente: segundo CODEOWNER<br/>antes de cargas reales a produccion"]
    Q3["Pendiente: lista blanca estricta de Bash<br/>riesgo aceptado en Bloque 1"]
    Q4["Futuro: tickets y proyectos adicionales a RD_UNICA"]

    N -.-> Q1
    O -.-> Q2
    I -.-> Q3
    P -.-> Q4

    classDef hecho fill:#d4edda,stroke:#2e7d32,color:#1b1b1b
    classDef pausa fill:#fff3cd,stroke:#b8860b,color:#1b1b1b
    classDef pendiente fill:#f8d7da,stroke:#a94442,color:#1b1b1b,stroke-dasharray: 4 3
    class A,B,C,D,E,F,G,H,I,J,K,L,M,O,P hecho
    class N pausa
    class Q1,Q2,Q3,Q4 pendiente
```

Verde: cerrado en `main`. Amarillo: pausado por decision. Rojo punteado: pendiente.

## 2. Manejo del repositorio: flujo de una solicitud de cuentas

```mermaid
flowchart TD
    S["Consultor pide cuentas en lenguaje natural"]
    R["Claude lee vault-patrones/kondor/cuentas/<br/>estandar vigente"]
    FD{"Faltan datos?"}
    PQ["Claude pregunta, no inventa (regla 1)"]
    J["Claude arma el JSON de entrada"]
    G["herramientas/generar_cuenta_xml.py"]
    V1{"Schema JSON valido?"}
    V2{"Proyecto en catalogo?"}
    V3{"Enums confirmados?"}
    V4{"Nombre ASCII y numero con largo esperado?"}
    V5{"XML ya existe?"}
    FZ["Avisar y preguntar; --forzar solo si el consultor lo pide (.bak)"]
    X["XML con CRLF en Account/"]
    RP["Reporte Excel consolidado en reportes/"]
    K["Consultor copia a Kondor y confirma carga"]
    RJ["Rechazo reportado con motivo"]
    CA["Documentar en vault-patrones/candidatos/"]

    S --> R --> FD
    FD -- si --> PQ --> J
    FD -- no --> J
    J --> G --> V1
    V1 -- no --> RJ
    V1 -- si --> V2
    V2 -- no --> CA
    V2 -- si --> V3
    V3 -- no --> CA
    V3 -- si --> V4
    V4 -- no --> RJ
    V4 -- si --> V5
    V5 -- si --> FZ
    V5 -- no --> X
    FZ --> X
    X --> RP --> K
    CA --> PR0["Propuesta de cambio al estandar (seccion 3)"]
```

## 3. Manejo del repositorio: cambios al estandar y al codigo

```mermaid
flowchart TD
    C0["Cambio propuesto: vault-patrones/, schemas/, herramientas/, .claude/, AGENTS.md"]
    B0["Consultor crea rama desde main (regla 9)"]
    CM["Commit en la rama"]
    PU["Push a GitHub y Pull Request"]
    CI{"Toca herramientas/, schemas/,<br/>vault-patrones/kondor/cuentas/ o .github/workflows/?"}
    GT["CI: validar-generador-cuentas<br/>pruebas de regresion + sincronia .md/codigo"]
    OK{"CI en verde?"}
    FX["Corregir en la misma rama"]
    CO["Revision CODEOWNER (@TCMP-MRoncancio)"]
    MG["Merge a main"]
    ME["Actualizar memoria/decisiones.md o lecciones.md"]

    C0 --> B0 --> CM --> PU --> CI
    CI -- si --> GT --> OK
    CI -- no --> CO
    OK -- no --> FX --> CM
    OK -- si --> CO
    CO --> MG --> ME
```

Nota: el ciclo "corregir y volver a commitear" no rompe la aciclicidad del historial; cada correccion es un commit nuevo sobre la rama.
