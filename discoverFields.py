import json
import os
import re

from monsterStatBlock import MonsterStatBlock

class discoverFields:

    @staticmethod
    def _flatten_mapping_values(substring_mapping):
        return [sub.lower() for substrings in substring_mapping.values() for sub in substrings]

    @staticmethod
    def _matches_with_rules(target, sub):
        """Match a substring against target using rules:
        - If the substring ends with '!', require a whole-word exact match for the phrase (word boundaries).
        - Otherwise, use simple containment (substring in target).
        Both inputs are expected to be lowercase when called from the callers below.
        """
        if not target or not sub:
            return False

        s = sub.lower()
        if s.endswith('!'):
            phrase = re.escape(s[:-1])
            pattern = r'(?<!\w)' + phrase + r'(?!\w)'
            return re.search(pattern, target) is not None
        return s in target

    @staticmethod
    def update_class_archetype_based_on_notes(blocks):
        base_dir = os.path.dirname(__file__)
        map_dir = os.path.join(base_dir, 'maps')
        with open(os.path.join(map_dir, 'class_archetype_map.json'), 'r') as f:
            substring_mapping = json.load(f)
        mapped_substrings = discoverFields._flatten_mapping_values(substring_mapping)

        for block in blocks:
            if not block.archetype or block.archetype == "":
                notes_lower = block.notes.lower() if block.notes else ""
                handle = block.handle.lower() if block.handle else ""
                type = block.type.lower() if block.type else ""
                subtype = block.subtype.lower() if block.subtype else ""
                full_guid = block.full_guid.lower() if block.full_guid else ""

                notes_lower_match = False
                type_match = False
                subtype_match = False
                handle_match = False
                full_guid_match = False

                if any(discoverFields._matches_with_rules(notes_lower, sub) for sub in mapped_substrings):
                    notes_lower_match = True
                if any(discoverFields._matches_with_rules(handle, sub) for sub in mapped_substrings):
                    handle_match = True
                if any(discoverFields._matches_with_rules(type, sub) for sub in mapped_substrings):
                    type_match = True
                if any(discoverFields._matches_with_rules(subtype, sub) for sub in mapped_substrings):
                    subtype_match = True
                if any(discoverFields._matches_with_rules(full_guid, sub) for sub in mapped_substrings):
                    full_guid_match = True

                matched_class_archetypes = []

                if type_match:
                    for archetype, substrings in substring_mapping.items():
                        if any(discoverFields._matches_with_rules(type, sub) for sub in substrings):
                            matched_class_archetypes.append(archetype.title())

                if full_guid_match:
                    for archetype, substrings in substring_mapping.items():
                        if any(discoverFields._matches_with_rules(full_guid, sub) for sub in substrings):
                            matched_class_archetypes.append(archetype.title())

                if subtype_match:
                    for archetype, substrings in substring_mapping.items():
                        if any(discoverFields._matches_with_rules(subtype, sub) for sub in substrings):
                            matched_class_archetypes.append(archetype.title())

                if handle_match:
                    for archetype, substrings in substring_mapping.items():
                        if any(discoverFields._matches_with_rules(handle, sub) for sub in substrings):
                            matched_class_archetypes.append(archetype.title())

                if notes_lower_match:
                    for archetype, substrings in substring_mapping.items():
                        if any(discoverFields._matches_with_rules(notes_lower, sub) for sub in substrings):
                            matched_class_archetypes.append(archetype.title())

                matched_class_archetypes = list(set(matched_class_archetypes))  # Remove duplicates

                if len(matched_class_archetypes) == 0:
                    continue
                elif len(matched_class_archetypes) == 1:
                    block.archetype = matched_class_archetypes[0]
                else:
                    print(f"Multiple class archetype matches found for {block.full_guid}: {matched_class_archetypes}. Setting archetype to 'Multiple'.")
                    block.archetype = f"Multiple: {', '.join(matched_class_archetypes)}"

    @staticmethod
    def update_monster_archetype_based_on_handle(blocks):
        base_dir = os.path.dirname(__file__)
        map_dir = os.path.join(base_dir, 'maps')
        with open(os.path.join(map_dir, 'monster_archetype_map.json'), 'r') as f:
            object_mapping = json.load(f)

        with open(os.path.join(base_dir, "output.txt"), 'w', encoding='utf-8') as of:
            of.write("Starting output file.")

            for block in blocks:
                if not block.monsterArchetype or block.monsterArchetype == "":
                    handle = block.handle.lower() if block.handle else ""
                    of.write(f"\n\nCurrent handle = {handle}")
                    matched_archetypes = []

                    for archetype in object_mapping.keys():
                        of.write(f"\nCurrent archetype = {archetype.lower()}")
                        of.write(f"\n{archetype.lower()} in {handle.lower()}? = {archetype.lower() in handle.lower()}")
                        if archetype.lower() in handle.lower():
                            # For single-word archetypes with oneWordMatch=True
                            if object_mapping[archetype].get('oneWordMatch', False):
                                matched_archetypes.append(archetype)
                                of.write(f"\nAppending {archetype} to matched_archetypes (oneWordMatch).")
                            # For multi-word archetypes (contain space or underscore) - match as substring
                            elif ' ' in archetype or '_' in archetype:
                                matched_archetypes.append(archetype)
                                of.write(f"\nAppending {archetype} to matched_archetypes (multi-word substring).")
                            # For word-boundary matching when useLongerMatches=True
                            elif object_mapping[archetype].get('useLongerMatches', False):
                                eachWordOfHandle = re.split(r'[_\s]+', handle)
                                if any(word == archetype.lower() for word in eachWordOfHandle):
                                    matched_archetypes.append(archetype)
                                    of.write(f"\nAppending {archetype} to matched_archetypes (useLongerMatches).")

                    if len(matched_archetypes) > 1:
                        count = 0
                        of.write(f"\nMultiple monster archetype matches found for {block.full_guid}: {matched_archetypes}.")
                        for archetype in matched_archetypes:
                            useLongerMatches = object_mapping[archetype].get('useLongerMatches', False)
                            if useLongerMatches:
                                continue
                            else:
                                block.monsterArchetype = archetype.title()
                                break
                                
                    elif len(matched_archetypes) == 1:
                        block.monsterArchetype = matched_archetypes[0]

            of.close()

        
    @staticmethod
    def update_subtype_based_on_notes(blocks):
        base_dir = os.path.dirname(__file__)
        map_dir = os.path.join(base_dir, 'maps')
        with open(os.path.join(map_dir, 'subtype_map.json'), 'r') as f:
            substring_mapping = json.load(f)
        mapped_substrings = discoverFields._flatten_mapping_values(substring_mapping)

        for block in blocks:
            if not block.subtype or block.subtype == "":
                notes_lower = block.notes.lower() if block.notes else ""
                handle = block.handle.lower() if block.handle else ""
                full_guid = block.full_guid.lower() if block.full_guid else ""

                notes_lower_match = False
                handle_match = False
                full_guid_match = False

                if any(discoverFields._matches_with_rules(notes_lower, sub) for sub in mapped_substrings):
                    notes_lower_match = True
                if any(discoverFields._matches_with_rules(handle, sub) for sub in mapped_substrings):
                    handle_match = True
                if any(discoverFields._matches_with_rules(full_guid, sub) for sub in mapped_substrings):
                    full_guid_match = True

                matched_subtypes = []

                if handle_match:
                    for subtype, substrings in substring_mapping.items():
                        if any(discoverFields._matches_with_rules(handle, sub) for sub in substrings):
                            matched_subtypes.append(subtype.title())

                elif notes_lower_match:
                    for subtype, substrings in substring_mapping.items():
                        if any(discoverFields._matches_with_rules(notes_lower, sub) for sub in substrings):
                            matched_subtypes.append(subtype.title())

                elif full_guid_match:
                    for subtype, substrings in substring_mapping.items():
                        if any(discoverFields._matches_with_rules(full_guid, sub) for sub in substrings):
                            matched_subtypes.append(subtype.title())

                matched_subtypes = list(set(matched_subtypes))  # Remove duplicates

                if len(matched_subtypes) == 0:
                    continue
                elif len(matched_subtypes) == 1:
                    block.subtype = matched_subtypes[0]
                else:
                    print(f"Multiple subtype matches found for {block.full_guid}: {matched_subtypes}. Setting subtype to 'Multiple'.")
                    block.subtype = f"Multiple: {', '.join(matched_subtypes)}"


    @staticmethod
    def update_type_based_on_notes(blocks):
        base_dir = os.path.dirname(__file__)
        map_dir = os.path.join(base_dir, 'maps')
        with open(os.path.join(map_dir, 'type_map.json'), 'r') as f:
            substring_mapping = json.load(f)
        mapped_substrings = discoverFields._flatten_mapping_values(substring_mapping)

        for block in blocks:
            if hasattr(block, 'type') and block.type not in ["Aberration", "Beast", "Celestial", "Construct", "Dragon", "Elemental", "Fey", "Fiend", "Giant", "Humanoid", "Monstrosity", "Ooze", "Plant", "Undead"]:
                block.type = ""
        
        for block in blocks:
            notes_lower = block.notes.lower() if block.notes else ""
            handle = block.handle.lower() if block.handle else ""
            subtype = block.subtype.lower() if block.subtype else ""

            notes_lower_match = False
            handle_match = False
            subtype_match = False

            if any(discoverFields._matches_with_rules(notes_lower, sub) for sub in mapped_substrings):
                notes_lower_match = True
            if any(discoverFields._matches_with_rules(handle, sub) for sub in mapped_substrings):
                handle_match = True
            if (any(discoverFields._matches_with_rules(subtype, sub) for sub in mapped_substrings)):
                subtype_match = True

            matched_types = []

            if handle_match:
                for type_, substrings in substring_mapping.items():
                    if any(discoverFields._matches_with_rules(handle, sub) for sub in substrings):
                        matched_types.append(type_.title())

            if notes_lower_match:
                for type_, substrings in substring_mapping.items():
                    if any(discoverFields._matches_with_rules(notes_lower, sub) for sub in substrings):
                        matched_types.append(type_.title())

            if subtype_match:
                for type_, substrings in substring_mapping.items():
                    if any(discoverFields._matches_with_rules(subtype, sub) for sub in substrings):
                        matched_types.append(type_.title())

            matched_types = list(set(matched_types))  # Remove duplicates

            if len(matched_types) == 0:
                continue
            elif len(matched_types) == 1:
                block.type = matched_types[0]
            else:
                print(f"Multiple type matches found for {block.full_guid}: {matched_types}. Setting type to 'Multiple'.")
                block.type = f"Multiple: {', '.join(matched_types)}"

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    blocks = MonsterStatBlock.load_from_json_file(os.path.join(base_dir, 'guid_mapper_master.json'))
    blocks = MonsterStatBlock.deduplicate(blocks)

    # Toggle on if you want to quickly populate new fields based on existing notes
    # discoverFields.update_subtype_based_on_notes(blocks)    
    # discoverFields.update_type_based_on_notes(blocks)
    # discoverFields.update_class_archetype_based_on_notes(blocks)
    discoverFields.update_monster_archetype_based_on_handle(blocks)

    MonsterStatBlock.save_to_json_file(blocks, os.path.join(os.path.dirname(__file__), 'guid_mapper_master_discoveredFields.json'))
