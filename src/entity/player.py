from ..items.items import Killed, Destroyed, Free, SetBomb, Shovel

class Player():

    def __init__(self):
        super().__init__()

        self.symbol: str = "@"
        self.possible_moves: dict[ str: tuple[int, int]] = { "d": (1, 0), "a": (-1, 0), "w": (0, -1), "s": (0, 1) }
        self._items = []
        self._score: int = 0
        self._step_count: int = 0
        self._step_free: int = 0
        self._old_pos: dict = {}
        self._starter_grid = (0, 0)
        self.can_be_destoyed = True
        self.alive = (True, "")


    # Limit starter
    @property
    def limit_grid(self) -> list:
        return self._starter_grid


    # Items
    @property
    def items(self) -> list:
        return self._items
    
    def remove_item(self, index: int):
        return self._items.pop(index)

    @property
    def inventory(self):
        return [_item.name for _item in self.items]
    

    # Score
    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, point):
        
        if self.score == 0 and point > 0:
            self._score += point
        
        elif self.score > 0:
            self._score += point
    
    @score.deleter
    def score(self):
        if self.free_steps == 0 and self.score > 0:
            self._score -= 1
    
    
    # Steps
    @property
    def steps(self):
        return self._step_count
    
    
    @steps.setter
    def steps(self, _):
        self._step_count += 1
    
    
    # Free steps
    @property
    def free_steps(self):
        return self._step_free

    @free_steps.setter
    def free_steps(self, nr_of_steps: int):
        self._step_free += nr_of_steps
    
    @free_steps.deleter
    def free_steps(self):
        if self.free_steps > 0:
            self._step_free -= 1


    # Old position
    @property
    def old_pos(self):
        return self._old_pos
    

    def add_old_pos(self, _pos, _item):
        self._old_pos = {"pos": _pos, "item": _item}



    # Add an item to the playes inventory if it does not already exists
    def add_player_items(self, item):
        
        if item.is_inventory:
            
            _add_item = True
            
            for _items in self.items:
                if _items.name == item.name:
                    _add_item = False
                    break
            
            if _add_item:
                self._items.append(item)
                return item.name

        return None
    
    # Remove something specific
    def remove_player_specific_items(self, item, a_class):
        """
        Remove a specific item and class from the players inventory
        """
        if item in self.inventory:
            inventory_remove_index = [i for i, class_item in enumerate(self.items) if item == class_item.name and isinstance(class_item, a_class)][0]
            
            return self.remove_item(inventory_remove_index) 


    # Remove an items of a specic class food, shovel, bombs, ...
    def remove_player_any_item(self, a_class):
        """
        Remove a item of a specific class from the players inventory
        """
        items = []
        
        for item in self.items:
            if isinstance(item, a_class):
                items.append(item)
            
        if items:
            return self.remove_player_specific_items(items[0].name, a_class)

        else:
            return None

    # Players inventory looking nice
    def get_player_inventory(self):
        
        s_inventory = " > Inventory:\n"
        _inventory = self.inventory
        
        if len(_inventory) == 0:
            s_inventory += "   -- Nothing --\n"
            
        else: 
            for _item in _inventory:
                s_inventory += f"    * {_item.title()}\n"
            
        return s_inventory


    # When the player does a move making sure that is is valid
    def next_move(self, g, move, jump, m):

        player_movement: list[tuple[int, int]] = g.get_path(self, move)
        player_current_pos = player_movement[0]
        
        player_next_pos = player_current_pos
        player_prev_pos = player_current_pos
        
        for player_next_pos in player_movement[1:]:
            
            # If the tile is blocked (Border Wall) '<item>.block = True' 
            if g.board[player_next_pos].block:
                player_next_pos = player_prev_pos
                self.remove_player_specific_items("shovel", Shovel)

            # Tile is not crossable for the Player but Player has the shovel
            elif not g.board[player_next_pos].cross and "shovel" in self.inventory:
                
                if isinstance(g.board[player_next_pos], type(m)):
                    g.board[player_next_pos] = m.dies("shovel")
                    
                    #monster_appears = self.steps + monster_appears // 2
                    
                if player_next_pos == player_movement[-1] or jump:
                    break
                
                else:
                    player_prev_pos = player_next_pos
                    continue
            
            # Tile is not crossable for Player (Fence) '<item>.cross = False' 
            elif not g.board[player_next_pos].cross:
                player_next_pos = player_prev_pos

            else:
                player_prev_pos = player_next_pos
                continue
    
            break

        return player_next_pos, player_current_pos
    


    # What happend to the Player doring a valid move
    def action(self, g, next_pos, fence_names):
        player_message = ""

        player_tile = g.board[next_pos]

        replace_item = Free()
    
        # Check if the tiles need to remain as something else
        if isinstance(player_tile, Killed):
            replace_item = Killed()
        
        elif isinstance(player_tile, Destroyed):
            replace_item = Destroyed()

        # Steps
        self.steps = 1
        del(self.score)
        del(self.free_steps)
        
        # If the tile has something on it that we need to react to
        if not isinstance(player_tile, Free):
                
            if (type(player_tile).__name__).lower() in fence_names:
                replace_item = Destroyed()
            
            # Perhaps we are able to pickup the item that is a tile
            message = self.add_player_items(player_tile)
            
            if message != None:
                player_message = f" > Found: {message.title()}"
            
            # And any points from the tile
            item_points = player_tile.item_points()
            
            if item_points > 0:
                    self.score = item_points
                    self.free_steps = 5

            
        # Move the player
        g.move_position(self, next_pos, replace_item)

        # If player stepped on the bomb
        if isinstance(player_tile, SetBomb):
            g.bomb_detonate(next_pos, player_tile)

        return player_message
    

    # When the player dies (very simple)
    def dies(self, reason):
        
        if reason == "bomb":
            message = " > Player was killed by a Bomb!"
            
        elif reason == "monster":
            message = " > Player was killed by the Monster!"

        elif reason == "steponbomb":
            message = " > Player stepped on the Bomb and was killed!"
            
        else:
            message = " > Player was killed by something!"
            
        self.alive = False, message
            
        return Killed()