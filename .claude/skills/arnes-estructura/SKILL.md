---
name: arnes-estructura
description: "Paso 2 de construir un arnes: crear el esqueleto del proyecto (carpetas, AGENTS.md, CLAUDE.md, settings.json con permisos, .gitignore, .gitattributes, memoria del sistema y separacion de repos). Usar cuando la ficha del arnes ya esta aprobada y hay que armar la estructura, o para revisar si la estructura de un arnes existente esta completa. No usar antes de tener ficha-arnes.md aprobada."
---

# Estructura del arnés (paso 2)

**Objetivo:** dejar un esqueleto donde cada cosa tiene un único lugar, con los permisos de seguridad activos desde el primer día.
**Entrada:** `ficha-arnes.md` aprobada (skill `arnes-concepcion`).
**Salida:** la carpeta del arnés con la estructura de abajo, los archivos base completos y los permisos probados.
**Plantillas:** en `references/` (listas para copiar y completar).

## Estructura estándar

```
<arnes>/                         ← repo del arnés
├── AGENTS.md                    ← reglas del proyecto (fuente única)
├── CLAUDE.md                    ← importa AGENTS.md con @AGENTS.md
├── README.md                    ← puerta de entrada para personas
├── .gitignore                   ← excluye vaults, estado personal, copias crudas
├── .gitattributes               ← finales de línea por tipo de archivo
├── .claude/
│   ├── settings.json            ← permisos (deny / ask) y hooks
│   ├── arnes.json               ← rutas que usan los hooks y la herramienta de tickets
│   ├── agents/                  ← un .md por agente (skill arnes-agentes-y-skills)
│   ├── skills/                  ← skills de dominio y de sesión
│   └── hooks/                   ← scripts de los hooks (skill arnes-memoria-y-sesiones)
├── contexto/                    ← material crudo: documentación y ejemplos. SOLO LECTURA
├── herramientas/                ← scripts deterministas (skill arnes-generador) y plantillas
│   ├── README.md
│   └── plantillas/              ← esqueletos de vault de cliente y de ticket
├── memoria/                     ← memoria del sistema (cómo trabajamos), no de los tickets
│   ├── MEMORIA.md
│   ├── ficha-arnes.md           ← ficha del arnés aprobada (skill arnes-concepcion)
│   ├── decisiones.md
│   ├── lecciones.md
│   └── sesiones/
├── vault-patrones/              ← repo propio, clonado aquí, ignorado por el arnés
└── vault-cliente-<cliente>/     ← repo propio por cliente, ignorado por el arnés
    └── tickets/<ticket>/
        ├── ESTADO.md, bitacora.md, decisiones.md, preguntas.md, incidencias.md
        ├── diseno/              ← ficha.yaml y diseno.md del ticket
        ├── salida/              ← entregable generado
        ├── entrega/             ← paquete de promoción y correcciones de desarrollo
        ├── evidencias/          ← capturas, extracciones de vuelta, resultados de consultas
        └── sesiones/            ← copias de conversaciones (las escriben los hooks)
```

Los nombres `diseno/`, `salida/` y `entrega/` son la convención recomendada. **Conviene no cambiarlos.** Si el caso necesita otros,
hay que cambiarlos en todos estos lugares a la vez: `.claude/arnes.json` (`dir_diseno`, `vigilar_cambios_en`), las carpetas de
`herramientas/plantillas/ticket/`, AGENTS.md, las definiciones de los agentes, las skills de dominio y el generador.

> **Variante del piloto de referencia.** El piloto guardaba el diseño en una carpeta aparte, `proyectos/<cliente>/<ticket>/`.
> Funciona, pero obliga a un tercer repo y complica aislar los datos de cada cliente. Para un arnés nuevo, el diseño va dentro
> del ticket en el vault del cliente.

## Pasos

### 1. Crear la carpeta y los archivos base

