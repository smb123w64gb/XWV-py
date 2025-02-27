from riff import RIFF
import sys,struct

def u16(file):
    return struct.unpack("<H", file.read(2))[0]
def w16(file,val):
    file.write(struct.pack("<H", val))
def f32(file):
    return struct.unpack("<f", file.read(4))[0]
def wf32(file,val):
    file.write(struct.pack("<f", val))

class lipValue(object):
    def __init__(self,key = 0,start = 0.0,end = 0.0):
        self.key = key
        self.start = start
        self.end = end
    def read(self,f):
        self.key = u16(f)
        self.start = f32(f)
        self.end = f32(f)
    def write(self,f):
        w16(f,self.key)
        wf32(f,self.start)
        wf32(f,self.end)
        

wavin = open(sys.argv[1],'rb')
riffter = RIFF()
riffter.read(wavin)

trig_set = False
capture = False

vdats = []

for x in riffter.chunks:
    if(x.header == 'VDAT'):
        split = str(x.data,'ascii').splitlines()

        for y in split:
            print(y.split(' '))
            splat = 
            key = y.split(' ')[0]
            if(key == 'WORD'):
                trig_set = True
            if(trig_set):
                if(key == '{'):
                    capture = True
                elif(key == '}'):
                    trig_set = False
                    capture = False
                elif(capture):
                    vdats.append(lipValue(int(y[0]),float(y[2]),float(y[3])))
                
