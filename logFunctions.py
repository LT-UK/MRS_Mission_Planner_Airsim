# ========================================================= #
# Multi-Robot Systems (MRS) Operation Framework
# Cranfield University - DARTeC                  
# ========================================================= #

# ===== Import libraries =====
from datetime import datetime

# ===== Log Report Functions =====
def logReport(type,msg):
    f = open("logs.log","a")
    f.write(str(datetime.now())+" - "+type+" - "+msg+"\n")
    f.close()
    
def resetLog():
    f = open("logs.log","w")
    f.write('')
    f.close()