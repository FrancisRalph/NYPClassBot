import csv
import pandas
class TimeTable():
    def __init__(self, image : str = ""):
        if image == "":
            print("Error, No Image was given.")
        else:
            self.__class__.readfile(image)
    def readfile(self, image):
        self.img = csv.imread(image, 0)


TimeTable("../Images/test.png")
