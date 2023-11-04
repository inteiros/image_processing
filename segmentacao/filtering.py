import cv2
import math
import numpy as np

def read_image(filename):
    image = cv2.imread(filename)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    return image
    
def resize_image(image,width,height):
    if (np.ndim(image) > 2): #if image has more than 2 dimensions it has 3 channels
        #get height, width and num of channels of the image 
        h, w, c = image.shape
    else:
        #it's a one channel image (such as a grayscale image)
        h,w = image.shape
    w = int(math.ceil(w*width/100))
    h = int(math.ceil(h*height/100))
    new_size = (w,h)
    image = cv2.resize(image,new_size)
    return image

def average_filter(image,kernel_size):
    image = cv2.blur(image,(kernel_size,kernel_size))
    return image

def gaussian_filter(image,kernel_size):
    #standard deviation controls the amount of image blur
    #standard_deviation = 0 means it will be calculated from the kernel size
    standard_deviation = 0
    image = cv2.GaussianBlur(image,(kernel_size,kernel_size),standard_deviation)
    return image

def median_filter(image,kernel_size):
    image = cv2.medianBlur(image,kernel_size)
    return image


def salt_and_pepper_noise(image):
    ##get height, width and num of channels of the image and
    #create an image (array) with the same resolution
    #as the input image with data type: unsigned int 8 bits (0-255)
    h, w, c = image.shape
    noise = np.zeros((h,w), np.uint8)
    #randu function fills the destination array with 
    #uniformly-distributed random numbers between 0 and 255
    cv2.randu(noise,0,255)
    #for each coordinate of noise whose value is <= 5 the same coordinate in image receives 0
    #for each coordinate of noise whose value is >= 250 the same coordinate in image receives 255
    image[noise <= 5] = 0
    image[noise >= 250] = 255
    return image

def laplacian_filter(image):
    #we can use (optional) a media filter to reduce the noise
    #of the image while preserving the edges before sharpening
    image = median_filter(image,3)
    #an example of a laplacian filter
    kernel = np.array([[0, -1, 0],
                       [-1, 4, -1],
                       [0, -1, 0]])
    #Destination depth (ddepth):number of bits of the output image
    #(-1) means the destination image will have the same depth as the input image
    ddepth = -1
    laplacian = cv2.filter2D(image,ddepth,kernel)
    image = cv2.add(image,laplacian)
    return image

def laplacian_filter_alternative(image):
    #we can use (optional) a media filter to reduce the noise
    #of the image while preserving the edges before sharpening
    image = median_filter(image,3)
    #an example of a laplacian filter where 
    #we do not need to add the input image and the laplacian result
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    #Destination depth (ddepth):number of bits of the output image
    #(-1) means the destination image will have the same depth as the input image
    ddepth = -1
    image = cv2.filter2D(image,ddepth,kernel)
    return image

def highboost_filter(image,a):
    #high-boost (amplifies the high frequency components - edges)
    #we can use (optional) a media filter to reduce the noise
    #of the image while preserving the edges before sharpening
    image = median_filter(image,3)
    #an example of a laplacian filter + a (amplification factor)
    kernel = np.array([[0, -1, 0],
                       [-1, 4+a, -1],
                       [0, -1, 0]])
    #Destination depth (ddepth):number of bits of the output image
    #(-1) means the destination image will have the same depth as the input image
    ddepth = -1
    image = cv2.filter2D(image,ddepth,kernel)
    return image
