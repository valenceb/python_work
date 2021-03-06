from flask import Flask, render_template, redirect, url_for, request
import re
import urllib.request
from io import BytesIO


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
    reg = r'src=\"(.{0,100}\.jpg)\" />'
    imglist = re.findall(reg, html)
    return imglist


def getNvyouIDs(html, category):
    reg = r'/'+category+'/(.{0,100}).html'
    nvyouIDList = re.findall(reg, html)
    nvyouIDList = list(map(int, nvyouIDList))
    nvyouIDList = list(set(nvyouIDList))
    nvyouIDList.sort()
    return nvyouIDList


def getImage(url):
    rq = urllib.request.Request(url)
    u = urllib.request.urlopen(rq)
    data = u.read()
    size = len(BytesIO(data).read())
    if size <= 19900:
        return False
    return url


class PicSite:
    def __init__(self, url):
        self.url = url
        self.subUrl = ''
        self.category = ''
        self.nvyouIDs = None
        self.nextNvYou = False
        self.locker = False

    def crawling_by_category(self):
        while (True):
            if not self.category:
                self.category = 'luyilu'
            if not self.nvyouIDs:
                self.nvyouIDs = getNvyouIDs(getHtml(self.url + self.category + "/"), self.category)
            nvyouID = self.nvyouIDs.pop()
            self.subUrl = self.url + self.category + "/" + str(nvyouID) + '.html'
            print("Current NvyouID: " + str(nvyouID))
            for value in range(1, 30):
                if value != 1:
                    self.subUrl = self.url + self.category + "/" + str(nvyouID) + '_' + str(value) + '.html'
                print("Crawling " + self.subUrl)
                srcHtml = getHtml(self.subUrl)
                if self.nextNvYou:
                    self.nextNvYou = False
                    break
                if not srcHtml:
                    break
                imglist = getAllImg(srcHtml)
                if not imglist:
                    break
                yield imglist


app = Flask(__name__)
app.secret_key = '123456'
picSite = PicSite("https://96jj.net/")
crawler = picSite.crawling_by_category()


@app.route('/')
def PeterParker():
    return redirect(url_for('PeterParker_next'))


@app.route('/next', methods=['post','get'])
def PeterParker_next():
    c = request.args.get('c')
    p = request.args.get('p')
    if p or c:
        #If new id requested, break the current one.
        if picSite.nvyouIDs:
            picSite.nextNvYou = True
        #Set the value to p/c respectively.
        picSite.category = c
        if p:
            p = int(p)
            picSite.nvyouIDs = list(range(p, p+51))
            picSite.nvyouIDs.reverse()
            print (picSite.nvyouIDs)
        else:
            picSite.nvyouIDs = p

    if not picSite.locker:
        picSite.locker = True
        displayImg = next(crawler)
        picSite.locker = False
        return render_template('default.html', picSource=displayImg)
    return "Loading..."

@app.route('/nextpage')
def PeterParker_nextpage():
    picSite.nextNvYou = True
    if not picSite.locker:
        picSite.locker = True
        img = next(crawler)
        picSite.locker = False
        return render_template('default.html', picSource=img)
    return "Loading..."


if __name__ == '__main__':
    app.run(port=5000, debug=False)
