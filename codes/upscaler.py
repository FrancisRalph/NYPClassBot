import cv2
from cv2 import dnn_superres
import time

start_time = time.time()

sr = dnn_superres.DnnSuperResImpl_create()
image = cv2.imread("./input/input.png")

#change path to change model
path = "./models/EDSR_x3.pb"
sr.readModel(path)

# first param is the name of the model
# second param is the scale of the model, scale of the model is in the name of the file of the model
sr.setModel("edsr", 3)

result = sr.upsample(image)
cv2.imwrite("./Images/upscaledx3.png", result)

print("--- %s seconds ---" % (time.time() - start_time))

#download models
#esdr: https://github.com/Saafke/EDSR_Tensorflow/tree/master/models
#lapsrn: https://github.com/Saafke/FSRCNN_Tensorflow/tree/master/models
#espcn: https://github.com/fannymonori/TF-ESPCN/tree/master/export
#fsrcnn: https://github.com/fannymonori/TF-LapSRN/tree/master/export
