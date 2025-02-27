from typing import Any


class StepTimer():
    """
    A class to handle events that are triggerd at a certain point in the future.
    The time is defined as the players movements (steps) When the player moves
    it adds 1. Each round the steptimer is checked and if it finds something
    it will send it to the defined method to handle it.
    """
    
    def __init__(self):
        self.steptimer_exec = {}
        
        
    def add_to_steptimer(self, step_timer: dict[str: str, str: int, str: Any, str: Any]):
        """
        Adds an event or trigger at a certain time to the instance
        """
        
        step_time = step_timer["exec_time"]
        
        # Add a new one
        if self.steptimer_exec.get(step_time, 0) == 0:
                        
            step_timer_pos = step_timer["position"]
            step_timer_item = step_timer["item"]
                        
            step_timer_exec = {"name": step_timer["name"], 
                               "position": step_timer_pos, 
                               "item": step_timer_item,
                               "exec_func": step_timer["exec_func"]
                                }
                        
            self.steptimer_exec.update({ step_time: { "steptimers": [step_timer_exec]} })
        
        # Add additional ones at the same time
        else:
            pass
    
        return step_timer_pos, step_timer_item
    
    
    
    def check_steptimer(self, player_step) -> None:
        """
        Method to find out if someting needs to be done at this player step
        Basically used for a bomb to explode. At a certain time it calls a 
        predefined method.
        """
        step_timers = self.steptimer_exec.get(player_step, None)
        
        if step_timers != None:
            
            for step_timer in step_timers["steptimers"]:
                
                step_timer_func = step_timer["exec_func"]
                step_timer_pos = step_timer["position"]
                step_timer_item = step_timer["item"]
                
                step_timer_func(step_timer_pos, step_timer_item)
                
            self.steptimer_exec.pop(player_step)
            
            

    
    