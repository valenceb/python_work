import re
import urllib.request
import os
import time
from io import BytesIO
from PIL import Image

number = 1


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


def saveImages(imglist, name, nvyouID):
    global number
    for imageURL in imglist:
        splitPath = imageURL.split('.')
        fTail = splitPath.pop()
        if len(fTail) > 3:
            fTail = 'jpg'
        fileName = name + "/" + str(nvyouID) + '_' + ("%03d" % number) + "." + fTail
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
            print('Saving a pic named ', fileName)
            f.close()
        except urllib.error.HTTPError as e:
            print(imageURL)
            print(e.reason)
        number += 1


# get all the image url from html
def getAllImg(html):
    reg = r'src=\"(.{0,100}\.jpg)\"'
    imglist = re.findall(reg, html)
    return imglist


def crawling(url, path, nvyouID):
    print("Crawling " + url)
    srcHtml = getHtml(url)
    if not srcHtml:
        return False
    imglist = getAllImg(srcHtml)
    saveImages(imglist, path, nvyouID)
    return True


def crawling_by_category(url, index):
    global number
    number = 1
    crawling(url + str(index) + '.html', path, index)
    for value in range(2, 30):
        if not crawling(url + str(index) + '_' + str(value) + '.html', path, index): break


if __name__ == '__main__':
    url = "https://96xx2019.com/luyilu/"
    path = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    path = "output/luyilu_" + path
    mkdir(path)
    for value in range(1262, 1900):
        crawling_by_category(url, value)
    print("Process Completed Successfully.")
