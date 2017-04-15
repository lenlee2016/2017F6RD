#!/usr/bin/env python3
'''Parse the SEG-D file(v1.0, created by Sercel SEL4X8 
to extract the external header for all information
about  Navigation external header,
source array and guns' firing header information'''
# # # protype made 18th June 2016
import os
import glob
import sqlite3
from construct import String
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')
def TabCre(TabLIST):
	ExeStr = ' CREATE TABLE ' + TabLIST[0] + '( '\
		  +TabLIST[1] +' ' + TabLIST[2] +' PRIMARY KEY '\
		  'UNIQUE NOT NULL'\
		  ')'
	cursor.execute(ExeStr)
def TabIndxADD(TabLIST):
	for I in range(3, len(TabLIST),2):
		ExeStr = 'ALTER TABLE ' + TabLIST[0] + ' ADD COLUMN '\
		+ TabLIST[I] + ' ' + TabLIST[I+1]
		cursor.execute(ExeStr)
def InstValue(TabLIST, ValuLIST):
	ExeStr= 'INSERT INTO ' + TabLIST[0]\
				+ '  VALUES (' +','.join(ValuLIST[1:len(ValuLIST)]) +')'
	cursor.execute(ExeStr)
TabNAV  = ['TabNavHead_LineName', #Table Name,each line's name
		  'SP','INTEGER',     #Primary Key
		  'Time','Time',
		  'Date','Date',
		  'WD','REAL',
		  'Mast_Lat','REAL',
		  'Mast_Long','REAL',
		  'Src_Lat','REAL',
		  'Src_Long','REAL',
		  'Mast_Sb','REAL']
TabSRC = ['TabSrcInfo_LineName', #Table Name,each line's name
		  'SP','INTEGER',     #Primary Key
		  'TriMode',"CHAR",
		  'Date','Date',
		  'Time','Time',
		  'SourceSeq','INTEGER',
		  'ActGNum','INTEGER',
		  'Spread_ms','REAL',
		  'VolumeFired','INTEGER',
		  'AvrDelta_ms','REAL',
		  'AvrDevDelta_ms','REAL',
		  'Manifold_PSI','INTEGER',
######for the next loop in sub-string######
		  'Str01PSI','INTEGER',
		  'Str02PSI','INTEGER',
		  'Str03PSI','INTEGER',
		  'Str04PSI','INTEGER']
TabGUN = ['TabGunInfo_LineName', #Table Name,each line's name
		  'IndexGUN','INTEGER',     #Primary Key
		  'SP','INTEGER',    
		  'GunPort','INTEGER',
		  'Mode',"CHAR",
		  'Detect',"CHAR",
		  'SourceSeq','INTEGER',
		  'AutoFire',"CHAR",
		  'StaticOffset_ms','REAL',
		  'GunDelay_ms','REAL',
		  'FireTime_ms','REAL',
		  'Delta_ms','REAL',
		  'Depth_m','REAL',]
