#!/usr/bin/env python3
import construct
from construct import Nibble ##Nibble equal to BitsInteger(4)
from construct import Int8ub,Int16ub,Int24ub,Int32ub
from construct import Int8sb,Int16sb
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')

def ContainExtr(ContainList):
	temp = []
	temp = list(ContainList)
	char = str(len(temp))
	value = 0
	for i in range(0,len(temp)):
		value =value + (temp.pop() * (10 **i))
	ContainExtr=("%0"+char+"d")%(value)
	return ContainExtr

def ContainExtrHexF(ContainList):
	temp = []
	temp = list(ContainList)
	char = str(len(temp))
	value = 0
	for i in range(0,len(temp)):
		value =value + (temp.pop() * (100 **i))
	ContainExtr=("%0"+char+"d")%(value)
	if ContainExtr == '15':
		ContainExtr = 'F'
	if ContainExtr == '1515':
		ContainExtr = 'FF'
	if ContainExtr == '151515':
		ContainExtr = 'FFF'
	if ContainExtr == '15151515':
		ContainExtr = 'FFFF'	
	return ContainExtr
##----------------------------------------------------------------------------------------------------## 
BINARYFILE = 'D:/Tools/run/2017F6RD_backs/00000759.segd'

# FOr  SERCEL SEAL408&428 SEG-D data version1.0
####---------------- General header block #1 -------------------------####
GenHeader_1 = construct.BitStruct(
	"FileNumber"				   /Nibble[4],  	
	"FormatCode"			   /Nibble[4],		##8058 32 IEEE demultiplexed
	"k1_k12"          		  	   /Nibble[12],	##General Constants, from k1 to k12 #
	"Year"						   /Nibble[2],
	"HDR"						   /Nibble,
	"Julian Day"   			   /Nibble[3],
	"Hour"						   /Nibble[2],
	"Minute"					   /Nibble[2],
	"Second"					   /Nibble[2],
	"ManufactuerCode"      /Nibble[2],
	"ManufactuerSN"         /Nibble[4],
	"BytesPerScan"         /Nibble[6],
	"BaseScanInterval"      /Nibble[2], ##0.25ms(4),0.5ms(8),1ms(10),2ms(20),4ms(40)
	"Polarity_untested"		  /Nibble,
	"NotUsed"					 /Nibble[3],
################################################## testing!
	"RecordType"			/Nibble,   ##8=normal,2 = test record
	"RecordLength"			/Nibble[3],  ##extended record length used
	"ScanTypePerRecord" /Nibble[2],
	"ChanSetsNum"         /Nibble[2],  ##Variable
	"SampleSkewNum"	/Nibble[2],  ##32byte extensions
	"ExtendHeaderLen"   /Nibble[2],
	"ExternalHeaderLen" /Nibble[2],
)
# # FD = open(BINARYFILE, 'rb')
# # N =32
# # FD.seek(0)  #omit the first N bytes on begining of SEG-D file
# # BINDATA = FD.read(N)  #define reading block's length
# # FileNum=ContainExtr(GenHeader_1.parse(BINDATA)["FileNumber"])
# # FormatCode=ContainExtr(GenHeader_1.parse(BINDATA)["FormatCode"])
# # k1_k12=ContainExtr(GenHeader_1.parse(BINDATA)["k1_k12"])
# # RecordLength=ContainExtrHexF(GenHeader_1.parse(BINDATA)["RecordLength"])
# # ExternalHeaderLen=ContainExtrHexF(GenHeader_1.parse(BINDATA)["ExternalHeaderLen"])
# # # # logging.debug(' GenHeader_1 Container is ', RecordLength)
# # # # logging.debug(' GenHeader_1 Container is ', ExternalHeaderLen)
# # FD.close()
####---------------- General header block #2 -------------------------####
GenHeader_2 = construct.Struct(
	"ef"				        /Int24ub,  	##Expanded file number
	"en_NotUsed"		/Int16ub,		##8058 32 IEEE demultiplexed
	"ecx_NotUsed"  	   /Int16ub,	##General Constants, from k1 to k12 #
	"eh"					   /Int16ub, ##External header blocks(Variable)
	"NA1"			       /Int8ub,    ##10 Not used
	"rev"	     			   /Int8ub,    ## Rev 1.0
	"gt"					   /Int16ub, ##13-14 Blocks of General trailer's number
	"erl"					   	/Int32ub,   ##15-17 Extended record length(0-128000ms)
	# "NA2"					/Int8ub,  ##18 Not used
	"bn"				        /Int8ub,   ##19 General header Block Number(2)
	"NA3"		            /Int8ub,   ##20 Not used(No comment on SEAL Manual)
	"SeqNum"      /Int16ub,  ##Defaults to GUI setup,or updated by navigation system.
	"NA4"					/Int8ub[10],
)
# FD = open(BINARYFILE, 'rb')
# N =32
# FD.seek(N)  #omit the first N bytes on begining of SEG-D file
# BINDATA = FD.read(32)  #define reading block's length
# ExpFileNum=GenHeader_2.parse(BINDATA)["ef"]
# ExtendHeaderLen=GenHeader_2.parse(BINDATA)["eh"]
# Revision=GenHeader_2.parse(BINDATA)["rev"]
# RL=GenHeader_2.parse(BINDATA)["erl"]
# logging.debug(' GenHeader_2 Container is ', ExpFileNum)
# logging.debug(' GenHeader_2 Container is ', ExtendHeaderLen)
# logging.debug(' GenHeader_2 Container is ', Revision)
# logging.debug(' GenHeader_2 Container is ', RL)7
	
