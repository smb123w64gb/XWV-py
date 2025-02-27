import struct
from enum import Enum
def u8(file):
    return struct.unpack("B", file.read(1))[0]
def w8(file,val):
    file.write(struct.pack("B", val))
def u16(file):
    return struct.unpack("<H", file.read(2))[0]
def w16(file,val):
    file.write(struct.pack("<H", val))
def u32(file):
    return struct.unpack("<I", file.read(4))[0]
def w32(file,val):
    file.write(struct.pack("<I", val))
def s32(file):
    return struct.unpack("<i", file.read(4))[0]
def ws32(file,val):
    file.write(struct.pack("<i", val))
class SamplerRate(Enum):
    XWV_RATE_11025 = 0
    XWV_RATE_22050 = 1
    XWV_RATE_44100 = 2

class Formats(Enum):
    XWV_FORMAT_PCM = 0
    XWV_FORMAT_XBOX_ADPCM = 1

class XWV(object):
    def __init__(self):
        self.hdr_size = 0x14
        self.loop_start = -1
        self.smp_rate = SamplerRate.XWV_RATE_22050
        self.channels = 1
        self.format = Formats.XWV_FORMAT_XBOX_ADPCM
        self.vdat = bytearray()
        self.data = bytearray()
    def read(self,f):
        self.hdr_size = u32(f)
        data_size = u32(f)
        data_off = u32(f)
        self.loop_start = s32(f)
        vdat_size = u16(f)
        self.format = Formats(u8(f))
        lmpData = u8(f)
        self.smp_rate = SamplerRate((lmpData & 0xF))
        self.channels = ((lmpData >> 4) & 0xF)
        self.vdat = f.read(vdat_size)
        f.seek(data_off)
        self.data = f.read(data_size)
    def write(self,f):
        w32(f,self.hdr_size)
        w32(f,len(self.data))
        w32(f,0)#0x8
        ws32(f,self.loop_start)
        w16(f,len(self.vdat))
        w8(f,self.format.value)
        lmpData = ((self.channels<<4) | self.smp_rate.value)
        w8(f,lmpData)
        f.write(self.vdat)
        seek = 0x200 - (f.tell()%0x200)
        if(seek == 0x200):
            seek = 0
        print(seek)
        f.seek(seek,1)
        svPos = f.tell()
        f.write(self.data)
        f.seek(8)
        w32(f,svPos)
