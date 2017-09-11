#-*- coding:utf-8 -*-
import re
import os
import pickle
import datetime
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class BadmintonVenueOrder(object):
    def __init__(self):
        self.year = str(time.localtime()[0])
        self.nowday = str(time.localtime()[1])+str(time.localtime()[2])
        self.pattern = re.compile(r'^U([0-9]{3})\s+'+self.year+'\-(0[1-9]|1[0-2])\-(3[0-1]|2[0-9]|1[0-9]|0[1-9])\s(09|1[0-9]|2[0-1])\:00\~(09|1[0-9]|2[0-2])\:00\s([ABCD])(\sC){0,1}$')
        self.pw = os.getcwd()+'\/' if os.name == "nt" else os.getcwd()+'/'


    def getdata(self,List):
        """
        打开文件
        """
        data = open(self.pw+'orderdata.pkl','rb')
        dataNow = pickle.load(data)
        List.extend(dataNow)
        data.close()
        return List

    def savedata(self,List):
        """
        存储文件
        """
        data = open(self.pw+'orderdata.pkl','wb')
        pickle.dump(List,data,-1)
        data.close()


    def main(self,userInput):
        if userInput == " ":
            self.inquire()
        elif self.pattern.match(userInput):
            Pattern = self.pattern.match(userInput)
            if Pattern.group(7) == " C":
                mode = "C"
                self.cancle(Pattern)
            else:
                mode = "O"
                self.order(Pattern)
        else:
            print "Error: the booking is invalid"


    def cancle(self,Pattern):
        """
        取消预定
        """
        userId = Pattern.group(1)
        date = Pattern.group(2)+Pattern.group(3)
        timescale = Pattern.group(4)+Pattern.group(5)
        venue = Pattern.group(6)
        status = Pattern.group(7)
        try:
            ListforCancle = self.getdata([])
        except:
            print "Error: the booking being cancelled does not exist!"
            return
        for i in ListforCancle:

            if i['status'] == None and i['userId'] == userId and i['date'] == date and i['timescale'] == timescale and i['venue'] == venue:
                if i['weekday'] == "5" or i['weekday'] == '6':
                    i['money'] = int(int(i['money'])*0.25)
                else:
                    i['money'] = int(int(i['money'])*0.5)
                i['status'] = "C"
                self.savedata(ListforCancle)
                print "Success: the booking is accepted!"
                return
        print "Error: the booking being cancelled does not exist!"
        return


    def order(self,Pattern):
        """
        进行预定
        """
        userId = Pattern.group(1)
        date = Pattern.group(2)+Pattern.group(3)
        timescale = Pattern.group(4)+Pattern.group(5)
        venue = Pattern.group(6)
        status = Pattern.group(7)
    # 打开数据文件，并加载到orderNow列表中
        try:
            orderNow = self.getdata([])
        except:
            orderNow = []
    # 判断是否可写入,是否有时间的重叠
        samedayorder = []
        for i in orderNow:
            if i['date'] == date and i['venue'] == venue and i['status'] == None:#时间相同，场地相同，未被取消
                samedayorder.append(i)
        nowstart = int(timescale[0:2])
        nowend = int(timescale[2:])
        if nowstart >= nowend or int(date)<int(self.nowday) or (int(date)==int(self.nowday) and nowstart <= time.localtime()[3]):
            print "Error: the booking is invalid"
            return

    #判断时间重叠
        timeList = [i for i in range(nowstart,nowend)]
        for j in samedayorder: #j是从数据库中取出来的
            jnowstart = int(j['timescale'][0:2])
            jnowend = int(j['timescale'][2:])
            timerange = [i for i in range(jnowstart,jnowend)]
            if len([val for val in timerange if val in timeList]) > 0:
                print "Error: the booking conflicts with existing bookings! "
                return
    # 判断金额,先判断是周几，是那一天
        try:
            weekday = datetime.date(int(self.year),int(date[0:2]),int(date[2:])).weekday()
        except:
            print "Error: the booking is invalid"
            return
        money = 0
        if weekday == 5 or weekday == 6:
            for i in range(nowstart+1,nowend+1):
                if 9<=i<=12:
                    money += 40
                elif 12<i<=18:
                    money += 50
                else:
                    money += 60
        else:
            for i in range(nowstart+1,nowend+1):
                if 9<=i<=12:
                    money += 30
                elif 12<i<=18:
                    money += 50
                elif 18<i<=20:
                    money += 80
                else:
                    money += 60
    # 往列表中添加数据
        orderInfo = {'userId':userId,'weekday':weekday,'date':date,'timescale':timescale,'venue':venue,'status':status,'money':money}
        data = open(self.pw+'orderdata.pkl','wb')
        orderNow.append(orderInfo)
        pickle.dump(orderNow,data,-1)
        data.close()
        print "Success: the booking is accepted! "


    def inquire(self):
        """
        查询结果
        """
        #计算并打印
        try:  #如果没有数据
             resultList = self.getdata([])
        except:
            print "There is no date"
            return
        StrA = u"场地: A\n"
        StrB = u"场地: B\n"
        StrC = u"场地: C\n"
        StrD = u"场地: D\n"
        Amoney,Bmoney,Cmoney,Dmoney = 0,0,0,0
        resultList.sort(lambda a,b:int(a['date']+a['timescale'])-int(b['date']+b['timescale'])) #按时间排序
        for i in resultList:
            if i['status'] == "C":
                tip = u" 违约金"
            else:
                tip = u""
            dataStr = "%s-%s-%s %s:00~%s:00 %s %s元\n"%(self.year,i['date'][0:2],i['date'][2:],i['timescale'][0:2],i['timescale'][2:],tip,i['money'])
            if i['venue'] == "A":
                Amoney += int(i['money'])
                StrA += dataStr
            elif i['venue'] == "B":
                Bmoney += int(i['money'])
                StrB += dataStr
            elif i['venue'] == "C":
                Cmoney += int(i['money'])
                StrC += dataStr
            elif i['venue'] == "D":
                Dmoney += int(i['money'])
                StrD += dataStr
        print u"收入总汇 "
        print "---"
        StrA += u"小计: %d元\n\n"%Amoney
        StrB += u"小计: %d元\n\n"%Bmoney
        StrC += u"小计: %d元\n\n"%Cmoney
        StrD += u"小计: %d元\n\n"%Dmoney

        print StrA+StrB+StrC+StrD
        print "---"
        print u"总计:%d元"%(Amoney+Bmoney+Cmoney+Dmoney)
        return


if __name__ == '__main__':
    Order = BadmintonVenueOrder()
    while True:
        userInput = raw_input()
        if userInput == "quit":
            print u"谢谢您的使用！"
            break
        Order.main(userInput)
