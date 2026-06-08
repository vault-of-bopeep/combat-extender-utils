import json
from operator import contains
import os

from monsterStatBlock import MonsterStatBlock

class alterStatistics:

    @staticmethod
    def add_by_handle(blocks, handle_match_phrase, passives_to_add=None, spells_to_add=None):
        for block in blocks:
            if handle_match_phrase in block.handle:
                if passives_to_add is not None:
                    if not hasattr(block, 'PassivesToAdd') or block.passives_to_add is None:
                        block.passives_to_add = []
                    block.passives_to_add.extend(passives_to_add)
                if spells_to_add is not None:
                    if not hasattr(block, 'SpellsToAdd') or block.spells_to_add is None:
                        block.spells_to_add = []
                    block.spells_to_add.extend(spells_to_add)
    
    @staticmethod
    def add_by_full_guid(blocks, full_guid_match_phrase, passives_to_add=None, spells_to_add=None):
        for block in blocks:
            if block.full_guid and full_guid_match_phrase in block.full_guid:
                if passives_to_add is not None:
                    if not hasattr(block, 'PassivesToAdd') or block.passives_to_add is None:
                        block.passives_to_add = []
                    block.passives_to_add.extend(passives_to_add)
                if spells_to_add is not None:
                    if not hasattr(block, 'SpellsToAdd') or block.spells_to_add is None:
                        block.spells_to_add = []
                    block.spells_to_add.extend(spells_to_add)

    @staticmethod
    def set_health_override_by_full_guid(blocks, full_guid_match_phrase, health_override_value):
        for block in blocks:
            if block.full_guid and full_guid_match_phrase in block.full_guid:
                block.health_override = health_override_value
    
    @staticmethod
    def set_health_override_by_handle(blocks, handle_match_phrase, health_override_value):
        for block in blocks:
            if handle_match_phrase in block.handle:
                block.health_override = health_override_value

    @staticmethod
    def add_location_by_guid(blocks, guid_match_phrase, location):
        """Add/replace Location for all blocks matching a guid phrase. Do not append or replace to an existing Location value.
        
        Args:
            blocks: List of MonsterStatBlock objects
            guid_match_phrase: String to search for in full_guid
            location: New location to set (typically a key from location_map.json)
        """
        for block in blocks:
            if hasattr(block, 'full_guid') and block.full_guid and guid_match_phrase in block.full_guid:
                block.location = location

    @staticmethod
    def replace_location_by_phrase(blocks, location_match_phrase, new_location):
        """Replace Location field for blocks where location contains the match phrase.
        Replaces the entire Location value, not just the phrase.
        
        Args:
            blocks: List of MonsterStatBlock objects
            location_match_phrase: String to search for in location field
            new_location: New location value to replace with
        """
        for block in blocks:
            if hasattr(block, 'location') and block.location and location_match_phrase in block.location:
                block.location = new_location

    @staticmethod
    def update_locations_from_map(blocks, location_map):
        """Update all Location fields based on location_map.json key-value pairs.
        
        For each location value in location_map, if a block's Location matches that value,
        replace it with the corresponding key. For example, NAUTILOID_CRASHED_3 becomes NAUTILOID_CRASHED
        because NAUTILOID_CRASHED_3 is in the values list for the NAUTILOID_CRASHED key.
        
        Args:
            blocks: List of MonsterStatBlock objects
            location_map: Dictionary loaded from location_map.json
        """
        for block in blocks:
            if hasattr(block, 'location') and block.location:
                for key, values in location_map.items():
                    if block.location in values:
                        block.location = key
                        break

if __name__ == "__main__":
    # Load the stat blocks from 'guid_mapper_master.json'
    base_dir = os.path.dirname(__file__)
    blocks = MonsterStatBlock.load_from_json_file(os.path.join(base_dir, 'guid_mapper_master.json'))

    alterStatistics.set_health_override_by_full_guid(blocks, "S_INT_GithRoyalGuard", 60)

        # Load location_map.json
    with open(os.path.join(base_dir, 'maps', 'location_map.json'), 'r', encoding='utf-8') as f:
        location_map = json.load(f)

    alterStatistics.

    # Save the updated blocks to a new JSON file
    MonsterStatBlock.save_to_json_file(blocks, os.path.join(base_dir, 'guid_mapper_master_alteredStats.json'))