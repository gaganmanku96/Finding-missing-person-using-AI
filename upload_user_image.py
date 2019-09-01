import io
import base64
import json

import numpy as np
from PIL import Image

from db_operations import *


def get_base64_form(image):
    buff = io.BytesIO()
    image.save(buff, format="JPEG")
    img_str = base64.b64encode(buff.getvalue())
    return img_str


def upload_image(base64_image):
    try:
        root = db.reference('user')
        user_upload = root.child('manual_upload').child('case2').set(
            {'image': str(base64_image),
             'location': "gurgaon"
             })
        return True
    except Exception as e:
        print("Insertion Error" + str(e))
        return False


if __name__ == '__main__':
    file_name = "images/salman.jpg"
    img = Image.open(file_name)
    base64_image = get_base64_form(img)
    result = upload_image(base64_image)
    if result is True:
        print("Uploaded")
    else:
        print("Failed")
