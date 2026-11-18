import threading
import time
from image_processing import pipeline, processing_worker

img = pipeline.load_cv("assets/current_wallpaper.png")
assert img is not None, "Failed to load test image!"

# 2. Spawn the background worker thread (just like a Start button will do later)
worker = threading.Thread(
    target=processing_worker.background_processing_worker,
    args=(img,),
    daemon=True
)
print("Main thread: Starting background worker...")
worker.start()

# 3. Simulate the main thread polling the queue while the worker runs
while worker.is_alive() or not processing_worker.frame_queue.empty():
    while not processing_worker.frame_queue.empty():
        w, h, flat_data = processing_worker.frame_queue.get_nowait()
        print(
            f"Main thread received frame -> {w}x{h} | "
            f"dtype: {flat_data.dtype} | "
            f"range: [{flat_data.min():.1f}, {flat_data.max():.1f}] | "
            f"length valid: {len(flat_data) == w * h * 4}"
        )
    time.sleep(0.1)

print("Main thread: All stages processed and received cleanly.")