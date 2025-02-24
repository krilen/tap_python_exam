from ..items.items import *
from .gridbomb import GridBomb

import random


class GridItems(GridBomb):
    
    def __init__(self):
        super().__init__()
    

    def set_inventory(self, nr_to_place, inventory, player_items):
        unused_inventory = {k: v for (k, v) in inventory.items() if v not in player_items}
        inventory_keys = list({ k for k in unused_inventory.keys() })
        
        _have_placed = 0
        _tries = 0
            
        # To make sure that we only place unique items, no dublicates on the board
        while _have_placed < nr_to_place and _tries < len(inventory_keys):
            item_place = random.choice(inventory_keys)
            item_cls = unused_inventory[item_place]

            _items_found = self.find_all_items(type(item_cls))
            _ok_to_place = True
            
            _tries += 1

            # Item exists but does a "sub item" exist?
            if _items_found:
                for _item_found in _items_found:
                    if item_place == self.board[_item_found].name:
                        _ok_to_place = False
                        break
             
            if not _ok_to_place:
                continue

            _free_pos = self.find_random_free()
            self.board[_free_pos] = item_cls

            _have_placed += 1
    
    
    # Find items of a certain type on the board
    def find_all_items(self, _class: type[Item]) -> list[tuple[int, int]]:
        """
        Find all the items of a certain type on the board (not instances)
        """        
        return list({k for (k, v) in self.board.items() if isinstance(v, _class)})
    
    
    # Find random free or open tile for use
    def find_random_free(self):
        """
        Find a random free tile
        """
        _free_pos = list({k for (k, v) in self.board.items() if isinstance(v, Free)})
        return random.choice(_free_pos)
    
    
    def place_player_home(self):
        """
        Place the home/exit for the player
        """
        if not self.find_all_items(PlayerHome):
            self.board[self.find_random_free()] = PlayerHome()