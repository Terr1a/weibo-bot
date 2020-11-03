import time

def push(info, flag):
    type = {"SUCCESS":"32","WARNING":"33","FAILED":"31"}
    color = type[flag]
    localtime = time.asctime( time.localtime(time.time()) )
    print("\033[0;%s;40m\t" % color+localtime+": "+info+"\033[0m" )