import random
from .items import *
from typing import Any

class Grid:
    """
    Representerar spelplanen. Du kan ändra standardstorleken och tecknen för olika rutor.
    """
    def __init__(self, width, height):
        """
        Skapa ett objekt av klassen Gridmax_size
        """
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
            for x in range(0, self.width):
                _item = self.board[(x, y)]

                _board += _item.symbol
                
            _board += "\n"
        return _board


    # Adds the border wall that you can not get pass
    def add_border_walls(self):
        """
        Creates the border wall and the perimeter of the game
        They can not be destoyed
        """
        for tile in self.board:
            (_x, _y) = tile
            
            if _x == 0 or _y == 0  or _x == self.width -1 or _y == self.height -1:
                self.board[tile] = BorderWall()





    def add_player(self, p):
        """
        Add the player to a random position somewhere in the middle of the board 
        """    
        while True:
            _pos = (self.width // 2 + random.randint(-2, 2)), (self.height // 2 + random.randint(-1, 1))

            if isinstance(self.board[_pos], Free):
                
                self.board[_pos] = p
                p.add_old_pos(_pos, Free())
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
        
        _end_pos = _pos[0] + move[0], _pos[1] + move[1] # calculated en position
        
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
    
    
    def path_diff(self, from_pos: tuple[int, int], to_pos: tuple[int, int]) -> tuple[int, int]:
        """
        Get the difference between to positions
        """
        return (from_pos[0] - to_pos[0]), (from_pos[1] - to_pos[1])
    
    
    #def move(self, entity, )
    

        
    def move_position(self, entity, new_pos, _item=Free()):
        
        # First lets get what happended before on this tile
        saved_pos = entity.old_pos
        _old_pos = saved_pos["pos"]
        _old_item = saved_pos["item"]
        
        # Save what has happened on this tile before we move
        entity.add_old_pos(new_pos, _item)
        
        # Lets write the changes to the board
        _tmp_copy = self.board[_old_pos]
        self.board[_old_pos] = _old_item
        self.board[new_pos] = _tmp_copy
        
        
    def place_inventory(self, nr_to_place, inventory):
        
        inventory_keys = list({ k for (k, v) in inventory.items() })

        _have_placed = 0
        _tries = 0
            
        # To make sure that we only place unique items, no dublicates on the board
        while _have_placed < nr_to_place and _tries < len(inventory_keys):
            item_place = random.choice(inventory_keys)
            item_cls = inventory[item_place]

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
                
                
        
    def find_random_free(self, limit=0):
        
        _free_pos = list({k for (k, v) in self.board.items() if isinstance(v, Free)})
        return random.choice(_free_pos)
        
        
    # Add fences to act as random walls
    def add_fences(self, nr_of_fences, min_size, max_size):
        """
        Creates fences within the perimeter of the game by random
        They can be destoyed
        """
        r_fence = 0
        
        while r_fence < nr_of_fences:
            _fence_types = {(0, 1): FenceVertical, (0, -1): FenceVertical, (1, 0): FenceHorizontal, (-1, 0): FenceHorizontal}
            _fence_align = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            _fence_pos = random.randint(min_size, self.width -1), random.randint(min_size, self.height -1)
            _fence_size = random.randint(min_size, max_size)
            
            if _fence_align in [(1, 0), (-1, 0)]:
                _fence_size *= 2
            
            _fence_ok = True
            fence = []
            
            for _ in range(1, _fence_size +1):
                _fence_pos_x = _fence_pos[0] + _fence_align[0]
                _fence_pos_y = _fence_pos[1] + _fence_align[1]

                if not 0 < _fence_pos_x < self.width -1 or not 0 < _fence_pos_y < self.height -1:
                    _fence_ok = False
                    break
                
                _fence_pos = _fence_pos_x, _fence_pos_y
                _tile_item = self.board[_fence_pos]
                
                # Add a fench to a free tile or keep building a fench in the same direction
                if ((isinstance(_tile_item, Free)) or 
                    (isinstance(_tile_item, FenceHorizontal) and _fence_align in [(1, 0), (-1, 0)]) or 
                    (isinstance(_tile_item, FenceVertical) and _fence_align in [(0, 1), (0, -1)])):
                    fence.append({_fence_pos: _fence_types[_fence_align]()})
                    
                elif ((isinstance(_tile_item, FenceHorizontal) and _fence_align not in [(1, 0), (-1, 0)]) or 
                      (isinstance(_tile_item, FenceVertical) and _fence_align not in [(0, 1), (0, -1)])):
                    fence.append({_fence_pos: FenceIntersect()})
                    
                else:
                    _fence_ok = False
                    break
            
            # If something went wrong when building the fence lets restart
            if not _fence_ok:
                continue
            
            # Add fench to the grid
            for f in fence:
                f_pos = list(f.keys())[0]
                f_type = list(f.values())[0]
                
                self.board[f_pos] = f_type
            
            r_fence += 1


    # Find items of a certain type on the board
    def find_all_items(self, _class: type[Item]) -> list[tuple[int, int]]:
        """
        Find all the items of a certain type on the board (not instances)
        """        
        return list({k for (k, v) in self.board.items() if isinstance(v, _class)})
    
    
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


