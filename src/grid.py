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
                
                self.board.update({ (x, y): {"symbol": ".", "item": None} })


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
        Creates the board and its content
        """
        _board = ""
        
        for y in range(0, self.height):
            
            for x in range(0, self.width):
                
                _board += self.board[(x, y)]["symbol"]
                
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
                
                self.board[tile]["symbol"] = wall.symbol
                self.board[tile]["item"] = wall

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

