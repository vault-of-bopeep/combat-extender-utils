import json
import os

base = os.path.dirname(__file__)
path = os.path.join(base, 'maps', 'monster_archetype_map.json')
if not os.path.exists(path):
    raise FileNotFoundError(path)

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

if not isinstance(data, list):
    print('File already a dict, no changes made.')
    raise SystemExit(0)

result = {}
duplicates = []
for item in data:
    name = item.get('archetypeName')
    if name is None:
        continue
    value = {k: v for k, v in item.items() if k != 'archetypeName'}
    if name in result:
        duplicates.append(name)
    result[name] = value

with open(path, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(path, 'written')
if duplicates:
    print('Warning: duplicate keys overwritten for:', duplicates)
