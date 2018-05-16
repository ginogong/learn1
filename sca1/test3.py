#coding:utf-8
import pyodbc
import numpy as np
import math

def baseDown(dataList):
    bd = 0.0    
    bd = min(dataList) -1
    return round(bd,4)

def MDD(dataList):
    maxNum = 0.0
    dd = 0.0
    MDD = 0.0
    for dataArr in dataList:
        if dataArr > maxNum:
            maxNum = dataArr
        elif dataArr < maxNum:
            dd = (dataArr - maxNum) / maxNum
            if dd < MDD : MDD =  dd
    return round(MDD,4)

def  sharpeRatio(array,stdev):
    sr = 0.0
    dayNoRiskReturn = 0.000082
    sumDayRatio = 0
    dayRatio = array - dayNoRiskReturn 
    sumDayRatio = np.sum(dayRatio)      
    meanData = sumDayRatio/len(dayRatio) 
    sr = math.sqrt(240.0) * meanData / stdev
    return round(sr,4)

def annReturn(dataList):
    AR = 0.0
    tradingDay = len(dataList)
    AR = np.power(dataList[len(dataList)-1],240.0 / (tradingDay-1) )- 1 
    return round(AR,4) 

def winRatio(dataList):
    WR = 0
    arrGain = np.diff(dataList,axis=0)
    winNum = np.shape(np.where(arrGain>0))[1]
    WR = winNum/ np.float64(len(arrGain))
    return round(WR,4)

def WvLRatio(dataList):
    WLR = 0.0
    winInd = np.where(dataList[...,1] > 0)
    losInd = np.where(dataList[...,1] <= 0)
    WLR =  - np.sum(np.take(dataList[...,1],winInd)) / float(np.sum(np.take(dataList[...,1],losInd)))
    return round(WLR,4)


def loadDataSet():
    dataMat = []
    fr = open('C:\\Users\\Gino\\Documents\\Python Scripts\\data\\FUDOE02.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([lineArr[0],lineArr[1],lineArr[2],lineArr[3],lineArr[4]])
    return dataMat

def createDOEName(dataMat):
    nameList = []
    '''F001_HYDC_15K_1HD_30Z_0.60CW_09:55'''
    for i in range(1,82):
        if i < 10:
            dataMat[i-1].append('F00' + '%d' % i)
        elif i<100:
            dataMat[i-1].append('F0' + '%d' % i)
        else: dataMat[i-1].append('F' + '%d' % i)        
    for info in dataMat:        
        nameList.append( "%s_HYDC_%sK_1HD_%sZ_%sCW_%s " 
                       %  (info[5],info[2],info[1],info[3],info[4]) )
    return nameList 

def main():
    dataMat = loadDataSet()
    nameList = ['DOEROUND2_001']
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.1.101;DATABASE=XGMFUDB;UID=GDXGM_ADMIN;PWD=GDXGM_ADMIN2016')
    cur = cnxn.cursor()
    result = ['NO', 'MDD', 'AnnReturn','volaility','basedown','sharpeRatio','winRatio','WLRatio'] 
    num = 1
    savePath = 'E:\\WORK\\autodata\\FUDOE\\1\\'
    std = 0
    for item in  nameList:        
        cur.execute("SELECT RQ,JZ/10000000,RSYL FROM T_ZH_JZQX WHERE LB='%s'"%item)
        df = cur.fetchall()
        df = np.array(df)
        df[...,1:2] = np.float64(df[...,1:2])
        df[...,-1:] = np.float64(df[...,-1:])
        df[0,2] = 0.0
        np.savetxt((savePath + '%d.csv') % num, df, fmt=['%s']*df.shape[1],delimiter=',')
        arrNW = df[...,1:2]
        arrDR = df[...,-1:]
        std = math.sqrt(np.var(arrDR))
        result.append(num)
        result.append(MDD(arrNW))
        result.append(annReturn(arrNW))
        result.append(math.sqrt(240) * std)
        result.append(baseDown(arrNW))
        result.append(sharpeRatio(arrDR,std))
        result.append(winRatio(arrNW))
        title = ['date','networth','dayreturn']
        df = np.vstack((np.array(title), df))
        

        
        cur.execute("SELECT RQ,YKJE FROM T_ZHMX_QZQX WHERE ZHBH IN(SELECT ZHBH FROM T_ZH WHERE LB='%s') \
                   And ccfx = '%s' order by RQ " % (item,'平'.decode('utf-8').encode('gb2312')) )
        df2 = cur.fetchall()
        df2 = np.array(df2)
        df2[...,1:2] = np.float64(df2[...,1:2])
        result.append(WvLRatio(df2))              
        num += 1

    cur.close()
    cnxn.close()
    result = np.array(result).reshape(2,8)
    np.savetxt(savePath + 'result04.csv', result, fmt='%s',delimiter=',')

main()

