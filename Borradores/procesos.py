import time
import os

print('INICIO')

print('PID: %d -- PPID: %d' % (os.getpid(), os.getppid()))

for i in range (5,0,-1):
    print(i)
    time.sleep(1)

print('\nFin')
print('PID: %ID -- PPID: %d' % (os.getpid(), os.getppid()))