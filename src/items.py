
class Item():
    def __init__(self):
        self.symbol = " "
        self.cross = True
        self.death = False
        self.points = 0


class Wall(Item):
    
    def __init__(self):
        super().__init__()
        self.symbol = "■"
        self.cross = False


class Pickup(Item):
    
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.symbol = "?"
        self.points = 20
