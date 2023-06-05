import cv2
import numpy as np
import glob
import os

fontIMGlist = sorted(glob.glob('c*.png'), key=os.path.getmtime)

cnt = 0
for fIMG in fontIMGlist:
    # read foreground image
    img = cv2.imread(fIMG, cv2.IMREAD_UNCHANGED)

    # read background image
    back = cv2.imread('DE.png')

    # extract alpha channel from foreground image as mask and make 3 channels
    alpha = img[:,:,3]
    alpha = cv2.merge([alpha,alpha,alpha])

    # extract bgr channels from foreground image
    front = img[:,:,0:3]

    # blend the two images using the alpha channel as controlling mask
    result = np.where(alpha==(0,0,0), back, front)

    fname = "charge_" + str(cnt) + ".png"
    cv2.imwrite(fname, result)
    cnt += 1













