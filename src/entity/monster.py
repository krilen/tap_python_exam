from ..items.items import Killed, SetBomb, Destroyed, Item


import random

class Monster(Item):
    
    def __init__(self):
        super().__init__()
        
        self._old_pos: dict = {}
        self.symbol: str = "#"
        self.points = 100
        self.cross = False
        self.possible_moves: list[tuple[int, int]] = [(2, 0), (-2, 0), (0, -2), (0, 2)]
        self.move_rate = 1
        self.alive = (True, "")
        self.monster_appears = 60


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

        elif reason == "steponbomb":
            message = " > Monster stepped on the Bomb and was killed!"
            
        else:
            message = " > Monster was killed!"
            
        self.alive = False, message
    
        return Killed()
    
    
    def should_move(self):
        if random.randint(0, 9) < self.move_rate:
            return False
        
        else:
            return True


    def action(self, g, monster_pos, p, player_next_pos):
        monster_player_diff = g.path_diff(player_next_pos, monster_pos[0])
        monster_path = g.get_path(self, monster_player_diff)
        
        if len(monster_path) == 2:
            monster_next_pos = monster_path[1]
            
        else:
            monster_next_pos = monster_path[2]
            
        print(monster_path)

        # For the path of the moster
        for monster_pos in monster_path[1:]:
            if monster_pos == monster_next_pos:
                break

            if isinstance(g.board[monster_pos], SetBomb):
                g.move_position(self, monster_pos, Destroyed())
                g.bomb_detonate(monster_pos, g.board[monster_pos])

            else:
                g.board[monster_pos] = Destroyed()

        if self.alive[0]:
            if isinstance(g.board[monster_pos], SetBomb):
                g.move_position(self, monster_next_pos, Destroyed())
                g.bomb_detonate(monster_pos, g.board[monster_pos])
            
            else:
                g.move_position(self, monster_next_pos, Destroyed())
        

        # Monster kills the player, game ends
        if monster_next_pos == player_next_pos:
            g.board[player_next_pos] = p.dies("monster")

        # If player stepped on the bomb
        if isinstance(monster_next_pos, SetBomb):
            g.bomb_detonate(monster_next_pos, g.board[monster_next_pos])
            

