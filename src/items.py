import inspect, sys


class Item():
    def __init__(self):
        self.symbol = "?"
        self.block = False          # If True you can never go on the tile (boderwall) 
        self.cross = True           # If True you can cross over it, False you can not cross it unless... (fence)
        self.points = 0
        self.item_inventory = False
        self.name = "item"
        self.is_fence = False
        
    def item_points(self):
        return self.points




class BorderWall(Item):
    
    def __init__(self):
        super().__init__()
        self.symbol = "■"
        self.block = True


class Food(Item):
    ITEMS = ["carrot", "apple", "strawberry", "cherry", "watermelon", "radish", "cucumber", "meatball"]
    
    def __init__(self, name=None):
        super().__init__()
        self.name = name
        self.symbol = "?"
        self.points = 20
        self.item_inventory = True
    
    @classmethod
    def create(cls, name):
        return cls(name)


class Free(Item):

    def __init__(self):
        super().__init__()
        self.symbol = "."

        
class Destroyed(Item):
    
    def __init__(self):
        super().__init__()
        self.symbol = ","


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
        self.item_inventory = True
    
    
class Bomb(Item):
    def __init__(self):
        super().__init__()
        self.name = "bomb"
        self.item_inventory = True



# Get any items that can be used as inventory
def get_items():
    
    _get_item_classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    
    inventory_classes = {}
    fence_classes = {}
    
    for name, item_class in _get_item_classes:
        _tmp = item_class()
        
        if _tmp.item_inventory:
            
            if "create" in dir(_tmp):
                for item in _tmp.ITEMS:
                    inventory_classes[item] = item_class.create(item)

            else:
                inventory_classes[name.lower()] = item_class()
                
        elif _tmp.is_fence:
            fence_classes[name.lower()] = item_class()
        
         
        del(_tmp)
    
    return {"inventory": inventory_classes, "fence": fence_classes}