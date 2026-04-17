# Left 4 Dead 2 Vault

Monorepo vault for L4D2 mutations (Squirrel scripts) and mods (compiled as VPK addons).

## Directory conventions

- `mutations/<name>/` — mutation scripts; must contain `mutation.nut`, `manifest.txt`, `addoninfo.txt`
- `mods/<name>/` — mod content; must contain `mod.json`, `addoninfo.txt`, `content/`
- `tools/` — build scripts; keep to bash, no new runtimes
- `docker/` — VPK builder image; changes trigger a new image push to GHCR
- `.github/workflows/` — `validate.yml`, `release.yml`, `docker-publish.yml`

## Release process

Tags drive releases. Format: `{type}/{name}/v{semver}`

```
mutations/hello-world/v1.0.0
mods/my-mod/v2.1.3
```

Only tag from `main`. The `release.yml` workflow builds the VPK and publishes a GitHub release automatically.

## Squirrel / VScript

L4D2 mutations run on Squirrel 2.x via Valve's VScript system.

- Entry hook: `OnGameplayStart()`
- Director config: `DirectorOptions <- { ... }` table at top level
- Per-frame hook: `Think()` — use sparingly, runs every tick
- API reference: https://developer.valvesoftware.com/wiki/L4D2_Vscript_Introduction

## File formats

### mutations/\<name\>/manifest.txt

```
name        = Hello World
description = Short description.
version     = 1.0.0
author      = left-4-dead-vault
type        = mutation
gamemode    = coop
```

### mutations/\<name\>/addoninfo.txt and mods/\<name\>/addoninfo.txt

```
"AddonInfo"
{
    addontitle          "My Addon"
    addondescription    "Short description."
    addonversion        "1.0"
    addontagline        "Tagline"
    addonContent_Script 1
}
```

Use `addonContent_Script 1` for mutations (script content). For mods with other asset types, set the appropriate `addonContent_*` key instead.

## Code Style

### Squirrel (.nut)

- **Indentation:** 4 spaces (no tabs)
- **Braces:** Opening brace on same line (K&R style)
- **Naming:** `snake_case` for functions and variables; `SCREAMING_SNAKE_CASE` for constants
- **Comments:** Use `//`; explain non-obvious logic only, not what the code does
- **`Think()`:** Only define when genuinely needed per-frame; leave it commented out in templates

### Shell (tools/)

- `set -euo pipefail` at top of every script
- No new runtimes or external dependencies beyond `bash` and `vpk`
- Portable bash — no zsh or fish idioms

## VPK layout built by tools/build.sh

`tools/build.sh <type> <name>` — directory names use hyphens; VPK-internal paths use underscores.

Mutations:
```
addoninfo.txt
scripts/vscripts/<mutation_name>.nut     (hyphens → underscores)
cfg/<mutation_name>.cfg                  (only if convars.cfg present)
```

Mods:
```
addoninfo.txt
<everything under content/>
```

## Before committing

1. Verify required files exist for every mutation and mod (CI runs the same checks)
2. Run `tools/build.sh <type> <name>` locally to confirm the VPK builds without error
3. Remove debug `Msg()` calls and dead/commented-out code
4. Only tag from `main`; do not change tag format without updating all three workflows

## Do not

- Commit built VPKs (`dist/` is gitignored)
- Add runtime dependencies to `tools/build.sh`
- Change tag format without updating all three workflows
- Use `Think()` in mutations unless genuinely required per-frame
