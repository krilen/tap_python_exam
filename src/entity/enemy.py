


class Enemy():
    
    def __init__(self):
        self._old_pos: dict = {}
        self.symbol: str = "#"
    
    
    
    # Old position
    @property
    def old_pos(self):
        return self._old_pos
    

    def add_old_pos(self, _pos, _item):
        self._old_pos = {"pos": _pos, "item": _item}