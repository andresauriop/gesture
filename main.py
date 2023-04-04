import os
import cv2
from cvzone.HandTrackingModule import  HandDetector
#Camera setup
width, height = 1200,720

cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)
folderPath = "Presentacion"


pathImages = sorted(os.listdir(folderPath),key=len)
#print(pathImages)

imagesNumber = 3
hs,ws = int(120*1),int(213*1)
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 30
# Hand Detector
detector = HandDetector(detectionCon=0.8,maxHands=1)



while True:
    #Import images
    success, img = cap.read()
    img=cv2.flip(img,1) #no cambia de mano

    pathFullImage = os.path.join(folderPath,pathImages[imagesNumber])
    imgCurrent = cv2.imread(pathFullImage)
    #hands, img = detector.findHands(img,flipType=False)
    hands, img = detector.findHands(img)
    cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),10)


    if hands and buttonPressed == False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx,cy = hand['center']

        #print(fingers)

        if cy<=gestureThreshold:
            if fingers==[1,0,0,0,0]:
                print("left")
                if imagesNumber > 0:
                    imagesNumber -= 1
                    buttonPressed = True

            if fingers==[0,0,0,0,1]:
                print("right")
                if imagesNumber < len(pathImages)-1:

                    imagesNumber += 1
                    buttonPressed = True

    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    # Adding webcam imagen on the slides
    imgSmall =  cv2.resize(img,(ws,hs))
    h,w,_ = imgCurrent.shape
    imgCurrent[0:hs,w-ws:w] = imgSmall

    cv2.imshow("Image",img)
    cv2.imshow("Slides",imgCurrent)


    key = cv2.waitKey(1)
    if key == ord('q'):
        break