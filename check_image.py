import cv2
import numpy as np
import csv
import webcolors

def get_img_by_url(url):
    from urllib.request import urlopen
    resp = urlopen(url)
    img = resp.read()
    return img

def dominant_color(img):
    from colorthief import ColorThief
    import io
    img = io.BytesIO(img)
    #gets the image file and analyzes the dominant color
    color_thief = ColorThief(img)
    dominant_color = color_thief.get_color(quality=1)
    #color_thief.get_palette(quality=1)
    return dominant_color

def get_color_rgb(color):
    r = color[0]
    g = color[1]
    b = color[2]
    t = 255/2 #threshold
    if r>t and g>t and b>t:
        return "white"
    elif r<t and g<t and b<t:
        return "black"
    elif r>t:
        if g<t and b<t:
            return "red"
        elif g>t and b<t:
            if r>g:
                return "red green"
            else:
                return "green red"
        else:
            if r>b:
                return "red blue"
            else:
                return "blue red"
    elif g>t:
        if b<t:
            return "green"
        else:
            if g>b:
                return "green blue"
            else:
                return "blue green"
    else:
        return "blue"

def get_color_name(requested_color):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_color)
    except ValueError:
        closest_name = closest_color(requested_color)
        try:
            actual_name = get_color_rgb(requested_color)
        except:
            actual_name = None
            print("error get colorname",requested_color)
    return actual_name, closest_name

def closest_color(requested_color):
    min_colors = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

def dark_or_light(img):
    #load image into numpy
    arr = np.asarray(bytearray(img), dtype="uint8")
    #arr = np.asarray(bytearray(img), dtype=np.uint8)
    #img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    img = cv2.imdecode(arr, 0)

    #arr = np.asarray(bytearray(img.read()), dtype=np.uint8)
    #img = cv2.imdecode(img, 0) # 'Load img as b/w as an numpy array
    #img = cv2.imdecode(arr, -1) # 'Load it as it is'
    #cv2.IMREAD_COLOR
    #img = cv2.imread('./h663_tn.jpg',0) #read img as b/w as an numpy array
    #https://stackoverflow.com/questions/28663856/how-to-count-the-occurrence-of-certain-item-in-an-ndarray
    unique, counts = np.unique(img, return_counts=True)
    mapColorCounts = dict(zip(unique, counts))
    #print(mapColorCounts) # mapColorCounts[0] is the number of black pixels in an image
    b = 0 #black
    w = 0 #white
    if 0 in mapColorCounts:
        b = mapColorCounts[0]
    if 255 in mapColorCounts:
        w = mapColorCounts[255]

    if b > w:
        dominant_shade = "mostly black"
    else:
        dominant_shade = "mostly white"

    return dominant_shade, mapColorCounts

def img_size(img):
    arr = np.asarray(bytearray(img), dtype="uint8")
    img = cv2.imdecode(arr, -1)
    h, w, _ = img.shape
    return h, w

def has_transparency(img):
    from PIL import Image
    from PIL import ImageOps
    import io
    img = io.BytesIO(img)
    img = Image.open(img)
    if img.mode == "P":
        #print("p")
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        #print("rgba")
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    return False

def fileextension(url):
    fileext = ""
    url = url.lower()
    if url.endswith(('.jpg', '.jpeg')):
        fileext = "jpg"
    elif url.endswith(('.png')):
        fileext = "png"
    elif url.endswith(('.gif')):
        fileext = "gif"
    return fileext

def top_left_pixel(img):
    #Getting the first top left pixel of image
    from PIL import Image
    import io

    img = io.BytesIO(img)
    img = Image.open(img)
    px = img.load()
    #print(img.size)  # Get the width and hight of the image for iterating over
    return px[0,0]


#tried this but file locked to pst domain
#https://spreadsheets.google.com/feeds/cells/YOURGOOGLESHEETCODE/SHEETPAGENUMBER/public/full?alt=json
print("Please wait... processing and writing to file.")
#https://realpython.com/python-csv/
with open('images_processed.csv', mode='w') as imgs_processed:
    imgs_writer = csv.writer(imgs_processed, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    imgs_writer.writerow(["code","url","file ext","dominant colour","dominant colour name","closest name","dominant shade","top left pixel","top left pixel color","height","width","transparent"]) #Headers
    with open('images.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1 # skip headers
            elif row[1] != "": # if url not blank
                code = row[0]
                #url = 'https://go.cin7.com/webfiles/ProSciTechAU/webpages/images/275564/h677-24_tn.jpg'
                url = str(row[1])
                #print(url)
                fileext = fileextension(url)
                try:
                    img = get_img_by_url(url)
                except:
                    print("could not get url",code,url)
                    imgs_writer.writerow([code,url,fileext,"error","error","error","error","error","error","error","error","error"])
                    pass

                color = dominant_color(img)
                color_name, closest_name = get_color_name(color)
                dominant_shade, mapColorCounts = dark_or_light(img)
                tl_pixel = top_left_pixel(img)
                try:
                    tl_pixel_color, a = get_color_name(tl_pixel)
                except:
                    tl_pixel_color = None
                    a = None
                height, width = img_size(img)
                transparent = False
                if fileext == "png" or fileext == "gif": #GIF, PNG, BMP, TIFF, TGA and JPEG 2000 support transparency
                    try:
                        transparent = has_transparency(img)
                    except:
                        transparent = "error"
                        print("error getting transparency",code,url)

                #print(f'\t{row[0]} {row[1]}')
                #print(f'{code} {fileext} {color} which is {color_name} closest color: {closest_name}. shade {dominant_shade} {height} {width} transparent? {transparent}')

                imgs_writer.writerow([code,url,fileext,color,color_name,closest_name,dominant_shade,tl_pixel,tl_pixel_color,height,width,transparent])
                #exit()
            line_count += 1
        print(f'Processed {line_count} lines/images.')
