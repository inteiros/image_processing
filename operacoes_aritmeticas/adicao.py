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

def showImages(img1, img2, img3, tituloSuperior):
    fig, (ax1, ax2, ax3) = plt.subplots(1,3,figsize=(12,4))
    fig.suptitle(tituloSuperior)
    ax1.imshow(img1)
    ax2.imshow(img2)
    ax3.imshow(img3)
    ax1.set_title('Imagem 1')
    ax2.set_title('Imagem 2')
    ax3.set_title('Resultado')
    plt.show()


def main():
    img1 = readImage()
    img2 = readImage()
    img1 = cv2.resize(img1,(1000,1000))
    img2 = cv2.resize(img2,(1000,1000))
    print('==IMG1==')
    print(img1)
    print('==IMG2==')
    print(img2)
    img3 = cv2.add(img1,img2)
    print('==IMG3==')
    print(img3)
    showImages(img1,img2,img3,'Adição de imagens')


if __name__ == '__main__':
    main()
