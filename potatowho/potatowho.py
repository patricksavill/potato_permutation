import sys, os
import numpy as np
from matplotlib import pyplot as plt
import tensorflow as tf

try:
    import urllib2 as urllib
except ImportError:
    import urllib.request as urllib

# The following is a bit cheeky. This whole thing needs the repository found here https://github.com/tensorflow/models, or specifically
# the slim package found within. This works around having to add that package to the path by checking some common spots first
def import_slim_modules():
    global imagenet, inception, inception_preprocessing
    from datasets import imagenet
    from nets import inception
    from preprocessing import inception_preprocessing

try:
    import_slim_modules()
except ImportError:
    # Try find slim relatively, if not then get the user to input it
    abs_path = os.path.abspath(os.path.dirname('../../models/slim/'))
    if os.path.isabs(abs_path):
        sys.path.append(abs_path)
        import_slim_modules()
    else:
        abs_path = input("Slim isn't set on pythons path. Enter the absolute path of Slim to fix this: ")
        sys.path.append(abs_path)
        import_slim_modules()

from tensorflow.contrib import slim
from downloader import Downloader

CHECKPOINTS_DIR = "checkpoints"

dl = Downloader(relative_path = CHECKPOINTS_DIR)
dl.download()

image_size = inception.inception_v4.default_image_size

with tf.Graph().as_default():
    url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Russet_potato_cultivar_with_sprouts.jpg/1920px-Russet_potato_cultivar_with_sprouts.jpg'
    image_string = urllib.urlopen(url).read()
    image = tf.image.decode_jpeg(image_string, channels=3)
    processed_image = inception_preprocessing.preprocess_image(image, image_size, image_size, is_training=False)
    processed_images  = tf.expand_dims(processed_image, 0)
    
    # Create the model, use the default arg scope to configure the batch norm parameters.
    with slim.arg_scope(inception.inception_v4_arg_scope()):
        logits, _ = inception.inception_v4(processed_images, num_classes=1001, is_training=False)
    probabilities = tf.nn.softmax(logits)
    
    init_fn = slim.assign_from_checkpoint_fn(
        os.path.join(CHECKPOINTS_DIR, 'inception_v4.ckpt'),
        slim.get_model_variables('InceptionV4'))
    
    with tf.Session() as sess:
        init_fn(sess)
        np_image, probabilities = sess.run([image, probabilities])
        probabilities = probabilities[0, 0:]
        sorted_inds = [i[0] for i in sorted(enumerate(-probabilities), key=lambda x:x[1])]

    names = imagenet.create_readable_names_for_imagenet_labels()
    for i in range(5):
        index = sorted_inds[i]
        print('Probability %0.2f%% => [%s]' % (probabilities[index] * 100, names[index]))
