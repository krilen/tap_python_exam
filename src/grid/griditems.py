from ..items.items import PlayerExit, Item, Free
from .gridbomb import GridBomb

import random


class GridItems(GridBomb):
    """
    A Class to handle all of the Items that can exists within the board
    """
    
    def __init__(self):
        super().__init__()
    

    def set_inventory(self, nr_to_place: int, inventory: Item, player_items: Item) -> None:
        """
        Adds the inventory on the board by determin what the playes does NOT have in its inventory
        If the player has it all no new items are added.
        """
        unused_inventory = {k: v for (k, v) in inventory.items() if v not in player_items}
        inventory_keys = list({ k for k in unused_inventory.keys() })
        
        have_placed = 0
        _tries_to_place = 0
            
        # To make sure that we only place unique items, no dublicates on the board
        while have_placed < nr_to_place and _tries_to_place < len(inventory_keys):
            item_place = random.choice(inventory_keys)
            new_item = unused_inventory[item_place]

            items_found = self.find_all_items(type(new_item))
            _ok_to_place = True
            
            _tries_to_place += 1

            # Item exists but does a "sub item" exist?
            if items_found:
                for item_found in items_found:
                    if item_place == self.board[item_found].name:
                        _ok_to_place = False
                        break
             
            if not _ok_to_place:
                continue

            self.board[self.find_random_free()] = new_item

            have_placed += 1
    
    
    # Find items of a certain type on the board
    def find_all_items(self, a_class: Item) -> list[tuple[int, int]]:
        """
        Find all the items of a certain type on the board (not instances)
        """        
        return list({k for (k, v) in self.board.items() if isinstance(v, a_class)})
    
    
    # Find random free or open tile for use
    def find_random_free(self) -> tuple[int, int]:
        """
        Find a random free tile
        """
        _free_pos = list({k for (k, v) in self.board.items() if isinstance(v, Free)})
        return random.choice(_free_pos)
    
    
    def place_player_exit(self) -> None:
        """
        Place the exit for the player, a specific item
        """
        self.board[self.find_random_free()] = PlayerExit()