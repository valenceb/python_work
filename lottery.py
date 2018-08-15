#coding=gbk
import csv
import random
import threading
import time
from tkinter import *

class myThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(myThread, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True
    def run(self):
        while self.__running.isSet():
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            process_data()
            time.sleep(0.1)
    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞
    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞
    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()        # 设置为False  
 
def process_data():
	if btn_var.get()!="开始抽奖":
		for var2Pos in entryVar:
			var2Pos.set(random.choice(emplist)[1])

def lottery_roller(btn_var):
	print (btn_var.get())
	if btn_var.get()=="开始抽奖":
		#print (str(exitFlag))
		btn_var.set("抽奖中")
		roll_thread.resume()
		print (btn_var.get())
	elif "继续抽奖"==btn_var.get():
		btn_var.set("抽奖中")
	elif "抽奖中"==btn_var.get():
		btn_var.set("继续抽奖")
		if len(entryVar)>0:
			luckyGuy = random.choice(emplist)
			entryVar[0].set(luckyGuy[1])
			entryVar.pop(0)
			emplist.remove(luckyGuy)

if __name__ == '__main__':
	#创建一个员工列表
	emplist = []
		#exitFlag = False
	#用with自动关闭文件
	with open('conf/emps.csv') as f:
		empf = csv.reader(f)
		for emp in empf:
			emplist.append(emp)
	
	root = Tk() # 初始化Tk()
	root.title("法拉公司年会抽奖")    # 设置窗口标题
	root.geometry("200x300")    # 设置窗口大小 注意：是x 不是*
	root.resizable(width=True, height=True) # 设置窗口是否可以变化长/宽，False不可变，True可变，默认为True
	
	btn_var = Variable()
	btn_var.set("开始抽奖")	
	entry = []
	entryVar = []
	
	#一个一等奖
	l1 = Label(root, text="一等奖", font=("Arial",12), width=8, height=3)
	l1.pack(side=TOP)   # 这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM
	entryVar.append(Variable())
	entryVar[len(entry)-1].set("未开奖")
	entry.append(Entry(root,textvariable=entryVar[len(entry)-1]))
	entry[len(entry)-1].pack(side=TOP)
	
	#三个二等奖
	l2 = Label(root, text="二等奖", font=("Arial",12), width=8, height=3)
	l2.pack(side=TOP)
	for num in range(1,4):
		entryVar.append(Variable())
		currentPos = len(entryVar)-1
		entryVar[currentPos].set("未开奖")
		entry.append(Entry(root,textvariable=entryVar[currentPos]))
		entry[len(entry)-1].pack(side=TOP)
	
	roll_thread=myThread()
	roll_thread.start()
	roll_thread.pause()
	
	btn1 = Button(root, textvariable=btn_var, background='yellow',command=lambda : lottery_roller(btn_var), width=30)
	btn1.pack(side=BOTTOM)
	root.mainloop() # 进入消息循环
