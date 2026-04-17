#!/usr/bin/env bash
# Usage: tools/build.sh <type> <name>
#   type: mutations | mods
#   name: directory name under <type>/
# Output: dist/<name>.vpk

set -euo pipefail

TYPE="${1:?type required (mutations|mods)}"
NAME="${2:?name required}"
SRC="${TYPE}/${NAME}"
STAGING="$(mktemp -d)"
DIST="dist"

[ -d "$SRC" ] || { echo "Not found: $SRC" >&2; exit 1; }

mkdir -p "$DIST"

# This big chunk prepares the source to be bundled to VPK
case "$TYPE" in
  mutations)
    mkdir -p "$STAGING/scripts/vscripts"
    # Filename inside VPK uses underscores (L4D2 convention)
    NUT_NAME="${NAME//-/_}.nut"
    cp "$SRC/mutation.nut"   "$STAGING/scripts/vscripts/$NUT_NAME"
    cp "$SRC/addoninfo.txt"  "$STAGING/addoninfo.txt"
    if [ -f "$SRC/convars.cfg" ]; then
      mkdir -p "$STAGING/cfg"
      cp "$SRC/convars.cfg" "$STAGING/cfg/${NAME//-/_}.cfg"
    fi
    ;;
  mods)
    [ -d "$SRC/content" ] || { echo "Missing content/ in $SRC" >&2; exit 1; }
    cp -r "$SRC/content/." "$STAGING/"
    cp "$SRC/addoninfo.txt" "$STAGING/addoninfo.txt"
    ;;
  *)
    echo "Unknown type: $TYPE (expected mutations|mods)" >&2
    exit 1
    ;;
esac

vpk "$STAGING"
mv "${STAGING}.vpk" "${DIST}/${NAME}.vpk"
rm -rf "$STAGING"

echo "Built: ${DIST}/${NAME}.vpk"
