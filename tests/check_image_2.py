from colorthief import ColorThief
from urllib.request import urlopen
import os
def dominant_color_from_url(url):
    #gets the image file and analyzes the dominant color
    color_thief = ColorThief(urlopen(url))
    dominant_color = color_thief.get_color(quality=1)
    #color_thief.get_palette(quality=1)
    return dominant_color

print(dominant_color_from_url('https://go.cin7.com/webfiles/ProSciTechAU/webpages/images/275564/h677-24_tn.jpg'))

# OR
#https://go.cin7.com/webfiles/ProSciTechAU/webpages/images/275564/h677-24_tn.jpg

import sys
#if sys.version_info < (3, 0):
#    from urllib2 import urlopen
#else:
from urllib.request import urlopen
import io
from colorthief import ColorThief
fd = urlopen('https://go.cin7.com/webfiles/ProSciTechAU/webpages/images/275564/h677-24_tn.jpg')
f = io.BytesIO(fd.read())
color_thief = ColorThief(f)
print(color_thief.get_color(quality=1)) #https://rgb.to/216,216,212
#print(color_thief.get_palette(quality=1))
