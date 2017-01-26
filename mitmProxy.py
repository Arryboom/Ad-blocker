"""
This script rotates all images passing through the proxy by 180 degrees.
"""
import io
from PIL import Image
import tensorflow as tf
from mitmproxy.script import concurrent

# Loads label file, strips off carriage return

print("+++++++++LOADING!")
with tf.gfile.FastGFile("/Users/hsin/Documents/Project/Python/labelFlower/retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')
sess = tf.Session()
softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
print("++++++++++LOADED")
erFilePath = "/Users/hsin/Documents/Project/Python/labelFlower/1.jpg"


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
        if predictions[0][0] > 0.5:
            errorf = open(erFilePath, 'rb')
            flow.response.content = errorf.read()
            flow.response.headers["content-type"] = "image/png"
        else:
            flow.response.content = s.getvalue()
            flow.response.headers["content-type"] = "image/png"
