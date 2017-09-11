### 羽毛球馆预定管理—说明

****
* 项目组成


###### ballorder.py  
主体文件，功能函数与类都在该文件中。其中order()函数负责用户预定， inquire()负责查询， cancle()函数负责用户取消预定，getdata()负责从orderdata.pkl文件中取出序列化的文件。
   
###### test_ballorder.py   
测试文件

###### orderdata.pkl 

项目序列化的数据放在此文件中，序列化对象为字典，键包括 

用户Id:userId, 日期:date, 时间段:timescale,场馆:venue,星期:weekday,金额:money,状态:status,

***

* 命令介绍

###### 打开项目

进入文件夹中，输入命令``` python ballorder.py```
即可启动项目

###### 用户预定
    
用户进入项目后输入```U123 2017-09-12 12:00~14:00 A```表明用户U123预定2017年9月12日中午12点到下午14点的A羽毛球场馆。

```
说明
1.用户只能输入与该格式相同的预约语句，格式不同则会报错.
2.输入条件应符合逻辑，不符合逻辑也会判做错误输出，比如用户只能输入今年的晚于今天时刻的整点时间，结束时间必须晚于开始时间.
3.用户预约时间与场地发生冲突则会提示'Error: the booking conflicts with existing bookings!',此时用户应该修改时间，再次预约.
4.输入错误会出现错误反馈`Error: the booking is invalid',成功则会提示'Success: the booking is accepted!'
```
###### 取消预约

用户可输入```U123 2017-09-12 12:00~14:00 A C```来取消预约，该条语句表示用户U123将取消预定2017年9月12日中午12点到下午14点的A羽毛球场馆.

```
说明
1.用户只能输入与该格式相同的预约语句，格式不同则会报错.
2.必须用户名，订单日期，时间，场地均相符且订单状态为未取消的状态下，才可以取消订单成功，并提示'Success: the booking is accepted!',否则报错"Error: the booking being cancelled does not exist!"
```
###### 用户查询

输入一个空格即可查询场馆预约情况，输入多个空格或其他字符则会被认定为非法字符，提示```Error: the booking is invalid```



###### 用户退出
用户输入```quit```即可退出管理界面，输入其他字符无效


 

*****
* 修改意见


***
* 关于测试


README
测试
跨平台
并发问题