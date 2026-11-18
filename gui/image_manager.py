import dearpygui.dearpygui as dpg
from image_processing import pipeline
from image_processing import utility

# Wewnętrzny słownik przechowujący stan załadowanego obrazu
_image_state = {
    "width": 0,
    "height": 0,
    "cv_image": None  
}

def get_image_size():
    """Zwraca obecną szerokość i wysokość załadowanego obrazu."""
    return _image_state["width"], _image_state["height"]

def _on_image_selected(sender, app_data, user_data):
    """Callback wywoływany po wybraniu pliku w oknie dialogowym."""
    file_path = app_data['file_path_name']

    image_data = dpg.load_image(file_path)
    cv_image = utility.load_cv(file_path)
    if image_data is None:
        print(f"BŁĄD: Nie udało się wczytać pliku {file_path}")
        return


    width, height, channels, data = image_data
    
    # Zapisujemy obraz i wymiary do stanu
    _image_state["cv_image"] = cv_image
    _image_state["width"] = width
    _image_state["height"] = height

    # Czyścimy stare elementy
    if dpg.does_item_exist("OriginalImage"):
        dpg.delete_item("OriginalImage")
    if dpg.does_item_exist("Original_Image_Texture"):
        dpg.delete_item("Original_Image_Texture")

    # Ładujemy nową teksturę
    texture_id = dpg.add_static_texture(
        width=width,
        height=height,
        default_value=data,
        parent="Texture_Registry",
        tag="Original_Image_Texture"
    )

    # Dodajemy obraz do głównego interfejsu (tag TopLeft musi istnieć w main.py)
    dpg.add_image(texture_id, parent="TopLeft", tag="OriginalImage", user_data=(width, height))
    
    # Create RGBA float32 buffer
    initial_blank_buffer = utility.create_image_buffer(width,height)
    setup_transformed_texture(width, height, initial_blank_buffer)
    
    # Wywołujemy resize_handler, który został przekazany przez user_data podczas inicjalizacji
    if user_data:
        user_data(None, None, None)

def setup_image_system(resize_callback):
    """
    Inicjalizuje rejestr tekstur i okno dialogowe.
    Przyjmuje funkcję callback (resize), aby móc wymusić odświeżenie interfejsu po załadowaniu.
    """
    with dpg.texture_registry(tag="Texture_Registry", show=False):
        pass

    with dpg.file_dialog(
        show=False,
        callback=_on_image_selected,
        user_data=resize_callback, # <-- Przekazujemy funkcję odświeżającą z main.py
        tag="FileDialog",
        width=750,
        height=450):
        dpg.add_file_extension("Image files (*.png *.jpg *.jpeg){.png,.jpg,.jpeg}", color=(255, 255, 255, 255))
        dpg.add_file_extension(".*", color=(255, 255, 255, 255))

def setup_transformed_texture(width, height, initial_data):
    """
    Tworzy teksturę dynamiczną w rejestrze oraz widżet obrazu w oknie TopRight.
    """
    # Sprawdzamy czy rejestr tekstur dynamicznych istnieje, jeśli nie - tworzymy go
    if not dpg.does_item_exist("Dynamic_Texture_Registry"):
        with dpg.texture_registry(tag="Dynamic_Texture_Registry", show=False):
            pass
    if dpg.does_item_exist("TransformedImage"):
        dpg.delete_item("TransformedImage")
    if dpg.does_item_exist("Transformed_Image_Texture"):
        dpg.delete_item("Transformed_Image_Texture")

    dpg.add_raw_texture(
        width=width,
        height=height,
        default_value=initial_data,
        format=dpg.mvFormat_Float_rgba,
        parent="Dynamic_Texture_Registry",
        tag="Transformed_Image_Texture"
    )

    # Dodajemy widżet wyświetlający teksturę w kontenerze TopRight
    dpg.add_image(
        "Transformed_Image_Texture", 
        parent="TopRight", 
        tag="TransformedImage", 
        user_data=(width, height)
    )

def get_cv_image():
    return _image_state["cv_image"]


