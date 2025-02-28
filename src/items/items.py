import inspect, sys

class Item():
    """
    General lass for all of the Items contains the all different attributes and thier default values.
    If the particulare item dont have the attributes.
    """
    
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

        
    def item_points(self) -> int:
        """
        It the item had point on it is returned
        """
        return self.points


class BorderWall(Item):
    """
    Perimeter of the game
    """
    def __init__(self):
        super().__init__()
        self.symbol = "■"
        self.block = True
        self.can_be_destoyed = False


class Food(Item):
    """
    A food items that can be picked up
    """
    ITEMS = ["carrot", "apple", "strawberry", "cherry", "watermelon", "radish", "cucumber", "meatball"]
    
    def __init__(self, name=None):
        super().__init__()
        self.name = name
        self.symbol = "?"
        self.points = 20
        self.is_inventory = True
    
    @classmethod
    def create(cls, name):
        """
        Class method to create an instance of a particulare food item
        """
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
    Nothing can be placed on it
    """
    def __init__(self):
        super().__init__()
        self.symbol = ","
        self.can_be_destoyed = False
        
        
class Killed(Destroyed):
    """
    Markes the tile where the Player or Moster have been killed
    """
    def __init__(self):
        super().__init__()
        self.symbol = "X"

class Fence(Item):
    """
    General fence
    """
    def __init__(self):
        super().__init__()
        self.symbol = "~" # symbol in case
        self.cross = False
        self.is_fence = True


class FenceIntersect(Fence):
    """
    Fence where a Vertical and Horizontal fence have intersect
    """
    def __init__(self):
        super().__init__()
        self.symbol = "+"
        self.is_fence = True
        

class FenceVertical(Fence):
    """
    Vertical fence
    """
    def __init__(self):
        super().__init__()
        self.symbol = "|"
        self.is_fence = True
        

class FenceHorizontal(Fence):
    """
    Horizontalal fence
    """
    def __init__(self):
        super().__init__()
        self.symbol = "-"
        self.is_fence = True
        

class Shovel(Item):
    """
    Shovel that can be picked up and used by the Player
    """
    def __init__(self):
        super().__init__()
        self.name = "shovel"
        self.is_inventory = True


class Bomb(Item):
    """
    Different bomb types that can be picked up and used by the Player
    """
    ITEMS = ["dynamite", "c4", "nitroglycerin"]
    
    def __init__(self, name=None):
        super().__init__()
        self.name = name
        self.is_inventory = True
        self.is_bomb = True
        self.points = 20
 

    @classmethod
    def create(cls, name):
        """
        Class method to create an instance of a particulare bomb item
        """
        return cls(name)
    
    
class SetBomb(Item):
    """
    Markes the tile where a bomb has been place that has not detonated
    """
    def __init__(self):
        super().__init__()
        self.symbol = "¤"
        
        
class PlayerExit(Item):
    """
    Markes the exit of the game for the player
    """
    def __init__(self):
        super().__init__()
        self.symbol = "E"
        self.name = "Exit"



# Get any items that are inventory or fence
def get_items() -> dict:
    """
    A function used to collect all of the items that can be used by the player
    as inventory (food, bombs and the shovel)
    It also collects the different fences that can exists witin the border wall
    """
    _get_item_classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    
    inventory_classes = {}
    fence_classes = {}
    
    for name, item_class in _get_item_classes:
        _tmp = item_class()
        
        # Inventory
        if _tmp.is_inventory:
            
            if "create" in dir(_tmp):
                for item in _tmp.ITEMS:
                    inventory_classes[item] = item_class.create(item)

            else:
                inventory_classes[name.lower()] = item_class()
        
        # Fence
        elif _tmp.is_fence:
            fence_classes[name.lower()] = item_class()
        
        del(_tmp)
    
    return {"inventory": inventory_classes, "fence": fence_classes}