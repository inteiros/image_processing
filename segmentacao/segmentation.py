import cv2
import numpy as np
from matplotlib import pyplot as plt


def read_image(filename):
    image = cv2.imread(filename)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    return image

def color_segmentation(image,lower_range,upper_range):
    if (np.ndim(image) > 2): # > 2 = colorida
        blur_image = cv2.medianBlur(image,5)
        hsv = cv2.cvtColor(blur_image, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv,lower_range,upper_range)
        result = cv2.bitwise_and(image,image,mask=mask)
        return 'Máscara Obtida', mask, 'Resultado da Segmentação', result
    else:
        None

def threshold(image, thresh):
    if (np.ndim(image) > 2): # > 2 = colorida
        gray_image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    else:
        gray_image = image
    blur_image = cv2.medianBlur(gray_image,5)  
    maxval = 255
    thresh, mask = cv2.threshold(blur_image,thresh,maxval,cv2.THRESH_BINARY)
    result = cv2.bitwise_and(image,image,mask=mask)
    return 'Máscara Obtida', mask, 'Resultado da Segmentação', result  

def otsu_threshold(image):
    if (np.ndim(image) > 2): # > 2 = colorida
        gray_image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    else:
        gray_image = image
    blur_image = cv2.medianBlur(gray_image,5)  
    thresh = 0 # será calculado pelo Método de Otsu
    maxval = 255
    thresh, mask = cv2.threshold(blur_image,thresh,maxval,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    result = cv2.bitwise_and(image,image,mask=mask)
    return f'Máscara Obtida (Threshold = {thresh})', mask, 'Resultado da Segmentação', result 

def canny(image,lower_thresh_rate):
    if (np.ndim(image) > 2): # > 2 = colorida
        gray_image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    else:
        gray_image = image
    blur_image = cv2.medianBlur(gray_image,5)  
    thresh = 0 # será calculado pelo Método de Otsu
    maxval = 255
    thresh, mask = cv2.threshold(blur_image,thresh,maxval,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    upper = thresh
    lower = int(thresh*lower_thresh_rate)
    edges = cv2.Canny(blur_image,lower,upper)
    kernel = np.ones((3,3),np.uint8)
    morph = cv2.morphologyEx(edges,cv2.MORPH_CLOSE,kernel)
    (contours,hierarchy) = cv2.findContours(morph,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    result = cv2.drawContours(image.copy(),contours,-1,color=(0,255,0),thickness=3)
    return 'Bordas detectadas', morph, f'Resultado - Qtde Contornos = {len(contours)} ', result