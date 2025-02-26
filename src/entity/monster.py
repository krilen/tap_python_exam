from ..items.items import *
import random

class Monster(Item):
    
    def __init__(self):
        super().__init__()
        
        self._old_pos: dict = {}
        self.symbol: str = "#"
        self.points = 300
        self.cross = False
        self.possible_moves: list[tuple[int, int]] = [(2, 0), (-2, 0), (0, -2), (0, 2)]
        self.move_rate = 1
        self.alive = (True, "")


    # Old position
    @property
    def old_pos(self):
        return self._old_pos
    
    
    

    def add_old_pos(self, _pos, _item):
        self._old_pos = {"pos": _pos, "item": _item}
        
        
        
    def dies(self, reason):
        
        if reason == "shovel":
            message = " > Player killed the Monster with the Shovel!"
            
        elif reason == "bomb":
            message = " > Player killed the Monster with a Bomb!"
            
        else:
            message = " > Monster was killed!"
            
        self.alive = False, message
    
        return Killed()
    
    
    
    def should_move(self):
        
        if random.randint(0, 9) < self.move_rate:
            return False
        
        else:
            return True
