import customtkinter as ctk
from PIL import Image, ImageTk
import pandas as pd
import openpyxl
import xlsxwriter
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import filedialog

font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 1
font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 2

def create_frame(parent,wight, height, x, y, fg_color, bg_color):
    frame = ctk.CTkFrame(master=parent,width=wight, height=height, fg_color=fg_color, bg_color=bg_color)
    frame.place(x=x, y=y)
    return frame
def create_label(parent, text, x, y):
    label = ctk.CTkLabel(parent, text=text, font=font1)
    label.place(x=x, y=y)
    return label
def create_entry(parent, wight, textvariable, x, y):
    Entry = ctk.CTkEntry(master=parent, width=wight, textvariable=textvariable)
    Entry.place(x=x, y=y)
    return Entry
def create_button(parent, text, command, font, width, x, y):
    button = ctk.CTkButton(master=parent, text=text, command=command, font=font, width=width)
    button.place(x=x, y=y)
    return button
def show_oxigen_properties(app):
    # Если изображение еще не было загружено, загружаем его
    if app.global_image is None:
        original_image = Image.open("oxigen.png")  # Путь к изображению
        resized_image = original_image.resize((round(1710 * 0.57), round(585 * 0.57)), Image.Resampling.LANCZOS)
        app.global_image = ImageTk.PhotoImage(resized_image)

    # Если метка изображения еще не была создана, создаем ее
    if app.image_label is None:
        app.image_label = ctk.CTkLabel(app, image=app.global_image)
        app.image_label.place(x=215, y=80)
        app.image_label.configure(text="")
    else:
        app.image_label.configure(image=app.global_image)
        app.image_label.place(x=215, y=80)
        app.image_label.configure(text="")

    if app.image_label_1 is not None:
        app.image_label_1.place_forget()
def show_fuel_properties(app):
    if app.global_image_1 is None:
        # Сначала изменяем размер изображения с помощью Pillow
        original_image_1 = Image.open("fuel.png")  # Замените на путь к вашему изображению
        resized_image_1 = original_image_1.resize((round(1710 * 0.56), round(720 * 0.56)),Image.Resampling.LANCZOS)  # Изменяем размер
        app.global_image_1 = ImageTk.PhotoImage(resized_image_1)

    # Если метка изображения еще не была создана, создаем ее
    if app.image_label_1 is None:
        app.image_label_1 = ctk.CTkLabel(app, image=app.global_image_1)
        app.image_label_1.place(x=220, y=80)  # Размещаем метку в координатах x=220, y=150
        app.image_label_1.configure(text="")
    else:
        # Просто обновляем изображение метки
        app.image_label_1.configure(image=app.global_image_1)
        app.image_label_1.place(x=220, y=80)
        app.image_label_1.configure(text="")
    if app.image_label is not None:
        app.image_label.place_forget()  # Скрываем метку изображения
def save_to_excel_I_a(impulse_array, alpha_array):
    df = pd.DataFrame({'Коэффициент избытка окислителя': alpha_array,'Импульс': impulse_array})
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                             filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        df.to_excel(file_path, index=False)
def save_to_txt_I_a(impulse_array, alpha_array):
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        with open(file_path, 'w') as f:
            for i, alpha in zip(impulse_array, alpha_array):
                f.write(f'{i}\t{alpha}\n')
def save_to_excel_T_a(impulse_array, alpha_array):
    df = pd.DataFrame({'Коэффициент избытка окислителя': alpha_array, 'Температура': impulse_array})
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                             filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        df.to_excel(file_path, index=False)
def save_to_txt_T_a(impulse_array, alpha_array):
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        with open(file_path, 'w') as f:
            for i, alpha in zip(impulse_array, alpha_array):
                f.write(f'{i}\t{alpha}\n')
def save_to_excel_R_a(impulse_array, alpha_array):
    df = pd.DataFrame({'Коэффициент избытка окислителя': alpha_array, 'Газовая постоянная': impulse_array})
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                             filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        df.to_excel(file_path, index=False)
def save_to_txt_R_a(impulse_array, alpha_array):
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        with open(file_path, 'w') as f:
            for i, alpha in zip(impulse_array, alpha_array):
                f.write(f'{i}\t{alpha}\n')
def save_properties_txt(properties):
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        with open(file_path, 'w') as f:
            f.write(properties)
def save_mass_txt(species_names,mass_fractions,mole_fractions):
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        with open(file_path, 'w') as f:
            f.write(f'Компонент\tМас. доля\tМольная доля\n')
            for name, mass_frac, mole_frac in zip(species_names, mass_fractions,mole_fractions):
                f.write(f'{name}\t{mass_frac}\t{mole_frac}\n')
def save_all_txt(properties,properties_2,properties_3,species_names,mass_fractions,mole_fractions,species_names_2,mass_fractions_2,mole_fractions_2,species_names_3,mass_fractions_3,mole_fractions_3):
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