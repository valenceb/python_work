import re
import urllib.request
# import urllib2
import os
import time

number = -1

def getHtml(url):  
	try:
		page = urllib.request.urlopen(url)
		html = page.read()  
		html=str(html)
		return html
	except urllib.error.HTTPError as e:  
		print (e.reason)
		return False

def mkdir(path):  
	path = path.strip()  
	isExists = os.path.exists(path)
	if not isExists:
		os.makedirs(path)
		print("Created file directory at "+path)
		return True
	else:  
		print(path+' created already.')
		return False  
  
# save all images with the filename  
def saveImages(imglist):  
	path = "output/"+str(number)
	mkdir(path)
	count=0
	for imageURL in imglist:
		count=count+1
		splitPath = imageURL.split('.')
		fTail = splitPath.pop()
		fName = splitPath.pop().split('/').pop()
		if len(fTail) > 3:  
			fTail = 'jpg'  
		fileName = fName + "." + fTail 
		try:  
			u = urllib.request.urlopen("http://imgsrc.baidu.com/forum/pic/item/"+fileName)  
			data = u.read()  
			f = open(path+"/"+str(count)+".jpg",'wb+')  
			f.write(data) 
			print('Saving a pic named ',fileName)
			f.close()
		except urllib.error.HTTPError as e:
			print (e.reason)

#get all the image url from html  
def getAllImg(html):  
    reg = r'https://imgsa.baidu.com/forum/(.+?\.jpg)'
    imglist = re.findall(reg,html)
    return imglist

def crawling(url):
	print("Crawling " + url)
	srcHtml = getHtml(url)
	if not srcHtml:
		return False
	imglist = getAllImg(srcHtml)
	print(imglist)
	saveImages(imglist)
	return True

def crawling_links(url):
	reg = 'target=\"_blank\">(http://tieba.baidu.com/p/.+?)</a>'
	tiebaHtml = getHtml(url)
	hrefList = re.findall(reg,tiebaHtml)
	hrefList = []
	hrefList.append("http://tieba.baidu.com/p/1427252597")
	hrefList.append("http://tieba.baidu.com/p/1972968578")
	print(hrefList)
	global number
	for href in hrefList:
		number=number+1
		if not crawling(href): continue

if __name__ == '__main__':
	crawling_links("https://tieba.baidu.com/p/3746891338?pn=2")
