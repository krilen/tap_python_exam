from .items import Item

class Player(Item):
    marker = "@"

    def __init__(self):
        super().__init__()

        self.symbol = "@"    
        self.possible_moves = { "d": (1, 0), "a": (-1, 0), "w": (0, -1), "s": (0, 1) }
        self._inventory = []
        self._score = 0
        
        
    @property
    def inventory(self):
        return self._inventory
    
    
    @inventory.setter
    def inventory(self, item):
        self._inventory.append(item)
        
        
    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, point):
        
        if self._score > 0 or point > 0:
            self._score += point
            
            
    def __str__(self):
        
        inv = "\nPlayers inventory:\n"
        
        if len(self.inventory) == 0:
            inv += "-- Nothing --\n"
            
        else: 
        
            for item in self.inventory:
                inv += f"  * {item.name}\n"
            
        return inv
    
    # Flyttar spelaren. "dx" och "dy" är skillnaden
    #def move(self, dx, dy):
    #    """
    #    Flyttar spelaren.
    #     * dx = horisontell förflyttning, från vänster till höger
    #     * dy = vertikal förflyttning, uppifrån och ned
    #    """
    #    self.pos_x += dx
    #    self.pos_y += dy
    #
    #def can_move(self, x, y, grid):
    #    return True
    #    #TODO: returnera True om det inte står något i vägen

