import time
import queue
from image_processing import pipeline

frame_queue = queue.Queue()

def background_processing_worker(image):
    """Runs pipeline stages in the background and sends each stage to the UI."""

    if image is None:
        print("Worker error: No image provided.")
        return


    
    # Define the sequence of pure functions from pipeline.py
    stages = [
        pipeline.grayscale,
        pipeline.gaussian_blur,
        # pipeline.otsu_threshold,
        pipeline.canny
    ]

    current_image = image.copy()

    for stage_func in stages:
        # 1. pipeline.py handles all OpenCV math
        current_image = stage_func(current_image)

        # 2. Covert image to dpg format
        width, height, flat_float32_rgba = pipeline.format_to_dpg(current_image)

        # 3. Push the ready-to-render frame into the thread-safe queue
        frame_queue.put((width, height, flat_float32_rgba))

        # 4. Pace the visualization so the user can watch each stage in TopRight
        time.sleep(1)