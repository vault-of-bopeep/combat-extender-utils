import json
from operator import contains
import os

from monsterStatBlock import MonsterStatBlock

class generateDictionaries:

    @staticmethod
    def generate_clones_dict(blocks):
        clones = {}
        for block in blocks:
            if block.clone_display_name:
                clone_entry = {'DisplayName': block.clone_display_name}
                if block.clone_template_guid:
                    clone_entry['Template'] = block.clone_template_guid
                clones[block.full_guid] = clone_entry
        return clones

    @staticmethod
    def generate_overrides_dict(blocks):
        overrides = {}
        for block in blocks:
            if block.health_override or block.spells_to_add or block.passives_to_add:
                override_entry = {}
                if block.health_override is not None and block.health_override != 0:
                    override_entry['HealthOverride'] = block.health_override
                if block.spells_to_add and block.spells_to_add != []:
                    override_entry['Spells'] = block.spells_to_add
                if block.passives_to_add and block.passives_to_add != []:
                    override_entry['Passives'] = block.passives_to_add
                if override_entry:
                    overrides[block.full_guid] = override_entry
        return overrides

    @staticmethod
    def generate_clones_dict(blocks):
        clones = {}
        for block in blocks:
            if block.clone_display_name:
                clone_entry = {'DisplayName': block.clone_display_name}
                if block.clone_template_guid:
                    clone_entry['Template'] = block.clone_template_guid
                clones[block.full_guid] = clone_entry
        return clones
    
    @staticmethod
    def generate_guids_by_location_dict(blocks):
        location_dict = {}
        for block in blocks:
            loc = block.location or "Unknown"
            if loc not in location_dict:
                location_dict[loc] = []
            location_dict[loc].append({"Handle": block.handle, "Type": block.type, "Guid": block.full_guid})
        # Sort each list A-Z
        for loc in location_dict:
            location_dict[loc].sort(key=lambda x: x["Guid"])
        return location_dict
    
    @staticmethod
    def generate_guids_by_type_dict(blocks):
        type_dict = {}
        for block in blocks:
            type_ = block.type or "Unknown"
            if type_ not in type_dict:
                type_dict[type_] = []
            type_dict[type_].append({"Handle": block.handle, "Location": block.location, "Guid": block.full_guid})
        # Sort each list A-Z
        for type_ in type_dict:
            type_dict[type_].sort(key=lambda x: x["Guid"])
        return type_dict
    
    @staticmethod
    def generate_lists_of_passives_and_spells(blocks):
        passiveMasterList = []
        spellMasterList = []
        for block in blocks:
            if block.passives_to_add and isinstance(block.passives_to_add, list) and len(block.passives_to_add) > 0:
                for passive in block.passives_to_add:
                    if passive not in passiveMasterList:
                        passiveMasterList.append(passive)
            if block.spells_to_add and isinstance(block.spells_to_add, list) and len(block.spells_to_add) > 0:
                for spell in block.spells_to_add:
                    if spell not in spellMasterList:
                        spellMasterList.append(spell)
        passiveMasterList.sort()
        spellMasterList.sort()
        return passiveMasterList, spellMasterList
    
    @staticmethod
    def generate_sorted_guid_list(blocks):
        guid_list = [block.full_guid for block in blocks if block.full_guid]
        guid_list.sort()
        return guid_list

    @staticmethod
    def generate_metadata_dicts():
        # Load the stat blocks from 'guid_mapper_master.json'
        base_dir = os.path.dirname(__file__)
        metadata_dir = os.path.join(base_dir, 'metadata')
        clean_blocks = MonsterStatBlock.load_from_json_file(os.path.join(base_dir, 'guid_mapper_master.json'))
        deduped_blocks = MonsterStatBlock.deduplicate(clean_blocks)

        # Generate clones dict
        clones_dict = generateDictionaries.generate_clones_dict(deduped_blocks)
        clones_path = os.path.join(metadata_dir, 'metadata_clones.json')

        # Generate overrides dict
        overrides_dict = generateDictionaries.generate_overrides_dict(deduped_blocks)
        overrides_path = os.path.join(metadata_dir, 'metadata_overrides.json')

        # Generates a dict of locations to lists of GUIDs for each location
        location_dict = generateDictionaries.generate_guids_by_location_dict(deduped_blocks)
        location_path = os.path.join(metadata_dir, 'metadata_guids_by_location.json')

        # Generates a dict of types to lists of GUIDs for each type
        type_dict = generateDictionaries.generate_guids_by_type_dict(deduped_blocks)
        type_path = os.path.join(metadata_dir, 'metadata_guids_by_type.json')

        # Generate lists of all passives and spells that are currently in use
        passiveMasterList, spellMasterList = generateDictionaries.generate_lists_of_passives_and_spells(deduped_blocks)
        passives_spells_path = os.path.join(metadata_dir, 'metadata_passives_and_spells.json')

        # Generate sorted list of all GUIDs
        sorted_guid_list = generateDictionaries.generate_sorted_guid_list(deduped_blocks)
        sorted_guid_path = os.path.join(metadata_dir, 'metadata_sorted_guids.json')


        with open(clones_path, 'w') as f:
            json.dump(clones_dict, f, indent=4)
        print(f"Clones dict saved to {clones_path}")

        with open(overrides_path, 'w') as f:
            json.dump(overrides_dict, f, indent=4)
        print(f"Overrides dict saved to {overrides_path}")

        with open(location_path, 'w') as f:
            json.dump(location_dict, f, indent=4)
        print(f"Locations dict saved to {location_path}")

        with open(type_path, 'w') as f:
            json.dump(type_dict, f, indent=4)
        print(f"Types dict saved to {type_path}")

        with open(passives_spells_path, 'w') as f:
            json.dump({"Passives": passiveMasterList, "Spells": spellMasterList}, f, indent=4)
        print(f"Passives and Spells dict saved to {passives_spells_path}")

        with open(sorted_guid_path, 'w') as f:
            json.dump(sorted_guid_list, f, indent=4)
        print(f"Sorted GUIDs dict saved to {sorted_guid_path}")


if __name__ == "__main__":
    # Toggle on if you want to regenerate the metadata dicts from the master JSON file
    generateDictionaries.generate_metadata_dicts()