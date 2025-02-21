
class Item():
    def __init__(self):
        self.symbol = " "
        self.block = False          # If True you can never go on the tile (boderwall) 
        self.cross = True           # If True you can cross over it, False you can not cross it unless... (fence)
        self.points = 0
        self.item_inventory = False
        self.destroy = True
        
    def item_points(self):
        return self.points
    
        


class BorderWall(Item):
    
    def __init__(self):
        super().__init__()
        self.symbol = "■"
        self.block = True
        #self.destroy = False


class Pickup(Item):
    
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.symbol = "?"
        self.points = 20
        self.item_inventory = True


class Free(Item):

    def __init__(self):
        super().__init__()
        self.symbol = "."

"""        
class Destroyed(Item):
    
    def __init__(self):
        super().__init__()
        self.symbol = ","
"""

class Fence(Item):
    def __init__(self):
        super().__init__()
        self.symbol = "~" # symbol in case
        self.cross = False

        
class FenceIntersect(Fence):
    
    def __init__(self):
        super().__init__()
        self.symbol = "+"
        

class FenceVertical(Fence):
    
    def __init__(self):
        super().__init__()
        self.symbol = "|"

        
class FenceHorizontal(Fence):
    
    def __init__(self):
        super().__init__()
        self.symbol = "-"


class Shovel(Item):
    
    def __init__(self):
        super().__init__()
        self.name = "shovel"
        self.symbol = "🪏"
        self.item_inventory = True
    
    
    
           
           
class Bomb(Item):
    def __init__(self):
        super().__init__()
        self.name = "bomb"
        self.symbol = "💣"
        self.item_inventory = True
