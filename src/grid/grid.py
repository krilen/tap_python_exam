from .griditems import GridItems
from .gridborder import GridBorder
from .gridfences import GridFences

from ..entity.player import Player
from ..items.items import Item, Free, PlayerExit, FenceHorizontal, FenceVertical, FenceIntersect, Fence, BorderWall

import random
from typing import Any



class Grid(GridItems, GridBorder, GridFences):

    def __init__(self, width, height):
        """
        Create an instance of Grid and also call GridFence and GridBorder
        """
        super().__init__() 
        
        self.width = width
        self.height = height
        self.items = []
        
        self.board = {}
        
        for y in range(0, self.height):
            for x in range(0, self.width):
                
                self.board.update({ (x, y): Free() })


    # Displays the board with all its content
    def __str__(self):
        """
        Displays the board and its contents
        """
        _board = ""
        
        for y in range(0, self.height):
            _board += " "
            for x in range(0, self.width):
                _item = self.board[(x, y)]

                _board += _item.symbol
                
            _board += "\n"
        return _board


    def add_entity(self, entity, limit: tuple[int, int]=(0, 0)):
        """
        Add the player to a random position somewhere in the middle of the board 
        """
        
        # Limit defines an area where the entity should randomly start
        _start_pos_x_min = 1 + limit[0]
        _start_pos_x_max = self.width - limit[0] -2
        _start_pos_y_min = 1 + limit[1]
        _start_pos_y_max = self.height - limit[1] -2
        
        
        while True:
            _pos = random.randint(_start_pos_x_min, _start_pos_x_max), random.randint(_start_pos_y_min, _start_pos_y_max)

            if isinstance(self.board[_pos], Free):
                
                self.board[_pos] = entity
                entity.add_old_pos(_pos, Free())
                break


    def get_path(self, entity: type[Any], move: tuple[int, int]) -> list[tuple[int, int]]:
        """
        A method that calculates the path from a position using a move (not end_pos)
        
        Ex pos: (2,4) move: (3,2) => path: [(2, 4), (3, 4), (3, 5), (4, 5), (4, 6), (5, 6)]
           The first element in the path list is the current position
           The last elment is the end position ((2,4) + (3,2) = (5,6))
           And everything between is the path that you should take
        """
        positions: list[tuple[int, int]] = []
        
        _pos = self.find_all_items(type(entity))[0] # Only one player exists
        positions.append(_pos) 
        
        _end_pos = _pos[0] + move[0], _pos[1] + move[1] # calculatedd en position
        
        if 0 <= _end_pos[0] < self.width and 0 <= _end_pos[1] < self.height:
        
            # Get the path to the end
            while not positions[-1] == _end_pos:
                _new_pos = ()
                _diff_pos_x, _diff_pos_y = self.path_diff(positions[-1], _end_pos)
            
                if abs(_diff_pos_x) > abs(_diff_pos_y):
                    if _diff_pos_x < 0:
                        _move_x = 1
                    else:
                        _move_x = -1
                        
                    _move_pos = _move_x, 0
                    
                else:
                    if _diff_pos_y < 0:
                        _move_y = 1
                    else:
                        _move_y = -1
                        
                    _move_pos = 0, _move_y
                
                _new_pos = positions[-1][0] + _move_pos[0], positions[-1][1] + _move_pos[1]
                positions.append(_new_pos)
        
        return positions
    
    
    def path_diff(self, pos1: tuple[int, int], pos2: tuple[int, int]) -> tuple[int, int]:
        """
        Get the difference between to positions
        """
        return (pos1[0] - pos2[0]), (pos1[1] - pos2[1])
    
    
    def move_position(self, entity, new_pos, _item=Free()):
        
        # First lets get what happended before on this tile
        saved_pos = entity.old_pos
        _old_pos = saved_pos["pos"]
        _old_item = saved_pos["item"]
        
        # Lets make sure that player are not at "Exit" and want to exit the game
        if isinstance(self.board[new_pos], PlayerExit) and isinstance(entity, Player):
            entity.alive = (False, " > Player went home!")

        # Save what has happened on this tile before we move
        entity.add_old_pos(new_pos, _item)
        
        # Lets write the changes to the board
        _tmp_copy = self.board[_old_pos]
        self.board[_old_pos] = _old_item
        self.board[new_pos] = _tmp_copy
        
    
    def check_walkthrough(self, p):
        """
        Verifying that you can reach all tiles on the board.
        Except border walls and fences
        """
        checked_pos = [] # pos that have been checked
        to_check_pos = [] # pos to be checked
        to_check_pos.append(self.find_all_items(p)[0]) # Start at the player pos
        
        _items_not_to_check: tuple[type[Item]] = (FenceHorizontal, FenceVertical, FenceIntersect, Fence, BorderWall)
        
        moves = [(1, 0), (-1, 0), (0, -1), (0, 1)] # Allowed movements
                           
        # Positions to be checked
        while to_check_pos:
            # The current pos to be checked
            check_pos = to_check_pos.pop(0)
            
            for move in moves:
                _pos_next_x = check_pos[0] + move[0]
                _pos_next_y = check_pos[1] + move[1]
                
                _pos_next = _pos_next_x, _pos_next_y
                
                # Make sure that the next_pos has not been checked or about to be checked
                if _pos_next not in checked_pos and _pos_next not in to_check_pos:
                    # Make sure that the pos is not a border or fence
                    if not isinstance(self.board[_pos_next], _items_not_to_check):
                        to_check_pos.append(_pos_next)
                        
            checked_pos.append(check_pos)

        # Nothing more to check but needs to verify that all items are there
        valid_positions = {k for (k, v) in self.board.items() if not isinstance(v, _items_not_to_check)}
        if set(checked_pos) == valid_positions:
            return True

        return False


