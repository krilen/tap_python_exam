import random
from .items import *

class Grid:
    """
    Representerar spelplanen. Du kan ändra standardstorleken och tecknen för olika rutor.
    """
    #width = 36
    #height = 12
    #item_empty = "."  # Tecken för en tom ruta
    #wall = "■"   # Tecken för en ogenomtränglig vägg

    def __init__(self, width, height):
        """
        Skapa ett objekt av klassen Grid
        """
        self.width = width
        self.height = height
        self.items = []
        
        self.board = {}
        
        for y in range(0, self.height):
            for x in range(0, self.width):
                
                self.board.update({ (x, y): None })


    #def get(self, pos):
    #    """
    #    Hämta det som finns på en viss position
    #    """
    #    #return self.data[y][x]
    #    return self.board[pos]


    #def set(self, pos, value):
    #    """
    #    Ändra vad som finns på en viss position
    #    """
    #    self.board[pos] = value
        
        

    #def set_player(self, player):
    #    self.player = player
        

    #def clear(self, pos):
    #    """
    #    Ta bort item från position
    #    """
    #    self.set(pos, " .")
        

    # Creates the bord with all its content
    def __str__(self):
        """
        Creates the board and its contents
        """
        _board = ""
        
        for y in range(0, self.height):
            for x in range(0, self.width):
                _item = self.board[(x, y)]
                
                if _item == None:
                    _board += "."
                    
                else:
                    _board += _item.symbol
                
            _board += "\n"
        return _board



    def make_walls(self):
        """
        Creates the wall perimeter
        """
        for tile in self.board:
            (_x, _y) = tile
            
            if _x == 0 or _y == 0  or _x == self.width -1 or _y == self.height -1:
                wall = Wall()
                
                self.board[tile] = Wall()


    def add_player(self, p):
        """
        Add the player to a random position in the middle of the board 
        """    
        while True:
            _pos = (self.width // 2 + random.randint(-2, 2)), (self.height // 2 + random.randint(-1, 1))
            
            if self.board[_pos] == None:
                self.board[_pos] = p
                break


    def calc_position(self, move, item):
        
        current_item_pos = list({k: v for (k, v) in self.board.items() if v == item}.keys())
        
        old_item_pos_x = current_item_pos[0][0]
        old_item_pos_y = current_item_pos[0][1]
        
        new_item_pos_x = old_item_pos_x + move[0]
        new_item_pos_y = old_item_pos_y + move[1]
        
        return (new_item_pos_x, new_item_pos_y), (old_item_pos_x, old_item_pos_y)
        
        
    def check_position(self, pos):
        
        item = self.board[pos]
        
        if item == None:
            return True
        
        else:
            return item.cross
        
        
    def move_position(self, new_pos, old_pos):
        
        _tmp_old = self.board[old_pos]
        self.board[old_pos] = None
        self.board[new_pos] = _tmp_old
        
        
    def set_pickup(self, pickups):
        
        for pickup in pickups:
            while True:
                _check_pos = random.randint(1, self.width -2), random.randint(1, self.height -2)
                                
                if self.board[_check_pos] == None:
                    self.board[_check_pos] = Pickup(pickup)
                    break
            
        
    # Används i filen pickups.py
    #def get_random_x(self):
    #    """Slumpa en x-position på spelplanen"""
    #    return random.randint(0, self.width-1)

    #def get_random_y(self):
    #    """Slumpa en y-position på spelplanen"""
    #    return random.randint(0, self.height-1)


    #def is_empty(self, x, y):
    #    """Returnerar True om det inte finns något på aktuell ruta"""
    #   return self.get(x, y) == self.empty

