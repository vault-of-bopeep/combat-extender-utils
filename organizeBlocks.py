"""
organizeBlocks.py

Utilities for ordering block output without changing block field values.
"""

import os

from monsterStatBlock import MonsterStatBlock

class organizeBlocks:

    @staticmethod
    def _location_sort_key(location, full_guid=""):
        """Return a sort key tuple for Location based on LOCATION_ORDER.

        If the Location field itself does not start with any known prefix, the
        FullGuid is checked next. That lets the S_* ordering list work for
        blocks whose Location is an actual location name.
        """
        location = "" if location is None else str(location)
        full_guid = "" if full_guid is None else str(full_guid)

        for index, prefix in enumerate(organizeBlocks.get_location_order()):
            if location.startswith(prefix):
                return index, location
        for index, prefix in enumerate(organizeBlocks.get_location_order()):
            if full_guid.startswith(prefix):
                return index, full_guid
        return len(organizeBlocks.get_location_order()), location or full_guid

    @staticmethod
    def _get_block_field(block, field_name):
        if isinstance(block, dict):
            return block.get(field_name, "")
        return getattr(block, field_name.lower(), "")

    @staticmethod
    def sort_blocks_by_location(blocks):
        """Sort blocks by the LOCATION_ORDER list without changing any field values."""
        return sorted(blocks, key=lambda block: organizeBlocks._location_sort_key(organizeBlocks._get_block_field(block, "Location")))


    @staticmethod
    def sort_blocks_by_fields(blocks, field_order=None):
        """Sort blocks by a progressive list of fields.

        The default field order is Location, Type, ClassArchetype, Handle.
        """
        if field_order is None:
            field_order = organizeBlocks.get_field_order()

        def block_key(block):
            key = []
            for field_name in field_order:
                if field_name == "Location":
                    key.append(
                        organizeBlocks._location_sort_key(
                            organizeBlocks._get_block_field(block, field_name),
                            organizeBlocks._get_block_field(block, "FullGuid")
                        )
                    )
                else:
                    value = organizeBlocks._get_block_field(block, field_name)
                    key.append("" if value is None else str(value))
            return tuple(key)

        return sorted(blocks, key=block_key)


    @staticmethod
    def reorder_blocks(blocks):
        """Alias to sort blocks by the default multi-field order."""
        return organizeBlocks.sort_blocks_by_fields(blocks)

    @staticmethod
    def get_location_order():
        """Return the current LOCATION_ORDER list."""
        return [
            "S_GLO_",
            "S_CAMP_",
            "S_ORI_",
            "S_SCE_",
            "S_OriginIntro_",
            "S_FirstFight_",
            "S_TUT_",
            "S_CRA_",
            "S_CHA_",
            "S_FOR_",
            "S_DEN_",
            "S_HAG_",
            "S_GOB_",
            "S_PLA_",
            "S_UND_",
            "S_CRE_",
            "S_SCL_",
            "S_HAV_",
            "S_TWN_",
            "S_SHA_",
            "S_MOO_",
            "S_COL_",
            "S_INT_",
            "S_WYR_",
            "S_LOW_",
            "S_IRN_",
            "S_END_",
            ""
        ]

    @staticmethod
    def get_field_order():
        """Return the current FIELD_ORDER list."""
        return ["Act", "Location", "Type", "ClassArchetype", "Handle"]

if __name__ == "__main__":
    # Load the stat blocks from 'guid_mapper_master.json'
    base_dir = os.path.dirname(__file__)
    clean_blocks = MonsterStatBlock.load_from_json_file(os.path.join(base_dir, 'guid_mapper_master.json'))
    MonsterStatBlock.populate_full_guid(clean_blocks)
    MonsterStatBlock.deduplicate(clean_blocks)

    organizeBlocks.reorder_blocks(clean_blocks)
    MonsterStatBlock.save_to_json_file(clean_blocks, os.path.join(base_dir, 'guid_mapper_master_organized.json'))