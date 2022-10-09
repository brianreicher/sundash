"""
File: image_reader.py

Description: HTML image reader to feed live images of the Sun into the dashboard
"""

import requests
import shutil
import urllib

class ImageReader:

    def __init__(self, link):
        self.link = link

    def parse_html(self):
        img = urllib.urlopen(self.link)
        # with open(path, 'w') as f:
        #     f.write(img.read())
        print(img)




img: ImageReader = ImageReader('http://soho.nascom.nasa.gov/data/realtime/eit_171/1024/latest.html')
img.parse_html()