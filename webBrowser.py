from skimage import io
img_src = 'http://wx2.sinaimg.cn/mw690/ac38503ely1fesz8m0ov6j20qo140dix.jpg'
image = io.imread(img_src)
io.imshow(image)
io.show()
