#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 09:23:33 2018

@author: codemaker
"""

try:
    import Image
except ImportError:
    from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
im = Image.open("background.jpg") # the second one 
im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(2)
im = im.convert('1')
im.save('temp2.jpg')
text = pytesseract.image_to_string(Image.open('temp2.jpg'))
print(text)

