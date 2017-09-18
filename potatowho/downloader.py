import sys, os
import util as dataset_utils
import tensorflow as tf
from pathlib import Path

# Class for 
class Downloader:
    def __init__(self, relative_path = "checkpoints", url = "http://download.tensorflow.org/models/inception_v4_2016_09_09.tar.gz"):
        self.relative_path = relative_path
        self.url = url
        
    def download(self):
        if not tf.gfile.Exists(self.relative_path):
            tf.gfile.MakeDirs(self.relative_path)

        abs_path = os.path.join(os.getcwd(), self.relative_path)
        filename = self.url.split('/')[-1]

        if Path(os.path.join(abs_path, filename)).is_file():
            print("The checkpoint exists already, don't worry about it")
        else:
            dataset_utils.download_and_uncompress_tarball(self.url, self.relative_path)