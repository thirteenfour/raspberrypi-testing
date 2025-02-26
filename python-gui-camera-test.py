import cv2
# import time

cam = cv2.VideoCapture(0)

while True:
    ret, image = cam.read()
    cv2.imshow('Imagetest',image)
    
    # convert to base64
    # convert to multipart data
    # submit to api
    # flask?
    k = cv2.waitKey(1)
    if k != -1:
        break
cv2.imwrite('/home/sprouttech/Desktop/testimage.jpg', image)
cam.release()
cv2.destroyAllWindows()