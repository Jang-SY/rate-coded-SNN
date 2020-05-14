# convert_mnist.py
# mnist 각각의 값을 frequency로 받아 spike를 일으키기 위한 source

import re
import numpy as np

class cv_mnist:
    def __init__(self, img_file, label_file, n_images, num_pixel=784):
        self.img_file = img_file
        self.label_file = label_file
        if n_images > 10000:
            print("10000개 이하의 데이터가 있습니다.")
            exit()
        else:
            self.n_images = n_images
        self.num_pixel = num_pixel
    
    # unzipped mnist file을 txt로 저장
    def flie2txt(self, txt_file):
        image_f = open(self.img_file, "rb")    # pixel value
#        label_f = open(self.label_file, "rb")  # MNIST has labels (digits)
        txt_f = open(txt_file, "w")     # output file
    
        image_f.read(16)   # discard header info
#        label_f.read(8)    # discard header info
    
        for i in range(self.n_images):   # number images requested 
#            label = ord(label_f.read(1))  # get label (unicode, one byte) 
#            txt_f.write(str(label) + "\n")
            for j in range(self.num_pixel):  # get 784 vals from the image file
                value = ord(image_f.read(1))
                txt_f.write(str(value) + " ")  # will leave a trailing space 
            txt_f.write("\n")  # next image
    
        image_f.close()
#        label_f.close()
        txt_f.close()

    # txt에 있는 숫자를 array에 저장(255로 나눠서 normalize)
    # 위에 있는 def와 합치면 더 빠름
    def str2num(self, txt_file):
        i = 0
        arr = np.zeros((self.n_images,self.num_pixel))
        txt_f = open(txt_file, "rt",encoding='utf-8')
        lines = txt_f.readlines()
        for line in lines:               
            strnum = re.findall("\d+", line)
            for j in range(self.num_pixel):
                arr[i][j] = float(strnum[j])/255
            i += 1
        txt_f.close()
        return arr
        
       
if __name__ == "__main__":
    mnist = cv_mnist("t10k-images.idx3-ubyte","t10k-labels.idx1-ubyte", 10)
    mnist.flie2txt("mnist_test.txt")
    arr = mnist.str2num("mnist_test.txt")
