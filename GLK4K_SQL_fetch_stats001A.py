import os
import glob
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
# import pygal as pg
# from scipy import stats
##change to use the INI file to input all initial information
LineSummary = ['16HB1315P1001','16HB1111P1002','16HB1111P2003',
		'16HB1267P1004','16HB1117P1005','16HB1309P1006',
		'16HB1123P1007','16HB1303P1008','16HB1129P1009']
# Y = stats.norm()
connect=sqlite3.connect('e:/mySQLite/test007F7.sqlite')
cursor  = connect.cursor()
def  FetchSpGp(LineName_str, KeyStr, GP):
	# SortStr  = 'SELECT SP , GunPort, GunDelay_ms ' \  ##ignore the GunPort##
	# 		         'FROM TabGun_'+LineName_str+' '\
	# 				 'ORDER BY '+ 'GunPort ;'
	# cursor.execute(SortStr)
	ExecStr = 'SELECT SP,' +KeyStr+' '\
		             ' FROM TabGun_'+LineName_str+' '\
					 ' WHERE GunPort='+str(GP)+' '\
					 ' AND SP >=905 AND SP<=1840 ;'
	cursor.execute(ExecStr)
	result=cursor.fetchall()
	return result
pdf = PdfPages('Multipage_001.pdf')
Choose='GunDelay_ms, FireTime_ms, Delta_ms' 
for GP in range(1, 16+1): ## for one loop, MAX  32
	#defind the  figure's size
	# plot and save in the same size as the original
	xinch =  15
	yinch =  10
	fig,axes = plt.subplots(len(LineSummary), 3,figsize=(xinch,yinch)) 
	axes = axes.flatten()
	result   = []  ##some changes could be done here.
	for I in range(0, len(LineSummary)):
		result= FetchSpGp(LineSummary[I],Choose,GP)
		SP         = []
		Delay     = []
		Fire       = []
		Delta     = []
		for N in range(0, len(result)):
			SP.append(result[N][0])
			Delay.append(result[N][1])
			Fire.append(40-result[N][2])
			Delta.append(result[N][3])
		axes[I*3].hist(Delay, 50, normed=1, color='g')
		axes[I*3].set_title(LineSummary[I]+' GunPort '+str(GP)+ u'延迟')
		axes[I*3+1].hist(Fire, 50, normed=1, color='r')
		axes[I*3+1].set_title(LineSummary[I]+' GunPort '+str(GP)+ u'激发')
		axes[I*3+2].hist(Delta, 50, normed=1, color='b')
		axes[I*3+2].set_title(LineSummary[I]+' GunPort '+str(GP)+' Delta')
	# stats_t = stats.ttest_1samp(Delay1, 13.0)
	# print(stats_t)
	# fig, axes = plt.subplots(2, sharex=True)
	# axes[0].plot(Delay1, Y.pdf(Delay1))
	# axes[1].plot(Delay1, Y.cdf(Delay1))
	plt.tight_layout(pad=0.05)
	pdf.savefig()
pdf.close()
# plt.show()
# print(Y.mean(),Y.std(),Y.var())
print("END !")
