
import imutils
import cv2
import numpy as np

def rectangle(image,result,crop):

	#gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(image, (5, 5), 0)
	thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

	# find contours(possible shapes or edges) in the image 
	contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	contours = contours[0] if imutils.is_cv2() else contours[1]

	area=0
	# loop over the contours
	for c in contours:
		M = cv2.moments(c)
		c=c.astype("int")
		if len(c)>100:	# should define a percentage of image size
			# condition is to check and disregard the small crop patches that may appear
			
			boundary=cv2.minAreaRect(c)
			rect=cv2.boxPoints(boundary)
			rect=np.int0(rect)
			cv2.drawContours(result,[rect],0,(0,0,255),2)
			area=area+cv2.contourArea(c)
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
			cv2.putText(result,crop,(cX,cY),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)

			print("length",len(c),"area",area)
	#cv2.imshow("result",result)
	#cv2.waitKey(0)
	return result



def density():
	pass