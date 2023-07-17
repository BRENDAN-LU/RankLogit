import os
import shutil
import sys

build_files = [
    r"_rankpermute.c",
    r"test1.cp310-win_amd64.pyd",
]

for file in build_files:
    try: 
        os.remove(file)
    except:
        pass

try: 
    shutil.rmtree(r"build")
except: 
    pass

if "-d" not in sys.argv: 
    os.system("python setup.py build_ext --inplace")