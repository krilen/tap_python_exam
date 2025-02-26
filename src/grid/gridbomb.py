from ..items.items import SetBomb, Destroyed

class GridBomb():
    
    def __init__(self):
        pass
    
    
    def bomb_set(self, p):
        
        _player_bombs = [b for b in p.items if b.is_bomb]
        
        if not _player_bombs:
            return "", None # No bombs to place
        
        _bomb = _player_bombs[0]
        _player_pos = self.find_all_items(type(p))[0]
        
        p.remove_player_specific_items(_bomb.name, type(_bomb))
        
        new_bomb = {"name": _bomb.name, 
                    "exec_time": p.steps +3, 
                    "exec_func": self.bomb_detonate, 
                    "position": _player_pos, 
                    "item": SetBomb()
                    }
        
        return _bomb.name, new_bomb
    
    
    def bomb_detonate(self, bomb_pos, bomb_item):
        
        if isinstance(self.board[bomb_pos], type(bomb_item)):
            
            bomb_pos_x = bomb_pos[0]
            bomb_pos_y = bomb_pos[1]
            
            _bomb_affected_all_pos = [(bomb_pos_x -1, bomb_pos_y -1),
                                      (bomb_pos_x, bomb_pos_y -1),
                                      (bomb_pos_x +1, bomb_pos_y -1),
                                      (bomb_pos_x -1, bomb_pos_y),
                                      bomb_pos,
                                      (bomb_pos_x +1, bomb_pos_y),
                                      (bomb_pos_x -1, bomb_pos_y +1),
                                      (bomb_pos_x, bomb_pos_y +1),
                                   (bomb_pos_x +1, bomb_pos_y +1)]
            
            for _bomb_affected_pos in _bomb_affected_all_pos:
                
                if (0 <= _bomb_affected_pos[0] < self.width -1 and 
                     0 <= _bomb_affected_pos[1] < self.height -1):
                   
                    # Something may die                    
                    try:
                        _replace_item = self.board[_bomb_affected_pos].dies("bomb")
                        
                    except:
                        game_continue = True
                        message = ""
                        replace_item = Destroyed()
                        
                    else:
                        replace_item = _replace_item
                    
                    finally:
                        
                        #if not game_continue and hasattr(self.board[_bomb_affected_pos], "alive"):
                        #    self.board[_bomb_affected_pos].alive = (False, message)

                        if self.board[_bomb_affected_pos].can_be_destoyed:
                            self.board[_bomb_affected_pos] = replace_item
