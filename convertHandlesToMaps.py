import json
import os


def convert(input_txt_path: str, output_json_path: str):
    with open(input_txt_path, 'r', encoding='utf-8') as f:
        lines = [ln.rstrip('\n') for ln in f]

    items = []
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        one_word = line.endswith('?') or line.endswith('*')
        use_longer = line.endswith('?') or line.endswith('!')
        # Trim trailing ? ! * characters for archetypeName
        archetype = line.rstrip('?!*').strip()
        items.append({
            'archetypeName': archetype,
            'oneWordMatch': one_word,
            'useLongerMatches': use_longer
        })

    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, 'w', encoding='utf-8') as out_f:
        json.dump(items, out_f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    base = os.path.dirname(__file__)
    input_txt = os.path.join(base, 'metadata', 'unique_handle_values.txt')
    output_json = os.path.join(base, 'maps', 'monster_archetype_map.json')
    if not os.path.exists(input_txt):
        raise FileNotFoundError(f"Input file not found: {input_txt}")
    convert(input_txt, output_json)
    print(f"Wrote {output_json}")
