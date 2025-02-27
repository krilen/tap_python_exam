from ..items.items import SetBomb, Destroyed
from ..entity.player import Player

class GridBomb():
    """
    A class to handle Bombs on the grid. Howto set an detonate them
    """
    
    def __init__(self):
        pass
    
    
    # From playes inventory add a bomb to the boars and creates a steptimer for it
    def bomb_set(self, p: Player) -> tuple[str, dict[str: str]] | tuple[str, None]:
        """
        Method that add a bomb on the boards and creats a "step timer"
        (utils.steptimer)
        """
        player_bombs = [b for b in p.items if b.is_bomb]
        
        if not player_bombs:
            return "", None # No bombs to place
        
        bomb = player_bombs[0]
        
        p.remove_player_specific_items(bomb.name, type(bomb))
        
        new_bomb = {"name": bomb.name, 
                    "exec_time": p.steps +3, 
                    "exec_func": self.bomb_detonate, 
                    "position": self.find_all_items(type(p))[0], 
                    "item": SetBomb()
                    }
        
        return bomb.name, new_bomb
    
    
    # When the steptimer for a set bomb is up it goes here
    def bomb_detonate(self, bomb_pos: tuple[int, int], bomb_item: tuple[str, dict[str: str]]) -> None:
        """
        A method to handle the bomd that is activated by a steptimer
        """
        if isinstance(self.board[bomb_pos], type(bomb_item)):
            bomb_pos_x = bomb_pos[0]
            bomb_pos_y = bomb_pos[1]
            
            bomb_affected_all_pos = [bomb_pos,
                                      (bomb_pos_x -1, bomb_pos_y -1),
                                      (bomb_pos_x, bomb_pos_y -1),
                                      (bomb_pos_x +1, bomb_pos_y -1),
                                      (bomb_pos_x -1, bomb_pos_y), 
                                      (bomb_pos_x +1, bomb_pos_y),
                                      (bomb_pos_x -1, bomb_pos_y +1),
                                      (bomb_pos_x, bomb_pos_y +1),
                                      (bomb_pos_x +1, bomb_pos_y +1)]
            
            for bomb_affected_pos in bomb_affected_all_pos:
                if (0 <= bomb_affected_pos[0] < self.width -1 and 
                     0 <= bomb_affected_pos[1] < self.height -1):
                   
                    # Something may die or get destoyed
                    try:
                        if bomb_affected_pos == bomb_pos:
                            replace_item = self.board[bomb_affected_pos].dies("steponbomb")
                        else:
                            replace_item = self.board[bomb_affected_pos].dies("bomb")
                        
                    except:
                        replace_item = Destroyed()

                    else:
                        pass
                    
                    finally:
                        if self.board[bomb_affected_pos].can_be_destoyed:
                            self.board[bomb_affected_pos] = replace_item
