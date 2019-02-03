import re
import urllib.request
import os
import time
from io import BytesIO
from PIL import Image


class PicSite:
    def __init__(self, url):
        self.url = url
        self.subUrl = ''
        self.picCount = 1
        self.nvyouID = 1
        path = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        path = "output/luyilu_" + path
        self.path = path

    def getDomain(self):
        reg = '(https://.+?)/.+'
        dmn = re.findall(reg, self.url)
        if len(dmn) > 0:
            dmnstr = dmn[0]
            return dmnstr
        else:
            return self.url


def getHtml(url):
    try:
        page = urllib.request.urlopen(url)
        html = page.read()
        html = str(html)
        return html
    except urllib.error.HTTPError as e:
        print(e.reason)
        return False


def mkdir(path):
    path = path.strip()
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print("Created file directory at " + path)
        return True
    else:
        print(path + ' created successfully.')
        return False


def saveImages(imglist, picSite):
    for imageURL in imglist:
        splitPath = imageURL.split('.')
        fTail = splitPath.pop()
        imageURL = imageURL if imageURL[0:4] == "http" else picSite.getDomain() + imageURL
        print(imageURL)
        if len(fTail) > 3:
            fTail = 'jpg'
        fileName = picSite.path + "/" + str(picSite.nvyouID) + '_' + ("%03d" % picSite.picCount) + "." + fTail
        try:
            rq = urllib.request.Request(imageURL)
            u = urllib.request.urlopen(rq)
            data = u.read()
            try:
                im = Image.open(BytesIO(data))
            except Exception as err:
                print(err)
            if im.size[0] <= 430:
                return
            f = open(fileName, 'wb+')
            f.write(data)
            print('Saving a pic named', fileName)
            f.close()
        except urllib.error.HTTPError as e:
            print(imageURL)
            print(e.reason)
        picSite.picCount += 1


# get all the image url from html
def getAllImg(html):
    reg = r'src=\"(.{0,100}\.jpg)\"'
    imglist = re.findall(reg, html)
    return imglist


def crawling(picSite):
    print("Crawling " + picSite.subUrl)
    srcHtml = getHtml(picSite.subUrl)
    if not srcHtml:
        return False
    imglist = getAllImg(srcHtml)
    if len(imglist) > 0 and imglist[0] == 'https://www.images.96xxpic.com:8819/allimg/161029/1-1610292146350-L.jpg':
        return False
    saveImages(imglist, picSite)
    return True


def crawling_by_category(picSite):
    picSite.picCount = 1
    picSite.subUrl = picSite.url + str(picSite.nvyouID) + '.html'
    # crawling(picSite)
    for value in range(1, 30):
        if value != 1:
            picSite.subUrl = picSite.url + str(picSite.nvyouID) + '_' + str(value) + '.html'
        if not crawling(picSite): break


if __name__ == '__main__':
    picSite = PicSite("https://96xx2019.com/luyilu/")
    mkdir(picSite.path)
    for value in range(3298, 4000):
        picSite.nvyouID = value
        crawling_by_category(picSite)
    print("Process Completed Successfully.")
