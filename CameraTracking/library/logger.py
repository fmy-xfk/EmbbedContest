import sys
import time

def log(msg,level=0):
    lvlstr=""
    if level==0:
        lvlstr="[INFO]"
    elif level==1:
        lvlstr="[WARN]"
    elif level==2:
        lvlstr="[ERROR]"
    elif level==3:
        lvlstr="[FATAL]"
    print(lvlstr,time.strftime("[%H:%M:%S]", time.localtime()),msg)
    if level==3:
        sys.exit()