from typing import List, Any, Union

import numpy as np
import cv2
import time
import sys

def FindContours(fimage, fullImage, crColour):
    lower = np.array([crColour, crColour, crColour])
    upper = np.array([255, 255, 255])
    mask = cv2.inRange(fimage, lower, upper)
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

    quality = 0
    full = 0
    good = 0
    bad = 0

    highQ = []
    lowQ = []
    ultraLowQ = []
    smallpiece = []
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if (6000 > cv2.contourArea(c) > 3000):
            #cv2.drawContours(fullImage, [approx], -1, (0, 255, 0), 4)
            highQ.append(cv2.contourArea(c))
            full += 1
            quality += 25
        elif (3000 >= cv2.contourArea(c) > 2000):
            lowQ.append(cv2.contourArea(c))
            #cv2.drawContours(fullImage, [approx], -1, (0, 255, 0), 4)
            good += 1
            quality += 15
        elif (2000 >= cv2.contourArea(c) > 900):
            ultraLowQ.append(cv2.contourArea(c))
            #cv2.drawContours(fullImage, [approx], -1, (0, 255, 0), 4)
        elif (900 >= cv2.contourArea(c) > 500):
            smallpiece.append(cv2.contourArea(c))
            #cv2.drawContours(fullImage, [approx], -1, (0, 255, 0), 4)
    if (len(smallpiece) == len(ultraLowQ)):
        bad += len(ultraLowQ)
        quality += 10 * bad

    total = good + full + bad
    if (total < 4):
        quality = 0
    if (quality > 100):
        quality = 100
    return fimage,fullImage, quality

def CropImage(I, d):
    height, width = I.shape[:2]
    print(height,width)
    cv2.imshow("sd", I)
    #polygon = [[[height,0],[width-height,0],[width,height],[0,height]]]
    polygon = d.copy()
    print(polygon)
    minX = I.shape[1]
    maxX = -1
    minY = I.shape[0]
    maxY = -1
    for point in polygon[0]:

        x = point[0]
        y = point[1]

        if x < minX:
            minX = x
        if x > maxX:
            maxX = x
        if y < minY:
            minY = y
        if y > maxY:
            maxY = y

    cropedImage = np.zeros_like(I)
    for y in range(0,I.shape[0]):
        for x in range(0, I.shape[1]):
            if x < minX or x > maxX or y < minY or y > maxY:
                continue

            if cv2.pointPolygonTest(np.asarray(polygon),(x,y),False) >= 0:
                cropedImage[y, x, 0] = I[y, x, 0]
                cropedImage[y, x, 1] = I[y, x, 1]
                cropedImage[y, x, 2] = I[y, x, 2]
    return cropedImage

def CalcColour(image):
    avgColor = [image[:, :, i].mean() for i in range(image.shape[-1])]
    return np.mean(avgColor)

def RoadColour(image):
    avgColor = [image[:, :, i].mean() for i in range(image.shape[-1])]
    return np.mean(avgColor)


