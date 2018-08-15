#coding=gbk
import csv
import random
import threading
import time
from tkinter import *

class myThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(myThread, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()     # ������ͣ�̵߳ı�ʶ
        self.__flag.set()       # ����ΪTrue
        self.__running = threading.Event()      # ����ֹͣ�̵߳ı�ʶ
        self.__running.set()      # ��running����ΪTrue
    def run(self):
        while self.__running.isSet():
            self.__flag.wait()      # ΪTrueʱ��������, ΪFalseʱ����ֱ���ڲ��ı�ʶλΪTrue�󷵻�
            process_data()
            time.sleep(0.1)
    def pause(self):
        self.__flag.clear()     # ����ΪFalse, ���߳�����
    def resume(self):
        self.__flag.set()    # ����ΪTrue, ���߳�ֹͣ����
    def stop(self):
        self.__flag.set()       # ���̴߳���ͣ״̬�ָ�, ����Ѿ���ͣ�Ļ�
        self.__running.clear()        # ����ΪFalse  
 
def process_data():
	if btn_var.get()!="��ʼ�齱":
		for var2Pos in entryVar:
			var2Pos.set(random.choice(emplist)[1])

def lottery_roller(btn_var):
	print (btn_var.get())
	if btn_var.get()=="��ʼ�齱":
		#print (str(exitFlag))
		btn_var.set("�齱��")
		roll_thread.resume()
		print (btn_var.get())
	elif "�����齱"==btn_var.get():
		btn_var.set("�齱��")
	elif "�齱��"==btn_var.get():
		btn_var.set("�����齱")
		if len(entryVar)>0:
			luckyGuy = random.choice(emplist)
			entryVar[0].set(luckyGuy[1])
			entryVar.pop(0)
			emplist.remove(luckyGuy)

if __name__ == '__main__':
	#����һ��Ա���б�
	emplist = []
		#exitFlag = False
	#��with�Զ��ر��ļ�
	with open('conf/emps.csv') as f:
		empf = csv.reader(f)
		for emp in empf:
			emplist.append(emp)
	
	root = Tk() # ��ʼ��Tk()
	root.title("������˾���齱")    # ���ô��ڱ���
	root.geometry("200x300")    # ���ô��ڴ�С ע�⣺��x ����*
	root.resizable(width=True, height=True) # ���ô����Ƿ���Ա仯��/��False���ɱ䣬True�ɱ䣬Ĭ��ΪTrue
	
	btn_var = Variable()
	btn_var.set("��ʼ�齱")	
	entry = []
	entryVar = []
	
	#һ��һ�Ƚ�
	l1 = Label(root, text="һ�Ƚ�", font=("Arial",12), width=8, height=3)
	l1.pack(side=TOP)   # �����side���Ը�ֵΪLEFT  RTGHT TOP  BOTTOM
	entryVar.append(Variable())
	entryVar[len(entry)-1].set("δ����")
	entry.append(Entry(root,textvariable=entryVar[len(entry)-1]))
	entry[len(entry)-1].pack(side=TOP)
	
	#�������Ƚ�
	l2 = Label(root, text="���Ƚ�", font=("Arial",12), width=8, height=3)
	l2.pack(side=TOP)
	for num in range(1,4):
		entryVar.append(Variable())
		currentPos = len(entryVar)-1
		entryVar[currentPos].set("δ����")
		entry.append(Entry(root,textvariable=entryVar[currentPos]))
		entry[len(entry)-1].pack(side=TOP)
	
	roll_thread=myThread()
	roll_thread.start()
	roll_thread.pause()
	
	btn1 = Button(root, textvariable=btn_var, background='yellow',command=lambda : lottery_roller(btn_var), width=30)
	btn1.pack(side=BOTTOM)
	root.mainloop() # ������Ϣѭ��
