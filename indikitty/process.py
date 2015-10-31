import base64
import logging
from itertools import izip

import cv2
import numpy as np
import indicoio

from ipdb import launch_ipdb_on_exception
from ipdb import set_trace

logging.basicConfig()
logger = logging.getLogger("CATZ")

def get_faces_dimens(image_string, bounds):
    try:
        result = indicoio.facial_localization(image_string)
        faces = []
        for face in result:
            x1, y1 = face["top_left_corner"]
            x2, y2 = face["bottom_right_corner"]
            faces.append((x1, y1, x2, y2))
        return faces
    except Exception as e:
        logger.error(e)

def get_suitable_cat(width, height):
    # TODO - pick most efficient cat  ( cat image dict with sizes )
    image = cv2.imread("cat_4.png", cv2.IMREAD_UNCHANGED)
    resized_image = cv2.resize(image, (width, height))
    return resized_image

def show(img):
    cv2.imshow("result", img)
    cv2.waitKey()

def main():
    image_string = open("sample_2.txt", 'rb').read()

    decoded = base64.b64decode(image_string)
    final = cv2.imdecode(np.fromstring(decoded, np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
    faces = get_faces_dimens(image_string, final.shape)

    cats = []
    for x1, y1, x2, y2 in faces:
        width, height = x2 - x1, y2 - y1
        cat = get_suitable_cat(width, height)
        cats.append(cat)

    for (x1, y1, x2, y2), cat in izip(faces, cats):
        mask = np.where(cat[:,:,3])
        final[y1:y2, x1:x2, :][mask] = cat[:,:,:3][mask]

    # show(final)
    cv2.imsave("save.png", final)

if __name__ == "__main__":
    with launch_ipdb_on_exception():
        main()
