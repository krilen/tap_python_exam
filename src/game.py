from .grid import Grid
from .player import Player
from .items import *
from .menu import Menu

import sys

# This is the setup of the board
# Loops until we fins a board that is playable
while True:
    
    grid: type[Grid] = Grid(36, 12)
    grid.add_border_walls()

    player: type[Player] = Player()
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
inventory_names: list[str] = list({k for k in inventory.keys()})
grid.place_inventory(4, inventory)

# Fences
fence_names: list[str] = list({k for k in fences.keys()})

# Start values
command: str = ""
message: str = ""
jump_active: int = 0 # To handle the jump

# Loopa tills användaren trycker Q eller X.
while not command.casefold() in ["q", "x"]:
    

    match command:
        
        # Player movement
        case "d" | "a" | "w" | "s":
            
        
            player_move: tuple[int, int] = player.possible_moves[command]
            
            if jump_active:
                player_move = player_move[0] *2, player_move[1] *2
                
            
            player_movement: list[tuple[int, int]] = grid.get_path(player, player_move)
            
            player_current_pos = player_movement[0]
            
            # Find out how far it is possible to move the player
            player_next_pos = player_current_pos
            player_prev_pos = player_current_pos
            
            for player_next_pos in player_movement[1:]:
                
                # If the tile is blocked (Border Wall) '<item>.block = True' 
                if grid.board[player_next_pos].block:
                    player_next_pos = player_prev_pos
                    
                    player.remove_player_specific_items("shovel", Shovel)

                # Tile is not crossable for the Player but Player has the shovel
                elif not grid.board[player_next_pos].cross and "shovel" in player.inventory:
                    
                    if player_next_pos == player_movement[-1] or jump_active:
                        break
                    
                    else:
                        player_prev_pos = player_next_pos
                        continue
                
                # Tile is not crossable for Player (Fence) '<item>.cross = False' 
                elif not grid.board[player_next_pos].cross:
                    player_next_pos = player_prev_pos

                else:
                    player_prev_pos = player_next_pos
                    continue
        
                break
            
            jump_active = 0
            

            # Only if the player have moved
            if player_current_pos != player_next_pos:
                
                tile_current = grid.board[player_current_pos]
                tile_next = grid.board[player_next_pos]
        
                _default_item = Free() # The default new item tile when we pass over it
            
                # A destoyed tile should remain destoyed
                if isinstance(tile_next, Destroyed):
                    _default_item = Destroyed()
                
                tile_class_name = (type(tile_next).__name__).lower()
                
                # Steps
                player.steps = 1
                del(player.score)
                del(player.free_steps)
                
                
                
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
                    _item_points = tile_next.item_points()
                    
                    if _item_points > 0:
                         player.score = _item_points
                         player.free_steps = 5
                        
                # Place new items if possible
                if player.steps % 2 == 0:
                    grid.place_inventory(1, inventory)
                

                
                # Move the player
                grid.move_position(player, player_next_pos, _default_item)

            
        # Players inventory
        case "i":
            message = player.get_player_inventory()
        
        # Player jump
        case "j":
            jump_active = 1
            
        # Player eats food
        case "e":
            _removed_food = player.remove_player_any_item(Food).name
            player.free_steps = 10
            
            message = f"You eat the {_removed_food.title()}!"
            


            
        case _:
            pass
        
    m = Menu()
    m.show(grid, message, player.score)
    message = ""
    
    command = input("Use WASD to move, Q/X to quit >> ").casefold()[:1]    

# Hit kommer vi när while-loopen slutar
print("Thank you for playing!")
