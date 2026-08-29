"""Validate Fantasy Travel's JSON, 26.2 layout, and function references."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = PROJECT_ROOT / "main" / "fantasy_travel"
RESOURCE_PACK_ROOT = PROJECT_ROOT / "optional" / "fantasy_travel_resources"
BANNED_DIRECTORIES = {
    "advancements",
    "functions",
    "item_modifiers",
    "loot_tables",
    "predicates",
    "recipes",
    "structures",
}
FUNCTION_REFERENCE = re.compile(
    r"(?:^|\brun\s+)function\s+(#?[a-z0-9_.-]+:[a-z0-9_./-]+)"
)


def resource_id(path: Path, resource_folder: str) -> str:
    relative = path.relative_to(PACK_ROOT / "data")
    namespace = relative.parts[0]
    prefix_length = 3 if resource_folder == "tags/function" else 2
    resource_path = Path(*relative.parts[prefix_length:]).with_suffix("").as_posix()
    return f"{namespace}:{resource_path}"


def main() -> int:
    errors: list[str] = []
    json_documents: dict[Path, object] = {}

    metadata_path = PACK_ROOT / "pack.mcmeta"
    resource_metadata_path = RESOURCE_PACK_ROOT / "pack.mcmeta"
    json_paths = [
        metadata_path,
        resource_metadata_path,
        *PACK_ROOT.rglob("*.json"),
    ]
    for path in json_paths:
        try:
            json_documents[path] = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"Invalid JSON: {path.relative_to(PROJECT_ROOT)}: {error}")

    metadata = json_documents.get(metadata_path)
    expected_format = [107, 1]
    if not isinstance(metadata, dict):
        errors.append("pack.mcmeta does not contain an object")
    else:
        pack = metadata.get("pack", {})
        if (
            pack.get("min_format") != expected_format
            or pack.get("max_format") != expected_format
        ):
            errors.append("pack.mcmeta must target exactly data pack format 107.1")

    resource_metadata = json_documents.get(resource_metadata_path)
    expected_resource_format = [88, 0]
    if not isinstance(resource_metadata, dict):
        errors.append("optional resource pack metadata does not contain an object")
    else:
        pack = resource_metadata.get("pack", {})
        if (
            pack.get("min_format") != expected_resource_format
            or pack.get("max_format") != expected_resource_format
        ):
            errors.append("optional resource pack must target format 88.0")

    for path in PACK_ROOT.rglob("*"):
        contains_files = path.is_dir() and any(
            child.is_file() for child in path.rglob("*")
        )
        if contains_files and path.name in BANNED_DIRECTORIES:
            errors.append(f"Legacy plural directory: {path.relative_to(PROJECT_ROOT)}")
        if contains_files and "lost_fly" in path.parts:
            errors.append(f"Legacy namespace path: {path.relative_to(PROJECT_ROOT)}")

    functions = {
        resource_id(path, "function")
        for path in (PACK_ROOT / "data").glob("*/function/**/*.mcfunction")
    }
    tags = {
        resource_id(path, "tags/function")
        for path in (PACK_ROOT / "data").glob("*/tags/function/**/*.json")
    }

    references: list[tuple[Path, str]] = []
    for path, document in json_documents.items():
        if "/tags/function/" not in path.as_posix() or not isinstance(document, dict):
            continue
        values = document.get("values", [])
        if not isinstance(values, list):
            errors.append(f"Tag values must be a list: {path.relative_to(PROJECT_ROOT)}")
            continue
        for value in values:
            if isinstance(value, str):
                references.append((path, value))
            elif isinstance(value, dict) and isinstance(value.get("id"), str):
                references.append((path, value["id"]))

    for path in (PACK_ROOT / "data").glob("*/function/**/*.mcfunction"):
        for line in path.read_text(encoding="utf-8").splitlines():
            match = FUNCTION_REFERENCE.search(line)
            if match:
                references.append((path, match.group(1)))

    for source, reference in references:
        if reference.startswith("#"):
            if reference[1:] not in tags:
                errors.append(
                    f"Missing function tag {reference}: "
                    f"{source.relative_to(PROJECT_ROOT)}"
                )
        elif reference not in functions:
            errors.append(
                f"Missing function {reference}: {source.relative_to(PROJECT_ROOT)}"
            )

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1

    print(
        f"Validated {len(json_paths)} JSON files, "
        f"{len(functions)} functions, and {len(tags)} function tags."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