def SEG_D_HeaderParse(THE_LIST, ARG1, ARG2, ARG3):
    GUNSTRINGS = 4 #define the number of gunstrings, this project used: 4
    GUNSTOTALNUM = ARG2 #define the number of air guns in total, this project used: 4 *16=64
    BINARYSAVE = ARG1
    Index = ARG3
    GUN_STR_OFSET = 90+GUNSTRINGS*4
    GUNS = list(range(GUNSTOTALNUM))
    Omit = 32*3 + 32*16 + 1024 + 125
    SrcBlk= 90 + GUNSTRINGS*4 + GUNSTOTALNUM*22
    for SEGD_SHOTFILE in THE_LIST:
        BINARYFILE = SEGD_SHOTFILE
        FD = open(BINARYFILE, 'rb')
        # SAVE = open(BINARYSAVE, 'at')#file appended ,text mode
        FD.seek(Omit)  #omit the first 96 bytes on begining of SEG-D file
        BINDATA = FD.read(SrcBlk) #define the external header's length
        BINSTR = String(SrcBlk, encoding="utf8").parse(BINDATA)
        if (BINSTR[1:6] == "GCS90"):
            GO=' '
        else:
            print("\n Missed External header!")
            print("LineID:  ", LINE)
            print("FileID  ", SEGD_SHOTFILE)
            continue
        RawValue =[0]
        try:
            RawValue.append(BINSTR[18:28])    #ShotPointNum
        except:
            RawValue.append(0)
        RawValue.append("'"+BINSTR[30:31]+"'")    #TriggerMode
        RawValue.append("'20"+BINSTR[31:39]+"'")    #ShotDate, Prefix 20
        RawValue.append('"'+str(BINSTR[40:48])+'"') #Insert Shooting Time
        RawValue.append(BINSTR[48:49])    #Current Sequence
        RawValue.append(BINSTR[52:54])    #Active Gun Num
        try:
            RawValue.append("%.2f"%(float(BINSTR[60:63])*0.1))    #Spread, Real #Delta Spread for Total Array(0.1ms)
        except:
            RawValue.append('0')
        RawValue.append(BINSTR[63:68])    #Volume Fired
        RawValue.append('0')
        RawValue.append('0')
        # RawValue.append("%.2f"%(float(BINSTR[68:73])))    #Average Delta# NN.NN
        # RawValue.append("%.3f"%(float(BINSTR[73:78])))    #Average Deviation of Delta#N.NNN
        RawValue.append(BINSTR[82:86])    #Manifold
        '''The offset 0 to 90 contained
    the fixed GCS90(SYNTRAK) header information'''
        for string in range(GUNSTRINGS):
            RawValue.append(BINSTR[(90+string*4):(94+string*4)])
            # SAVE.write(';GunString No.'+str(string+1)+' Pres.:'+\
            #                         BINSTR[(90+string*4):(94+string*4)])
        # # # '''The each single gun's firing detail'''
        # # # '''(GUN_STR_OFSET+6)one Byte with BLANK'''
        InstValue(TabSRC, RawValue)
        GunValue = [0]
        for GUN in GUNS:
            GunValue.append(RawValue[1])# the SP number
            GunValue.insert(1, str(Index))  # insert the Index
            Temp = BINSTR[(GUN_STR_OFSET+0+GUN*22):(GUN_STR_OFSET+ 2+GUN*22)]
            if Temp:
                GunValue.append(Temp) #GunPortNo
            else:
                print("\n Missed Part of External header!")
                print("LineID====:  ", LINE)
                print("FileID====  ", SEGD_SHOTFILE)
                continue	
            GunValue.append("'"+BINSTR[(GUN_STR_OFSET+2+GUN*22):\
				    (GUN_STR_OFSET+ 3+GUN*22)]+"'") #Gun Mode
            GunValue.append("'"+BINSTR[(GUN_STR_OFSET+3+GUN*22):\
					(GUN_STR_OFSET+ 4+GUN*22)]+"'") # Detect Mode
            GunValue.append(BINSTR[(GUN_STR_OFSET+4+GUN*22):\
	              (GUN_STR_OFSET+ 5+GUN*22)]) # Sequence Mode
            GunValue.append("'"+BINSTR[(GUN_STR_OFSET+5+GUN*22):\
	              (GUN_STR_OFSET+ 6+GUN*22)]+"'") # AutoFire Mode YES/NO
            try:
                GunValue.append("%.2f"%(int(BINSTR[(GUN_STR_OFSET+ 7+GUN*22):\
	              (GUN_STR_OFSET+ 10+GUN*22)])*0.1))#
            except:
                GunValue.append('0')
            try:
                GunValue.append("%.2f"%(int(BINSTR[(GUN_STR_OFSET+10+GUN*22):\
	              (GUN_STR_OFSET+ 13+GUN*22)])*0.1)) #
            except:
                GunValue.append('0') #
            try:
                GunValue.append("%.2f"%(int(BINSTR[(GUN_STR_OFSET+13+GUN*22):\
	              (GUN_STR_OFSET+ 16+GUN*22)])*0.1))#
            except:
                GunValue.append('0')#
            try:
                GunValue.append("%.2f"%(int(BINSTR[(GUN_STR_OFSET+16+GUN*22):\
	              (GUN_STR_OFSET+ 19+GUN*22)])*0.1))#
            except:
                GunValue.append('0')#
            try:
                GunValue.append("%.1f"%(int(BINSTR[(GUN_STR_OFSET+19+GUN*22):\
	              (GUN_STR_OFSET+ 22+GUN*22)])*0.1))#
            except:
                GunValue.append('0')#
            InstValue(TabGUN, GunValue)
            GunValue = [0]	
            Index=Index+1
        FD.close()
sqlite3.PrepareProtocol()
SEGD_FOLD = "I:/MX1_lines/"
os.chdir(SEGD_FOLD)
LINES = glob.glob('MX1_*')       
connection = sqlite3.connect('e:/mySQLite/15MX_D1_LinesSrcGun001.sqlite')
cursor = connection.cursor()
cursor.execute(" PRAGMA synchronous = OFF ")
cursor.execute(" PRAGMA CACHE_SIZE = 9000000 ")
for LINE in LINES:
	TabNav[0]  = 'TabNav_' + LINE
	TabSRC[0] = 'TabSrc_' + LINE
	TabGUN[0] = 'TabGun_' + LINE
	BS = "E:/mypython/"+LINE+"SEAL4X8_SEG-D_ExtHed01.txt"
	TabCre(TabNAV)
	TabIndxADD(TabNAV)
	TabCre(TabSRC)
	TabIndxADD(TabSRC)
	TabCre(TabGUN)
	TabIndxADD(TabGUN)
	GunIndex=1
	# print(BS)
	os.chdir(SEGD_FOLD+LINE+"/")
	print(SEGD_FOLD+LINE+"/")
	os.listdir('.')
	SEGD_LIS = glob.glob('*.segd')
	SEG_D_HeaderParse(SEGD_LIS, BS, 36,GunIndex)
connection.commit()
connection.close()
logging.debug('End of program')
