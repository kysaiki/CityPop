from PIL import Image, ImageEnhance, ImageFilter
import matplotlib.pyplot as plt
import cv2
import numpy as np
import random
import requests
import urllib.request 
import json
import os

#--------------------------------------------------------------------------------------------------
#return pixel art of image
#params: image (image to edit), i_size (initial size), o_size (final size)
def photo2pixelart(image, i_size, o_size):
    img=Image.open(image)
    small_img=img.resize(i_size,Image.BILINEAR)
    res=small_img.resize(img.size, Image.NEAREST)
    #filename=f'test_{i_size[0]}x{i_size[1]}.png'
    #res.save(filename)
    return res

#get image from API and save to directory
#params: filename - name of file
def getImage(filename):
    # API_KEY = '26011168-5fd01a4694e4c25728f50c859'
    response = requests.get('https://pixabay.com/api/?key=26011168-5fd01a4694e4c25728f50c859&q=tokyo|kyoto&image_type=photo&pretty=true&per_page=200&page=1+2+3&min_width=250&min_height=250&category=backgrounds+places+nature+buildings+fashion+travel+religion')
    apiImages = json.loads(response.text)
    imgNum = random.randint(0, len(apiImages["hits"]) - 1)
    url = apiImages["hits"][imgNum]["webformatURL"]
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)
    return filename

def createNewImageColorArray(newImage, f=16):
    imgArray = []
    options = [0, 1]

    colorArray = [random.choice(options), random.choice(options), random.choice(options)]
    print(colorArray)
    for i in range(newImage.size[0]):
        column = []
        for j in range(newImage.size[1]):
            r, g, b = newImage.getpixel((i, j))
            r = round(r/f)*f
            g = round(g/f)*f
            b = round(b/f)*f

            p = round((r + b)/2)
            y = round((r + g)/2)
            a = round((b + g)/2)    

            ry = [r, y]
            ga = [g, a]
            bp = [b, p]

            column.append((ry[colorArray[0]], ga[colorArray[1]], bp[colorArray[2]]))
        imgArray.append(column)   
    return imgArray
    
#--------------------------------------------------------------------------------------------------
def createImage(amount):
    for n in range(amount):
        imageName = getImage("../assets/preImage/testimage" + str(n) + ".jpg")
        newImage = photo2pixelart(image=imageName,i_size=(200,150), o_size=(200,150))
        os.remove(imageName)
        newImage = newImage.filter(ImageFilter.SHARPEN);
        newImage = newImage.resize((1920, 970))

        img = Image.new( 'RGB', (newImage.size[0],newImage.size[1]), "black") # create a new black image
        pixels = img.load() # create the pixel map
        newImage = createNewImageColorArray(newImage, 8)

        for i in range(img.size[0]):    # for every col:
            for j in range(img.size[1]):    # For every row
                pixels[i,j] = newImage[i][j]

        enhancer = ImageEnhance.Contrast(img)
        im_output = enhancer.enhance(1.2)
        im_output.save('../assets/images/image' + str(n) + '.png')

#--------------------------------------------------------------------------------------------------
createImage(10)