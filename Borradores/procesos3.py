import os
import sys
import time

# print('SOY EL PADRE (PID: %d)' %os.getpid())
# print('..........................')
# try:
#     ret=os.fork()
# except OSError:
#     print('ERROR AL CREAR HIJO')
ret=os.fork()

while True:
    if ret>0:
        print('SOY EL PADRE (PID: %d)' % os.getpid())
        sys.exit(0)
        #este break deja huerfano al hijo
    elif ret ==0:
        print('SOY EL HIJO (PID: %d) -- (PPID: %d) ' % (os.getpid(),os.getppid()))
        time.sleep(1)
        #este break deja un hijo zombie
        print()