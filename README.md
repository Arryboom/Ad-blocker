# Ad-Blocker

Using Deep Learning to detect and block advertisements


# Requirements

>* [tensorflow](https://github.com/tensorflow/tensorflow)
>* [mitmproxy](https://github.com/mitmproxy/mitmproxy)

# Usage

```mitmdump -s mitmProxy.py```      
then point your browser proxy to http://127.0.0.1:8080

or

```mitdump -s mitmProxy.py --socks```     
then point your browser proxy to socks5://127.0.0.1:8080

# How to train the dataset

follow the [instruction](https://www.tensorflow.org/how_tos/image_retraining/) to retrain the dataset,then put the  .pd and label file into the source
 folder


