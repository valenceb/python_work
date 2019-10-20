import tkinter as tk, os
from io import BytesIO

from PIL import Image, ImageTk
import re
import urllib.request


def getHtml(url):
    try:
        page = urllib.request.urlopen(url)
        html = page.read()
        html = str(html)
        return html
    except urllib.error.HTTPError as e:
        print(e.reason)
        return False


def getAllImg(html):
    reg = r'src=\"(.{0,100}\.jpg)\"'
    imglist = re.findall(reg, html)
    return imglist


def getNvyouIDs(html):
    reg = r'/luyilu/(.{0,100}).html'
    nvyouIDList = re.findall(reg, html)
    nvyouIDList = list(map(int, nvyouIDList))
    nvyouIDList = list(set(nvyouIDList))
    nvyouIDList.sort()
    nvyouIDList.reverse()
    return nvyouIDList


def getImage(url):
    rq = urllib.request.Request(url)
    u = urllib.request.urlopen(rq)
    data = u.read()
    img = Image.open(BytesIO(data))
    if img.size[0] <= 430:
        return False
    return ImageTk.PhotoImage(img)


class PicSite:
    def __init__(self, url):
        self.url = url
        self.subUrl = ''
        self.nvyouIDs = getNvyouIDs(getHtml(url))
        self.image = ''
        self.nPerPage = 0

    def crawling_by_category(self):
        for nvyouID in self.nvyouIDs:
            self.subUrl = self.url + str(nvyouID) + '.html'
            # crawling(picSite)
            for value in range(1, 30):
                if value != 1:
                    self.subUrl = self.url + str(nvyouID) + '_' + str(value) + '.html'
                print("Crawling " + self.subUrl)
                srcHtml = getHtml(self.subUrl)
                if not srcHtml:
                    return False
                imglist = getAllImg(srcHtml)
                if len(imglist) > 0 and imglist[
                    0] == 'https://www.images.96xxpic.com:8819/allimg/161029/1-1610292146350-L.jpg':
                    return False
                #每页只显示三张
                self.nPerPage = 0
                for il in imglist:
                    self.nPerPage += 1
                    if self.nPerPage >= 4: break
                    photoImage = getImage(il)
                    if not photoImage: continue
                    yield photoImage
                    print("peek " + il)



class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.picSite = PicSite("https://96xx2019.com/luyilu/")
        self.crawlingGenerator = self.picSite.crawling_by_category()
        self.img = next(self.crawlingGenerator)
        self.createWidgets()

    def createWidgets(self):
        # self.btnPrev = tk.Button(self, text='Prev', command=self.prev)
        # self.btnPrev.pack(side=tk.TOP)
        self.btnNext = tk.Button(self, text='Next', command=self.next)
        self.btnNext.pack(side=tk.TOP)
        self.btnNext = tk.Button(self, text='Next Page', command=self.nextPage)
        self.btnNext.pack(side=tk.TOP)
        self.lblImage = tk.Label(self)
        self.lblImage['image'] = self.img
        self.lblImage.pack()

    # def prev(self):
    #     self.showfile(-1)

    def next(self):
        self.showfile()

    def nextPage(self):
        self.picSite.nPerPage = 4 #直接翻页
        self.showfile()

    def showfile(self):
        self.img = next(self.crawlingGenerator)
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
