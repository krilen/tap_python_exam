

class Player():

    def __init__(self):
        super().__init__()

        self.symbol = "@"    
        self.possible_moves = { "d": (1, 0), "a": (-1, 0), "w": (0, -1), "s": (0, 1) }
        self._items = []
        self._score = 0
        self._step_count = 1
        self._step_free = 0
        self._old_pos = {}

        
    @property
    def items(self):
        return self._items
    
    def remove_item(self, index):
        self._items.pop(index)
    
    def add_player_items(self, item):
        
        if item.item_inventory:
            
            _add_item = True
            
            for _items in self.items:
                if _items.name == item.name:
                    _add_item = False
                    break
            
            if _add_item:
                self._items.append(item)
                return True
            
        return False
    
    
    def remove_player_items(self, item, a_class):
        """
        Remove an item from the players inventory
        """

        if item in self.inventory:
            inventory_remove_index = [i for i, class_item in enumerate(self.items) if item == class_item.name and isinstance(class_item, a_class)][0]
            self.remove_item(inventory_remove_index) 
        
        
            
            
    @property
    def inventory(self):
        return [_item.name for _item in self.items]
    
        
    @property
    def score(self):
        return self._score


    @score.setter
    def score(self, point):
        
        if self._score == 0 and point > 0:
            self._score += point +1
        
        elif self._score > 0:
            self._score += point
            
    @property
    def steps(self):
        return self._step_count
    
    
    @steps.setter
    def steps(self, _):
        self._step_count += 1
    
    
    @property
    def old_pos(self):
        return self._old_pos
    

    def add_old_pos(self, _pos, _item):
        self._old_pos = {"pos": _pos, "item": _item}
        
    

    
            
    def __str__(self):
        
        
        s_inventory = "\nPlayers inventory:\n"
        
        _inventory = self.inventory
        
        if len(_inventory) == 0:
            s_inventory += "-- Nothing --\n"
            
        else: 
        
            for _item in _inventory:
                
                s_inventory += f" * {_item.title()}\n"
            
        return s_inventory
    
    
    
