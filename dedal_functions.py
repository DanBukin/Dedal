from dedal_graphs import *
from PIL import Image, ImageTk
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os
import scipy
from ctypes import windll


if os.name == 'nt':
    windll.gdi32.AddFontResourceExW("data/ofont.ru_Futura PT.ttf", 0x10, 0)
else:
    pass
font0 = ("Futura PT Book", 18)
font1 = ("Futura PT Book", 16)
font2 = ("Futura PT Book", 14)
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
def est_li_soplo_rk(R_ks,R_kp,R_1,R_2,alpha_grad):
    beta_grad=90-alpha_grad
    beta_rad = beta_grad * math.pi / 180
    proverka = R_ks - R_1 + R_1 * math.sin(beta_rad) - (R_kp + R_2 - R_2 * math.sin(beta_rad))
    if proverka > 0:
        blr=f"Радиусно-коническое сопло можно спроектировать"
        aar=2
    else:
        blr='Радиусно-коническое сопло невозможно спроектировать'
        aar = 1
    return blr,aar
def est_li_soplo_rr(R_ks,R_kp,R_1,R_2):
    beta_rad=math.asin( (R_kp+R_2-R_ks+R_1)/(R_1+R_2) )
    alpha_rad=math.pi*0.5 - beta_rad
    alpha_grad=alpha_rad*180/math.pi
    return alpha_grad
def print_options_rr(R_1,R_2,R_ks,R_kp):
    beta_rad = math.asin((R_kp + R_2 - R_ks + R_1) / (R_1 + R_2))
    beta_grad=beta_rad * 180 / math.pi
    alpha_rad = math.pi * 0.5 - beta_rad
    alpha_grad = alpha_rad * 180 / math.pi
    R_1_x=R_1*math.cos(beta_rad)
    R_1_r=R_1-R_1*math.sin(beta_rad)
    R_2_x=R_2*math.cos(beta_rad)
    R_2_r=R_2-R_2*math.sin(beta_rad)
    l_suzh=R_2*math.cos(beta_rad)+R_1*math.cos(beta_rad)
    V_suzh = find_volume_rr(R_ks, R_kp, R_1, R_2, beta_grad)
    properties = f"""alpha = {round(alpha_grad,3)} 
R_кс = {round(R_ks,3)} мм
R_1 = {round(R_1,3)} мм
R_1_x = {round(R_1_x,3)} мм 
R_1_r = {round(R_1_r,3)} мм
R_кр = {round(R_kp,3)} мм
R_2 = {round(R_2,3)} мм
R_2_x = {round(R_2_x,3)} мм
R_2_r = {round(R_2_r,3)} мм
l_суж = {round(l_suzh,3)} мм
V_суж = {round(V_suzh,6)} м3
"""
    return properties,V_suzh
def print_options_rk(R_1,R_2,R_ks,R_kp,alpha_grad):
    alpha_rad = alpha_grad * math.pi/180
    beta_grad=90-alpha_grad
    beta_rad=beta_grad * math.pi/180
    l = R_2*math.cos(beta_rad)+( (R_ks-(R_kp+R_2-R_2*math.sin(beta_rad)+R_1-R_1*math.sin(beta_rad))) /math.tan(alpha_rad))
    R_1_x=R_1*math.cos(beta_rad)
    R_1_r=R_1-R_1*math.sin(beta_rad)
    R_2_x=R_2*math.cos(beta_rad)
    R_2_r=R_2-R_2*math.sin(beta_rad)
    l_suzh=l+R_1*math.cos(beta_rad)
    delta_x=l-R_2*math.cos(beta_rad)
    delta_r = R_ks-R_1+R_1*math.sin(beta_rad)-R_kp-R_2+R_2*math.sin(beta_rad)
    V_suzh=find_volume_rk(R_ks, R_kp, R_1, R_2, beta_grad)
    properties = f"""alpha = {round(alpha_grad,3)} 
R_кс = {round(R_ks,3)} мм
R_1 = {round(R_1,3)} мм
R_1_x = {round(R_1_x,3)} мм 
R_1_r = {round(R_1_r,3)} мм
R_кр = {round(R_kp,3)} мм
R_2 = {round(R_2,3)} мм
R_2_x = {round(R_2_x,3)} мм
R_2_r = {round(R_2_r,3)} мм
l_суж = {round(l_suzh,3)} мм
delta_x = {round(delta_x,3)} мм
delta_r = {round(delta_r,3)} мм
V_суж = {round(V_suzh,6)} м3
"""
    return properties,V_suzh
