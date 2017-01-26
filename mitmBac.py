"""
This script rotates all images passing through the proxy by 180 degrees.
"""
import io
import random
from PIL import Image
import tensorflow as tf
from os import listdir
from os import mkdir
from shutil import copyfile
from os.path import isfile, join


# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line
        in tf.gfile.GFile("retrained_labels.txt")]
# Unpersists graph from file
with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')



def response(flow):
    if flow.response.headers.get("content-type", "").startswith("image"):
        s = io.BytesIO(flow.response.content)
        #img = Image.open(s).rotate(180)
        img = Image.open(s)
        s2 = io.BytesIO()
        img.save(s2, "png")
        ranNum=random.uniform(100000,999999)
        picName="temp/"+str(ranNum)+'.jpg'
        img.convert('RGB').save(picName)

        image_path = picName

        # Read in the image_data

        image_data = tf.gfile.FastGFile(image_path, 'rb').read()

        with tf.Session() as sess:
            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

            predictions = sess.run(softmax_tensor, \
                                   {'DecodeJpeg/contents:0': image_data})

            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

            for node_id in top_k:
                human_string = label_lines[node_id]
                score = predictions[0][node_id]
                if human_string == "normal" and score > 0.5:
                    #copyfile(varPath + "/" + imageFile, normalDir + "/" + newFileName)
                    flow.response.content = s.getvalue()
                    print('%s (score = %.5f)' % (human_string, score))
                if human_string == "ads" and score > 0.5:
                    #copyfile(varPath + "/" + imageFile, adsDir + "/" + newFileName)
                    flow.response.content = s2.getvalue()
                    print('%s (score = %.5f)' % (human_string, score))
                    # os.remove(os.path.abspath(imageFile))
        flow.response.content = s2.getvalue()
        flow.response.headers["content-type"] = "image/png"