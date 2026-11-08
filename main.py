import dearpygui.dearpygui as dpg

dpg.create_context()

# Callback to keep the 4 sections scaled on resize
def resize_handler():
    # Get the current height
    height = dpg.get_viewport_client_height()
    
    # Calculate 50% height minus a small margin to prevent scrollbars
    child_height = (height // 2) - 15 
    
    for window_tag in ["TopLeft", "TopRight", "BottomLeft", "BottomRight"]:
        if dpg.does_item_exist(window_tag):
            dpg.set_item_height(window_tag, child_height)

with dpg.window(tag="Main Window"):
    
    with dpg.table(header_row=False, resizable=True, policy=dpg.mvTable_SizingStretchProp):
        dpg.add_table_column()
        dpg.add_table_column()

        # --- TOP ROW ---
        with dpg.table_row():
            # Top Left: Original Image
            with dpg.child_window(tag="TopLeft"):
                dpg.add_text("1. Original Image to Draw", color=(150, 255, 150))
                dpg.add_separator()
                # TODO: Add dpg.add_image() or drawlist here
                
            # Top Right: Transformation Process
            with dpg.child_window(tag="TopRight"):
                dpg.add_text("2. Current Transformation Process", color=(150, 255, 255))
                dpg.add_separator()
                # TODO: Add matrices, sliders, or intermediate image previews here

        # --- BOTTOM ROW ---
        with dpg.table_row():
            # Bottom Left: Current Drawing Process
            with dpg.child_window(tag="BottomLeft"):
                dpg.add_text("3. Current Drawing Process", color=(255, 200, 150))
                dpg.add_separator()
                # TODO: Add live drawing simulation or progress bar here
                
            # Bottom Right: Full G-code
            with dpg.child_window(tag="BottomRight"):
                dpg.add_text("4. Full G-code Output", color=(255, 150, 255))
                dpg.add_separator()
                
                # Example G-code
                dpg.add_input_text(
                    multiline=True, 
                    default_value="G90 ; Absolute positioning\nG21 ; Set units to millimeters\nG00 X0 Y0 ; Move to origin\n...", 
                    width=-1, 
                    height=-1
                )

# Viewport setup
dpg.create_viewport(title='CNC Image to G-Code Generator', width=1200, height=800)

# Attach the resize callback to the viewport
dpg.set_viewport_resize_callback(resize_handler)

dpg.setup_dearpygui()
dpg.show_viewport()

# Bind the UI to fill the entire application window
dpg.set_primary_window("Main Window", True)


dpg.start_dearpygui()
dpg.destroy_context()