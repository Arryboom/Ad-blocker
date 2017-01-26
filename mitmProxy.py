"""
This script rotates all images passing through the proxy by 180 degrees.
"""
import io
from PIL import Image
import tensorflow as tf
from mitmproxy.script import concurrent
import logging
import uuid
from PIL import ImageDraw
from PIL import ImageFont
path="/Users/hsin/Documents/Project/Python/labelFlower/"

# Loads label file, strips off carriage return
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler(path+'img.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

font = ImageFont.truetype(path+"arial.ttf", 20)

print("+++++++++LOADING!")
with tf.gfile.FastGFile(path+"retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')
    sess = tf.Session()
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    print("++++++++++LOADED")
    erFilePath = path+"1.jpg"


@concurrent
def response(flow):
    if flow.response.headers.get("content-type", "").startswith("image"):
        s = io.BytesIO(flow.response.content)
        s2 = io.BytesIO()
        try:
            Image.open(s).convert('RGB').save(s2, "JPEG")
            image_data = s2.getvalue()
        except Exception as ex:
            errorf = open(erFilePath, 'rb')
            flow.response.content = errorf.read()
            flow.response.headers["content-type"] = "image/png"
            print("error image")
            return
        predictions = sess.run(softmax_tensor, \
                               {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        predictions[0].argsort()[-len(predictions[0]):][::-1]
        # Ads
        imgUrl=flow.request.url
        ranNum = uuid.uuid4().time_low
        logger.info(str(ranNum)+" "+imgUrl)
        s3 = io.BytesIO()

        if predictions[0][0] > 0.5:
            errorf = open(erFilePath, 'rb')
            img = Image.open(erFilePath)
            draw = ImageDraw.Draw(img)
            draw.text((0, 0), str(ranNum), font=font, fill="#000000")
            img.save(s3,"PNG")
            flow.response.content = s3.getvalue()
            flow.response.headers["content-type"] = "image/png"
        else:
            img = Image.open(s)
            draw = ImageDraw.Draw(img)
            draw.text((0, 0), str(ranNum), font=font, fill="#000000")
            img.save(s3,"PNG")
            flow.response.content = s3.getvalue()
            flow.response.headers["content-type"] = "image/png"
