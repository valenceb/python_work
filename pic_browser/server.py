from flask import Flask, render_template, session, redirect, url_for
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
    size = len(BytesIO(data).read())
    if size <= 19900:
        return False
    return url


class PicSite:
    def __init__(self, url):
        self.url = url
        self.subUrl = ''
        self.nvyouIDs = getNvyouIDs(getHtml(url))
        self.image = ''
        self.nPerPage = 0
        self.locker = False

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
                    continue
                imglist = getAllImg(srcHtml)
                if len(imglist) > 0 and imglist[
                    0] == 'https://www.images.96xxpic.com:8819/allimg/161029/1-1610292146350-L.jpg':
                    continue
                # 每页只显示三张
                self.nPerPage = 0
                for il in imglist:
                    self.nPerPage += 1
                    if self.nPerPage >= 4: break
                    photoImage = getImage(il)
                    if not photoImage: continue
                    yield photoImage
                    print("peek " + il)


app = Flask(__name__)
app.secret_key = '123456'
picSite = PicSite("https://96xx2019.com/luyilu/")
crawler = picSite.crawling_by_category()


@app.route('/')
def PeterParker():
    return redirect(url_for('PeterParker_next'))


@app.route('/next')
def PeterParker_next():
    if not picSite.locker:
        picSite.locker = True
        img = next(crawler)
        picSite.locker = False
        return render_template('default.html', picSource=img)
    return "Loading..."

@app.route('/nextpage')
def PeterParker_nextpage():
    picSite.nPerPage = 4
    if not picSite.locker:
        picSite.locker = True
        img = next(crawler)
        picSite.locker = False
        return render_template('default.html', picSource=img)
    return "Loading..."


if __name__ == '__main__':
    app.run(port=5000, debug=True)
