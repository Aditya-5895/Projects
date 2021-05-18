import cv2
import numpy as np


cap = cv2.VideoCapture(0)
# cap.set(10,500)
bf = cv2.BFMatcher()
imgTarget = cv2.imread("TargetImg.jpeg ")
myVid = cv2.VideoCapture("tom and jerry.mp4")
success, imgVideo = myVid.read()

detection = False
frameCounter = 0
key = 2
kernel = np.ones((5,5),np.uint8)
play = False


imgTarget = cv2.resize(imgTarget,(400,400))
imgVideo = cv2.resize(imgVideo,(400,400))
pts = np.float32([[0,0],[0,400],[400,400],[400,0]]).reshape(-1, 1, 2)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
orb = cv2.ORB_create(nfeatures=1000)
kp1, des1 = orb.detectAndCompute(imgTarget,None)
#imgTarget = cv2.drawKeypoints(imgTarget,kp1,None)

upper_hsv = np.float64([153,255,255])
lower_hsv = np.float64([64,72,49])

while True:
    _,imgWebcam = cap.read()
    imgAug = imgWebcam.copy()

    imgControl = imgAug[:180,:600,:]
    # cv2.imshow("haqbs",imgControl)
    hsv = cv2.cvtColor(imgControl , cv2.COLOR_BGR2HSV)
    Mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    Mask = cv2.erode(Mask, kernel, iterations=1)
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.dilate(Mask, kernel, iterations=1)
    
    cnts,_ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    center = None
    
    if len(cnts) > 0:
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        cv2.circle(imgWebcam, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        if center[1] <= 65:
            if 40 <= center[0] <= 140:
                key = 1
            elif 505 <=center[0] <= 600:
                key = 2
            elif 160<= center[0] <= 255:
                play = False
            elif 275<=center[0] <=370:
                play = True
            elif 390 <= center[0] <=485:
                key = 3
        
    
    kp2, des2 = orb.detectAndCompute(imgWebcam,None)
    
    imgWebcam = cv2.rectangle(imgWebcam, (40,1), (140,65), (122,122,122), -1)                                   
    imgWebcam = cv2.rectangle(imgWebcam, (160,1), (255,65), colors[0], -1)
    imgWebcam = cv2.rectangle(imgWebcam, (275,1), (370,65), colors[1], -1)
    imgWebcam = cv2.rectangle(imgWebcam, (390,1), (485,65), colors[2], -1)
    imgWebcam = cv2.rectangle(imgWebcam, (505,1), (650,65), colors[3], -1)
    
    cv2.putText(imgWebcam, "Video", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(imgWebcam, "Pause", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(imgWebcam, " Play ", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(imgWebcam, "Countour ", (400, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(imgWebcam, "Feature Map", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)
    
    #imgWebcam = cv2.drawKeypoints(imgWebcam,kp2,None)
    if detection == False:
        myVid.set(cv2.CAP_PROP_POS_FRAMES,0)
        frameCounter = 0     
        
    else:
        if frameCounter == myVid.get(cv2.CAP_PROP_FRAME_COUNT):
            myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0
        if play:    
            success, imgVideo = myVid.read()
            success, imgVideo = myVid.read()
            success, imgVideo = myVid.read()
            imgVideo = cv2.resize(imgVideo, (400,400))
        
    ##Matching
    
    matches = bf.knnMatch(des1,des2,k=2)
    good =[ ]
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append(m)
            
    if len(good)>15:
        detection = True
        # Feature Match Draw
        if key == 2 :
            imgFinal = cv2.drawMatches(imgTarget, kp1, imgAug, kp2, good, None,flags=2)
            imgFinal = cv2.rectangle(imgFinal, (400,1), (500,65), (122,122,122), -1)
            imgFinal = cv2.rectangle(imgFinal, (790,1), (885,65), colors[2], -1)
            cv2.putText(imgFinal, " Countour ", (790, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(imgFinal, "Video", (433, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            try:
                cv2.circle(imgFinal, (int(x)+400, int(y)), int(radius), (0, 255, 255), 2)
            except:
                pass
                
        elif key == 1 :
            # Augmenting Video
            srcPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dstPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            matrix, mask = cv2.findHomography(srcPts,dstPts,cv2.RANSAC,5)
            imgWrap = cv2.warpPerspective(imgVideo, matrix, (imgWebcam.shape[1], imgWebcam.shape[0]))
            dst = cv2.perspectiveTransform(pts, matrix)
            #img2 = cv2.polylines(imgWebcam,[np.int32(dst)],True,(255,0,255),3)
            imgWebcam = cv2.fillPoly(imgWebcam, [np.int32(dst)],(0,0,0))
            imgFinal = cv2.bitwise_or(imgWebcam ,imgWrap)
        
        elif key == 3 :
            # Showing Countours
            srcPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dstPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            matrix, mask = cv2.findHomography(srcPts,dstPts,cv2.RANSAC,5)
            # imgWrap = cv2.warpPerspective(imgVideo, matrix, (imgWebcam.shape[1], imgWebcam.shape[0]))
            dst = cv2.perspectiveTransform(pts, matrix)
            imgFinal = cv2.polylines(imgWebcam,[np.int32(dst)],True,(255,0,255),3)
            
        cv2.imshow('output',imgFinal)
        #cv2.imshow("Webcam",imgAug)
        #cv2.imshow("crop",imgControl)
    
    #
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
    
cap.release()
cv2.destroyAllWindows()