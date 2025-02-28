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
itemes: dict = get_items()
inventory: dict = itemes["inventory"]
fences:dict = itemes["fence"]

# Inventory
inventory_names: list[str] = list({k for k in inventory.keys()})
grid.set_inventory(6, inventory, [])

# Fences
fence_names: list[str] = list({k for k in fences.keys()})

# Step Timer
steptimer = StepTimer()
steptimer_items = []

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
    
    match command:
        
        # Player movement
        case "d" | "a" | "w" | "s":
            
            # Player choosen move
            player_move: tuple[int, int] = player.possible_moves[command]
            
            if jump_active:
                player_move = player_move[0] *2, player_move[1] *2

            player_next_pos, player_current_pos = player.next_move(grid, player_move, jump_active, monster)
            jump_active = False
            
            if player_current_pos != player_next_pos:

                # Player actions
                messages.append( player.action( grid, player_next_pos, fence_names ))
                
                # Add to steptimer after the player moves
                for steptime in steptimer_items:
                    steptime_pos, steptime_item = steptimer.add_to_steptimer(steptime)
                    grid.board[steptime_pos] = steptime_item
    
                steptimer_items.clear()

                # Monster action
                monster_pos = grid.find_all_items(Monster)
                monster_move = monster.should_move()
                
                if monster_pos and monster_move:
                    monster.action( grid, monster_pos, player, player_next_pos )

                elif player.steps > monster_appears and not grid.find_all_items(Monster):
                    grid.add_entity(monster)
                    messages.append(" > A Monster has been spotted!")

                # Other actions

                if player.steps % items_appears == 0:
                    grid.set_inventory(2, inventory, player.items)

                steptimer.check_steptimer(player.steps)
            
        # Players inventory
        case "i":
            messages.append( player.get_player_inventory() )
            
            
        # Player jump
        case "j":
            jump_active = True
            messages.append( " > Ready to jump!" )


        # Player eats food
        case "e":
            removed_food = player.remove_player_any_item(Food)
            
            if removed_food != None:
                player.free_steps = 10
                messages.append( f" > You eat the {removed_food.name.title()}!" )
                
            else:
                messages.append( " > You have no food to eat!" )
        
        
        # Player places a Bomb
        case "b":
            message, add_bomb = grid.bomb_set(player)
            
            if add_bomb != None:
                steptimer_items.append(add_bomb)
                
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
