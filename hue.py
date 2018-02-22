import os
import sys

def get_script():
    return os.path.realpath(sys.argv[0])


print(sys.executable)
os.system('pkexec %s %s' % (get_script(), ' '.join(sys.argv[1:])))
