# -*- coding:utf-8 -*-
import os
import glob
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from statsmodels.tsa.stattools import adfuller
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
# import pygal as pg
# from scipy import stats
# 移动平均图
def draw_trend(timeSeries, size):
    f = plt.figure(facecolor='white')
    # 对size个数据进行移动平均
    rol_mean = timeSeries.rolling(window=size).mean()
    # 对size个数据进行加权移动平均
    rol_weighted_mean = pd.ewma(timeSeries, span=size)
    timeSeries.plot(color='blue', label='Original')
    rolmean.plot(color='red', label='Rolling Mean')
    rol_weighted_mean.plot(color='black', label='Weighted Rolling Mean')
    plt.legend(loc='best')
    plt.title('Rolling Mean')
    plt.show()
def draw_ts(timeSeries):
    f = plt.figure(facecolor='white')
    timeSeries.plot(color='blue')
    plt.show()
'''
　　Unit Root Test
   The null hypothesis of the Augmented Dickey-Fuller is that there is a unit
   root, with the alternative that there is no unit root. That is to say the
   bigger the p-value the more reason we assert that there is a unit root
'''
def testStationarity(ts):
    dftest = adfuller(ts)
    # 对上述函数求得的值进行语义描述
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    return dfoutput

# 自相关和偏相关图，默认阶数为31阶
def draw_acf_pacf(ts, lags=31):
    f = plt.figure(facecolor='white')
    ax1 = f.add_subplot(211)
    plot_acf(ts, lags=31, ax=ax1)
    ax2 = f.add_subplot(212)
    plot_pacf(ts, lags=31, ax=ax2)
    plt.show()
##change to use the INI file to input all initial information
LineSummary = ['16HB1315P1001','16HB1111P1002','16HB1111P2003',
		'16HB1267P1004','16HB1117P1005','16HB1309P1006',
		'16HB1123P1007','16HB1303P1008','16HB1129P1009']

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
