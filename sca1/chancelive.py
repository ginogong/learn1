import matplotlib.pyplot as plt
import tushare as ts
import numpy as np
import time
import datetime

path = 'E:\\WORK\\autodata\\data\\'
grid = 0.003
volume_amount = 500
code = '300017'

def vwap(num,volume):
    if volume  > (num + 1) * volume_amount :
        num += 1
        print 'try NO:',num
        return True,num
    else:
        return False,num
    time.sleep(3)

def trade_strategy(chance):
    price_now = series_reverse['price'][0]
    price_weight = calc_weight_price(series_reverse)
    if (price_now <= price_weight * (1 + 5 * grid) and price_now >= price_weight * (1 + 1 *grid) ):
         print ' \nlimit order sell 1lot'
         print 'order_sell at price - 0.01 and order_buy at price - grid - 0.01'
         chance += 1
         plot(series_pos,price_weight)
    elif (price_now <= price_weight * (1 - 1 * grid) and price_now >= price_weight * (1 -5 *grid) ):
        print '\nlimit order buy 1lot'
        print 'order_sell at price - 0.01 and order_buy at price - grid - 0.01'
        chance += 1
        plot(series_pos,price_weight)
    elif (price_now > price_weight * (1 - 1 * grid) and price_now < price_weight * (1 + 1 *grid)):
        print '\nno trading chance'
        plot(series_pos,price_weight)
    else:
        print '\n trending'
        volume_avg = np.mean(series_reverse['volume'])
        volume_recent = np.mean(series_revers['volume'].head(30))
        volume_power = calc_volume_power(volume_avg,volume_recent)
        if volume_power == 1:
            price_low = np.min(series_reverse['price'])
            price_high = np.max(series_reverse['price'])
            relative = calc_relative_positon(price_high,price_low,price_now)
            if relative >= 0.9:
                print '\nbuy at sell1 , 5 lot;sell at sell1 + grid , 5lot'
                chance += 1
                plot(series_pos,price_weight)
            elif relative <= 0.1:
                print '\nsell at buy1 , 5 lot; buy at buy1 - grid, 5lot'
                chance += 1
                plot(series_pos,price_weight)
            else:
                series_now_100 = series_reverse.head(100)
                price_weight100 = calc_weight_price(series_now_100)
                if (price_now <= price_weight100 * (1 + 5 * grid) and price_now >=  price_weight100 * (1 + 1 *grid) ):
                    print ' limit order sell 1lot'
                    print 'order_sell at price - 0.01 and order_buy at price - grid - 0.01'
                    chance += 1
                    plot(series_pos,price_weight100)
                elif (price_now <= price_weight100 * (1 - 1 * grid) and price_now >=  price_weight100 * (1 -5 *grid) ):
                    print '\nlimit order buy 1lot'
                    print '\norder_sell at price - 0.01 and order_buy at price - grid - 0.01'
                    chance += 1
                    plot(series_pos,price_weight100)
                else:
                    print '\n no tradint chance'
                    plot(series_pos,price_weight100)
    return chance
 
 
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
    if 3.0 * volume_avg < volume_recent:
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