def CalibratePOV(image, x1, x2, y1, y2):
    height = y2 - y1
    width = x2 - x1
    starting = image.copy()
    print("Define lane size:")
    print("-use W A S D for position")
    print("-use R F for width")
    print("-use T G for height")
    d1, d2, d3, d4 = [height + x1, 0+y1], [width - height + x1, 0 + y1], [width + x1, height+y1], [0+x1, height+y1]

    while(1):
        processed = starting.copy()
        cv2.line(processed, (d1[0], d1[1]), (d4[0], d4[1]), (255, 0, 0), 5)
        cv2.line(processed, (d2[0], d2[1]), (d3[0], d3[1]), (255, 0, 0), 5)
        cv2.imshow("Calibration", processed)
        k = cv2.waitKey()
        if (k == 13):
            cv2.destroyAllWindows()
            break
        if (k == 27):
            exit()
        if (k == 119): # W
            d1[1] -= 10
            d2[1] -= 10
            d3[1] -= 10
            d4[1] -= 10
        if (k == 97): # A
            d1[0] -= 10
            d2[0] -= 10
            d3[0] -= 10
            d4[0] -= 10
        if (k == 115): # S
            d1[1] += 10
            d2[1] += 10
            d3[1] += 10
            d4[1] += 10
        if (k == 100): # D
            d1[0] += 10
            d2[0] += 10
            d3[0] += 10
            d4[0] += 10
        if (k == 113): # Q
            d1[0] += 10
            d2[0] -= 10
        if (k == 101): # E
            d1[0] -= 10
            d2[0] += 10
        if (k == 114): # R
            d1[0] -= 10
            d2[0] += 10
            d3[0] += 10
            d4[0] -= 10
        if (k == 102): # F
            d1[0] += 10
            d2[0] -= 10
            d3[0] -= 10
            d4[0] += 10
        if (k == 116): # T
            d1[1] -= 10
            d2[1] -= 10
            #d3[1] += 10
            #d4[1] += 10
        if (k == 103): # G
            d1[1] += 10
            d2[1] += 10
            #d3[1] -= 10
            #d4[1] -= 10
    #d = [d1,d2,d3,d4]
    povX1 = d4[0]
    povX2 = d3[0]
    povY1 = d1[1]
    povY2 = d4[1]
    d = [d1, d2, d3, d4]
    d1[0] -= povX1
    d1[1] -= povY1
    d2[0] -= povX1
    d2[1] -= povY1
    d3[0] -= povX1
    d3[1] -= povY1
    d4[0] -= povX1
    d4[1] -= povY1
    return d, povX1, povX2, povY1, povY2


def DetectLane(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 10, 250)
    cv2.imshow("edged.jpg", edged)
    cv2.waitKey()



# =============================#
# ---------MAIN PROGRAM--------#
# =============================#

povX1, povX2, povY1, povY2 = 0, 0, 0, 0

cap = []

W = 0
H = 0


if (len(sys.argv) < 3):
    fileName = str(input("Enter file name: "))
    #print("------")
    cap = cv2.VideoCapture(fileName)

    W = cap.get(3)
    H = cap.get(4)
    try:
        ratio = W / H
    except:
        print("File does not exist!\nTry again.")
        c = sys.stdin.read(1)
        exit()
    H = 480
    W = int(H * ratio)
    povX1, povX2, povY1, povY2 = int(W / 2 - 250), int(W / 2 + 250), 380, 480

else:
    fileName = str(sys.argv[1])
    cap = cv2.VideoCapture(fileName)

    W = cap.get(3)
    H = cap.get(4)
    ratio = W / H
    H = 480
    W = int(H * ratio)

    if (sys.argv[2] == "DEFAULT"):
        if (int(sys.argv[3]) == 1):
            povX1, povX2, povY1, povY2 = 144, 785, 383, 480
        if (int(sys.argv[3]) == 2):
            povX1, povX2, povY1, povY2 = int(W / 2 - 250), int(W / 2 + 250), 380, 480
        if (int(sys.argv[3]) == 3):
            povX1, povX2, povY1, povY2 = 0, 500, 363, 460
    else:
        povX1, povX2, povY1, povY2 = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])

#c = sys.stdin.read(1)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fileName = fileName.split('\\')
outputName, _ = fileName[-1].split('.')
#print(outputName)

out = cv2.VideoWriter('processed' + outputName + ".mp4", fourcc, 30.0, (int(W), int(H)))
DELAY_CAPS = 15
FPS = 30
colourArray = 9
avgRoad = 255
delayCount = DELAY_CAPS
roadArray = []
crossnum = 0
roadFrames = 0
cntTry = 0
framesCount = 0

newcount = 0

SOME_CONSTANT = 10
SOME_CROP_CONST = 10
quality = 0
cropframe = 0
prevColour = 10
prevImage = []
prevFull = []

