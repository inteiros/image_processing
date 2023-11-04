import cv2
import matplotlib.pyplot as plt
from tkinter import filedialog
import os
import sys

def readImage():
    filename = filedialog.askopenfilename(initialdir=os.getcwd())
    if not(os.path.isfile(filename)):
        sys.exit()
    img = cv2.imread(filename)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    return img

def showImages(img1, img2, tituloSuperior):
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(12,4))
    fig.suptitle(tituloSuperior)
    ax1.imshow(img1)
    ax2.imshow(img2)
    ax1.set_title('Imagem 1')
    ax2.set_title('Resultado')
    ax1.axis('off')
    ax2.axis('off')
    plt.show()

def saveImage(img):
    filename = filedialog.asksaveasfilename(initialdir=os.getcwd(),defaultextension='.jpg')
    if not(os.path.exists(os.path.dirname(filename))):
        sys.exit()
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename,img)


def main():
    img1 = readImage()
    img1 = cv2.resize(img1,(1000,1000))
    (r,g,b,a) = (1.6,1.6,1.6,0)
    img2 = cv2.multiply(img1,(r,g,b,a))
    #saveImage(img3)
    showImages(img1,img2,'Multiplicação de imagens')


if __name__ == '__main__':
    main()
