import matplotlib.pyplot as plt
import tushare as ts
import numpy as np
import time
import datetime
import pandas as pd
import os

path = 'E:\\WORK\\autodata\\data\\'
grid = 0.013
code = '000567'
ratio_funds = 0.9
date_start = '2016-2-25'
date_end = '2016-8-24'
number_date_volume_avg = 10
chance_num = 90
od_num = 30

def gen_name(code,date):
    name = code +'-' + date.replace('-','')
    return name

def gen_date_list(start,end):
    date_list = []
    dates = pd.date_range(start=start,end=end,freq='B')
    for i in dates:
        date_list.append(i.strftime('%Y-%m-%d'))
    return date_list
         
def gen_date_list2(end,num):
    date_list = []
    dates = pd.date_range(end=end,periods=10,freq='B')
    for i in dates:
        date_list.append(i.strftime('%Y-%m-%d'))
    return date_list

def calc_avg_volume_amount(dataframe,datelist,chance_number):
    li = []
    for dt in datelist:
        if len(dataframe[dataframe.index==dt]['volume']) >0:           
            li.append(dataframe[dataframe.index==dt]['volume'][0])
    amount = int(np.array(li).mean() / chance_number)
    return amount
    
        
    


def vwap(num,volume,amount):
    if volume  > (num + 1) * amount :
        num += 1
        #print 'try NO:',num
        return True,num
    else:
        return False,num

def cut_plus_price(pr):
    pr_tm = (round(pr * 100) + 1) / 100.0
    return pr_tm

def cut_minus_price(pr):
    pr_tm = round(pr * 100)  / 100.0
    return pr_tm

def trade_strategy(series_reverse,chance):
    global amount_order
    global grid
    order = []
    index_num = len(series_reverse)
    price_now = series_reverse['price'][index_num]
    time_now = series_reverse['time'][index_num]
    price_weight = calc_weight_price(series_reverse)
    if (price_now <= price_weight * (1 + 4 * grid) and price_now >= price_weight * (1 + 1 * grid) ):
         direction = 'sell'
         lot = 1
         price = price_now
         order = create_order(direction,price,lot,time_now,grid)
         chance += 1
         amount_order -= 1
         #plot(series_pos,price_weight)
    elif (price_now <= price_weight * (1 - 1 * grid) and price_now >= price_weight * (1 -4 * grid) ):
        direction = 'buy'
        lot = 1
        price = price_now
        order = create_order(direction,price,lot,time_now,grid)
        chance += 1
        amount_order -= 1
        #plot(series_pos,price_weight)
    else:
        #print '\n trending'
        volume_avg = np.mean(series_reverse['volume'])
        volume_recent = np.mean(series_reverse['volume'].tail(100))
        volume_power = calc_volume_power(volume_avg,volume_recent)
        if volume_power == 1:
            price_low = np.min(series_reverse['price'])
            price_high = np.max(series_reverse['price'])
            relative = calc_relative_positon(price_high,price_low,price_now)
            if relative == 1:        
                direction = 'buy'
                lot = 5
                price = price_now
                order = create_order(direction,price,lot,time_now,2 * grid)               
                chance += 1
                amount_order -= 5
                #plot(series_pos,price_weight)
            elif relative == -1:
                direction = 'sell'
                lot = 5
                price = price_now
                order = create_order(direction,price,lot,time_now,2 * grid)
                chance += 1
                amount_order -= 5
                #plot(series_pos,price_weight)
            else:
                series_now_100 = series_reverse.head(300)
                price_weight100 = calc_weight_price(series_now_100)
                if (price_now <= price_weight100 * (1 + 4 * grid) and price_now >=  price_weight100 * (1 + 1 *grid) ):
                    direction = 'sell'
                    lot = 1
                    price = price_now
                    order = create_order(direction,price,lot,time_now,grid)
                    chance += 1
                    amount_order -= 1
                    #plot(series_pos,price_weight100)
                elif (price_now <= price_weight100 * (1 - 1 * grid) and price_now >=  price_weight100 * (1 - 4 *grid) ):
                    direction = 'buy'
                    lot = 1
                    price = price_now
                    order = create_order(direction,price,lot,time_now,grid)                    
                    chance += 1
                    amount_order -= 1
                    #plot(series_pos,price_weight100)

    return order,chance
 
 
def get_data(stock_code):
    df = ts.get_today_ticks(stock_code)
    df1 = df[['time','price','volume']]
    df2 = df[['time','price','volume']]
    num = len(df1)
    index_list = np.arange(num-1,-1,-1)
    df2.index = index_list
    return df1,df2

