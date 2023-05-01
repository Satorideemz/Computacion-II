import os
import sys

import argparse
import time


def sumthin():
    print("proceso actual:",os.getpid())


if __name__ =="__main__":
    for i in range(4):
        pid=os.fork()
        if pid==0:
            sumthin()
            #this shows that the return of each procces is 0
            os._exit(0)

    #this for loop prevents the code from finishing before all the child processes had finished    
    for i in range(4):
        os.wait()

    print("all proccesses have finished")    

