from __future__ import absolute_import, division, print_function, unicode_literals
import os

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)

class ImageDataFolder:

    DIRECTORIES = ['train', 'test']

    def __init__(self, path):
        self.path = path
        self._class_names = None
        self.validate(path)

    def validate(self, path):
        assert set(self.DIRECTORIES).issubset(set(os.listdir(self.path)))
    
    def load_data(self):
        train_labels = self.get_class_names().values()
        train_images = None
        test_labels = self.get_labels('test')
        test_images = None
        return (train_images, train_labels), (test_images, test_labels)

    def get_labels(self, directory):
        return os.listdir('%s/%s' % (self.path, directory))


    def get_class_names(self):
        if self._class_names is None:
            self._class_names = {
                index: lable for index, lable in enumerate(image_data.labels)
            }
        return self._class_names

    @property
    def labels(self):
        return self.get_labels('train')

##############################
###   Import the dataset   ###
##############################

image_data = ImageDataFolder('assets')

(train_images, train_labels), (test_images, test_labels) = image_data.load_data()

class_names = image_data.get_class_names()
assert False, class_names

##############################
###   Import the dataset   ###
##############################
print(len(train_labels))
plt.imshow(train_images[0])