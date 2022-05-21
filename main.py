#main.py
import pyb
import time
from ssd1306 import SSD1306_SPI
from machine import Pin
import menu
#import _thread   #没有线程模块

#全局设定内容可以放到一个模块中
oled_SPI=pyb.SPI(1) #edit to your IIC OLED Pin
oled=SSD1306_SPI(128,64,oled_SPI,Pin('Y9'),Pin('Y10'),Pin('Y11')) #edit to your IIC OLED DPI
oled.fill(0xff)
global m,a,change_value_Flage  #声明全局变量，且要求初始化要在函数外
change_value_Flage = 0
def write_file(write_dic):   #文件写入字典,把字典转化为str
    f = open('1.txt', 'w+') #以写的方式打开一个文件，没有该文件就自动新建
    f.write(str(write_dic)) #写入数据,把字典转化为str
    f.close() #每次操作完记得关闭文件

def read_file():
    file = open("1.txt", "r+")
    read_dic = eval(file.read())   #读取的str转换为字典
    file.close()
    return read_dic

def get_num(a):
    #print('a',a)
    dictAll=read_file()
    val=dictAll[a]
    return val,dictAll
#初始上电时，判断文件是否存在，若存在，不写入原始初始值，并读取文件
#set_value = {'a': 1, 'b': 2, 'c': 3}
#write_file(set_value)

def minusOne(a):  #显示数据-1
    num,dictAll = get_num(a)
    num = num-1
    print("*******num is:",num)
    dictAll[a]= num
    print("*******dictAll['a'] is:",dictAll[a])
    write_file(dictAll)
    return num

def plusOne(a):  #显示数据+1
    num,dictAll = get_num(a)
    num = num+1
    print("*******num is:",num)
    dictAll[a]= num
    print("*******dictAll['a'] is:",dictAll[a])
    write_file(dictAll)
    
m = menu.menu(oled,0,0,128,64) 
#主界面显示，考虑不保存到文件中
# maintext=[['Temp',str(get_ontime_value('Temp'))],
#           ['Press',str(get_ontime_value('Press'))],
#           ['Flow',str(get_ontime_value('Flow'))],
#           ]
text=[['music','','print("perform a music1")'],
        ['photo','','m.initText(subtext)','print("Special click detacted")'],
        ['game','a'],
        ['mam','k'],
        ['google','g'],
        ['meer','a'],
        ['mamer','k'],
        ['gobb','','m.initText(subtext)']
              ]    
subtext=[['back','','m.initText(text)'],
            ['a',str(get_num('a')[0])],   #按确定进入数据加减模式 m.moveRight()
            ['b',str(get_num('b')[0])],   #按确定进入数据加减模式 m.moveRight()
            ['c',str(get_num('c')[0])],   #按确定进入数据加减模式 m.moveRight()
        ]#显示a的数值，str格式  
m.initText(text,0,0,0) # main menu 

def main():
    global change_value_Flage
    led_red = pyb.LED(1)      
    LED_D12 = Pin('X12',Pin.OUT_PP)  
    time.sleep_ms(200)
    LED_D12.low()
    btn_1 = Pin('X1', Pin.IN , Pin.PULL_UP)
    btn_2 = Pin('X2', Pin.IN , Pin.PULL_UP)
    btn_3 = Pin('X3', Pin.IN , Pin.PULL_UP)
    print(btn_1.value())
    while(True):
        led_red.toggle() 
        if btn_3.value()==0:  # 按下 下
            time.sleep_ms(120)
            if btn_3.value()==0:  # 按下 下
                if change_value_Flage == 1 :
                    minusOne(m.nowlist[m.menuoffset+m.hightlightnum][0])
                    m.nowlist[m.menuoffset+m.hightlightnum][1] = str(get_num(m.nowlist[m.menuoffset+m.hightlightnum][0])[0]) 
                    m.arrowShow()                    
                elif change_value_Flage == 0 :
                    m.moveDown()
                    m.rushTest() #元素写入后需要刷新显示  
                LED_D12.high()
                print("nowTest=",m.nowlist[m.menuoffset+m.hightlightnum],"offset=",m.menuoffset,"widthlightnum=",m.widthlightnum,"hightlightnum=",m.hightlightnum)
                #执行自定义函数
                #可以判断按键时长，进行特殊操作       

        elif btn_2.value()==0:  # 按下 上
            time.sleep_ms(120)
            if btn_2.value()==0:  # 按下 下
                if change_value_Flage == 1 :
                    plusOne(m.nowlist[m.menuoffset+m.hightlightnum][0])
                    m.nowlist[m.menuoffset+m.hightlightnum][1] = str(get_num(m.nowlist[m.menuoffset+m.hightlightnum][0])[0])
                    m.arrowShow
                elif change_value_Flage == 0 :
                    m.moveUp()
                    m.rushTest() #元素写入后需要刷新显示  
                #print(btn_1.value())
                LED_D12.low()
                print("nowTest=",m.nowlist[m.menuoffset+m.hightlightnum],"offset=",m.menuoffset,"widthlightnum=",m.widthlightnum,"hightlightnum=",m.hightlightnum)
        elif btn_1.value()==0:  # 按下 确定
            time.sleep_ms(120)
            if btn_1.value()==0:  # 按下 下
                LED_D12.low()
                #判断在value那列吗？
                if m.widthlightnum == 1 :
                    if change_value_Flage== 0 :
                        change_value_Flage = 1  
                        print('change_value_Flage== 1')
                        m.arrowShow()
                    elif change_value_Flage== 1 :  
                        change_value_Flage = 0
                        print('change_value_Flage== 0')
                        m.arrowClose()
                elif m.widthlightnum == 0 and len(m.nowlist[m.menuoffset+m.hightlightnum])  > 2 :
                    m.click()   
                    m.rushTest()        #元素写入后需要刷新显示 
                    print("nowTest=",m.nowlist[m.menuoffset+m.hightlightnum],"offset=",m.menuoffset,"widthlightnum=",m.widthlightnum,"hightlightnum=",m.hightlightnum)
                else:
                    print('nothing')

            #print("nowTest=",m.nowlist[m.menuoffset+m.hightlightnum],"offset=",m.menuoffset,"widthlightnumlightnum=",m.widthlightnum,"hightlightnum=",m.hightlightnum)
        #m.nowlist[m.hightlightnum][0] = 'a='+str(set_num["a"])  #由于Text是列表，需要更新列表的方式是向对应的元素写入                 
                
        #m.initText(m.nowlist,m.menuoffset,m.widthlightnum,m.hightlightnum)   
        #time.sleep_ms(200)
        
            
if __name__ == '__main__':
    main() 