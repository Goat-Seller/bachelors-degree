import dearpygui.dearpygui as dpg
from gui import image_manager
from gui import layout_manager

VIEWPORT_WIDTH = 1200
VIEWPORT_HEIGHT = 800

dpg.create_context()

# --- INITIALIZATION EXTERNAL MODULES ---
image_manager.setup_image_system(resize_callback=layout_manager.resize_handler)


# --- MAIN VIEW ---
with dpg.window(tag="Main Window"):
    with dpg.table(header_row=False, resizable=True, policy=dpg.mvTable_SizingStretchProp):
        dpg.add_table_column()
        dpg.add_table_column()

        # --- TOP ROW ---
        with dpg.table_row():
            with dpg.child_window(tag="TopLeft"):
                dpg.add_text("Original Image to Draw", color=(150, 255, 150))
                dpg.add_separator()
                dpg.add_button(label="Load Image", callback=lambda: dpg.show_item("FileDialog"))
                
            with dpg.child_window(tag="TopRight"):
                dpg.add_text("Current Transformation Process", color=(150, 255, 255))
                dpg.add_separator()

        # --- BOTTOM ROW ---
        with dpg.table_row():
            with dpg.child_window(tag="BottomLeft"):
                dpg.add_text("Current Drawing Process", color=(255, 200, 150))
                dpg.add_separator()
                
            with dpg.child_window(tag="BottomRight"):
                dpg.add_text("Full G-code Output", color=(255, 150, 255))
                dpg.add_separator()
                dpg.add_input_text(
                    multiline=True, 
                    default_value="G90 ; Absolute positioning\nG21 ; Set units to millimeters\nG00 X0 Y0 ; Move to origin\n...", 
                    width=-1, 
                    height=-1
                )

# --- INITIALIZATION ---
dpg.create_viewport(title='CNC Image to G-Code Generator', width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT)

dpg.set_viewport_resize_callback(layout_manager.resize_handler)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main Window", True)

layout_manager.resize_handler(None, None, None)

while dpg.is_dearpygui_running():
    # Check frame_queue here with get_nowait() and call dpg.set_value(...)
    dpg.render_dearpygui_frame()
dpg.destroy_context()