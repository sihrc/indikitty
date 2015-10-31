import base64
import logging
from itertools import izip
from cStringIO import StringIO

import cv2
import numpy as np
from skimage.io import imread
import indicoio

from .keys import INDICO_API_KEY
indicoio.api_key = INDICO_API_KEY

SERVER_URL = "http://localhost:3000/random"

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
    image = imread(SERVER_URL)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(image, (width, height))
    return resized_image

def show(img):
    cv2.imshow("result", img)
    cv2.waitKey()

def process(input_url):
    input_image = imread(input_url)
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

    image_string = base64.b64encode(cv2.imencode(".png", input_image)[1].tostring())
    faces = get_faces_dimens(image_string, input_image.shape)

    cats = []
    for x1, y1, x2, y2 in faces:
        width, height = x2 - x1, y2 - y1
        cat = get_suitable_cat(width, height)
        cats.append(cat)

    for (x1, y1, x2, y2), cat in izip(faces, cats):
        if cat.shape[2] > 3:
            mask = np.where(cat[:,:,3])
            input_image[y1:y2, x1:x2, :][mask] = cat[:,:,:3][mask]
        else:
            input_image[y1:y2, x1:x2, :] = cat

    output = StringIO()
    output.write(cv2.imencode(".png", input_image)[1].tostring())
    output.seek(0)
    return output
