from ..items.items import BorderWall


class GridBorder():
    """
    A class that cretaed the Border Wall or perimeter of the game
    """
    
    def __init__(self):
        pass

    # Adds the border wall that you can not get pass
    def add_border_walls(self) -> None:
        """
        Creates the border wall and the perimeter of the game
        They can not be destoyed
        """
        for tile in self.board:
            (_x, _y) = tile
            
            if _x == 0 or _y == 0  or _x == self.width -1 or _y == self.height -1:
                self.board[tile] = BorderWall()
                
                
                
