class Player:
    marker = "@"

    def __init__(self, x, y):
        self.pos = (x, y)
        #self.pos_y = y

    # Flyttar spelaren. "dx" och "dy" är skillnaden
    def move(self, dx, dy):
        """
        Flyttar spelaren.
         * dx = horisontell förflyttning, från vänster till höger
         * dy = vertikal förflyttning, uppifrån och ned
        """
        self.pos_x += dx
        self.pos_y += dy

    def can_move(self, x, y, grid):
        return True
        #TODO: returnera True om det inte står något i vägen


