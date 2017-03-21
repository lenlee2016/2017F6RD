import os
import glob
import sqlite3
import matplotlib.pyplot as plt
from scipy import stats
LineSummary = ['16HB1315P1001','16HB1111P2003',
			   '16HB1117P1005','16HB1309P1006',
			   '16HB1303P1008','16HB1129P1009']
# Y = stats.norm()
connect=sqlite3.connect('e:/mySQLite/test007F7.sqlite')
cursor  = connect.cursor()
def  FetchSpGp(LineName_str, KeyStr, GP):
	# SortStr  = 'SELECT SP , GunPort, GunDelay_ms ' \
	# 		         'FROM TabGun_'+LineName_str+' '\
	# 				 'ORDER BY '+ 'GunPort ;'
	# cursor.execute(SortStr)
	ExecStr = 'SELECT SP, GunPort, ' +KeyStr+' '\
		             ' FROM TabGun_'+LineName_str+' '\
					 ' WHERE GunPort='+str(GP)+' '\
					 ' AND SP >=905 AND SP<=1840 ;'
	cursor.execute(ExecStr)
	result=cursor.fetchall()
	return result
SP          = []
GunPort = []
Delay     = []
Fire        = []
result1   = []  ##some changes could be done here.
result2   = []  ##some changes could be done here.
GP        = 1  ## choose the  Gun Port Number here.
fig,axes = plt.subplots(len(LineSummary), 2)  #Set the Column 1
plt.subplots_adjust(bottom=0.05, right=0.8, top=0.95)
axes = axes.flatten()
for I in range(0, len(LineSummary)):
	result1 = FetchSpGp(LineSummary[I], 'GunDelay_ms',GP)
	result2 = FetchSpGp(LineSummary[I], 'FireTime_ms',GP)
	for N in range(0, len(result1)):
		SP.append(result1[N][0])
		Delay.append(result1[N][2])
		#GunPort.append(result01[I][1])
		Fire.append(result2[N][2] )
	axes[I*2].hist(Delay, 50, normed=1, color='g')
	axes[I*2].set_title(LineSummary[I]+' GunPort '+str(GP)+' Delay')
	axes[I*2+1].hist(Fire, 50, normed=1, color='r')
	axes[I*2+1].set_title(LineSummary[I]+' GunPort '+str(GP)+' Firing')
	SP  = []
	Fire = []
# stats_t = stats.ttest_1samp(Delay1, 13.0)
# print(stats_t)
# fig, axes = plt.subplots(2, sharex=True)
# axes[0].plot(Delay1, Y.pdf(Delay1))
# axes[1].plot(Delay1, Y.cdf(Delay1))
plt.tight_layout(pad=0.05)
plt.show()
# print(Y.mean(),Y.std(),Y.var())
print("END !")
