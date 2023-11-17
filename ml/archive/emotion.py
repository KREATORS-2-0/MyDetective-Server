'''
$ pip install deepface
'''

# import modules for emotion classification
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from deepface import DeepFace

# image path
image_path2 = 'https://www.shutterstock.com/image-photo/photo-portrait-calm-pretty-girl-260nw-1847880169.jpg'

try: 
  analysis = DeepFace.analyze(img_path=image_path2, actions=['emotion'])

  print(analysis)

except Exception as e:
  print("An error occurred:", e)