import cv2 as cv
import numpy as np

def grayscale(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY) 
    
def gaussian_blur(image):
    return cv.GaussianBlur(image, (5, 5), 0)

def otsu_threshold(image):
    _, thresh = cv.threshold(image,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    return thresh

def canny(image):
    return cv.Canny(image, 100, 200)

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

def process_image_pipeline(image):

    if image is None or image.size == 0:
        raise  ValueError("Wejściowa macierz obrazu jest niepoprawna.")

    # 1. Przekształcenie do skali szarości metodą luminancji
    gray = grayscale(image)

    # 2. Wygładzanie (filtr Gaussa) w celu redukcji szumów wysokoczęstotliwościowych - maska = 5x5 std dev. = 0
    blurred = gaussian_blur(gray)

    # 3. Detekcja krawędzi z użyciem algorytmu Canny'ego (100 - min threshold, 200 - max -threshold) - standardowa heurestyka
    edges = canny(blurred)

    # 4. Konwersja z powrotem do formatu RGBA wymaganego przez dpg
    edges_rgba = image_to_dpg(edges)

    # 5. Normalizacja wartości do zakresu [0.0, 1.0] i zmiana typu na float32
    normalized_data = normalization(edges_rgba)
    height, width, _ = normalized_data.shape
    
    # Zwracamy wymiary oraz spłaszczoną tablicę 1D
    return width, height, normalized_data.ravel()