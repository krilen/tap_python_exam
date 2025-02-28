from ..items.items import Killed, SetBomb, Destroyed, Item

from typing import Any
import random

class Monster(Item):
    """
    A class to handle the Msoter that will chace the Player
    """
    def __init__(self):
        super().__init__()
        
        self._old_pos: dict = {}
        self.symbol: str = "#"
        self.points = 100
        self.cross = False
        self.possible_moves: list[tuple[int, int]] = [(2, 0), (-2, 0), (0, -2), (0, 2)]
        self.move_rate = 3
        self.alive = (True, "")
        self.monster_appears = 60


    # Old position
    @property
    def old_pos(self) -> tuple[int, int]:
        """
        Simple attribute to return the old stored item and position during a move
        """
        return self._old_pos
    

    def add_old_pos(self, pos: tuple[int, int], item: type[Any]) -> None:
        """
        Simple attribute to store the old stored item and position during a move
        """
        self._old_pos = {"pos": pos, "item": item}
        
        
    def dies(self, reason: str) -> Item:
        """
        Method to simply handle the different ways the Monster can die and
        the message that it would send.
        """
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
    
    
    def should_move(self) -> bool:
        """
        Method that descides IF the monster should move. If the random value (0-9)
        is higher than the attribute 'move_rate' the monster moves.
        This is used to see if the method 'action' should be called.        
        """
        if random.randint(0, 9) < self.move_rate:
            return False
        
        else:
            return True


    def action(self, g, monster_pos: tuple[int, int], p, player_next_pos: tuple[int, int]) -> None:
        """
        Method to handle the mosters action, the mostes movements when chacing the player.
        It calculate the path that it should take. If it steps on any bomb.
        Ath the end it move the moster to its final position before the next round
        """
        monster_player_diff = g.path_diff(player_next_pos, monster_pos[0])
        monster_path = g.get_path(self, monster_player_diff)
        
        if len(monster_path) == 2:
            monster_next_pos = monster_path[1]
            
        else:
            monster_next_pos = monster_path[2]

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
            

