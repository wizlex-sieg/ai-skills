#!/usr/bin/env python3
"""Build standalone skill and combined plugin ZIPs from the canonical sources."""

from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


def build_packages() -> None:
    root = Path(__file__).resolve().parent.parent
    plugin = root / "plugins" / "wizlex-office"
    targets = [plugin, *sorted((plugin / "skills").iterdir())]
    destination = root / "packages"
    destination.mkdir(exist_ok=True)
    checksums = []
    for folder in targets:
        if not folder.is_dir():
            continue
        archive = destination / f"{folder.name}.zip"
        with ZipFile(archive, "w", compression=ZIP_DEFLATED) as output:
            for path in sorted(folder.rglob("*")):
                if not path.is_file() or "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
                    continue
                entry = ZipInfo(path.relative_to(folder.parent).as_posix(), (2026, 1, 1, 0, 0, 0))
                entry.compress_type = ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                output.writestr(entry, path.read_bytes())
        checksums.append(f"{sha256(archive.read_bytes()).hexdigest()}  {archive.name}")
        print(archive.name)
    (destination / "SHA256SUMS").write_text("\n".join(checksums) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build_packages()
