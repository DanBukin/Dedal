# Импорт библиотек
import customtkinter as ctk
from PIL import Image, ImageTk

global_image = None
image_label = None
global_image_1 = None
image_label_1 = None
oxigen = None
fuel = None
label_oxigen = None
label_fuel = None

def get_selected_option():
    # Возвращает выбранный вариант
    selected_option = None
    if radio_var.get() == 1:
        selected_option = "Равновесный"
    elif radio_var.get() == 2:
        selected_option = "Замороженный"
    return selected_option

def get_selected_option_alpha():
    # Возвращает выбранный вариант
    selected_option_alpha = None
    if radio_var_alpha.get() == 1:
        selected_option_alpha = "Оптимальный"
    elif radio_var_alpha.get() == 2:
        selected_option_alpha = "Заданный"
    return selected_option_alpha







