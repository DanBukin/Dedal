import math

import customtkinter as ctk
from PIL import Image, ImageTk
import pandas as pd
# import openpyxl
# import xlsxwriter
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import filedialog
import os
from ctypes import windll, byref, create_string_buffer
FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20
if os.name == 'nt':
    windll.gdi32.AddFontResourceExW("data/ofont.ru_Futura PT.ttf", FR_PRIVATE, 0)
else:
    pass
font0 = ("Futura PT Book", 18)  # Настройка пользовательского шрифта 1
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
def create_label_0(parent, text, x, y):
    label = ctk.CTkLabel(parent, text=text, font=font0)
    label.place(x=x, y=y)
    return label
def create_label_2(parent, text, x, y):
    label = ctk.CTkLabel(parent, text=text, font=font2)
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
def show_spravka(app):
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
def save_to_excel_param(x, y):
    df = pd.DataFrame({'X': x, 'Y': y})
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                             filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        df.to_excel(file_path, index=False)
def save_to_txt_param(x, y):
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        with open(file_path, 'w') as f:
            for x_0, y_0 in zip(x, y):
                f.write(f'{x_0}\t{y_0}\n')
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
def save_options_subsonic_txt(properties):
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        with open(file_path, 'w') as f:
            f.write(properties)
def save_geom_subsonic_txt(x_rr,y_rr):
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        with open(file_path, 'w') as f:
            for x, y in zip(x_rr, y_rr):
                f.write(f'{x}\t{y}\n')
def save_geom_subsonic_exel(x_rr,y_rr):
    df = pd.DataFrame({'X': x_rr, 'Y': y_rr})
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                             filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        df.to_excel(file_path, index=False)
def find_teta_a(p_a,p_k):
    p_a_1 = float(p_a) * 1000000
    p_k_1 = float(p_k) * 1000000
    num=p_k_1/p_a_1
    numbers=[10,50,100,500,1000,2000]
    if num < numbers[0]:
        return 6
    if num > numbers[-1]:
        return 12

    for i in range(len(numbers) - 1):
        if numbers[i] < num <= numbers[i + 1]:
            closer = numbers[i] if num - numbers[i] < numbers[i + 1] - num else numbers[i + 1]
            if closer == 10:
                return 6
            elif closer == 50:
                return 9
            elif closer == 100:
                return 9.5
            elif closer == 500:
                return 10
            elif closer == 1000:
                return 11.5
            else:
                return 12
def find_teta_m(w_a,T_kp,R,k):
    a_kp=(k*R*T_kp)**0.5
    lambda_a=w_a/a_kp
    k_1=( (k+1)/(k-1) )**0.5
    k_2=math.atan( (((k-1)/(k+1))**0.5) * (( ((lambda_a**2)-1)/(1-( ((k-1)*(lambda_a**2))/(k+1))) )**0.5) )
    k_3=math.atan(( ((lambda_a**2)-1)/(1-( ((k-1)*(lambda_a**2))/(k+1))) )**0.5)
    psi_lambda=k_1*k_2-k_3
    teta_m_1=(psi_lambda/3)*180/math.pi
    return teta_m_1
def find_coef_par(R_kp,R_a,teta_a,teta_m):
    print(R_kp,R_a,teta_a,teta_m)
    alpha_m =90-teta_m
    alpha_a =90-teta_a
    alpha_a_rad = math.pi * alpha_a / 180
    alpha_m_rad = math.pi * alpha_m / 180
    y_1=R_kp+(0.45*R_kp)-(0.45*R_kp*math.sin(alpha_m_rad))
    y_2=R_a
    a= (math.tan(alpha_m_rad)-math.tan(alpha_a_rad))/(2*(y_1-y_2))
    b=math.tan(alpha_a_rad)-(2*a*R_a)
    c=(0.45*R_kp*math.cos(alpha_m_rad))-(a*y_1*y_1+b*y_1)
    return a,b,c
def save_to_excel_laval(x,y):
    df = pd.DataFrame({'X': x, 'R': y})
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                             filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        df.to_excel(file_path, index=False)
def save_to_txt_laval(x_total, y_total):
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        with open(file_path, 'w') as f:
            for x, r in zip(x_total, y_total):
                f.write(f'{x}\t{r}\n')
def find_angle(x_array,y_array):
    length = len(x_array)-1
    x_j = [0] *length
    y_j = [0] * length
    beta_j = [0] * length
    for i in range(0, length):
        x_j[i] = (abs(x_array[i] - x_array[i + 1]))
        y_j[i] = (abs(y_array[i] - y_array[i + 1]))
        beta_j[i] = (math.atan(y_j[i] / x_j[i]))
    return beta_j
def srednee_znachenie(array_0):
    lenght=len(array_0)
    array_1 = [0] *(lenght-1)
    for i in range(0,lenght-1):
        array_1[i]=abs((array_0[i]+array_0[i+1])/2)
    return array_1
def srednee_znachenie_F(array_0,m):
    lenght=len(array_0)
    array_1 = [0] *(lenght-1)
    for i in range(0,lenght-1):
        array_1[i]=m*abs(array_0[i]-array_0[i+1])
    return array_1
def save_txt_poteri(text):
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        with open(file_path, 'w') as f:
            f.write(f'{text}')
def save_txt_graph_poteri(phi_r,phi_tr,phi_s,beta_kon_grad):
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        with open(file_path, 'w') as f:
            for y_1,y_2,y_3,x in zip(phi_r,phi_tr,phi_s,beta_kon_grad):
                f.write(f'{y_1}\t{y_2}\t{y_3}\t{x}\n')
def save_excel_graph_poteri(phi_r,phi_tr,phi_s,beta_kon_grad):
    df = pd.DataFrame({'phi_r': phi_r, 'phi_tr': phi_tr, 'phi_s': phi_s, 'beta': beta_kon_grad})
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                             filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        df.to_excel(file_path, index=False)
def save_txt_konus(x_array,y_array):
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        with open(file_path, 'w') as f:
            for x, y in zip(x_array, y_array):
                f.write(f'{x}\t{y}\n')
def save_excel_konus(x_array,y_array):
    df = pd.DataFrame({'X': x_array, 'R': y_array})
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                             filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран
        df.to_excel(file_path, index=False)