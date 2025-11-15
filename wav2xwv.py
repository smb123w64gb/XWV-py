from riff import RIFF
from xwv import XWV,Formats,SamplerRate
import sys,struct

def u16(file):
    return struct.unpack("<H", file.read(2))[0]
def w16(file,val):
    file += struct.pack("<H", val)
def f32(file):
    return struct.unpack("<f", file.read(4))[0]
def wf32(file,val):
    file += struct.pack("<f", val)


wavin = open(sys.argv[1],'rb')
riffter = RIFF()
riffter.read(wavin)

class RIFFRIPPER(object):
    def __init__(self):
        self.vdats = []
        self.fmtData = [0,0,0,0,0]
        self.wavData = bytearray()
    def read(self,riff):
        trig_set = False
        capture = False
        for x in riff.chunks:
            if(x.header == 'VDAT'):
                split = str(x.data,'ascii').splitlines()

                for y in split:
                    #print(y.split(' '))
                    splat = y.split(' ')
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
                            self.vdats.append(lipValue(int(splat[0]),float(splat[2]),float(splat[3])))
            elif(x.header == 'fmt '):
                self.fmtData = struct.unpack_from("<HHIIH", x.data)
                print(self.fmtData)
            elif(x.header == 'data'):
                self.wavData = x.data

mainAudio = RIFFRIPPER()
mainAudio.read(riffter)



xwav = XWV()
if(mainAudio.fmtData[0] == 0x69):
    xwav.format = Formats.XWV_FORMAT_XBOX_ADPCM
    match mainAudio.fmtData[2]:
        case 11025:
            xwav.smp_rate = SamplerRate.XWV_RATE_11025
        case 22050:
            xwav.smp_rate = SamplerRate.XWV_RATE_22050
        case 44100:
            xwav.smp_rate = SamplerRate.XWV_RATE_44100
        case _:
            print("NON CONFORMANT AUDIO SAMPLERATE FOR HL2:XBOX %i"%mainAudio.fmtData[2])
    #xwav.vdat = vdat_blob
    xwav.channels = mainAudio.fmtData[1]
    xwav.data = mainAudio.wavData
    wavin.close()
    xwavrOut = open(sys.argv[2],'wb')
    xwav.write(xwavrOut)
    xwavrOut.close()

