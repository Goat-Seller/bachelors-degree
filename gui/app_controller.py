import threading
import queue
from gui import image_manager
import dearpygui.dearpygui as dpg
from image_processing import processing_worker

active_worker_thread = None

def app_start():
    # Poll the thread-safe queue without blocking the 60 FPS render loop
    while not processing_worker.frame_queue.empty():
        try:
            width, height, flat_data = processing_worker.frame_queue.get_nowait()
            if dpg.does_item_exist("Transformed_Image_Texture"):
                dpg.set_value("Transformed_Image_Texture", flat_data)
        except queue.Empty:
            break
    dpg.render_dearpygui_frame()

def start_processing_callback(sender, app_data, user_data):
    global active_worker_thread

    # Do nothing if no image is loaded yet
    cv_img = image_manager.get_cv_image()
    if cv_img is None:
        print("Load an image first before starting processing.")
        return

    # Prevent overlapping worker threads if already running
    if active_worker_thread is not None and active_worker_thread.is_alive():
        print("Processing is already running.")
        return

    # Clear any stale frames from a previous run
    while not processing_worker.frame_queue.empty():
        try:
            processing_worker.frame_queue.get_nowait()
        except queue.Empty:
            break

    # Spawn the background daemon thread
    active_worker_thread = threading.Thread(
        target=processing_worker.background_processing_worker,
        args=(cv_img,),
        daemon=True
    )
    active_worker_thread.start()