import os
import glob
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
# import pygal as pg
# from scipy import stats
##change to use the INI file to input all initial information
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
pdf = PdfPages('Multipage_String04.pdf')
for GP in range(49, 64+1): ## for one loop, MAX  32 
	xinch =  20
	yinch = 10
	fig,axes = plt.subplots(len(LineSummary), 2,figsize=(xinch,yinch))  #Set the Column 1
	axes = axes.flatten()
	result1   = []  ##some changes could be done here.
	result2   = []  ##some changes could be done here.
	for I in range(0, len(LineSummary)):
		result1 = FetchSpGp(LineSummary[I], 'GunDelay_ms',GP)
		result2 = FetchSpGp(LineSummary[I], 'FireTime_ms',GP)
		SP          = []
		Delay     = []
		Fire        = []
		for N in range(0, len(result1)):
			SP.append(result1[N][0])
			Delay.append(result1[N][2])
			Fire.append(40-result2[N][2] )
		# hist = pg.Bar()
		# hist.title = LineSummary[I]+' GunPort '+str(GP)+' Delay'
		# hist.add(LineSummary[I]+'GunPort'+str(GP), Delay)
		# hist.render_to_file(LineSummary[I]+'GunPort'+str(GP)+'_Delay.svg')
		# hist = pg.Bar()
		# hist.title = LineSummary[I]+' GunPort '+str(GP)+' Fire'
		# hist.add(LineSummary[I]+'GunPort'+str(GP), Fire)
		# hist.render_to_file(LineSummary[I]+'GunPort'+str(GP)+'_FIRE.svg')
		#defind the  figure's size
		# plot and save in the same size as the original
		axes[I*2].hist(Delay, 50, normed=1, color='g')
		axes[I*2].set_title(LineSummary[I]+' GunPort '+str(GP)+' Delay')
		axes[I*2+1].hist(Fire, 50, normed=1, color='b')
		axes[I*2+1].set_title(LineSummary[I]+' GunPort '+str(GP)+' Firing')
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
