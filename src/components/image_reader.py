"""
File: image_reader.py

Description: HTML image reader to feed live images of the Sun into the dashboard
"""

class ImageReader:

    def __init__(self, img_name):
        self.name = img_name


    def set_im_link(self):
        if self.name == 'SDO/HMI Continuum':
            return 'https://soho.nascom.nasa.gov/data/realtime/hmi_igr/1024/latest.jpg'
        elif self.name == 'SDO HMI Magnetogram':
            return 'https://soho.nascom.nasa.gov/data/realtime/hmi_mag/1024/latest.jpg'
        elif self.name == 'SOHO EIT 171':
            return 'https://soho.nascom.nasa.gov/data/realtime/eit_171/1024/latest.jpg'
