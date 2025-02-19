


class Item():
    def __init__(self):
        self.cross = True



class Wall(Item):
    
    def __init__(self):
        super().__init__()
        self.symbol = "■"
        self.cross = False
