from dedal_graphs import *
from PIL import Image, ImageTk
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os
from ctypes import windll


if os.name == 'nt':
    windll.gdi32.AddFontResourceExW("data/ofont.ru_Futura PT.ttf", 0x10, 0)
else:
    pass
font0 = ("Futura PT Book", 18)
font1 = ("Futura PT Book", 16)
font2 = ("Futura PT Book", 14)
def create_frame(parent,wight, height, x, y, fg_color, bg_color):
    """=====Быстрое создание мини-окон====="""
    frame = ctk.CTkFrame(master=parent,width=wight, height=height, fg_color=fg_color, bg_color=bg_color)
    frame.place(x=x, y=y)
    return frame
def create_label(parent, text, x, y):
    """=====Быстрое создание надписей с шрифтом №1====="""
    label = ctk.CTkLabel(parent, text=text, font=font1)
    label.place(x=x, y=y)
    return label
def create_label_0(parent, text, x, y):
    """=====Быстрое создание мини-окон с шрифтом №0====="""
    label = ctk.CTkLabel(parent, text=text, font=font0)
    label.place(x=x, y=y)
    return label
def create_label_2(parent, text, x, y):
    """=====Быстрое создание мини-окон с шрифтом №2====="""
    label = ctk.CTkLabel(parent, text=text, font=font2)
    label.place(x=x, y=y)
    return label
def create_entry(parent, wight, textvariable, x, y):
    """=====Быстрое создание ячеек для ввода числа====="""
    Entry = ctk.CTkEntry(master=parent, width=wight, textvariable=textvariable)
    Entry.place(x=x, y=y)
    return Entry
def create_button(parent, text, command, font, width, x, y):
    """=====Быстрое создание кнопок====="""
    button = ctk.CTkButton(master=parent, text=text, command=command, font=font, width=width)
    button.place(x=x, y=y)
    return button
def show_spravka(app):
    """=====Создание изображения со справкой====="""
    if app.global_image_3 is None:
        # Сначала изменяем размер изображения с помощью Pillow
        original_image_3 = Image.open("data/Spravka.png")  # Замените на путь к вашему изображению
        resized_image_3 = original_image_3.resize((round(1130 * 0.83), round(422 * 0.83)),
                                                  Image.Resampling.LANCZOS)  # Изменяем размер
        app.global_image_3 = ImageTk.PhotoImage(resized_image_3)

    # Если метка изображения еще не была создана, создаем ее
    if app.image_label_3 is None:
        app.image_label_3 = ctk.CTkLabel(app, image=app.global_image_3)
        app.image_label_3.place(x=225, y=95)  # Размещаем метку в координатах x=220, y=150
        app.image_label_3.configure(text="")
    else:
        # Просто обновляем изображение метки
        app.image_label_3.configure(image=app.global_image_3)
        app.image_label_3.place(x=225, y=95)
        app.image_label_3.configure(text="")
    if app.image_label is not None:
        app.image_label.place_forget()  # Скрываем метку изображения
    if app.image_label_1 is not None:
        app.image_label_1.place_forget()  # Скрываем метку изображения
    if app.image_label_2 is not None:
        app.image_label_2.place_forget()  # Скрываем метку изображения
def show_oxigen_properties(app):
    """=====Создание изображения с параметрами окислителей====="""
    # Если изображение еще не было загружено, загружаем его
    if app.global_image is None:
        original_image = Image.open("data/oxigen.png")  # Путь к изображению
        resized_image = original_image.resize((round(1710 * 0.57), round(585 * 0.57)), Image.Resampling.LANCZOS)
        app.global_image = ImageTk.PhotoImage(resized_image)

    # Если метка изображения еще не была создана, создаем ее
    if app.image_label is None:
        app.image_label = ctk.CTkLabel(app, image=app.global_image)
        app.image_label.place(x=215, y=100)
        app.image_label.configure(text="")
    else:
        app.image_label.configure(image=app.global_image)
        app.image_label.place(x=215, y=100)
        app.image_label.configure(text="")
    if app.image_label_1 is not None:
        app.image_label_1.place_forget()
    if app.image_label_2 is not None:
        app.image_label_2.place_forget()
    if app.image_label_3 is not None:
        app.image_label_3.place_forget()  # Скрываем метку изображения
def show_fuel_properties(app):
    """=====Создание изображения с параметрами горючих====="""
    if app.global_image_1 is None:
        # Сначала изменяем размер изображения с помощью Pillow
        original_image_1 = Image.open("data/fuel.png")  # Замените на путь к вашему изображению
        resized_image_1 = original_image_1.resize((round(1710 * 0.56), round(720 * 0.56)),Image.Resampling.LANCZOS)  # Изменяем размер
        app.global_image_1 = ImageTk.PhotoImage(resized_image_1)

    # Если метка изображения еще не была создана, создаем ее
    if app.image_label_1 is None:
        app.image_label_1 = ctk.CTkLabel(app, image=app.global_image_1)
        app.image_label_1.place(x=220, y=100)  # Размещаем метку в координатах x=220, y=150
        app.image_label_1.configure(text="")
    else:
        # Просто обновляем изображение метки
        app.image_label_1.configure(image=app.global_image_1)
        app.image_label_1.place(x=220, y=100)
        app.image_label_1.configure(text="")
    if app.image_label is not None:
        app.image_label.place_forget()  # Скрываем метку изображения
    if app.image_label_2 is not None:
        app.image_label_2.place_forget()
    if app.image_label_3 is not None:
        app.image_label_3.place_forget()  # Скрываем метку изображения