1. Crear la carpeta del arnés y las subcarpetas de la estructura (sin los vaults todavía).
2. Copiar desde `references/`:
   - `AGENTS-plantilla.md` → `AGENTS.md`
   - `CLAUDE-plantilla.md` → `CLAUDE.md`
   - `settings-plantilla.json` → `.claude/settings.json`
   - `gitignore-plantilla.txt` → `.gitignore`
   - `gitattributes-plantilla.txt` → `.gitattributes`
   - `memoria-MEMORIA.md`, `memoria-decisiones.md`, `memoria-lecciones.md` → `memoria/MEMORIA.md`, `memoria/decisiones.md`, `memoria/lecciones.md`
3. Crear `README.md` con: qué resuelve, estado, estructura, requisitos, puesta en marcha, cómo se trabaja, reglas, cómo retomar.

**Termina cuando:** existen todos los archivos base, aunque con marcadores por completar.

### 2. Completar AGENTS.md desde la ficha del arnés

AGENTS.md es la fuente única de reglas. Se completa **solo** con lo que está en `ficha-arnes.md`:

| Sección de AGENTS.md | Sale de la ficha del arnés |
|---|---|
| Descripción (una línea) | Caso de uso |
| Reglas duras | Prohibiciones (sección 5) y las reglas fijas del método (preguntar en vez de inventar, contexto de solo lectura, no avanzar sin control) |
| Mapa del proyecto | Esta estructura, con quién escribe en cada carpeta |
| Protocolo de sesión | Fijo (inicio, durante, cierre); se ajusta en `arnes-memoria-y-sesiones` |
| Dónde se anota qué | Fijo; se ajusta si cambian los nombres de carpetas |
| Fases y controles | Se completa en `arnes-fases-y-tickets` |
| Agentes y skills | Se completa en `arnes-agentes-y-skills` |
| Herramientas | Se completa en `arnes-generador` |

Reglas de redacción:
- Cada regla dura es una frase corta, verificable y numerada. "Nunca X" o "Siempre Y", con el motivo en una línea si no es obvio.
- AGENTS.md dice **dónde** está el conocimiento; no lo copia (lección M09 del piloto: un dato en dos lugares, uno queda viejo).
- Nada de credenciales, servidores, usuarios ni rutas personales.

**Termina cuando:** no quedan marcadores sin completar en las secciones que corresponden a este paso.

### 3. Configurar los permisos

Editar `.claude/settings.json`:

1. **`deny`**: una entrada por cada prohibición de la ficha que se pueda expresar como permiso. Siempre incluye:
   - editar `contexto/`;
   - los clientes de consola que escriben en el ambiente (en bases SQL Server: `sqlcmd`, `osql`, `bcp`; ajustar al sistema);
     si el sistema se modifica por API, los clientes HTTP (`curl`, `Invoke-WebRequest`, `wget`) o, como mínimo, sus usos con
     métodos de escritura; si se despliega por consola propia del sistema, esa consola;
   - `git push`, `git clone`, creación de repos remotos.
2. **`ask`**: editar `vault-patrones/`, `.claude/` y `herramientas/`. Así el arnés no se modifica a sí mismo sin aprobación
   (lección M03 del piloto: en un piloto anterior, las definiciones se reescribían solas y el comportamiento derivaba).
3. `cleanupPeriodDays`: 365, para que las conversaciones se conserven un año.

La plantilla trae dos familias de clientes de escritura como ejemplo: consolas de base SQL Server (`sqlcmd`, `osql`, `bcp`, las del
piloto) y clientes HTTP (`curl`, `wget`, `Invoke-WebRequest`). **Dejar las que correspondan al sistema destino, agregar las que
falten y quitar las que no apliquen**, registrando la decisión. Si un cliente HTTP hace falta para leer, se reemplaza el `deny`
general por uno sobre sus métodos de escritura y se prueba.

La sintaxis exacta de los permisos puede cambiar entre versiones de Claude Code: confirmarla en la documentación oficial
antes de dar por buena la plantilla, y probarla (paso 6).

