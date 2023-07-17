import os
import sys
import time

for file in os.listdir(): 
    if file.endswith(".o") or file.endswith(".exe"): 
        os.remove(file)
        print("Removed", file)

# can pass -d flag for just delete, and not this next bit
if "-d" not in sys.argv:
    print("Compiling test")
    os.system("gcc -Wall -g -c rankpermute.c")
    time.sleep(0.2)
    os.system("gcc -Wall -g -c test.c")
    time.sleep(0.2)
    os.system("gcc -o test rankpermute.o test.o")