firstFrame = True
snoopMode = False
startDelay = False
calibration = True
fullCycle = True

crossArray = []
allCrossArray = []

ret1, frame1 = cap.read()
img = cv2.resize(frame1, (W, H))
d, povX1,povX2,povY1,povY2 = CalibratePOV(img, povX1, povX2, povY1, povY2)

roadX1 = povX1 + povY2 - povY1
roadX2 = povX2 - (povY2 - povY1)
roadY1 = povY1 + 20
roadY2 = povY2 - 20

#print("-----------------------------")
#print(roadX1, roadX2, roadY1, roadY2)
#print(povX1, povX2, povY1, povY2)
#print(d)
showProcess = False
a = input("Show process? (y/n) ")
if (a == "y" or a == "Y"):
    showProcess = True

start_time = time.time()

while (cap.isOpened()):
    ret, frame = cap.read()
    try:
        #print("sad")
        framesCount += 1
        img = cv2.resize(frame, (W, H))
        DetectLane(img)
        roadColour = RoadColour(img[roadY1:roadY2, roadX1:roadX2])
        if (snoopMode == False):
            roadFrames += 1
            roadArray.append(roadColour)
            if (roadFrames == 10):
                avgRoad = np.mean(roadArray)
                roadArray.clear()
                roadFrames = 0
        else:
            delayCount += 1
            if (delayCount >= DELAY_CAPS):
                startDelay = False
                snoopMode = False
                firstFrame = True
                avgRoad = roadColour
        processedFrame = img
        font = cv2.FONT_HERSHEY_SIMPLEX
        if (startDelay == False and roadColour > avgRoad + SOME_CONSTANT):
            #print("sdadsad")
            #cropIm = CropImage(img[povY1:povY2, povX1:povX2], d)
            cropIm = img[povY1:povY2, povX1:povX2]
            cropColour = CalcColour(cropIm)
            #print("frrrrrrrrrrrrrr")
            if (firstFrame == True):
                prevImage = cropIm
                prevColour = cropColour
                firstFrame = False
                snoopMode = True
                prevFull = img
                delayCount = 0
                fullCycle = False
            allCrossArray.append(cropColour)
            if (prevColour > cropColour):
                newcount += 1
                if (prevColour > 10):
                    delayCount = 0
                    processedFrame, drewIm, quality = FindContours(prevImage, prevFull, int(RoadColour(prevFull[roadY1:roadY2, roadX1:roadX2])) + 5)#STANDART_CR_COLOUR - (STANDART_CR_COLOUR - RoadColour(prevFull)))
                    startDelay = True
                    if (quality > 0):
                        crossnum += 1
                        print("------------------")
                        print(f'{crossnum} crosswalk found')
                        print("Quality = ", quality)
                        print("Frame %d (%f second)" %(framesCount, framesCount/30))
                        print("Image saved as: " + str(outputName) + "cr"+ str(crossnum)+".jpg")
                        print("------------------")
                        fullCycle = True
                        cv2.imwrite(str(outputName) + "cr"+ str(crossnum)+".jpg", prevFull)
                        prevImage = []
            else:
                prevImage = cropIm
                prevColour = cropColour
                prevFull = img
        elif (snoopMode == True and fullCycle == False):
            avgRoad = avgRoad - SOME_CONSTANT
            fullCycle = True
        strRoad = str(RoadColour(img))
        cv2.putText(img, "Found: " + str(crossnum), (100, 50), font, 2, (255, 0, 0), 2, cv2.LINE_AA)
        if (showProcess):
            cv2.imshow("Process", img)
            cv2.waitKey(30)
        out.write(img)
    except:
        print('End of file')
        break

cv2.destroyAllWindows()

print("TOTAL: ", crossnum)
print("Output video saved as: processed" + outputName + ".mp4")
print("--- %s seconds ---" % (time.time() - start_time))
print("Press any key to exit")
c = sys.stdin.read(1)