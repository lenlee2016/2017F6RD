#!/usr/bin/env python3
import construct
from construct import Float32b
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.debug('Start of program')
##----------------------------------------------------------------------------------------------------## 
BINARYFILE = 'D:/Tools/run/2017F6RD_backs/2016-03-23.04-10-02.0904.segd'
# FOr  SERCEL SEAL408&428 SEG-D data version1.0
####---------------- General header block #1 -------------------------####
GL4K_TraceData = construct.Struct(
	"SampleData" / Float32b,	
	)
FD = open(BINARYFILE, 'rb')
SL = 6144
N_Chan = 6
Ch01 = []
Ch02 = []
Ch03 = []
Ch04 = []
Ch05 = []
Ch06 = []
Data = [Ch01,Ch02,Ch03,Ch04,Ch05,Ch06]
for Num in range(0, N_Chan):
	HB = 32*3+32*16*0+1024*0+1536*1+(20 + 32*7*0 )*(1+Num)+int(SL*2)*Num
	for N in range(0, int(SL/2) +1):
		OmitBlc =HB +4*N
		DataBlc = 4
		FD.seek(OmitBlc)  #omit the first N bytes on begining of SEG-D file
		BINDATA = FD.read(DataBlc)  #define reading block's length
		Sample001=GL4K_TraceData.parse(BINDATA)["SampleData"]
		if(N< int(SL/2)):
			Data[Num].append(round(Sample001,6))
			# print('%.8f'%Sample001)
FD.close()


t = 2 * np.arange(SL/2 )
plt.xlim(-0.02,0.01)
plt.ylim(len(t),0)
plt.fill_betweenx(t,Data[0])
# plt.fill(Data[0],t)
plt.xlabel('Channel')
plt.ylabel('Time')
plt.show()
# labels = ["Chan01", "Chan02", "Chan03"]
# # Computed quantities to aid plotting
# fill_range = (np.min(Data), np.max(Data))
# X_Chan01 = 0.000001
# Offset = 0.03
# x_locations = [X_Chan01, X_Chan01+Offset, X_Chan01+Offset*2]
# # The bin_edges are the same for all of the fill_plotting
# bin_edges = np.linspace(fill_range[0], fill_range[1], SL/2 + 1)
# t = np.arange(SL/2)
# # Cycle through and plot each fill_plotting
# fig, ax = plt.subplots()
# for x_loc, binned_data in zip(x_locations, Data):
#     # lefts = x_loc - 0.5 * binned_data
#     ax.fill(binned_data,t)
# ax.set_xticks(x_locations)
# ax.set_xticklabels(labels)
# 
# ax.set_ylabel("Time")
# ax.set_xlabel("Channels")

plt.show()
# for Num in range(0,N_Chan):
# 	print(Data[Num],"=========End of list=============\n")
# logging.debug('End of program')