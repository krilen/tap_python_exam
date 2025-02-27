from .grid.grid import Grid
from .entity.player import Player
from .items.items import get_items, PlayerExit, Food
from .menu.menu import Menu
from .utils.steptimer import StepTimer
from .entity.monster import Monster

grid_height = 12 # y
grid_width = 36 # x

# Player limit start position
player_starter_limit: tuple[int, int] = (grid_width // 2 -3, grid_height // 2 -2)

# This is the setup of the board
# Loops until we find a board that is playable
while True:
    
    grid: Grid = Grid(grid_width, grid_height)
    grid.add_border_walls()

    player: Player = Player()
    grid.add_entity(player, player_starter_limit)
    
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
grid.set_inventory(6, inventory, [])

# Fences
fence_names: list[str] = list({k for k in fences.keys()})

# Step Timer
steptimer = StepTimer()
steptimer_tmp = []

# Monster
monster: Monster = Monster()

# Start values
command: str = ""
messages: list[str] = []
jump_active: int = 0
jump_active = False

# Steps
items_appears = 25
exit_appears = 50
monster_appears = 60

# Loopa tills användaren trycker Q eller X.
while not command.casefold() in ["q", "x"]:
    
    """
    The grid is the board with a Borederwall around it
    The grid contains items (can also be referred as tiles)   
    """

    match command:
        
        # Player movement
        case "d" | "a" | "w" | "s":
        
            player_move: tuple[int, int] = player.possible_moves[command]
            
            if jump_active:
                player_move = player_move[0] *2, player_move[1] *2

            player_next_pos, player_current_pos = player.next_move(grid, player_move, jump_active, monster)

            """
            player_movement: list[tuple[int, int]] = grid.get_path(player, player_move)
            player_current_pos = player_movement[0]
            
            player_next_pos = player_current_pos
            player_prev_pos = player_current_pos

            
            
            for player_next_pos in player_movement[1:]:
                
                # If the tile is blocked (Border Wall) '<item>.block = True' 
                if grid.board[player_next_pos].block:
                    player_next_pos = player_prev_pos
                    player.remove_player_specific_items("shovel", Shovel)

                # Tile is not crossable for the Player but Player has the shovel
                elif not grid.board[player_next_pos].cross and "shovel" in player.inventory:
                    
                    if isinstance(grid.board[player_next_pos], Monster):
                        grid.board[player_next_pos] = monster.dies("shovel")
                        
                        monster_appears = player.steps + monster_appears // 2
                        
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
            """
                
            jump_active = False
            
            if player_current_pos != player_next_pos:

                # Player actions
                messages.append( player.action( grid, player_next_pos, fence_names ))

                # Monster action
                monster_pos = grid.find_all_items(Monster)
                monster_move = monster.should_move()
                                           
                if monster_pos and monster_move:
                    monster.action( grid, monster_pos, player, player_next_pos )

                elif player.steps > monster_appears and not grid.find_all_items(Monster):
                    grid.add_entity(monster)
                    messages.append(" > The Monster has been seen!")


                # Other actions

                if player.steps % items_appears == 0:
                    grid.set_inventory(2, inventory, player.items)

                # Check the step timer
                for _steptime in steptimer_tmp:
                    _pos, _item = steptimer.add_to_steptimer(_steptime)
                    grid.board[_pos] = _item
                    
                steptimer_tmp.clear()
                
                steptimer.check_steptimer(player.steps)

                """
                #tile_current = grid.board[player_current_pos]
                player_tile = grid.board[player_next_pos]
        
                replace_item = Free()
            
                # Check if the tiles need to remain as something else
                if isinstance(player_tile, Killed):
                    replace_item = Killed()
                
                elif isinstance(player_tile, Destroyed):
                    replace_itemm = Destroyed()

                # Steps
                player.steps = 1
                del(player.score)
                del(player.free_steps)
                
                # If the tile has something on it that we need to react to
                if not isinstance(player_tile, Free):
                        
                    if (type(player_tile).__name__).lower() in fence_names:
                        replace_item = Destroyed()
                    
                    # Perhaps we are able to pickup the item that is a tile
                    message = player.add_player_items(player_tile)
                    
                    if message!= None:
                        messages.append( f" > Found: {message.title()}" )
                    
                    del(message)
                    
                    # And any points from the tile
                    _item_points = player_tile.item_points()
                    
                    if _item_points > 0:
                         player.score = _item_points
                         player.free_steps = item_pickup_free_step

                
                # Place new inventory if possible
                if player.steps % items_appears  == 0:
                    grid.set_inventory(2, inventory, player.items)
                    
                    
                # Move the player
                grid.move_position(player, player_next_pos, replace_item)

                # If player stepped on the bomb
                if isinstance(player_tile, SetBomb):
                    grid.bomb_detonate(player_next_pos, grid.board[player_next_pos])
                
                



                # Monster moves                
                monster_pos = grid.find_all_items(Monster)
                monster_move = monster.should_move()
                                           
                if monster_pos and monster_move:
                    
                    monster_player_diff = grid.path_diff(player_next_pos, monster_pos[0])
                    monster_path = grid.get_path(monster, monster_player_diff)
                    
                    if len(monster_path) == 2:
                        moster_next_pos = monster_path[1]
                        
                    else:
                        moster_next_pos = monster_path[2]

                    # For the path of the moster
                    for monster_tile in monster_path[1:]:
                        if monster_tile == moster_next_pos:
                            break

                        if isinstance(grid.board[monster_tile], SetBomb):
                            grid.bomb_detonate(monster_tile, grid.board[monster_tile])
                        else:
                            grid.board[monster_tile] = Destroyed()

                    # End pos
                    if isinstance(grid.board[monster_tile], SetBomb):
                        grid.move_position(monster, moster_next_pos, Destroyed())    
                        grid.bomb_detonate(monster_tile, grid.board[monster_tile])
                    else:
                        grid.move_position(monster, moster_next_pos, Destroyed())
                    
                    # Monster kills the player, game ends
                    if moster_next_pos == player_next_pos:
                        grid.board[player_next_pos] = player.dies("monster")

                    # If player stepped on the bomb
                    if isinstance(moster_next_pos, SetBomb):
                        grid.bomb_detonate(moster_next_pos, grid.board[moster_next_pos])
                        
        
                # Monster enters the board
                elif player.steps > monster_appears and not grid.find_all_items(Monster):
                    grid.add_entity(monster)
                    messages.append(" > The Monster has been seen!")
                """


            
        # Players inventory
        case "i":
            messages.append( player.get_player_inventory() )
            
            
        # Player jump
        case "j":
            jump_active = True
            messages.append( " > Ready to jump!" )


        # Player eats food
        case "e":
            _removed_food = player.remove_player_any_item(Food)
            
            if _removed_food != None:
                player.free_steps = 10
                messages.append( f" > You eat the {_removed_food.name.title()}!" )
                
            else:
                messages.append( " > You have no food to eat!" )
        
        
        # Player places a Bomb
        case "b":
            message, _add_bomb = grid.bomb_set(player)
            
            if _add_bomb != None:
                steptimer_tmp.append(_add_bomb)
                
                messages.append( f" > {message.upper()} have been placed, run!" )

            else:
                messages.append( " > You do not have any bomb to use!" )
        
        
            del(message)

        case _:
            pass

    # Add Exit for Player
    if player.steps > exit_appears and not grid.find_all_items(PlayerExit) and player.alive[0]:
        grid.place_player_exit()
        messages.append(" > Players Exit has appeared!")  
        
    # If the Player has died prepair the game to end
    if not player.alive[0]:
        messages.append(player.alive[1])
        
    # If the Monster has died it will be spawn in the future
    if not monster.alive[0]:
        player.score = monster.points
        messages.append(monster.alive[1])
        monster.alive = True, ""
        monster_appears = player.steps + monster_appears // 2
    
    # Display
    m = Menu()
    m.show(grid, messages, player.score)
    messages.clear()
   
    # End game if Player has died
    if not player.alive[0]:
         break
    
    command = input(" Use WASD to move, Q/X to quit >> ").casefold()[:1]    

print(" Thank you for playing!")
print()
