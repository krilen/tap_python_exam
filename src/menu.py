
class Menu():
    
    
    def show(self, g, points):
        """
        Visa spelvärlden och antal poäng.
        """
        print()
        print(g)
        print(f"You have {points} point{'' if points == 1 else 's'}.")
        print("--------------------------------------")