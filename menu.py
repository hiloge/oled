# MicroPython menu driver on ssd1306 interfaces
#Code By WMD 2019-4-16 21:18:28
from micropython import const
import ssd1306

class menu:
    #global m
    def __init__(self,display,x,y,w,h):
        '''
        Init menu bar area in a screen.
        Arg display is the ssd1306 object
        X and y is the start point of the screen
        w and h set the width and height of the menu.w 和 h 设置菜单的宽度和高度。
        Tips: You can create a menu area which not use all of the screen space,so that you can use remaining area to display other views.
        Warning: This area couldn't bigger than the screen display area
        '''
        self.display=display   #ssd1306 object，就是建的对象oled
        self.hightlightnum=0
        self.widthlightnum=0
        self.menux=x
        self.menuy=y
        self.menuw=w
        self.menuh=h
    def initText(self,TextList,offset=0,widthlightnum=0,hightlightnum=0):
        '''
        Init menuText in menu bar.
        this function will refresh menu area to new TextList
        arg TextList should be a list. The first element is the text to display, and the second element is 
        arg offset is use to display middle parts of the menu.                 偏移量用于显示菜单的中间部分。
        the command.When submenu is needed, the command should be 'initText(theSubTextList)'
        '''
        self.display.fill_rect(self.menux,self.menuy,self.menuw,self.menuh,0) #clear old menu
        self.menuoffset=offset #Save offset value
        self.nowlist=TextList
        for i in range(len(TextList)):
            if (i+1)*10>self.menuh:    #Text is out of range   高度
                break
            elif len(self.nowlist[offset+i][1]) != 0 :
                self.display.text(TextList[i+offset][0],self.menux+1,self.menuy+i*10+1,1)  #[0]代表Text里面，第一个是用来显示的菜单名称
                self.display.text(TextList[i+offset][1],self.menux+65,self.menuy+i*10+1,1)  #[1]代表Text里面，第二个是用来显示的数据 
            else:
                self.display.text(TextList[i+offset][0],self.menux+1,self.menuy+i*10+1,1)  #[0]代表Text里面，第一个是用来显示的菜单名称     
        self.moveHighLight(widthlightnum,hightlightnum)
        
    def rushTest(self):     #刷新显示
        self.initText(self.nowlist,self.menuoffset,self.widthlightnum,self.hightlightnum)
        self.moveHighLight(self.widthlightnum,self.hightlightnum)
        
    def moveHighLight(self,xnum,ynum):   #显示并移动方框亮的上下左右位置
        '''
        Select HightLight num 
        The argument num is relative the manu bar, not equal to Selected element
        '''
        self.display.rect(self.menux + self.widthlightnum*64, self.menuy+self.hightlightnum*10, 64, 10,0) #  self.menuw   clear old rect  #这里的hightlightnum还是上一次的，没有更新，所以把上一次的清除了
        self.widthlightnum=xnum
        self.hightlightnum=ynum                                                            #更新方框位置，这个标志可以用来确认现在选择的是哪个选项框，这样就可以选择对应的菜单
        self.display.rect(self.menux + self.widthlightnum*64, self.menuy+self.hightlightnum*10, 64, 10,1) #set new rect      
        self.display.show()
    
    def arrowShow(self):
        self.rushTest()
        self.display.hline(self.menux + self.widthlightnum*110, self.menuy+self.hightlightnum*10+5, 16,1)
        self.display.line(self.menux + self.widthlightnum*110, self.menuy+self.hightlightnum*10+5, self.menux + self.widthlightnum*115, self.menuy+self.hightlightnum*10+1,1)
        self.display.line(self.menux + self.widthlightnum*110, self.menuy+self.hightlightnum*10+5, self.menux + self.widthlightnum*115, self.menuy+self.hightlightnum*10+8,1)
        self.display.show()
        
    def arrowClose(self):
        self.rushTest()
        self.display.hline(self.menux + self.widthlightnum*110, self.menuy+self.hightlightnum*10+5, 16,0)
        self.display.line(self.menux + self.widthlightnum*110, self.menuy+self.hightlightnum*10+5, self.menux + self.widthlightnum*115, self.menuy+self.hightlightnum*10+1,0)
        self.display.line(self.menux + self.widthlightnum*110, self.menuy+self.hightlightnum*10+5, self.menux + self.widthlightnum*115, self.menuy+self.hightlightnum*10+8,0)
        self.display.show()    
        
    def moveRight():    #按键后光标右移       
        pass
            
    def moveLift():    #按键后光标左移
        pass    
        
    def moveDown(self):   #方框下移，用户操作使用的函数
        '''
        User function.
        Make menu downside one element
        '''
        #先判断左右，再判断上下
        if self.widthlightnum == 0 :
            if len(self.nowlist[self.menuoffset+self.hightlightnum][1]) != 0:
                self.moveHighLight(self.widthlightnum + 1 , self.hightlightnum)
                return
            else:
                if(self.menuoffset+self.hightlightnum == len(self.nowlist)-1): ## equal to max value向下移动到等于最大值，到底了
                    return
                if (self.hightlightnum+2)*10>self.menuh: #Text is out of range
                    self.initText(self.nowlist,self.menuoffset+1,self.widthlightnum,self.hightlightnum) #refresh the Text List  刷新到下个页面,只下移一个，因为menuoffset只加1而已
                    return
                else:
                    self.moveHighLight(self.widthlightnum,self.hightlightnum+1)   
                    return
                
        elif self.widthlightnum == 1 :
            if(self.menuoffset+self.hightlightnum == len(self.nowlist)-1): ## equal to max value向下移动到等于最大值，到底了
                return
            if (self.hightlightnum+2)*10>self.menuh: #Text is out of range
                #self.display.rect(self.menux + self.widthlightnum*64, self.menuy+self.hightlightnum*10, 64, 10,0)  #先清除之前的光标
                self.initText(self.nowlist,self.menuoffset+1,self.widthlightnum-1,self.hightlightnum) #refresh the Text List  刷新到下个页面,只下移一个，因为menuoffset只加1而已 
                return               
            else:
                self.moveHighLight(self.widthlightnum-1,self.hightlightnum+1)
                return
    def moveUp(self):    #方框上移，用户操作使用的函数
        '''
        User function.
        Make menu upside one element
        '''
        #先判断左右，再判断上下
        if self.widthlightnum == 0 :
            if(self.menuoffset+self.hightlightnum == 0): ## equal to min value
                return
            if len(self.nowlist[self.menuoffset+self.hightlightnum-1][1])  != 0:     
                if self.hightlightnum==0: #Text is out of range
                    #self.display.rect(self.menux + self.widthlightnum*64, self.menuy+self.hightlightnum*10, 64, 10,0)  #先清除之前的光标
                    
                    self.initText(self.nowlist,self.menuoffset-1,self.widthlightnum+1,self.hightlightnum) #refresh the Text List
                    return
                else:                   
                    self.moveHighLight(self.widthlightnum+1,self.hightlightnum-1)
                    return
            elif len(self.nowlist[self.menuoffset+self.hightlightnum-1][1])  == 0:
                if self.hightlightnum==0:
                    self.initText(self.nowlist,self.menuoffset-1,self.widthlightnum,self.hightlightnum)     
                    return  
                else:
                    self.moveHighLight(self.widthlightnum,self.hightlightnum-1)
                    return
        elif self.widthlightnum == 1 :
            self.moveHighLight(self.widthlightnum-1,self.hightlightnum)
            return
                

    def click(self):    #确认按键，用户操作使用的函数
        '''
        User function.
        run the selected element command.
        '''
        #if self.nowlist[self.menuoffset+self.hightlightnum][1][0]=='@': #this point to another menu
        #    tmp=self.nowlist[self.menuoffset+self.hightlightnum][1].lstrip('@')
        #    self.initText() 
        eval(self.nowlist[self.menuoffset+self.hightlightnum][2])    #这里的[1]只能到二级菜单，不能到再下一级菜单。考虑后续改成菜单等级标志符。不对，看下面一行
        self.display.show()                                                              #这个菜单因为已经更新，所以再进入下一级菜单，还是nowlist的[1]的内容
        
    def clickSpecial(self):      #特色（长按）确认按键，用户操作使用的函数。
        '''
        User function.
        run the selected element command.
        it can be use like a "long press"
        '''
        if len(self.nowlist[self.menuoffset+self.hightlightnum]) > 3 :   #从这个菜单进入同级别的另一个菜单。比如两个不同密码的设置界面，如果密码A则进入[1]菜单，密码B则进入[2]菜单
            eval(self.nowlist[self.menuoffset+self.hightlightnum][3])
            self.display.show() 
            
