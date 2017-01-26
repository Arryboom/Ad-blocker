from glob import glob
import os
from PIL import Image as image
from PIL import ImageDraw
from PIL import ImageFont
import uuid

fileDir="pic/"
fileDest="CleanPic/"
def convert(fileExt):
    for file in glob(fileDir+'*.'+fileExt):
        ranName= uuid.uuid4().time_low
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

def addnumber():
    font = ImageFont.load_default().font
    img=image.open("1.jpg")
    draw=ImageDraw.Draw(img)
    fillcolor = "#ff0000"  # R,G,B的值
    width, height = img.size
    ranNum=uuid.uuid4().time_low
    draw.text((0, 0), str(ranNum), font=font, fill="#000000")
    img.save("2.jpg")

def convertPic():
    convert("jpg")
    convert("png")
    convert("gif")
    convert("jpeg")

def getLog():
    f=open("1.log")
    o=open("log.log",'w')
    for line in f:
        if(line.startswith("LOG")):
            o.write(line)
    f.close()
    o.close()


# deleteFile()
# addnumber()
getLog()