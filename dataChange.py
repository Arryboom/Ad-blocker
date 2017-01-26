from glob import glob
import os
from PIL import Image as image
import random

fileDir="pic/"
fileDest="CleanPic/"
def convert(fileExt):
    for file in glob(fileDir+'*.'+fileExt):
        ranName=round(random.uniform(100000,999999)*10000)
        try:

            name, ext = os.path.splitext(file)
            print (name)
            img = image.open(file).convert('RGB').save(fileDest+str(ranName)+'.jpg')
            #os.remove(os.path.abspath(file))

        except Exception as xc:
            #os.remove(os.path.abspath(file))
            print("error:"+str(xc)+"file:"+os.path.abspath(file))
def deleteFile():
        for file in glob('normal/*.gif'):
            try:
                print(os.path.abspath(file))
                os.remove(os.path.abspath(file))
            except Exception as exc:
                print(str(exc))
            
convert("jpg")
convert("png")
convert("gif")
convert("jpeg")
#deleteFile()