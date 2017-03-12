#!/usr/bin/env python3
from construct import *

def ContainExtr(ContainList):
	temp = []
	temp = list(ContainList)
	char = str(len(temp))
	value = 0
	for i in range(0,len(temp)):
		value =value + (temp.pop() * (10 **i))
	ContainExtr=("%0"+char+"d")%(value)
	return ContainExtr
##----------------------------------------------------------------------------------------------------## 

BINARYFILE = '00000759.segd'
FD = open(BINARYFILE, 'rb')
BINDATA = FD.read(32)  #define reading block's length

# FOr  SERCEL SEAL408&428 SEG-D data version1.0
####---------------- General header block #1 -------------------------####
GenHeader_1 = BitStruct(
	"FileNumber"				   /Nibble[4],  	##Nibble equal to BitsInteger(4)
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
	"Polarity_untested"		  /Nibble[2],
	
	
	
	
	
	
	
	
	
	
	
	
)

FileNum=ContainExtr(GenHeader_1.parse(BINDATA)["FileNumber"])
FormatCode=ContainExtr(GenHeader_1.parse(BINDATA)["FormatCode"])
k1_k12=ContainExtr(GenHeader_1.parse(BINDATA)["k1_k12"])
# # Block1=GenHeader_1.parse(BINDATA)
# containlist = (GenHeader_1.parse(BINDATA)).FileNumber
# list=list((GenHeader_1.parse(BINDATA)).FileNumber)
# # list=list(Block1.k1_k12)
# value = 0
# width = str(len(list))
# for i in range(0,len(list)):
# 	value =value + (list.pop() * (10 **i))
# FileNum=("%0"+width+"d")%(value)




####---------------- General header block #2 -------------------------####
##TODO
	
####---------------- General header block #2 -------------------------####
##TODO

####---------------- Scan type header (Channel set descriptor ) from 1 to 16 ------####
##TODO

print("End of the coeds!")