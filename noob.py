import numpy as np
import cv2

img = cv2.imread(r"E:\OpenCV\Agri\DJI_0346.JPG")
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
(h,w)=img.shape[:2]
print(img.shape[:2])

#light
lower=np.array([50,110,150])
upper=np.array([70,250,250])
mask=cv2.inRange(hsv,lower,upper)
result=cv2.bitwise_or(img,img,mask=mask)
result=cv2.cvtColor(result,cv2.COLOR_HSV2BGR)
result=cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
O_O,threshold=cv2.threshold(result,40,255,cv2.THRESH_BINARY)

#32 is the window traversal size
lightHist=np.zeros((int(w/32),int(h/32)),np.uint16)
whites=np.copy(lightHist)

for Y in range(0,h,32):
	for X in range(0,w,32):
		histogram=cv2.calcHist([threshold[Y:Y+32,X:X+32]],[0],None,[256],[0,256])
		lightHist[int(X/32)][int(Y/32)]=histogram[255]
	

print(np.nanmax(lightHist))
print(threshold[1392][2559])

#calculating the no of white pixels above threshold and entering it in another array
count=0
for i in range(lightHist.shape[0]):
	for j in range(lightHist.shape[1]):
		if lightHist[i][j]>256:
			count+=1
			whites[i][j]=1
print("count ",count)

#converting the false white values into black values (takes time)
''''''
for y in range(h):
	for x in range(w):
		threshold[y][x]=threshold[y][x]*whites[int(x/32)][int(y/32)]



cv2.imshow("frame",threshold)
cv2.imwrite("smooth_DJI346.jpg",threshold)
cv2.waitKey(0)

'''



#dark
lower=np.array([50,0,0])
upper=np.array([70,100,130])
mask=cv2.inRange(hsv,lower,upper)
result2=cv2.bitwise_and(img,img,mask=mask)
result=cv2.cvtColor(result2,cv2.COLOR_HSV2BGR)
result=cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
O_O,threshold=cv2.threshold(result,40,255,cv2.THRESH_BINARY)
cv2.imshow("frame",threshold)
cv2.waitKey(0)

lower=np.array([50,110,170])
upper=np.array([70,250,250])
mask=cv2.inRange(hsv,lower,upper)
result3=cv2.bitwise_and(img,img,mask=mask)
cv2.imshow("frame",result3)
cv2.waitKey(0)

cv2.imwrite("11.jpg",result)
cv2.imwrite("12.jpg",result2)
cv2.imwrite("13.jpg",result3)

'''


