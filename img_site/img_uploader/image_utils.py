# -*- coding: utf-8 -*-
import os  
from PIL import Image  
import images2gif 
#import pdb

def getImgList(dirPath, ext):
	ext = '.' + ext
	return [os.path.join(dirPath, f) for f in os.listdir(dirPath) if f.endswith(ext)]

def getImageList(directoryPath, recusive = True):  
    imgPaths = []  
    for file in os.listdir(directoryPath):  
		filePath = os.path.join(directoryPath, file)
		if os.path.isdir(filePath):
			if recusive == True:
				subResult = getDirImageList(filePath, recusive)
				imgPaths.append(subResult)
			else:
				pass # just do nothing
		else:
			imgPaths.append(filePath)  
    return imgPaths

def combineImgsToGif(targetGifPath, imgPaths):
	imagesForGif = []
	for path in imgPaths:
		try:
			img = Image.open(path)
			width,height = img.size  
			newImg = Image.new("RGB", [width,height], (255,255,255))  
			newImg.paste(img, (0,0))  
			imagesForGif.append(newImg)
		except IOError:
			print "Error: Failed to open image at %s." % path
	try:
		images2gif.writeGif(targetGifPath, imagesForGif, duration=1, nq=0.1)
	except IOError:
		print "Error: Failed to create gif at %s." % targetGifPath


def sortAndCombineImgsToGif(targetGifPath, imgPaths, sortCriteria = 0):
	'''
	# SORT_BY_WIDTH = 0
	# SORT_BY_HEIGHT = 1
	'''
	mapPath2Size = []
	for path in imgPaths:
		f = open(path, "rb")
		img = Image.open(f)  
		mapPath2Size.append((path, img.size))
		f.close()
	mapPath2Size.sort(key=lambda item: item[1][sortCriteria], reverse=True)
	combineImgsToGif(targetGifPath, [mapItem[0] for mapItem in mapPath2Size])


def resizeAndCombineImgsToGif(targetGifFilePath, srcImageFilePaths, type = 0):  
	'''
	the images in gif is central aligned, with a white background, paste using the max size
	#type
	#0：resize to max size, rectangle
	#1：resize to max size, square
	#2：no resize, rectangle
	#3：no resize, square
	''' 
	if type > 3 or type < 0:
		type = 0
	maxWidth = 1  
	maxHeight = 1
	for imageFilePath in srcImageFilePaths:  
		fp = open(imageFilePath, "rb")  
		width,height = Image.open(fp).size  
		maxWidth = max(maxWidth, width)  
		maxHeight = max(maxHeight, height)  
		fp.close()  
	 
	usedFrame = ()
	if type == 0 or type == 2:    
		usedFrame = (maxWidth,maxHeight)
	elif type == 1 or type == 3:  
		maxSize = max(maxWidth, maxHeight) 
		usedFrame = (maxSize, maxSize)
	backgroundColor = (0,0,0)
	
	imagesForGif = []
	for imageFilePath in srcImageFilePaths:  
		fp = open(imageFilePath, "rb")  
		img = Image.open(fp)  
		width,height = img.size  
		imgResizeAndCenter = Image.new("RGB", usedFrame, backgroundColor)  
		if type == 0 or type == 1:  
			#use the smaller resize scale  
			if maxWidth / width >= maxHeight / height:  
				width = width * usedFrame[1] / height
				height = usedFrame[1]
			else:
				height = height * usedFrame[0] / width
				width = usedFrame[0]
			img = img.resize((width, height),Image.ANTIALIAS)  
		imgResizeAndCenter.paste(img, ((usedFrame[0] - width) / 2,(usedFrame[1] - height) / 2))   
		imagesForGif.append(imgResizeAndCenter)  
		fp.close()
	images2gif.writeGif(targetGifFilePath, imagesForGif, duration=1, nq=0.1)  

def generateThumbnail(imgPath, thumbnailDir):
	try:
		dirName, fullFileName = os.path.split(imgPath)
		fileName, ext = os.path.splitext(fullFileName)
		img = Image.open(imgPath)
		img.thumbnail((240, 240))
		newPath = os.path.join(thumbnailDir, fileName + '.thumbnail')
		img.save(newPath, "JPEG")
		return newPath
	except IOError:
		print "Failed to generate thumbnail for %s to %s" % (imgPath, thumbnailDir)

