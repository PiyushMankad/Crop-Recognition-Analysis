import numpy as np
import cv2

img = cv2.imread(r"E:\OpenCV\Agri\DJI_0602.JPG")
(h,w)=img.shape[:2]

# adjusting for the size of the image so that the width and height maintains a ratio of 1.5
				# # #	 NOT REQUIRED 	# # #
if (w/h != 1.5):
	if (h%2==1):
		h=h-1
	w=h*1.5

# adjusting the resize parameters of the image to get in shape with the window
reducSize=8							# reduction size of the image to keep ratio
window=8							# is the window size in the power of 2
minWhites=(window*window)/4			# is the minimmum no of whites required in a histogram
window2=8							# is the window size for the darker 
minWhites2=int((window*window)*0.025)


#h*w should be small so that less iterations are made
h=int(h/reducSize)									
w=int(w/reducSize)								
h=int(h/window)*window
w=int(w/window)*window

# resizing both the origional and hsv images 
img=cv2.resize(img,(w,h))
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
(h,w)=hsv.shape[0:2]
print("height",h," width",w)

# lighter crop MAIZE
lower=np.array([50,110,150])	# MANUALLY SET through testing
upper=np.array([70,250,250])	# MANUALLY SET through testing
mask=cv2.inRange(hsv,lower,upper)
result=cv2.bitwise_and(img,img,mask=mask)
result=cv2.cvtColor(result,cv2.COLOR_HSV2BGR)
result=cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
O_O,threshold=cv2.threshold(result,40,255,cv2.THRESH_BINARY)

#cv2.imshow("rough image1",threshold)
#cv2.imwrite("roughDJI_0403.JPG",threshold)


#window is the window traversal size
lightHist=np.zeros((int(w/window),int(h/window)),np.uint16)
whites=np.copy(lightHist)

#calculating the no of white pixels above threshold and entering it in another array
for Y in range(0,h,window):
	for X in range(0,w,window):
		histogram=cv2.calcHist([threshold[Y:Y+window,X:X+window]],[0],None,[256],[0,256])
		lightHist[int(X/window)][int(Y/window)]=histogram[255]
	
# taking a minimum threshold of white pixels
count=0
for i in range(lightHist.shape[0]):
	for j in range(lightHist.shape[1]):
		if lightHist[i][j]>minWhites:
			count+=1
			whites[i][j]=1
print("count",count)

#converting the false white values into black values (takes time)
for y in range(h):
	for x in range(w):
		threshold[y][x]=threshold[y][x]*whites[int(x/window)][int(y/window)]
'''
'''
cv2.imshow("smooth image1",threshold)
#cv2.imwrite("smoothDJI_0403.JPG",threshold)
#cv2.waitKey(0)
'''
'''

##########################################################################################
##########################################################################################

#darker crop COTTON
lower=np.array([50,0,0])		# MANUALLY SET
upper=np.array([70,100,130])	# MANUALLY SET	
mask=cv2.inRange(hsv,lower,upper)
result=cv2.bitwise_and(img,img,mask=mask)
result=cv2.cvtColor(result,cv2.COLOR_HSV2BGR)
result=cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
O_O,threshold=cv2.threshold(result,40,255,cv2.THRESH_BINARY)

#cv2.imshow("rough image2",threshold)
#cv2.imwrite("roughDJI_0403.JPG",threshold)

#window is the window traversal size
lightHist=np.zeros((int(w/window),int(h/window)),np.uint16)
whites=np.copy(lightHist)

#calculating the no of white pixels above threshold and entering it in another array
for Y in range(0,h,window):
	for X in range(0,w,window):
		histogram=cv2.calcHist([threshold[Y:Y+window,X:X+window]],[0],None,[256],[0,256])
		lightHist[int(X/window)][int(Y/window)]=histogram[255]
	
print("whites2",minWhites2)
# taking a minimum threshold of white pixels
count=0
for i in range(lightHist.shape[0]):
	for j in range(lightHist.shape[1]):
		if lightHist[i][j]>minWhites2:
			count+=1
			whites[i][j]=1
print("count",count)

#converting the false white values into black values (takes time)
for y in range(h):
	for x in range(w):
		threshold[y][x]=threshold[y][x]*whites[int(x/window)][int(y/window)]

cv2.imshow("smooth image2",threshold)
cv2.waitKey(0)


'''
cv2.imwrite("11.jpg",result)
cv2.imwrite("12.jpg",result2)
cv2.imwrite("13.jpg",result3)

'''


