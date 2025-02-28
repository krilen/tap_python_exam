from ..items.items import FenceHorizontal, FenceVertical, FenceIntersect, Free

import random


class GridFences():
    """
    A class that created by random fences within the Border walls. A fence can be destoyed 
    if the Player hasthe shovel or it is near when a bomb detonate. The Moster also 
    destroys a fench. 
    """
    
    def __init__(self):
        pass
    
    # Add fences to act as random walls
    def add_fences(self, nr_of_fences: int, min_size: int, max_size: int) -> None:
        """
        Method to build and add the random fences to the board
        """
        r_fence = 0
        
        while r_fence < nr_of_fences:
            _fence_types = {(0, 1): FenceVertical, (0, -1): FenceVertical, (1, 0): FenceHorizontal, (-1, 0): FenceHorizontal}
            _fence_align = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            _fence_pos = random.randint(min_size, self.width -1), random.randint(min_size, self.height -1)
            _fence_size = random.randint(min_size, max_size)
            
            # Horizontal fences a doubled in length
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