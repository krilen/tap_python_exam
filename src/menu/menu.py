
class Menu():
    
    
    def show(self, g, message, points):
        """
        Visa spelvärlden och antal poäng.
        """
        print()
        print(g)
        if message:
            print(f"{message}")
        print()
        print(f" You have {points} point{'' if points == 1 else 's'}.")

        print(" --------------------------------------")