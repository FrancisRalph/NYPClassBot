import cv2
from cv2 import dnn_superres
import time
import os

start_time = time.time()


def upscale(path, guildId):
    start_time = time.time()
    sr = dnn_superres.DnnSuperResImpl_create()
    image_path = cv2.imread(path)

    # change path to change model
    model_path = os.path.join(os.getcwd(), "models/EDSR_x3.pb")
    sr.readModel(model_path)

    # first param is the name of the model
    # second param is the scale of the model, scale of the model is in the name of the file of the model
    sr.setModel("edsr", 3)

    result = sr.upsample(image_path)
    cv2.imwrite(path, result)
    print("--- %s seconds ---" % (time.time() - start_time))


# download models
# esdr: https://github.com/Saafke/EDSR_Tensorflow/tree/master/models
# fsrcnn: https://github.com/Saafke/FSRCNN_Tensorflow/tree/master/models
# espcn: https://github.com/fannymonori/TF-ESPCN/tree/master/export
# lapsrn: https://github.com/fannymonori/TF-LapSRN/tree/master/export
# so far, esdr produced the best results