def calc_weight_price(series):
    weight_price = np.sum(series['price'] * series['volume']) / np.sum(series['volume'])   
    return weight_price

    
def calc_relative_positon(high_price,low_price,now_price):
    sig = 0
    relative = (now_price - low_price) / (high_price - low_price)
    if relative >= 0.9:
        sig = 1
    elif relative <= 0.1:
        sig = -1
    else:
        sig = 0
    return sig

def calc_volume_power(volume_avg,volume_recent):
    if 3 * volume_avg < volume_recent:
        return 1
    else:
        return 0

def breakpoint(p_num,c_num):
    if (p_num == 0 and c_num ==0):
        if not os.path.exists(path + date_now + '.txt'):
            p_num = p_num
            c_num = c_num
        else:
            f = open(path + date_now + '.txt')
            arr = f.readlines()
            arr_list = []
            for item in arr:
                arr_list = item.split('\t')
            pulse_num_record = int(arr_list[0])
            chance_num_record = int(arr_list[1])
            if not (pulse_num_record and chance_num_record ):
                p_num = 0
                c_num = 0 
            else:
                p_num = pulse_num_record
                c_num = chance_num_record
    return p_num, c_num

def savenum(p_num,c_num):
    f = open(path + date_now + '.txt','w')
    f.write(str(p_num))
    f.write('\t')
    f.write(str(c_num))
    f.close()

def plot(series,midline):
    up = []
    down = []
    plt.plot(series.index,series['price'])
    plt.axhline(midline,color='k',linestyle='solid')
    for i in range(1,6):
        up.append(midline * ( 1+ i * grid) )
        down.append(midline * (1 - i * grid))
    for line in up:
        plt.axhline(line,color='r',linestyle='dashed')
    for line in down:
        plt.axhline(line,color='g',linestyle='dashed')
    plt.grid(True)
    plt.xlabel('ticks')
    plt.ylabel('price')
    plt.title('pulse:%d chance:%d' % (pulse_num,chance_num))
    plt.show()

def create_order(dirction,price,lot,open_time,G):
    order = []
    global order_num
    order_num += 1
    #订单编号,交易方向, 数量，建仓价格,开仓时间，平仓时间， 止盈价格,止损价格， 订单状态
    order.append(order_num)
    order.append(dirction)
    order.append(lot)
    order.append(price)
    order.append(open_time)
    order.append(None)
    if lot ==1:
        if dirction == 'sell':
            order.append(cut_minus_price(price * (1 - G)))
            order.append(cut_minus_price(price * (1 + 4 * G)))
        else:
            order.append(cut_plus_price(price * (1 + G)))
            order.append(cut_plus_price(price * (1 - 4 * G)))
    else:
        if dirction == 'sell':
            order.append(cut_minus_price(price * (1 - 3 *G)))
            order.append(cut_minus_price(price * (1 + 3 * G)))
        else:
            order.append(cut_plus_price(price * (1 + 3 * G)))
            order.append(cut_plus_price(price * (1 - 3 * G)))   
    order.append(True)
    return order

        
def change_order_status(order,tm,pr_cl):
    order[8] = False
    order[5] = tm
    order.append(pr_cl)

def close_buy_order(od,pr,tm):
    if pr >= od[6]:
        change_order_status(od,tm,od[6])
    elif pr <= od[7]:
        change_order_status(od,tm,od[7])

def close_sell_order(od,pr,tm):
    if pr <= od[6]:
        change_order_status(od,tm,od[6])
    elif pr >= od[7]:
        change_order_status(od,tm,od[7])

def close_order(order,price,tm):
    time_num = float(tm.split(':')[0] + '.' + tm.split(':')[1])
    if order[8]:
        if time_num <= 14.3:
            if order[1] == 'buy':
                close_buy_order(order,price,tm)
            else:
                close_sell_order(order,price,tm)

def close_modify_buy_order(od,pr,tm):
    if pr <= od[7]:
        change_order_status(od,tm,od[7])

def close_modify_sell_order(od,pr,tm):
    if pr >= od[7]:
        change_order_status(od,tm,od[7])

def close_modify_order(order,price,tm):
    time_num = float(tm.split(':')[0] + '.' + tm.split(':')[1])
    if order[8]:
        if order[1] == 'buy':
            close_modify_buy_order(order,price,tm)
        else:
            close_modify_sell_order(order,price,tm)
        
    

def modify_order(od,pr):
    if od[8]:
        if od[1] == 'buy':
            if (pr *(1 - 2 * grid)) > od[7]:
                od[7] += 0.01
        else:
            if (pr *(1 + 2 * grid)) < od[7]:
                od[7] -= 0.01
 
