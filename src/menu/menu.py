
class Menu():
    
    
    def show(self, g, messages, points):
        """
        Visa spelvärlden och antal poäng.
        """
        print()
        print(g)
        if messages:
            for message in messages:
                print(message)
        print()
        print(f" You have {points} point{'' if points == 1 else 's'}.")

        print(" --------------------------------------")