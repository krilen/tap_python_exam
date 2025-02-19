from .grid import Grid
from .player import Player
from .items import Pickup

grid = Grid(36, 12)
grid.make_walls()

# Random walls

player = Player()
grid.add_player(player)

# random items
pickups = ["carrot", "apple", "strawberry", "cherry", "watermelon", "radish", "cucumber", "meatball"]
grid.set_pickup(pickups)



# TODO: flytta denna till en annan fil
def print_status(game_grid):
    """Visa spelvärlden och antal poäng."""
    print("--------------------------------------")
    print(f"You have 0 points.")
    print(game_grid)


command = "a"
# Loopa tills användaren trycker Q eller X.
while not command.casefold() in ["q", "x"]:
    
    match command:
        
        case "d" | "a" | "w" | "s":
        
            player_move = player.possible_moves[command]
            player_new_pos, player_old_pos = grid.calc_position(player_move, player)
            
            if grid.check_position(player_new_pos):
                
                # Before we move we migh want to pickup or collect what is there then move
                
                board_type = grid.board[player_new_pos] 
                
                if board_type != None:
                    
                    print(type(grid.board[player_new_pos]) )
                    
                    if isinstance(board_type, Pickup):
                        
                        print(f"You picked up: {board_type.name}")
                        player.inventory = board_type
                        player.score = board_type.points
                
                
                
                else:
                    player.score = -1
                
                
                grid.move_position(player_new_pos, player_old_pos)
    
    
        case "i":
            print(player)
            
        case _:
            pass
    
    
    print_status(grid)

    command = input("Use WASD to move, Q/X to quit. ").casefold()[:1]
            

    """
    if command == "d" and player.can_move(1, 0, g):  # move right
        # TODO: skapa funktioner, så vi inte behöver upprepa så mycket kod för riktningarna "W,A,S"
        maybe_item = g.get(player.pos_x + 1, player.pos_y)
        player.move(1, 0)

        if isinstance(maybe_item, pickups.Item):
            # we found something
            score += maybe_item.value
            print(f"You found a {maybe_item.name}, +{maybe_item.value} points.")
            #g.set(player.pos_x, player.pos_y, g.empty)
            g.clear(player.pos_x, player.pos_y)
    """

# Hit kommer vi när while-loopen slutar
print("Thank you for playing!")