'''   
def close_order_old(order,price,tm):
    time_num = float(tm.split(':')[0] + '.' + tm.split(':')[1])
    if order[8]:
        if time_num <= 14.3:
            if (order[1] == 'buy' and price >= order[6]):
                order[8] = False
                order[5] = tm
                order.append(price)
            elif (order[1] == 'sell' and price <=order[6]):
                order[8] = False
                order[5] = tm
                order.append(price)
        elif  14.3< time_num and time_num < 15.0:
            if order[3] == 5:
                if (order[1] == 'buy' and price + 3 * grid >= order[6]):
                    order[8] = False
                    order[5] = tm
                    order.append(price)
                elif (order[1] == 'sell' and price -  3 * grid <=order[6]):
                    order[8] = False
                    order[5] = tm
                    order.append(price)
            else:
                if (order[1] == 'buy' and price + 2 *grid >= order[6]):
                    order[8] = False
                    order[5] = tm
                    order.append(price)
                elif (order[1] == 'sell' and price - 2 * grid <=order[6]):
                    order[8] = False
                    order[5] = tm
                    order.append(price)
'''
        
def auto_close_order(order,price,tm):
    if order[8]:
        order[8] = 'autoclosed'
        order[5] = tm
        if len(order)==9:
            order.append(price)


    

def calc_profit(dataSet):
    for item in dataSet:
        item.append(0.0)
        #print item
        item[10] = ((item[9] - item[3]) * item[2]) / item[3]
        if item[1] == 'sell':
            item[10] = -1 * item[10]
    return dataSet

def turn_dataframe(dataSet):
    df = pd.DataFrame(order_list,columns=['No','direction','lot','price_open',\
                                          'time_open','time_close','price_win', \
                                          'price_lose','status','price_close',\
                                          'profit_ratio'])
    df['status'] = df['status'].replace(False,'finished')
    df['cumsum'] = np.cumsum(df['profit_ratio']) / od_num
    return df
      
        
def get_hist_tick_data(code,date):
    df = ts.get_tick_data(code,date=date)
    df1 = df[['time','price','volume']]
    num = len(df1)
    df1.index = np.arange(num-1,-1,-1)
    df1 = df1.sort_index()
    return df1

def get_hist_day_data(code):
    df = ts.get_hist_data(code)
    return df

def manage_open_order(amount):
    if amount > 0:
        return True
    else:
        return False
        
def back_test(dataFrame,vol_amount):
    pulse_num = 0
    chance_num = 0
    time_stop_open_order = 14.3
    order_list = []
    num = len(dataFrame)
    for i in range(2,num+1,1):
        order_tem = []
        input_dataFrame = dataFrame[1:i]
        index_num = len(input_dataFrame)
        #print 'ticks numebers:',index_num
        volume_total = np.sum(input_dataFrame['volume'])
        signal,pulse_num = vwap(pulse_num,volume_total,vol_amount)
        price_now = input_dataFrame['price'][index_num]
        time_now = input_dataFrame['time'][index_num]
        time_num = float(time_now.split(':')[0] + '.' + time_now.split(':')[1])
        #print time_num
        if signal and time_num > 9.4 and time_num <= time_stop_open_order and manage_open_order(amount_order):
            order_tem,chance_num = trade_strategy(input_dataFrame,chance_num)
        if len(order_tem) > 0: 
            order_list.append(order_tem)
        for item in order_list:
            if time_num >= 14.59:
                auto_close_order(item,price_now,time_now)
            else:
                #close_order(item,price_now,time_now)
                modify_order(item,price_now)
                close_modify_order(item,price_now,time_now)
    return order_list

def calc_dpr(dataFrame,dpr_list,date):
    if len(dataFrame) > 1 :
        dp = dataFrame['cumsum'][len(dataFrame)-1]
        dpr_list.append([date,dp])
    return dpr_list

def make_folder(name):
    if not os.path.exists(name):
        os.mkdir(name)
        
def get_file_name_index_number(code,pth):
    num = 0
    l = os.listdir(pth+code+'\\')
    if len(l) < 1:
       num += 1
    else:
        arr = []
        for item in l:
            arr.append(int(item.split('.')[0].split('_')[-1]))
        num = np.array(arr).max()
        num += 1
    return num

