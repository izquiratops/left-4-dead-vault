#!/usr/bin/env python3
"""Build VPK bundles for Left 4 Dead 2 mutations and mods.

Usage: tools/build.py <type> <name>
  type: mutations | mods
  name: directory name under <type>/
Output: dist/<name>.vpk
"""

import sys
import shutil
import tempfile
import vpk
from pathlib import Path


def prepare_mutation(src: Path, staging: Path, name: str):
    """Prepare mutation source for VPK bundling."""
    scripts_dir = staging / "scripts" / "vscripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)

    nut_name = name.replace("-", "_") + ".nut"
    shutil.copy(src / "mutation.nut", scripts_dir / nut_name)
    shutil.copy(src / "addoninfo.txt", staging / "addoninfo.txt")

    convars_src = src / "convars.cfg"
    if convars_src.exists():
        cfg_dir = staging / "cfg"
        cfg_dir.mkdir(parents=True, exist_ok=True)
        cfg_name = name.replace("-", "_") + ".cfg"
        shutil.copy(convars_src, cfg_dir / cfg_name)


def prepare_mod(src: Path, staging: Path, name: str):
    """Prepare mod source for VPK bundling."""
    content_dir = src / "content"
    if not content_dir.is_dir():
        print(f"Missing content/ in {src}", file=sys.stderr)
        sys.exit(1)

    for item in content_dir.iterdir():
        if item.is_file():
            shutil.copy(item, staging / item.name)
        else:
            shutil.copytree(item, staging / item.name)

    shutil.copy(src / "addoninfo.txt", staging / "addoninfo.txt")


def main():
    if len(sys.argv) < 3:
        print("Error: type and name required", file=sys.stderr)
        sys.exit(1)

    build_type = sys.argv[1]
    name = sys.argv[2]

    src = Path(build_type) / name
    dist = Path("dist")

    if build_type not in ("mutations", "mods"):
        print(f"Unknown type: {build_type} (expected mutations|mods)", file=sys.stderr)
        sys.exit(1)

    if not src.is_dir():
        print(f"Not found: {src}", file=sys.stderr)
        sys.exit(1)

    dist.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as staging:
        staging_path = Path(staging)

        if build_type == "mutations":
            prepare_mutation(src, staging_path, name)
        else:
            prepare_mod(src, staging_path, name)

        output_vpk = dist / f"{name}.vpk"
        vpk_archive = vpk.new(str(staging_path))
        vpk_archive.version = 1
        vpk_archive.save(str(output_vpk))

    print(f"Built: {output_vpk}")


if __name__ == "__main__":
    main()
