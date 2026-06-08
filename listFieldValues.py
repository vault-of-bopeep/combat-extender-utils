import json
import os
from typing import List


def gather_unique_field_values(file_path: str, field_name: str) -> List[str]:
    """Return a sorted list of unique, non-empty string values for `field_name` from the JSON file.

    The JSON file is expected to contain a top-level object with a "Guids" list of entries (dicts).
    Field name matching is case-insensitive; the first matching key per entry is used.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    entries = data.get('Guids', []) if isinstance(data, dict) else []
    key_lower = field_name.lower()
    values = set()

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        # Direct lookup first, then case-insensitive key match
        if field_name in entry:
            val = entry.get(field_name)
        else:
            val = None
            for k, v in entry.items():
                if k.lower() == key_lower:
                    val = v
                    break
        if isinstance(val, str):
            s = val.strip()
            if s:
                values.add(s)

    return sorted(values)


def main():
    # Edit these values for quick testing in your editor before running
    FIELD_NAME = 'Handle'  # e.g., 'Location', 'Type', 'Handle', 'MonsterArchetype'
    INPUT_FILENAME = 'guid_mapper_input.json'  # the fixed input filename you requested

    # Resolve input path relative to script directory
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, INPUT_FILENAME)

    # Fallback for convenience during testing: use master JSON if the input file is missing
    if not os.path.exists(file_path):
        fallback = os.path.join(script_dir, 'guid_mapper_master.json')
        if os.path.exists(fallback):
            file_path = fallback
        else:
            raise FileNotFoundError(f"File not found: {file_path}")

    values = gather_unique_field_values(file_path, FIELD_NAME)

    output_dir = os.path.join(script_dir, 'metadata')
    os.makedirs(output_dir, exist_ok=True)
    output_name = f'unique_{FIELD_NAME.lower()}_values.txt'
    out_path = os.path.join(output_dir, output_name)

    with open(out_path, 'w', encoding='utf-8') as out_f:
        out_f.write('\n'.join(values))


if __name__ == '__main__':
    main()