def place_subsonic_nozzle_rk(R_ks,R_kp,R_1,R_2,alpha_grad,frame):

    alpha_rad = alpha_grad*math.pi/180
    beta_grad = 90 - alpha_grad
    beta_rad = beta_grad*math.pi/180
    l_eb = -R_2 * math.cos(beta_rad) - ((R_ks - (R_kp + R_2 - R_2 * math.sin(beta_rad) + R_1 - R_1 * math.sin(beta_rad))) / math.tan(alpha_rad))
    x_01 = l_eb - R_1 * math.cos(beta_rad)
    line_params = {'alpha': alpha_grad, 'beta': beta_grad, 'r_kp': R_kp}
    x_total, y_total=plot_partial_circle_with_line(R_1, x_01, R_ks - R_1, beta_grad, 90, line_params, 270 - alpha_grad, 270, 0,
                                  R_kp + R_2, R_2,frame,R_kp,l_eb,beta_grad,R_ks)
    return x_total, y_total
def place_subsonic_nozzle_rr(R_ks,R_kp,R_1,R_2,frame):

    beta_rad = math.asin((R_kp+R_2-R_ks+R_1)/(R_1+R_2))
    beta_grad=beta_rad*180/math.pi
    alpha_grad = 90 - beta_grad
    alpha_rad = alpha_grad*math.pi/180
    x_01=-R_2*math.cos(beta_rad)-R_1*math.cos(beta_rad)
    y_01= R_ks-R_1
    x_02=0
    y_02=R_kp+R_2
    x_total, y_total=plot_subsonic_nozzle_rr(R_ks,R_kp,R_1,R_2,beta_grad,alpha_grad,x_01,y_01,x_02,y_02,frame)
    return x_total, y_total
def find_volume_rr(R_ks,R_kp,R_1,R_2,beta_grad):
    f_x_1 = lambda x: (((R_1 ** 2) - ((x - (-R_2 * np.cos(np.radians(beta_grad)) - R_1 * np.cos(np.radians(beta_grad)))) ** 2)) ** 0.5 + (R_ks - R_1)) ** 2
    f_x_2 = lambda x: ((-((R_2 ** 2 - x ** 2) ** 0.5) + R_kp + R_2)) ** 2
    int_okr_1, _ = scipy.integrate.quad(f_x_1,-R_2 * np.cos(np.radians(beta_grad)) - R_1 * np.cos(np.radians(beta_grad)),-R_2 * np.cos(np.radians(beta_grad)))
    int_okr_2, _ = scipy.integrate.quad(f_x_2, -R_2 * np.cos(np.radians(beta_grad)), 0)
    resylt_int_1 = math.pi * int_okr_1
    resylt_int_2 = math.pi * int_okr_2
    result_int_sum = (resylt_int_1 + resylt_int_2) / 1000000000
    return result_int_sum
def find_volume_rk(R_ks,R_kp,R_1,R_2,beta_grad):
    alpha_grad=90-beta_grad
    l = -R_2*np.cos(np.radians(beta_grad))-((R_ks-(R_kp+R_2-R_2*np.sin(np.radians(beta_grad))+R_1-R_1*np.sin(np.radians(beta_grad))))/(np.tan(np.radians(alpha_grad))))
    f_x_1 = lambda x: ((R_1**2-(x-(l-R_1*np.cos(np.radians(beta_grad))))**2)**0.5+R_ks-R_1) ** 2
    f_x_2 = lambda x: (-np.tan(np.radians(alpha_grad))*(x+R_2*np.cos(np.radians(beta_grad)))+R_kp+R_2-R_2*np.sin(np.radians(beta_grad))) ** 2
    f_x_3 = lambda x: (-((R_2**2)-(x**2))**0.5+R_kp+R_2) ** 2
    int_okr_1, _ = scipy.integrate.quad(f_x_1,l-R_1*np.cos(np.radians(beta_grad)),l)
    int_okr_2, _ = scipy.integrate.quad(f_x_2,l,-R_2*np.cos(np.radians(beta_grad)))
    int_okr_3, _ = scipy.integrate.quad(f_x_3,-R_2*np.cos(np.radians(beta_grad)),0)
    resylt_int_1 = math.pi * int_okr_1
    resylt_int_2 = math.pi * int_okr_2
    resylt_int_3 = math.pi * int_okr_3
    result_int_sum = (resylt_int_1 + resylt_int_2+resylt_int_3)/1000000000
    return result_int_sum