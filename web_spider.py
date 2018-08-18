import re
import urllib.request
import os
import time
from io import BytesIO
from PIL import Image


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


def saveImages(imglist, name):
    number = 1
    for imageURL in imglist:
        splitPath = imageURL.split('.')
        fTail = splitPath.pop()
        fName = splitPath.pop().split('/').pop()
        if len(fTail) > 3:
            fTail = 'jpg'
        fileName = name + "/" + fName + str(number) + "." + fTail
        try:
            # header = {'Host':'96xxnet1.com',  
            #         'Connection':'keep-alive',  
            #         'Cache-Control':'max-age=0',  
            #         'Accept': 'text/html, */*; q=0.01',  
            #         'X-Requested-With': 'XMLHttpRequest',  
            #         'useragent' : 'User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',  
            #         'DNT':'1',  
            #         'Referer': 'http://96xxnet1.com/',  
            #         'Accept-Encoding': 'gzip, deflate, sdch',  
            #         'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6'}
            rq = urllib.request.Request(imageURL)
            u = urllib.request.urlopen(rq)
            data = u.read()
            try:
                im = Image.open(BytesIO(data))
            except Exception as err:
                print(err)
            if im.size[0] < 300:
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


def crawling(url, path):
    print("Crawling " + url)
    srcHtml = getHtml(url)
    if not srcHtml:
        return False
    mkdir(path)
    imglist = getAllImg(srcHtml)
    # print(imglist)
    saveImages(imglist, path)
    return True


def getDomain(urlstr):
    reg = '(http://.+?)/.+'
    dmn = re.findall(reg, urlstr)
    if len(dmn) > 0:
        dmnstr = dmn[0][:-1]
        print(str(dmnstr))
        return dmnstr
    else:
        return urlstr


def crawling_by_category(url, subcategory):
    reg = '<a target=\"_blank\" href=\"(/' + subcategory + '/3.+?\.html)\"'
    path = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    path = "output/" + subcategory + "_" + path
    xxnetHtml = getHtml(url + subcategory)
    domain = getDomain(url)
    hrefList = re.findall(reg, xxnetHtml)
    print(hrefList)
    for href in hrefList:
        # print (href if href[0:4]=="http" else domain+href)
        if not crawling(href if href[0:4] == "http" else domain + href, path): continue
        for value in range(2, 30):
            href_sub = href[:-5] + "_" + str(value) + ".html"
            if not crawling(href_sub if href[0:4] == "http" else domain + href_sub, path): break


if __name__ == '__main__':
    url = "https://96xxfl.com/"
    crawling_by_category("https://96xxfl.com/", "luyilu")
    print("Process Completed Successfully.")
