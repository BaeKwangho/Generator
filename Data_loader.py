import PIL.Image as Image
import numpy as np
import matplotlib.pyplot as plt
import cv2

class DataLoader(object):
    def __init__(self,txt_path,bg_path):
        self.txt_path = txt_path
        self.bg_path = bg_path
        
    