

class Player():
    marker = "@"

    def __init__(self):
        super().__init__()

        self.symbol = "@"    
        self.possible_moves = { "d": (1, 0), "a": (-1, 0), "w": (0, -1), "s": (0, 1) }
        self._items = []
        self._score = 0
        self._step_count = 1
        self._step_free = 0
        
        
    @property
    def inventory(self):
        return [_item.name for _item in self._items if _item.item_inventory]
    
    
    @property
    def items(self):
        return self._items
    
    @items.setter
    def inventory(self, item):
        
        if item:
            self._items.append(item)
        
        
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
            
    def __str__(self):
        
        inv = "\nPlayers inventory:\n"
        
        _inventory = self.inventory
        
        if len(_inventory) == 0:
            inv += "-- Nothing --\n"
            
        else: 
        
            for item in _inventory:
                inv += f"  * {item.name.title()}\n"
            
        return inv
    
    
    
