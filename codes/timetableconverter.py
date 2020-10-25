import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


class TimeTable():
    def __init__(self, image : str = ""):
        if image == "":
            print("Error, No Image was given.")
        else:
            self.__class__.readfile(self, image)
    def readfile(self, image):
        self.img = cv2.imread(image, 0)
        #thresholding the image to a binary image
        thresh,img_bin = cv2.threshold(self.img,128,255,cv2.THRESH_BINARY |cv2.THRESH_OTSU)
        #inverting the image 
        img_bin = 255-img_bin
        cv2.imwrite("../Images/inverted.png",img_bin)
        #Plotting the image to see the output
        plotting = plt.imshow(img_bin,cmap='gray')
        plt.show()


TimeTable("../Images/test.png")
