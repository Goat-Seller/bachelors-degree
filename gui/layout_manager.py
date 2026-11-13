import dearpygui.dearpygui as dpg
from gui import image_manager

PADDING = 15
TOP_UI_HEIGHT = 80

image_tags = ["OriginalImage", "TransformedImage", "FinalGCodeImage"]

def resize_handler(sender, app_data, user_data):
    vp_width = dpg.get_viewport_client_width()
    vp_height = dpg.get_viewport_client_height()
    
    child_width = (vp_width // 2) - PADDING 
    child_height = (vp_height // 2) - PADDING 
    
    # Scaling main windows
    for window_tag in ["TopLeft", "TopRight", "BottomLeft", "BottomRight"]:
        if dpg.does_item_exist(window_tag):
            dpg.set_item_height(window_tag, child_height)

            
    img_width, img_height = image_manager.get_image_size()
            
    # Scaling image
    for image in image_tags:
        if dpg.does_item_exist(image):
            
            img_width, img_height = dpg.get_item_user_data(image)
            
            if img_width > 0 and img_height > 0:
                avail_w = max(1, child_width - (PADDING * 2))
                avail_h = max(1, child_height - TOP_UI_HEIGHT)
                
                # Scaling with proportion
                scale = min(avail_w / img_width, avail_h / img_height)
                
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                
                dpg.set_item_width(image, new_width)
                dpg.set_item_height(image, new_height)