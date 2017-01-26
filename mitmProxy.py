"""
This script rotates all images passing through the proxy by 180 degrees.
"""
import io
from PIL import Image
import tensorflow as tf
from mitmproxy.script import concurrent

# Loads label file, strips off carriage return






    # Unpersists graph from file
with tf.gfile.FastGFile("/Users/hsin/Documents/Project/Python/labelFlower/retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')
print ("AAAAAAAAAAAAAAAA++++++LOAD!")


sess=tf.Session()
softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

@concurrent
def response(flow):
    if flow.response.headers.get("content-type", "").startswith("image"):
        s = io.BytesIO(flow.response.content)
        s2 = io.BytesIO()
        try:
            img = Image.open(s).convert('RGB').save(s2,"JPEG")
            image_data=s2.getvalue()
        except Exception as ex:
            errorFile = "/Users/hsin/Documents/Project/Python/labelFlower/1.jpg"
            errorf = open(errorFile, 'rb')
            flow.response.content = errorf.read()
            flow.response.headers["content-type"] = "image/png"
            print("error image")
            return

        predictions = sess.run(softmax_tensor, \
                                   {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        label_lines=["ads","normal"]
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            if human_string == "normal" and score > 0.5:
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA++++++++++NORMAL")
                # copyfile(varPath + "/" + imageFile, normalDir + "/" + newFileName)
                flow.response.content = s.getvalue()
                flow.response.headers["content-type"] = "image/png"
                print('%s (score = %.5f)' % (human_string, score))
            if human_string == "ads" and score > 0.5:
                errorFile = "/Users/hsin/Documents/Project/Python/labelFlower/1.jpg"
                errorf = open(errorFile, 'rb')
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA++++++++++ADS")
                flow.response.content = errorf.read()
                flow.response.headers["content-type"] = "image/png"


