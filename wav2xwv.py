import sys
from xwv import XWV

xwvIN = open(sys.argv[1],'rb')
testXWV = XWV()
testXWV.read(xwvIN)
print(testXWV.channels)