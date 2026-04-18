# Left 4 Dead 2 Vault

Enjoymaxxing the best game ever made with LLMs. Content is built automatically and published as `.vpk` releases via GitHub Actions.

## Structure

```
mutations/          Squirrel (.nut) mutation scripts
mods/               Source mod content (materials, models, sounds, scripts)
tools/              Build helpers
.github/workflows/  CI/CD pipelines
```

## Adding a Mutation

1. Create `mutations/<name>/` — use `mutations/hello-world/` as a template
2. Required files: `mutation.nut`, `manifest.txt`, `addoninfo.txt`
3. Optional: `convars.cfg` — packed into `cfg/<name>.cfg` inside the VPK
4. Tag `mutations/<name>/v1.0.0` to trigger a release build

## Adding a Mod

1. Create `mods/<name>/`
2. Required files: `mod.json`, `addoninfo.txt`, `content/`
3. `content/` mirrors L4D2's VFS layout (`materials/`, `models/`, `sounds/`, `scripts/`)
4. Tag `mods/<name>/v1.0.0` to trigger a release build

## Building Locally

Build VPK files manually using the build script:

```bash
uv run tools/build.py <type> <name>
```

Examples:
```bash
uv run tools/build.py mutations hello-world
```

Output appears in `dist/<name>.vpk`

## CI Workflows

| Workflow | Trigger | Action |
|---|---|---|
| `validate` | Every PR | Checks required files exist |
| `release` | Tag `{type}/{name}/v{semver}` | Builds VPK, creates GitHub Release |

Download VPKs from the [Releases](../../releases) tab.

## Official Documentation

- [Intro to Scripting](https://developer.valvesoftware.com/wiki/Left_4_Dead_2/Scripting)
- [Expanded Mutation System](https://developer.valvesoftware.com/wiki/Left_4_Dead_2/Scripting/Expanded_Mutation_System)
- [Mutation Gametype](https://developer.valvesoftware.com/wiki/Left_4_Dead_2/Scripting/Mutation_Gametype)
- [Decrypted Mutations](https://developer.valvesoftware.com/wiki/Left_4_Dead_2/Scripting/Decrypted_mutations)