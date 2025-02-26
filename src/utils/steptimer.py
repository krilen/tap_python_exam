
class StepTimer():
    
    def __init__(self):
        self.steptimer_exec = {}
        
        
    
    def add_to_steptimer(self, step_timer):
        
        _step_time = step_timer["exec_time"]
        
        # Add a new one
        if self.steptimer_exec.get(_step_time, 0) == 0:
                        
            _step_timer_pos = step_timer["position"]
            _step_timer_item = step_timer["item"]
                        
            _step_timer_exec = {"name": step_timer["name"], 
                               "position": _step_timer_pos, 
                               "item": _step_timer_item,
                               "exec_func": step_timer["exec_func"]
                                }
                        
            self.steptimer_exec.update({ _step_time: { "steptimers": [_step_timer_exec]} })
            
            
        
        # Add additional ones at the same time
        else:
            pass
    
        return _step_timer_pos, _step_timer_item
    
    
    
    def check_steptimer(self, player_step):
        """
        Method to find out if someting needs to be done at this player step
        Basically used for a bomb to explode
        """
        _step_timers = self.steptimer_exec.get(player_step, None)
        
        if _step_timers != None:
            
            for _step_timer_exec in _step_timers["steptimers"]:
                
                _step_timer_exec_func = _step_timer_exec["exec_func"]
                _step_timer_exec_pos = _step_timer_exec["position"]
                _step_timer_exec_item = _step_timer_exec["item"]
                
                _step_timer_exec_func(_step_timer_exec_pos, _step_timer_exec_item)
                
            self.steptimer_exec.pop(player_step)
            
            

    
    