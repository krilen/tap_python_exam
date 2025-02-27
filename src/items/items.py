import inspect, sys

class Item():
    def __init__(self):
        self.symbol = "?"
        self.block = False # If True you can never go on the tile (boderwall) 
        self.cross = True # If True you can cross over it, False you can not cross it unless... (fence)
        self.points = 0
        self.is_inventory = False # Save to the playes inventory
        self.name = "item"
        self.is_fence = False # Defined as a fence
        self.is_bomb = False
        self.can_be_destoyed = True

        
    def item_points(self):
        return self.points


class BorderWall(Item):
    
    def __init__(self):
        super().__init__()
        self.symbol = "■"
        self.block = True
        self.can_be_destoyed = False


class Food(Item):
    ITEMS = ["carrot", "apple", "strawberry", "cherry", "watermelon", "radish", "cucumber", "meatball"]
    
    def __init__(self, name=None):
        super().__init__()
        self.name = name
        self.symbol = "?"
        self.points = 20
        self.is_inventory = True
    
    @classmethod
    def create(cls, name):
        return cls(name)


class Free(Item):
    """
    Items that indicate on the board that is in no use
    """
    def __init__(self):
        super().__init__()
        self.symbol = "."
        

class Destroyed(Item):
    """
    Item that indicate on the board that the tile is destroyed
    """
    def __init__(self):
        super().__init__()
        self.symbol = ","
        self.can_be_destoyed = False
        
        
class Killed(Destroyed):
    def __init__(self):
        super().__init__()
        self.symbol = "X"

class Fence(Item):
    def __init__(self):
        super().__init__()
        self.symbol = "~" # symbol in case
        self.cross = False
        self.is_fence = True


class FenceIntersect(Fence):
    
    def __init__(self):
        super().__init__()
        self.symbol = "+"
        self.is_fence = True
        

class FenceVertical(Fence):
    
    def __init__(self):
        super().__init__()
        self.symbol = "|"
        self.is_fence = True
        

class FenceHorizontal(Fence):
    
    def __init__(self):
        super().__init__()
        self.symbol = "-"
        self.is_fence = True
        

class Shovel(Item):
    
    def __init__(self):
        super().__init__()
        self.name = "shovel"
        self.is_inventory = True


class Bomb(Item):
    ITEMS = ["dynamite", "c4", "nitroglycerin"]
    
    
    def __init__(self, name=None):
        super().__init__()
        self.name = name
        self.symbol = "B"
        self.is_inventory = True
        self.is_bomb = True
        self.points = 20
 

    @classmethod
    def create(cls, name):
        return cls(name)
    
    
class SetBomb(Item):
    def __init__(self):
        super().__init__()
        self.symbol = "¤"
        
        
class PlayerExit(Item):
    def __init__(self):
        super().__init__()
        self.symbol = "E"
        self.name = "Exit"



# Get any items that are inventory or fence
def get_items():
    
    _get_item_classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    
    inventory_classes = {}
    fence_classes = {}
    
    for name, item_class in _get_item_classes:
        _tmp = item_class()
        
        if _tmp.is_inventory:
            
            if "create" in dir(_tmp):
                for item in _tmp.ITEMS:
                    inventory_classes[item] = item_class.create(item)

            else:
                inventory_classes[name.lower()] = item_class()
                
        elif _tmp.is_fence:
            fence_classes[name.lower()] = item_class()
        
         
        del(_tmp)
    
    return {"inventory": inventory_classes, "fence": fence_classes}