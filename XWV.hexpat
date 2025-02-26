enum xwvsamplerates_t : u8
{
    XWV_RATE_11025 = 0,
    XWV_RATE_22050 = 1,
    XWV_RATE_44100 = 2,
};

enum xwvformats_t : u8
{
    XWV_FORMAT_PCM = 0,
    XWV_FORMAT_XBOX_ADPCM = 1,
};

bitfield smolData {
 xwvsamplerates_t sampleRate : 4;
 channels : 4;
};
struct phoneme{
    u16 ph;
    float start;
    float end;
};
struct vdat{
    u8 ver;
    u16 PhonemeCount;
    phoneme Phonemes[PhonemeCount];
};
struct XWV{
    u32 headerSize;
    u32 dataSize;
    u32 dataOffset;
    s32 loopStart;
    u16 vdatSize;
    xwvformats_t format;
    smolData d;
    vdat phons;
    u8 data[dataSize] @ dataOffset;
};
XWV wav @ 0;