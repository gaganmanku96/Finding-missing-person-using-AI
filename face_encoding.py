import logging

import face_recognition_api


def get_key_points(image, mode='local'):
    result = None
    try:
        if mode == 'local':
            result = face_recognition_api.get_encoding(image)
        elif mode == 'docker':
            pass
        return result
    except Exception as e:
        logging.error("Error in get_key_points - " + str(e))
        return None


def encode(key_points):
    encoded_string = ""
    for value in key_points[0]:
        svalue = str(value)
        if value < 0:
            svalue = svalue.replace('-', '1')  # Replace '-' with 1
        svalue = svalue.replace('.', '$')  # Replace . with $
        encoded_string = encoded_string + '@' + svalue
    return encoded_string


def decode(image):
    keypt = []
    keypt.append(image)
    encoded = []
    text = keypt[0].split('@')
    text = text[1:]
    for t in text:
        t = t.replace('$', '.')
        if t[0:1] == '1':
            t = '-' + t[1:]
        else:
            pass
        encoded.append(float(t))
    return encoded