def show_alpha_properties(app):
    """=====Создание изображения с параметрами смешения компонентов====="""
    if app.global_image_2 is None:
        # Сначала изменяем размер изображения с помощью Pillow
        original_image_2 = Image.open("data/alpha_105.png")  # Замените на путь к вашему изображению
        resized_image_2 = original_image_2.resize((round(3564 * 0.22), round(1852 * 0.22)),Image.Resampling.LANCZOS)  # Изменяем размер
        app.global_image_2 = ImageTk.PhotoImage(resized_image_2)

    # Если метка изображения еще не была создана, создаем ее
    if app.image_label_2 is None:
        app.image_label_2 = ctk.CTkLabel(app, image=app.global_image_2)
        app.image_label_2.place(x=300, y=95)  # Размещаем метку в координатах x=220, y=150
        app.image_label_2.configure(text="")
    else:
        # Просто обновляем изображение метки
        app.image_label_2.configure(image=app.global_image_2)
        app.image_label_2.place(x=300, y=95)
        app.image_label_2.configure(text="")
    if app.image_label is not None:
        app.image_label.place_forget()  # Скрываем метку изображения
    if app.image_label_1 is not None:
        app.image_label_1.place_forget()  # Скрываем метку изображения
    if app.image_label_3 is not None:
        app.image_label_3.place_forget()  # Скрываем метку изображения
def save_properties_txt(properties):
    """=====Сохранение результатов в формате txt (1 параметр)====="""
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        with open(file_path, 'w') as f:
            f.write(properties)
def save_to_excel(impulse_array, alpha_array,text_1,text_2):
    """=====Сохранение результатов в формате excel (2 параметра)====="""
    df = pd.DataFrame({text_1: alpha_array,text_2: impulse_array})
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                             filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        df.to_excel(file_path, index=False)
def save_to_txt(impulse_array, alpha_array):
    """=====Сохранение результатов в формате txt (2 параметра)====="""
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        with open(file_path, 'w') as f:
            for i, alpha in zip(impulse_array, alpha_array):
                f.write(f'{i}\t{alpha}\n')

def save_mass_txt(species_names,mass_fractions,mole_fractions):
    """=====Сохранение результатов в формате txt (3 параметра)====="""
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        with open(file_path, 'w') as f:
            f.write(f'Компонент\tМас. доля\tМольная доля\n')
            for name, mass_frac, mole_frac in zip(species_names, mass_fractions,mole_fractions):
                f.write(f'{name}\t{mass_frac}\t{mole_frac}\n')
def save_txt_graph_poteri(phi_r,phi_tr,phi_s,beta_kon_grad):
    """=====Сохранение результатов в формате txt (4 параметра)====="""
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        with open(file_path, 'w') as f:
            for y_1,y_2,y_3,x in zip(phi_r,phi_tr,phi_s,beta_kon_grad):
                f.write(f'{y_1}\t{y_2}\t{y_3}\t{x}\n')
def save_excel_graph_poteri(phi_r,phi_tr,phi_s,beta_kon_grad):
    """=====Сохранение результатов в формате excel (4 параметра)====="""
    df = pd.DataFrame({'phi_r': phi_r, 'phi_tr': phi_tr, 'phi_s': phi_s, 'beta': beta_kon_grad})
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                             filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        df.to_excel(file_path, index=False)
def save_all_txt(properties,properties_2,properties_3,species_names,mass_fractions,mole_fractions,species_names_2,mass_fractions_2,mole_fractions_2,species_names_3,mass_fractions_3,mole_fractions_3):
    """=====Сохранение всех результатов в формате txt====="""
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        with open(file_path, 'w') as f:
            f.write(f"""------------------------Параметры в камере сгорания------------------------
""")
            f.write(properties)
            f.write(f"""
=============Содержание компонентов=============
""")
            f.write(f'Компонент\tМас. доля\tМольная доля\n')
            for name, mass_frac, mole_frac in zip(species_names, mass_fractions, mole_fractions):
                f.write(f'{name}\t{mass_frac}\t{mole_frac}\n')
            f.write(f"""

------------------------Параметры в критическом сечении------------------------
""")
            f.write(properties_2)
            f.write(f"""
=============Содержание компонентов=============
""")
            f.write(f'Компонент\tМас. доля\tМольная доля\n')
            for name, mass_frac, mole_frac in zip(species_names_2, mass_fractions_2, mole_fractions_2):
                f.write(f'{name}\t{mass_frac}\t{mole_frac}\n')
            f.write(f"""

------------------------Параметры на срезе сопла------------------------
""")
            f.write(properties_3)
            f.write(f"""
=============Содержание компонентов=============
""")
            f.write(f'Компонент\tМас. доля\tМольная доля\n')
            for name, mass_frac, mole_frac in zip(species_names_3, mass_fractions_3, mole_fractions_3):
                f.write(f'{name}\t{mass_frac}\t{mole_frac}\n')
