import os
import cv2
import numpy as np

from cvzone.HandTrackingModule import  HandDetector




#Camera setup
width, height = 1200,720

cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)
folderPath = "Presentacion"

pathImages = sorted(os.listdir(folderPath),key=len)
print(pathImages)

imagesNumber = 4
hs,ws = int(120*1),int(213*1)
gestureThreshold = 500
buttonPressed = False
buttonCounter = 0
buttonDelay = 30

annotations = []

# Hand Detector
detector = HandDetector(detectionCon=0.8,maxHands=1)



while True:
    #Import images
    success, img = cap.read()
    img=cv2.flip(img,1) #no cambia de mano

    pathFullImage = os.path.join(folderPath,pathImages[imagesNumber])
    imgCurrent = cv2.imread(pathFullImage)
    h, w, _ = imgCurrent.shape


    #hands, img = detector.findHands(img,flipType=False)
    hands, img = detector.findHands(img)
    cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),10)


    if hands and buttonPressed == False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx,cy = hand['center']
        lmList = hand['lmList']
        indexFinger = lmList[8][0],lmList[8][1]
        #print(indexFinger)
        indexFinger = lmList[8][0]*2,lmList[8][1]*2


        #xVal = int(np.interp(lmList[8][0],[width,width-100],[0,width]))

        #xVal = int(np.interp(lmList[8][0],[50,w-50],[0,w]))
        #yVal = int(np.interp(lmList[8][1],[50,height-50], [0, height]))

        #xVal = int(np.interp(lmList[8][0],[50,w-50],[0,w]))
        #yVal = int(np.interp(lmList[8][1],[50,h-50], [0, h]))
        #indexFinger = xVal,yVal

        #print(fingers)

        if cy<=gestureThreshold:
            '''if fingers==[1,0,0,0,0]:
                print("left")
                if imagesNumber > 0:
                    imagesNumber -= 1
                    buttonPressed = True

            if fingers==[0,0,0,0,1]:
                print("right")
                if imagesNumber < len(pathImages)-1:

                    imagesNumber += 1
                    buttonPressed = True
            '''

            # delete
            #if fingers == [1, 1, 1, 1, 1]:
            #    cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
            #    annotations.clear()


            if fingers==[0,1,1,0,0]:
                cv2.circle(imgCurrent,indexFinger,12,(0,0,255),cv2.FILLED)
                annotations.append((9999, 9999))

            ##if fingers == [0, 0, 0,0, 0]:

            ##    cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

            ##    annotations.append((9999,9999))



            #draw
            if fingers==[0,1,0,0,0]:
                cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
                annotations.append(indexFinger)


    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    for i in range(len(annotations)):
        if i!=0:
            print(annotations[i])
            if annotations[i] != (9999,9999) and annotations[i-1] != (9999,9999):
                cv2.line(imgCurrent,annotations[i-1],annotations[i],(0,0,200),12)



    # Adding webcam imagen on the slides
    imgSmall =  cv2.resize(img,(ws,hs))
    h,w,_ = imgCurrent.shape
    imgCurrent[0:hs,w-ws:w] = imgSmall

    cv2.imshow("Image",img)
    cv2.imshow("Slides",imgCurrent)


    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    if key == ord('c'):
        annotations.clear()