####---------------- General header block #3 -------------------------####
GenHeader_3 = construct.Struct(
	"ef"				        /Int24ub,  	##01-03,Expanded file number
	"sln"		                /Int24ub,	##04-06,Source Line Number(integer)
	"sln_Fract"  	   		/Int16ub,	##07-08,Source Line Number(Fraction)
	"spn"					   /Int24ub, ##09-11, Source Point Number(Integer)
	"spn_Fract"		  /Int16ub,    ##12-13, Source Point Number(Fraction)
	"spi"	     			   /Int8ub,    ## 14, Source Point Index, Always 1 in marine operations
	"pc_NA"				   /Int8ub, ##15, Phase control(not recorded)
	"vl_NA"	     	   	/Int8ub,   ##16, Type vibrator(not recorded)
	"pa_NA"				/Int16sb,  ##17-18, Phase angle(not recorded)
	"bn"				        /Int8ub,   ##19 General header Block Number(3)
	"ss"		            /Int8ub,   ##20, Source Set Number
	"NA1"					/Int8ub[12], ##21 - 32, Not used, Reserved.
)
# FD = open(BINARYFILE, 'rb')
# N =32
# FD.seek(N*2)  #omit the first N bytes on begining of SEG-D file
# BINDATA = FD.read(32)  #define reading block's length
# ExpFileNum=GenHeader_3.parse(BINDATA)["ef"]
# SPN=GenHeader_3.parse(BINDATA)["spn"]
# SPI=GenHeader_3.parse(BINDATA)["spi"]
# BlockNum=GenHeader_3.parse(BINDATA)["bn"]
# SSN=GenHeader_3.parse(BINDATA)["ss"]

ChanSetHeader_def =[]
'''below section---Scan type header --- should be repeated for 16 times,
a loop should be designed'''
####---------------- Scan type header (Channel set descriptor ) from 1 to 16 ------####
ChanSetHeader_01 = construct.Struct(
		# "Byte1_2"	/ construct.BitStruct(
		# 	"st"	/Nibble[2],    #01    Scan type 
		# 	"cn" /Nibble[2],     #02    Channel set number
		# ),
 	"st"	/Int8ub,    #01    Scan type 
 	"cn" /Int8ub,     #02    Channel set number
	"tf"	/Int16ub,		#03-04 Channel set start time(Units:2ms)
	"te"  /Int16ub,		# 05-06 Channel set end time(Units:2ms)
	"mp" /Int8sb[2],		# 07-08 Descaling exponent
	"cs"  /Int16ub, 		#09-10 Channels in this channel set
		"Byte11_12" / construct.BitStruct(			
			"c"   /Nibble, #11H   Channel type identification(9-Aux, 1-Seismic)
			"NA1" /Nibble,#11L Not used
			"nse" /Nibble, #12H Number of subscans exponent
			"cgcm" /Nibble,#12L Gain control method(fixed gain)
			),
	"af"  /Int16ub, #13-14 Alias filter frequency
	"as" /Int16ub, #15-16 Alias filter slope
	"lc"  /Int16ub, #17-18 Low cut filter frequency
	"ls"  /Int16ub, #19-20 Low cut filter slope 	

	"ntf"		/Int16ub, #21-22 Notch filter frequency
	"2ntf"	/Int16ub, #23-24 2nd Notch filter frequency
	"3ntf"	/Int16ub, #25-26 3rd Notch filter frequency
	"ecsn"  /Int16ub, #27-28 Extended channel set number
			"Byte29" / construct.BitStruct(
			"ehf"     /Nibble, #29H    Extended header flag				
			"the"  	/Nibble, #29L	Trace Header Extensions	
			),
	"vs"		/Int8ub,	   #30    Vertical stack
	"cabN"  /Int8ub,   #31    Streamer number
	"ary"     /Int8ub,   #32    Array forming
)
# FD = open(BINARYFILE, 'rb')
# N =32
# FD.seek(N*3)  #omit the first N bytes on begining of SEG-D file
# BINDATA = FD.read(32)  #define reading block's length
# ScanType=ChanSetHeader_01.parse(BINDATA)["st"]
# ChanSetN=ChanSetHeader_01.parse(BINDATA)["cn"]
# TimeStart=str(ChanSetHeader_01.parse(BINDATA)["tf"]) + " ms"
# TimeEnd=str(2*ChanSetHeader_01.parse(BINDATA)["te"]) +" ms"
# DescaleMultip=ChanSetHeader_01.parse(BINDATA)["mp"]
# DescaleMultip=ChanSetHeader_01.parse(BINDATA)["cs"]
# AliasFF=ChanSetHeader_01.parse(BINDATA)["af"]
# AliasFS=ChanSetHeader_01.parse(BINDATA)["as"]
# LowCutF=ChanSetHeader_01.parse(BINDATA)["lc"]
# LowCutS=ChanSetHeader_01.parse(BINDATA)["ls"]
# Byte11_12=ChanSetHeader_01.parse(BINDATA)["Byte11_12"]
# Byte29=ChanSetHeader_01.parse(BINDATA)["Byte29"]
# CableNum=ChanSetHeader_01.parse(BINDATA)["cabN"]

####---------------- Extended header ( ) 1024Bytes --------------------------------------####
##TODO here

####---------------- External header ( ) 4096Bytes --------------------------------------####
##TODO here

##----------------------------------------------------------------------------------------------------## 
FD.close()
logging.debug('End of program')