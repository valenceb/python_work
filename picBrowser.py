import tkinter as tk, os
from PIL import Image, ImageTk

class Application(tk.Frame):
    def __init__(self, master=None):
        self.files = os.listdir(r'D:\Picture')
        self.index = 0
        img = Image.open(r'D:\Picture' + '\\' + self.files[self.index])  # 打开图片
        self.img = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        # self.f = tk.Frame()
        # self.f.pack()
        self.btnPrev = tk.Button(self, text='Prev', command=self.prev)
        self.btnPrev.pack(side=tk.LEFT)
        self.btnNext = tk.Button(self, text='Next', command=self.next)
        self.btnNext.pack(side=tk.RIGHT)
        self.lblImage = tk.Label(self)
        self.lblImage['image'] = self.img
        self.lblImage.pack()

    def prev(self):
        self.showfile(-1)

    def next(self):
        self.showfile(1)

    def showfile(self, n):
        self.index += n
        if self.index < 0:
            self.index = len(self.files) - 1
        if self.index > (len(self.files) - 1):
            self.index = 0
        img = Image.open(r'D:\Picture' + '\\' + self.files[self.index])
        self.img = ImageTk.PhotoImage(img)
        self.lblImage['image'] = self.img


if __name__ == '__main__':
    # 设置背景颜色
    bgcolor = '#000000'
    root = tk.Tk()
    root.title('简易图片浏览器')
    root.configure(bg=bgcolor)

    # 窗口最大化
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.geometry("%dx%d" % (w, h))

    app = Application(master=root)
    app.mainloop()
