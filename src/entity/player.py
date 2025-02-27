from ..items.items import Killed

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
    

    def remove_player_specific_items(self, item, a_class):
        """
        Remove a specific item and class from the players inventory
        """
        if item in self.inventory:
            inventory_remove_index = [i for i, class_item in enumerate(self.items) if item == class_item.name and isinstance(class_item, a_class)][0]
            
            return self.remove_item(inventory_remove_index) 


    def remove_player_any_item(self, a_class):
        """
        Remove a item of a specific class from the players inventory
        """
        
        _items = []
        
        for item in self.items:
            if isinstance(item, a_class):
                _items.append(item)
            
        if _items:
            return self.remove_player_specific_items(_items[0].name, a_class)

        else:
            return None


    def get_player_inventory(self):
        
        s_inventory = " Inventory:\n"
        _inventory = self.inventory
        
        if len(_inventory) == 0:
            s_inventory += "  -- Nothing --\n"
            
        else: 
            for _item in _inventory:
                s_inventory += f"  * {_item.title()}\n"
            
        return s_inventory
    

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