**Termina cuando:** cada prohibición de la ficha está como `deny`, como herramienta ausente de un agente o, si no se puede
bloquear, marcada en AGENTS.md como "solo regla" con el motivo.

### 4. Separar los repos

1. El `.gitignore` del arnés excluye `vault-patrones/`, `vault-cliente-*/`, el estado personal (`.claude/*.local.json`,
   `.claude/.marcas/`) y las copias crudas de conversaciones sin ticket (`memoria/sesiones/raw/`).
   **Cada vault lleva su propio `.gitignore` y `.gitattributes`**: git no aplica las reglas del arnés dentro de un repo anidado.
   La plantilla de vault de cliente (`arnes-fases-y-tickets`) ya los trae (ignora `tickets/*/sesiones/raw/`, protege `evidencias/`).
2. `vault-patrones` y cada `vault-cliente-<c>` son repos propios. Los crea y publica el humano (regla: git remoto lo opera el humano).
3. Decidir con el humano si `contexto/` se versiona en el repo del arnés. Si tiene material de clientes o de terceros con
   restricciones, **no** se versiona ahí: se excluye en `.gitignore` y se comparte por otro medio.

**Termina cuando:** `git status` del arnés no muestra archivos de ningún vault ni de `contexto/` (si se excluyó).

### 5. Finales de línea y codificación

1. `.gitattributes` fija los finales de línea por tipo de archivo (plantilla en `references/`).
2. `contexto/` lleva `-text` en el `.gitattributes` del arnés y `evidencias/` en el de cada vault de cliente: git no los toca y se
   conservan byte a byte, porque son evidencia.
3. El entregable lleva el final de línea que exige el sistema destino. Si la herramienta que aplica lo altera, la defensa va
   **dentro** del entregable (ver `arnes-seguridad-y-entrega`), no solo en git.
4. Todo script del arnés que escriba archivos lo hace con final de línea explícito (en Python: `newline="\n"` o en bytes).
   Lección M15 del piloto: un script que escribía en modo texto en Windows convirtió 34 archivos a CRLF sin que nadie lo notara.

**Termina cuando:** `.gitattributes` existe y los scripts del arnés escriben con final de línea explícito.

### 6. Probar los permisos

En una sesión nueva de Claude Code dentro de la carpeta, pedir a propósito una acción denegada de cada tipo (por ejemplo,
"edita un archivo de contexto/") y comprobar que se bloquea. Anotar el resultado en `memoria/decisiones.md`.

**Termina cuando:** cada `deny` se probó y bloqueó.

## Control de salida

- [ ] Estructura creada; cada carpeta con su dueño en el mapa de AGENTS.md.
- [ ] AGENTS.md completo en las secciones de este paso, sin datos sensibles.
- [ ] CLAUDE.md importa AGENTS.md.
- [ ] `settings.json` con `deny` y `ask`, probados.
- [ ] `.gitignore` excluye vaults, estado personal y copias crudas; decisión sobre `contexto/` registrada.
- [ ] `.gitattributes` presente.
- [ ] `memoria/` con MEMORIA.md, decisiones.md (con la decisión de estructura) y lecciones.md.
- [ ] README.md con puesta en marcha.

## Errores que ya cometimos (piloto de referencia)

- **Reglas solo en texto.** Un agente al que se le pidió "usar Bash solo para X" usó Bash para otras cosas, dos veces. La
  solución fue quitarle la herramienta. Si algo se puede bloquear, se bloquea.
- **Un comando de lectura que escribe.** Un `git status` corrido desde una sesión sin permiso de borrar dejó un archivo de
  bloqueo (`.git/index.lock`) que impedía los commits. En repos del humano, los agentes no corren git.
- **Vaults dentro del repo del arnés.** Se estuvo a punto de publicar todo en un solo repo. El `.gitignore` los excluía y eso
  lo evitó.

## Siguiente paso

`arnes-conocimiento`: poblar `contexto/` y armar `vault-patrones/`.
