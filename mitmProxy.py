
import io
from PIL import Image
import tensorflow as tf
from mitmproxy.script import concurrent
from mitmproxy import http
import uuid
from PIL import ImageDraw
from PIL import ImageFont
import logging

# can not be same,the script will reload again and again
path="/Users/hsin/Documents/Project/Python/labelFlower/"
logPath="/Users/hsin/Documents/img.log"

font = ImageFont.truetype(path+"arial.ttf", 14)
font.color = "black"
logger = logging.getLogger('myapp')

hdlr = logging.FileHandler(logPath)

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


logger.info("STU LOAD BEGIN")
with tf.gfile.FastGFile(path+"retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')
    sess = tf.Session()
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    erFilePath = path+"1.jpg"
logger.info("STU LOAD END")

reqList=[]

@concurrent
def response(flow):
    if flow.response.headers.get("content-type", "").startswith("image"):

        imgUrl = flow.request.url
        ranNum = uuid.uuid4().time_low

        if(imgUrl in reqList):
            logger.info("STU PROCESS RETURN "+str(ranNum) + " " + imgUrl)
            flow.response = http.HTTPResponse.make(404)
            return
        else:
            reqList.append(imgUrl)
        logger.info("STU PROCESS BEGIN " + str(ranNum) + " " + imgUrl)
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
        logger.info("STU PROCESS END " + str(ranNum) + " " + imgUrl)
        # Sort to show labels of first prediction in order of confidence
        predictions[0].argsort()[-len(predictions[0]):][::-1]
        # Ads
        s3 = io.BytesIO()

        if predictions[0][0] > 0.5:
            img = Image.open(erFilePath)
            draw = ImageDraw.Draw(img)
            draw.text((0, 0), str(ranNum), font=font,fill="#000000")
            img.save(s3,"PNG")
            flow.response.content = s3.getvalue()
            # flow.response.content = s.getvalue()
            flow.response.headers["content-type"] = "image/png"
            logger.info("STU OUT AD " + str(ranNum) + " " + imgUrl)
        else:
            img = Image.open(s)
            draw = ImageDraw.Draw(img)
            draw.text((0, 0), str(ranNum), font=font,fill="#000000")
            img.save(s3,"PNG")
            flow.response.content = s3.getvalue()
            # flow.response.content = s.getvalue()
            flow.response.headers["content-type"] = "image/png"
            logger.info("STU OUT NO " + str(ranNum) + " " + imgUrl)
