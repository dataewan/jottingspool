#!python
import sys
from jottingspool import interface

if __name__ == "__main__":
    i = interface.Interface(sys.argv[1])
    i.run()
