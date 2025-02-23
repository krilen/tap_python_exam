
class Menu():
    
    
    def show(self, g, message, points):
        """
        Visa spelvärlden och antal poäng.
        """
        print()
        print(g)
        print(f"You have {points} point{'' if points == 1 else 's'}.")
        if message:
            print()
            print(f"{message}")
        print("--------------------------------------")