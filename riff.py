import struct
def u32(file):
    return struct.unpack("<I", file.read(4))[0]
def w32(file,val):
    file.write(struct.pack("<I", val))
class RIFF(object):
    class CHUK(object):
        def __init__(self):
            self.header = '    '
            self.data = bytearray()
        def read(self,f):
            self.header = str(f.read(4),'utf8')
            size = u32(f)
            self.data = f.read(size)
            return size + 8
        def write(self,f):
            f.write(self.header)
            w32(f,len(self.data))
    def __init__(self):
        self.header = 'RIFF'
        self.size = 0
        self.spec = 'WAVE'
        self.chunks = []
    def read(self,f):
        self.header = str(f.read(4),'utf8')
        if(self.header != 'RIFF'):
            print(self.header)
            print("NOT A RIFF")
            return 0
        self.size = u32(f)
        self.spec = str(f.read(4))
        while((self.size) > f.tell()):
            chk = self.CHUK()
            chk.read(f)
            self.chunks.append(chk)
    def write(self,f):
        f.write(self.header)
        w32(f,0)
        f.write(self.spec)
        for x in self.chunks:
            x.write(f)
        size = f.tell() - 7
        self.size = size
        f.seek(4)
        w32(f,size)