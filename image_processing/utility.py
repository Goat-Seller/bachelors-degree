import numpy as np
import cv2 as cv

def image_to_dpg(image):
    return cv.cvtColor(image, cv.COLOR_GRAY2RGBA)
    
def normalization(image):
    return image.astype(np.float32) / 255.0

def format_to_dpg(image):
    image = image_to_dpg(image)
    image = normalization(image)
    height, width, _ = image.shape
    return width, height, image.ravel()

def load_cv(path):
    return cv.imdecode(np.fromfile(path, dtype=np.uint8), cv.IMREAD_COLOR) # format wczytywania uwzględniajaca polskie znaki w scieżce

def create_image_buffer(width,height):
    "Create RGBA Float32 buffer."
    return np.zeros(width * height * 4, dtype=np.float32)

