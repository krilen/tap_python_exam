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

# Items to be found and used
itemes = get_items()
inventory = itemes["inventory"]
fences = itemes["fence"]

# Inventory
inventory_names = list({k for k in inventory.keys()})
grid.place_inventory(4, inventory)

# Fences
fence_names = list({k for k in fences.keys()})


command = ""
# Loopa tills användaren trycker Q eller X.
while not command.casefold() in ["q", "x"]:
    
    match command:
        
        # Player movement
        case "d" | "a" | "w" | "s":
            
            player_move = player.possible_moves[command]
            player_next_pos, player_current_pos = grid.calc_position(player_move, player)[0]
            
            tile_current = grid.board[player_current_pos]
            tile_next = grid.board[player_next_pos]


        
                        
            # Tiles that are blocked can never be crossed over
            if not tile_next.block: 
                
                # You are not able to cross fences (if you have a shovel upi destoy it)
                if tile_next.cross or (not tile_next.cross and "shovel" in player.inventory):
                
                    _default_item = Free() # The default new item tile when we pass over it
                
                    # A destoyed tile should remain destoyed
                    if isinstance(tile_next, Destroyed):
                        _default_item = Destroyed()
                    
                    tile_class_name = (type(tile_next).__name__).lower()
                    
                    # If the tile has something on it that we need to react to
                    if not isinstance(tile_next, Free):
                        
                        

                        
                        # If the tile is a fence that we can break it and leave some destruction
                        if tile_class_name in fence_names:
                            _default_item = Destroyed()
                        
                        
                        
                        # Perhaps we are able to pickup the item that is a tile
                        _add_item_status = player.add_player_items(tile_next)
                        
                        
                        # Mark the item as found but not placed in inventory
                        if not _add_item_status and tile_next.name in inventory_names:
                            _default_item = tile_next # Reset the tile from default to the item
                            _default_item.symbol = "!" # Marked it as already picked up
                            _default_item.points = 0 # Set the points for it to 0 the next time

                        # And any points from the tile
                        player.score = tile_next.item_points()
                        
                    # Place new items if possible
                    if player.steps % 2 == 0:
                        grid.place_inventory(1, inventory)
                    
                    
                    player.score = -1 # each step cost the player a point if he has one
                    player.steps = 1 # number of steps
                    
                    # Move the player
                    grid.move_position(player, player_next_pos, _default_item)
                    
                else:
                    pass
            
            else:
                
                print(player.remove_player_items("shovel", Shovel))
    
        # Players inventory
        case "i":
            print(player)
        
        # Player jump
        case "j":
            print("Lets jump")
            
            #Here I am but best to fix eat food first so we can jump different length
            
        # Player eats food
        case "e":
            print("Lets eat food")
            
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
