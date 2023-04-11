th_running_flag='RUN'

def get_thread_status():
   global th_running_flag
   return th_running_flag
 
def set_thread_running(): 
   global th_running_flag
   th_running_flag = "RUN"

def set_thread_control():
   global th_running_flag
   th_running_flag = 'RUN' if (th_running_flag == "STOP") else 'STOP'

def set_thread_break():
   global th_running_flag
   th_running_flag = "BREAK"