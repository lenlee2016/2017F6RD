#!/usr/bin/env python3
'''Parse the SEG-D file(created by SeaMAP GunLink4000
to extract the external header for all inormation
about source array and guns' firing'''
# # # protype made 18th June 2016
import os
import glob
from construct import String
#BINARYFILE = '2016-03-23.04-08-58.0907.segd'
GUNSTRINGS = 4
GUNSTOTALNUM = 64
GUN_STR_OFSET = 90+GUNSTRINGS*4
GUNS = list(range(GUNSTOTALNUM))
SEGD_FOLD = "F:/Faxian6_Backups/programming/2016YQ/"
os.chdir(SEGD_FOLD)
LINES = glob.glob('2016YQ*')
for LINE in LINES:
    BINARYSAVE = "E:/mypython/"+LINE+"GLK4K_SEG-D_ExtHedSAVE02.txt"
    os.chdir(SEGD_FOLD+LINE+"/")
    SEGD_LIST = glob.glob('*.segd')
    for SEGD_SHOTFILE in SEGD_LIST:
        #print(SEGD_SHOTFILE)
        BINARYFILE = SEGD_SHOTFILE
        FD = open(BINARYFILE, 'rb')
        SAVE = open(BINARYSAVE, 'at')#file appended ,text mode
        FD.seek(96)  #omit the first 96 bytes on begining of SEG-D file
        BINDATA = FD.read(1514) #define the external header's length
        BINSTR = String(1514, encoding="utf8").parse(BINDATA)
        # print(BINSTR)
        '''The offset 0 to 90 contained
        the fixed GCS90(SYNTRAK) header information'''
        SAVE.write('ID:'+BINSTR[0:6]+\
                                ';Size:'+BINSTR[6:10]+'bytes'+\
                                ';Line:'+BINSTR[10:18]+\
                                ';ShotPoint:'+str(int(BINSTR[18:28]))+\
                                ';ArrayMask:'+BINSTR[28:30]+\
                                ';TriggerMode:'+BINSTR[30:31]+\
                                ';GPS ShotDate:'+BINSTR[31:39]+\
                                ';GPS ShotTime:'+BINSTR[40:48]+\
                                ';Current Sequence:'+BINSTR[48:49]+\
                                ';Strings:'+BINSTR[49:50]+\
                                ';Guns in Array:'+BINSTR[50:52]+\
                                ';Active Guns:'+BINSTR[52:54]+\
                                ';DeltaError Guns:'+BINSTR[54:56]+\
                                ';AutoFire Guns:'+BINSTR[56:58]+\
                                ';MissFire Guns:'+BINSTR[58:60]+\
                                ';Spread:'+BINSTR[60:63]+\
                                ';VolumeFired(C.I.):'+BINSTR[63:68]+\
                                ';AverAbsErr(ms):'+BINSTR[68:73]+\
                                ';StdDevErr(ms):'+BINSTR[73:78]+\
                                ';Spare:'+BINSTR[78:82]+\
                                ';ManifoldPres(PSI):'+BINSTR[82:86]+\
                                ';Deep Tow:'+'Used for time micro seconds'\
                                )
        '''The each gun string's air pressure values'''
        for string in range(GUNSTRINGS):
            SAVE.write(';GunString No.'+str(string)+' Pres.:'+\
                                    BINSTR[(90+string*4):(94+string*4)])
        '''The each single gun's firing detail'''
        '''(GUN_STR_OFSET+6)one Byte with BLANK'''
        for GUN in GUNS:
            SAVE.write(';GunPortNo.:'+BINSTR[(GUN_STR_OFSET+GUN*22):\
                (GUN_STR_OFSET+2+GUN*22)]+\
        ';GunMode:'+BINSTR[(GUN_STR_OFSET+2+GUN*22):\
                (GUN_STR_OFSET+3+GUN*22)]+\
        ';DetectMode:'+BINSTR[(GUN_STR_OFSET+3+GUN*22):\
                (GUN_STR_OFSET+4+GUN*22)]+\
        ';Sequence(SOURCE)No.:'+BINSTR[(GUN_STR_OFSET+4+GUN*22):\
                (GUN_STR_OFSET+5+GUN*22)]+\
        ';AutoFire:'+BINSTR[(GUN_STR_OFSET+5+GUN*22):\
                (GUN_STR_OFSET+6+GUN*22)]+\
        ';Static Offset(ms):'+str((int(BINSTR[(GUN_STR_OFSET+7+GUN*22):\
                (GUN_STR_OFSET+10+GUN*22)]))/10)+\
        ';GunDelay(ms):'+str((int(BINSTR[(GUN_STR_OFSET+10+GUN*22):\
                (GUN_STR_OFSET+13+GUN*22)]))/10)+\
        ';FireTime(ms):'+str((int(BINSTR[(GUN_STR_OFSET+13+GUN*22):\
                (GUN_STR_OFSET+16+GUN*22)]))/10)+\
        ';DeltaErrTime(ms):'+str((int(BINSTR[(GUN_STR_OFSET+16+GUN*22):\
               (GUN_STR_OFSET+19+GUN*22)]))/10)+\
        ';Depth(meter):'+str((int(BINSTR[(GUN_STR_OFSET+19+GUN*22):\
               (GUN_STR_OFSET+22+GUN*22)]))/10)\
        )
        SAVE.write('\n')
        FD.close()
        SAVE.close()