#统计正常下单和趋势下单的胜率
def count_value(orderlist):
    fini_nm_num = 0.0
    fini_tr_num = 0.0
    auto_nm_num = 0.0
    auto_tr_num = 0.0
    for item in orderlist:
        if item[2] ==1:
            if item[8] == False :
                fini_nm_num += 1
            else:
                auto_nm_num += 1
        else:
            if item[8] == False:
                fini_tr_num += 1
            else:
                auto_tr_num += 1
    if (fini_nm_num + auto_nm_num) != 0:
        rate_nm = fini_nm_num / (fini_nm_num + auto_nm_num)
    else:
        rate_nm = 0.0
    if (fini_tr_num + auto_tr_num) != 0:
        rate_tr = fini_tr_num / (fini_tr_num + auto_tr_num)
    else:
        rate_tr = 0
    #item.extend((rate_nm,rate_tr))
                
    
  
dpr_list = []
dates = gen_date_list(date_start,date_end) # gen trading day list
make_folder(path+code)   # make stock folder at path
file_number = get_file_name_index_number(code,path) # file back index
print 'file_back_index_number:',file_number
day_data = get_hist_day_data(code) # stock history day data
for dt in dates:
    print 'date:',dt
    order_num = 0 
    amount_order = od_num
    tick_data = get_hist_tick_data(code,dt) # get tick data in spec day
    date_volume = gen_date_list2(dt,number_date_volume_avg) 
    volume_amount = calc_avg_volume_amount(day_data,date_volume,chance_num)   # calc  avg date volume
    if len(tick_data) > 10 :
        order_li = back_test(tick_data,volume_amount) # gen order list
        order_list = calc_profit(order_li) # calc profit
        count_value(order_list) # calc ratio success
        #print order_list
        df = turn_dataframe(order_list) # turn dataframe
        dpr_list = calc_dpr(df,dpr_list,dt) # turn day profit ratio
        df.to_csv(path + code+ '\\' + gen_name(code,dt) +'_'+ str(file_number) + '.csv') # save csv
        
funds = 1.0
for item in dpr_list:
    if item == dpr_list[0]:
        funds = funds + item[1]
        item.append(funds)
    else:
        funds = funds * (1 + item[1]) 
        item.append(funds)


nd_list = np.array(dpr_list)
plt.plot(nd_list[:,2])
print nd_list

#np.savetxt(path + code +'20160810.csv',np.array(order_list),fmt='%s,%s,%s,%s,%s,%s,%s,%s')
   
    
'''
if __name__ == '__main__':
    date_now = datetime.datetime.now().strftime('%Y%m%d')
    pulse_num = 0
    chance_num = 0
    while True:
        time_now = float(datetime.datetime.now().strftime('%H.%M'))
        print time_now

        if time_now < 9.3:
            print 'not ready for trading'
            time.sleep(60)
        elif (time_now >=11.31 and time_now < 12.59):
            print 'middle rest, please wait for a while'
            time.sleep(60)
            
        elif time_now > 15.01:
            print 'out of trading time'
            break
        else:
            try:
                pulse_num,chance_num = breakpoint(pulse_num,chance_num)
                series_reverse,series_pos = get_data(code)
                volume_total = np.sum(series_reverse['volume'])
                signal,pulse_num = vwap(pulse_num,volume_total)
                print series_reverse['price'][0]
                if signal:
                    chance_num = trade_strategy(chance_num)
                    print ' trading chance:',chance_num
                    savenum(pulse_num,chance_num)
                else:
                    print 'not reach the volume,please wait.'
            except Exception,e:
                print Exception,':',e
'''
            
'''       
order_num = 0
order_list = []
order_closed = []
order_unclosed = []
pulse_num = 0
chance_num = 0
time_stop_open_order = 14.3


num = len (tick_data)

for i in range(2,num+1,1):  
    #time.sleep(5)
    order_tem = []
    input_dataFrame = tick_data[1:i]
    index_num = len(input_dataFrame)
    print 'ticks numebers:',index_num
    volume_total = np.sum(input_dataFrame['volume'])
    signal,pulse_num = vwap(pulse_num,volume_total)
   # print signal
    price_now = input_dataFrame['price'][index_num]
    time_now = input_dataFrame['time'][index_num]
    time_num = float(time_now.split(':')[0] + '.' + time_now.split(':')[1])
    if signal and time_num <= time_stop_open_order and manage_open_order(amount_order):
        order_tem,chance_num = trade_strategy(input_dataFrame,chance_num)
    if len(order_tem) > 0: 
        order_list.append(order_tem)
    for item in order_list:
        if item[7]  and item not in order_unclosed :
            order_unclosed.append(item)
    for item in order_unclosed:
        if time_num == 15.0:
            auto_close_order(item,price_now)
           # print item
        else:
            close_order(item,price_now)
            #time.sleep(0.2)
            #print order_unclosed
    #print 'order_list:', order_list
'''