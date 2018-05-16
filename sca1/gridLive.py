# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os
import shutil
import tushare as ts
import time

code = '300017'
margin = 0.003
lineNum = 5
basepath = 'E:\\WORK\\autodata\\plot1\\'
wpList = []


# fit function
def fit_list(t, y):
    A = np.vstack([t, np.ones_like(t)]).T
    return np.linalg.lstsq(A, y)[0]

#create grid
def grid(price):
    upList = []
    downList = []
    for i in range(1,lineNum+1):
        upList.append(price * (1 + i * margin))
        downList.append(price * (1 - i * margin))
    return upList, downList

# getTick data
def getTick():
    ''' pre data gene '''
    df = ts.get_today_ticks(code)
    df['weightprice'] = np.sum(df['price'] * df['volume']) / np.sum(df['volume'])
    df1 = df[-200:]
    #df1['weightprice'] = np.sum(df1['price'] * df1['volume']) / np.sum(df1['volume'])
    #weightPrice200 = df1['weightprice'][0]
    weightPrice = df['weightprice'][0]
    print '\nnow weightpirce:',weightPrice
    #print '\nnow weightpirce200:',weightPrice200
    f = open((basepath + str(folder) + 'weightprice.txt'),'w')
    f.write('\n' + str(timeNow))
    f.write(str(weightPrice))
    f.close()
    dfRe = df
    dfRe.index =  sorted(df.index,reverse=True)
    fk, fb = fit_list(np.array(dfRe.index), np.array(dfRe['price']))
    upList,downList = grid(weightPrice)
    fprice = fk * dfRe.index + fb
    plt.plot(dfRe.index,dfRe['price'])
    plt.plot(dfRe.index,fprice,'y--')
    weightPriceLine = np.ones((1,len(dfRe.index))) * weightPrice
    plt.plot(dfRe.index,weightPriceLine[0],'b-')
    for i in range(len(upList)):
        num = len(dfRe.index)
        line = np.ones((1,num)) * upList[i]
        plt.plot(dfRe.index,line[0],'r--')
    for i in range(len(downList)):
        num = len(dfRe.index)
        line = np.ones((1,num)) * downList[i]     
        plt.plot(dfRe.index,line[0],'g--')
    plt.grid(True)
    plt.xlabel('ticks')
    plt.ylabel('price')
    if not os.path.exists(basepath + folder + '\\' + str(fileNum) + '.png'):
        plt.savefig(basepath + folder + '\\' + str(fileNum) + '.png')
    else:
        fileList = []
        fileList = os.listdir(basepath + folder + '\\')
        maxNum = 0
        for i in fileList:
            indexNum = int(i.split('.')[0])
            if indexNum > maxNum:
                maxNum = indexNum
        plt.savefig(basepath + folder + '\\' + str(maxNum + 1) + '.png')
    plt.show()

if __name__ == '__main__':
    
    
    fileNum = 0
    folder = datetime.datetime.now().strftime('%Y%m%d')
    if not os.path.exists(basepath + folder):
        os.mkdir(basepath + folder)
    while True:
        timeNow = float(datetime.datetime.now().strftime('%H.%M'))
        print '\n' + str(timeNow)
        try:
            print datetime.datetime.now()
            if timeNow > 15.01 :
                print 'out of trade time.'
                break
            elif (timeNow > 11.31 and timeNow < 13.0 ):
                print 'middle rest, please wait !'
            else : 
                getTick()
        except Exception , e:
            print e
        time.sleep(120)
        fileNum += 1

