import cv2
from cv2 import dnn_superres
import time

start_time = time.time()

sr = dnn_superres.DnnSuperResImpl_create()
image = cv2.imread("./input/input.png")
path = "./models/EDSR_x3.pb"
sr.readModel(path)
sr.setModel("edsr", 3)
result = sr.upsample(image)
cv2.imwrite("./Images/upscaledx3.png", result)

print("--- %s seconds ---" % (time.time() - start_time))