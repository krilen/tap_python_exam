
class Menu():
    """
    A class to display the board
    """
    def show(self, g, messages: list, points: int) -> None:
        """
        Prints out the board, points and any messages
        """
        print()
        print(g)
        if messages:
            for message in messages:
                print(message)
        print()
        print(f" You have {points} point{'' if points == 1 else 's'}.")
        print(" --------------------------------------")