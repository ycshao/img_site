from image_utils import *


def test_generateThumbnail(): 
    lightsImgList = getImgList(r'src', 'jpg')
    for lightImg in lightsImgList:
		generateThumbnail(lightImg, r'out')
        
        
def test_generateGif():
	#combineImgsToGif(outPath, imgPaths) #only show 1
	sortAndCombineImgsToGif(r'out/changing_me.gif', getImageList(r"src")) # only show 2
	#resizeAndCombineImgsToGif(r'out\changing_me.gif', getImageList(r'src', 'jpg'), 0)
	#resizeAndCombineImgsToGif(r'out\changing_me1.gif', getImageList(r'src', 'jpg'), 1)
	#resizeAndCombineImgsToGif(r'out\changing_me2.gif', getImageList(r'src', 'jpg'), 2)
	#resizeAndCombineImgsToGif(r'out\changing_me3.gif', getImageList(r'src', 'jpg'), 3)

if __name__ == '__main__':
    #test_generateThumbnail()
    test_generateGif()