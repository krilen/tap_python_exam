from .grid import Grid
from .player import Player
from .items import *
from .menu import Menu



# This is the setup of the board
# Loops until we fins a board that is playable
while True:
    
    grid = Grid(36, 12)
    grid.add_border_walls()

    player = Player()
    grid.add_player(player)
    
    grid.add_fences(6, 3, 7) # nr of fences (can be merged), min size, max_size (without merge)

    # Need to walk trough the board to verify access to every tile
    if grid.check_walkthrough(Player):
        break


# random items
pickups = ["carrot", "apple", "strawberry", "cherry", "watermelon", "radish", "cucumber", "meatball"]
grid.set_pickup(pickups)

# shovel
grid.set_shovel()

command = ""
# Loopa tills användaren trycker Q eller X.
while not command.casefold() in ["q", "x"]:
    
    match command:
        
        case "d" | "a" | "w" | "s":
            
            player_move = player.possible_moves[command]
            player_next_pos, player_current_pos = grid.calc_position(player_move, player)[0]
            
            tile_current = grid.board[player_current_pos]
            tile_next = grid.board[player_next_pos]
            
            # ARE HERE WORKING ON HOW TO USE ITEMS Shovel and bombs
                        
            # Tile is always block (perimeter border)
            if not tile_next.block: 
            
                # You are not able to cross fences (, if you do not also have a shovel)
                if tile_next.cross or (not tile_next.cross and "shovel" in player.inventory):
                
                    _default_item = Free()
                    
                    if not isinstance(tile_next, Free):
                        
                        player.inventory = tile_next
                        player.score = tile_next.item_points()

                    print(player.steps)
                    
                    
                    
                    player.score = -1
                    player.steps = 1
                    grid.move_position(player_next_pos, player_current_pos, _default_item)
                    
                else:
                    pass
                    
    
        case "i":
            print(player)
            
        case _:
            pass
    
    m = Menu()
    m.show(grid, player.score)

    command = input("Use WASD to move, Q/X to quit >> ").casefold()[:1]
            

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
