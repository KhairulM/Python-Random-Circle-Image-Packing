import cv2
import numpy as np
import random
import time
import argparse

class CIRCLE :
    def __init__(self, point, radius, color) :
        self.point = point
        self.radius = radius
        self.color = color
        self.growing = True

    def grow(self) :
        if self.growing :
            self.radius += 2

    def touchEdge(self, img) :
        height, width = img.shape[:2]
        return ((self.point[0] + self.radius > width) or (self.point[0] - self.radius < 0) or (self.point[1] + self.radius > height) or (self.point[1] - self.radius < 0))

    def touchCIRCLE(self, arrCIRCLES) :
        overlapping = False

        for other in arrCIRCLES :
            if not (other.point[0] == self.point[0] and other.point[1] == self.point[1]) :
                dist = ((other.point[0]-self.point[0])**2 + (other.point[1]-self.point[1])**2)**0.5 - 1
                if (dist < (other.radius + self.radius)) :
                    overlapping = True

        return overlapping

def newCIRCLE(img, arrCIRCLES) :
    height, width = img.shape[:2]
    
    newRadius = 2
    newX = random.randint(newRadius, width-newRadius)
    newY = random.randint(newRadius, height-newRadius)
    newC = CIRCLE((newX, newY), newRadius, img[newY][newX])
    
    if newC.touchCIRCLE(arrCIRCLES) :
        return None
    else :
        return newC

def updateAll(canvas, arrCIRCLES, scl) :
    lengthArr = len(arrCIRCLES)

    for i in range(0, lengthArr) :
        if arrCIRCLES[i].growing and (arrCIRCLES[i].radius>=scl or arrCIRCLES[i].touchEdge(canvas) or arrCIRCLES[i].touchCIRCLE(arrCIRCLES)) :
           arrCIRCLES[i].growing = False

        cv2.circle(canvas, (int(arrCIRCLES[i].point[0]), int(arrCIRCLES[i].point[1])), arrCIRCLES[i].radius, (int(arrCIRCLES[i].color[0]), int(arrCIRCLES[i].color[1]), int(arrCIRCLES[i].color[2])), -1)
        arrCIRCLES[i].grow()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--image", type = str, help = "Path to the image file")
    ap.add_argument("-r", "--runtime", type = float, default = 5.0, help = "Program runtime in minutes")
    ap.add_argument("-s", "--maxsize", type = int, default = 999, help = "Maximum radius for each circles in pixel")
    ap.add_argument("-c", "--bgcolor", type = str, default = "0,0,0", help = "Background canvas color RGB comma seperated eg. 255,255,255")
    args = vars(ap.parse_args())

    arrCIRCLES = []

    if not args.get("image", False):
        print("[ERROR] : Image file not provided")
        quit()

    imgName = args["image"]
    runtime = args["runtime"]
    maxSize = args["maxsize"]
    runtime *= 60

    img = cv2.imread(imgName, cv2.IMREAD_COLOR)
    height, width = img.shape[:2]

    """
    if width > height :
        scl = width//30
    else :
        scl = height//30
    """

    print("[INFO] : Creating Canvas")
    colors = [int(i) for i in args["bgcolor"].split(",")]
    canvas = np.zeros((height, width, 3), np.uint8)      # Black Canvas
    canvas[:] = (colors[2], colors[1], colors[0])
    
    print("[INFO] : Starting")
    startTimer = time.process_time()

    while (time.process_time() - startTimer <= runtime) :
        for i in range(0, 5) :
            c = newCIRCLE(img, arrCIRCLES)
            if c != None :
                arrCIRCLES.append(c)
        
        updateAll(canvas, arrCIRCLES, maxSize)

        rez = cv2.resize(canvas, ((width*500) // height, 500), interpolation = cv2.INTER_AREA)
        cv2.imshow("Processing", rez)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    saveImage = input("Save the Image? (Y/N): ")
    if saveImage == "Y" or saveImage == "y":
        saveName = input("Name : ")
        cv2.imwrite(saveName, canvas)
main() 