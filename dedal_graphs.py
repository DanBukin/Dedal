from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import AutoMinorLocator
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter
import os
from ctypes import windll
import numpy as np
import math
import customtkinter as ctk

font_path = 'data/ofont.ru_Futura PT.ttf'
font_props = font_manager.FontProperties(fname=font_path)
if os.name == 'nt':
    windll.gdi32.AddFontResourceExW("data/ofont.ru_Futura PT.ttf", 0x10, 0)
else:
    pass
font1 = ("Futura PT Book", 16)
custom_font = FontProperties(fname='data/ofont.ru_Futura PT.ttf', size=16)
formatter = FuncFormatter(lambda x, _: f"{x:.2f}")
def print_graph_R_opt(T_array,alpha_array,frame,x,alpha_opt,T_opt,alpha_zad):
    """=====Построение графика газовой постоянной от к.и.о.====="""
    fig = Figure(figsize=(9,7), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#171717') #171717
    ax.plot(alpha_array, T_array, color='white')
    ax.set_title("Зависимость газовой постоянной от к.и.о.", fontproperties=custom_font)
    ax.tick_params(axis='x', colors='white', labelsize=16)
    ax.tick_params(axis='y', colors='white', labelsize=16)
    ax.grid(True, color='white', linestyle='--', linewidth=1)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=1)
    ax.grid(which='minor', color='gray', linestyle='--', linewidth=1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    if alpha_zad!="Оптимальный":
        index_zad_alpha=alpha_array.index(alpha_zad)
        T_zad=T_array[index_zad_alpha]
        ax.plot(alpha_opt, T_opt, 'o', color='#96cdff', markersize=10)  # 'o' - это маркер круглой формы
        ax.plot(alpha_zad, T_zad, 'o', color='#0b8bff', markersize=10)  # 'o' - это маркер круглой формы

        ax.hlines(y=T_zad, xmin=min(alpha_array) * 0.98, xmax=alpha_zad, color='#0b8bff', linewidth=2, linestyle='--')
        ax.vlines(x=alpha_zad, ymin=min(T_array) * 0.98, ymax=T_zad, color='#0b8bff', linewidth=2, linestyle='--')

        ax.hlines(y=T_opt, xmin=min(alpha_array) * 0.98, xmax=alpha_opt, color='#96cdff', linewidth=2, linestyle='--')
        ax.vlines(x=alpha_opt, ymin=min(T_array) * 0.98, ymax=T_opt, color='#96cdff', linewidth=2, linestyle='--')

        label1 = ctk.CTkLabel(master=frame,
                              text=f'R_опт = {round(T_opt)} Дж/кг*К \nR_зад = {round(T_zad)} Дж/кг*К \nα_опт = {alpha_opt} \nα_зад = {alpha_zad}',
                              font=font1)
        label1.grid(row=7, column=1, sticky='w', padx=0, pady=0)


    else:
        ax.plot(alpha_opt, T_opt, 'o', color='#96cdff', markersize=10)  # 'o' - это маркер круглой формы
        ax.hlines(y=T_opt, xmin=min(alpha_array) * 0.98, xmax=alpha_opt, color='#96cdff', linewidth=2, linestyle='--')
        ax.vlines(x=alpha_opt, ymin=min(T_array) * 0.98, ymax=T_opt, color='#96cdff', linewidth=2, linestyle='--')


        label1 = ctk.CTkLabel(master=frame,
                              text=f'R_опт = {round(T_opt)} Дж/кг*К \nα_опт = {alpha_opt}',
                              font=font1)
        label1.grid(row=7, column=1, sticky='w', padx=0, pady=0)


    ax.set_xlabel('Коэффициент избытка окислителя', fontsize=16, fontproperties=font_props, color='white',)
    ax.set_ylabel("R, Дж/(кг*К)", fontsize=16, rotation='horizontal',fontproperties=font_props, color='white', labelpad=60, va='bottom')
    ax.set_xlim(min(alpha_array) * 0.98, max(alpha_array) * 1.02)
    ax.set_ylim(min(T_array) * 0.98, max(T_array) * 1.01)
    # Установите форматирование для осей X и Y
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    # Получите текущие метки и примените к ним новые настройки шрифта
    ax.set_xticklabels([f"{x:.2f}" for x in ax.get_xticks()], fontproperties=font_props)
    ax.set_yticklabels([f"{x:.0f}" for x in ax.get_yticks()], fontproperties=font_props)

    # Обновите параметры тиков после изменения меток, если нужно
    ax.tick_params(axis='x', colors='white', labelsize=15)  # Используйте свой размер шрифта
    ax.tick_params(axis='y', colors='white', labelsize=15)  # Используйте свой размер шрифта
    ax.title.set_color('white')
    fig.patch.set_facecolor('#171717')
    fig.subplots_adjust(left=0.22, bottom=0.1, right=0.97, top=0.95)
    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=7, column=0, padx=0, pady=0)

    canvas.draw()
def print_graph_T_opt(T_array,alpha_array,frame,x,alpha_opt,T_opt,alpha_zad):
    """=====Построение графика температуры от к.и.о.====="""
    fig = Figure(figsize=(9,7), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#171717') #171717
    ax.plot(alpha_array, T_array, color='white')
    ax.set_title("Зависимость Температуры в КС от к.и.о.",fontproperties=custom_font)
    ax.tick_params(axis='x', colors='white', labelsize=16)
    ax.tick_params(axis='y', colors='white', labelsize=16)
    ax.grid(True, color='white', linestyle='--', linewidth=1)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=1)
    ax.grid(which='minor', color='gray', linestyle='--', linewidth=1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    if alpha_zad!="Оптимальный":
        index_zad_alpha=alpha_array.index(alpha_zad)
        T_zad=T_array[index_zad_alpha]
        ax.plot(alpha_opt, T_opt, 'o', color='#96cdff', markersize=10)  # 'o' - это маркер круглой формы
        ax.plot(alpha_zad, T_zad, 'o', color='#0b8bff', markersize=10)  # 'o' - это маркер круглой формы

        ax.hlines(y=T_zad, xmin=min(alpha_array) * 0.98, xmax=alpha_zad, color='#0b8bff', linewidth=2, linestyle='--')
        ax.vlines(x=alpha_zad, ymin=min(T_array) * 0.98, ymax=T_zad, color='#0b8bff', linewidth=2, linestyle='--')

        ax.hlines(y=T_opt, xmin=min(alpha_array) * 0.98, xmax=alpha_opt, color='#96cdff', linewidth=2, linestyle='--')
        ax.vlines(x=alpha_opt, ymin=min(T_array) * 0.98, ymax=T_opt, color='#96cdff', linewidth=2, linestyle='--')
        label1 = ctk.CTkLabel(master=frame,
                              text=f'T_опт = {round(T_opt)} K \nT_зад = {round(T_zad)} K \nα_опт = {alpha_opt} \nα_зад = {alpha_zad}',
                              font=font1)
        label1.grid(row=6, column=1, sticky='w', padx=0, pady=0)

    else:
        ax.plot(alpha_opt, T_opt, 'o', color='#96cdff', markersize=10)  # 'o' - это маркер круглой формы
        ax.hlines(y=T_opt, xmin=min(alpha_array) * 0.98, xmax=alpha_opt, color='#96cdff', linewidth=2, linestyle='--')
        ax.vlines(x=alpha_opt, ymin=min(T_array) * 0.98, ymax=T_opt, color='#96cdff', linewidth=2, linestyle='--')

        label1 = ctk.CTkLabel(master=frame,
                              text=f'T_опт = {round(T_opt)} K \nα_опт = {alpha_opt}',
                              font=font1)
        label1.grid(row=6, column=1, sticky='w', padx=0, pady=0)


    ax.set_xlabel('Коэффициент избытка окислителя', fontsize=16, fontproperties=font_props, color='white',)
    ax.set_ylabel("Т, К", fontsize=16, rotation='horizontal',fontproperties=font_props, color='white', labelpad=20, va='bottom')
    ax.set_xlim(min(alpha_array) * 0.98, max(alpha_array) * 1.02)
    ax.set_ylim(min(T_array) * 0.98, max(T_array) * 1.01)
    # Установите форматирование для осей X и Y
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    # Получите текущие метки и примените к ним новые настройки шрифта
    ax.set_xticklabels([f"{x:.2f}" for x in ax.get_xticks()], fontproperties=font_props)
    ax.set_yticklabels([f"{x:.0f}" for x in ax.get_yticks()], fontproperties=font_props)

    # Обновите параметры тиков после изменения меток, если нужно
    ax.tick_params(axis='x', colors='white', labelsize=15)  # Используйте свой размер шрифта
    ax.tick_params(axis='y', colors='white', labelsize=15)  # Используйте свой размер шрифта
    ax.title.set_color('white')
    fig.patch.set_facecolor('#171717')
    fig.subplots_adjust(left=0.13, bottom=0.1, right=0.97, top=0.95)
    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=6, column=0, padx=0, pady=0)

    canvas.draw()
def print_graph_I_opt(I_array,alpha_array,frame,x,alpha_opt,I_max,alpha_zad):
    """=====Построение графика удельного пустотного импульса от к.и.о.====="""
    fig = Figure(figsize=(9,7), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#171717') #171717
    ax.plot(alpha_array, I_array, color='white')
    ax.set_title("Зависимость удельного пустотного импульса от к.и.о.",fontproperties=custom_font)
    ax.tick_params(axis='x', colors='white', labelsize=16)
    ax.tick_params(axis='y', colors='white', labelsize=16)
    ax.grid(True, color='white', linestyle='--', linewidth=1)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=1)
    ax.grid(which='minor', color='gray', linestyle='--', linewidth=1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    if alpha_zad!="Оптимальный":
        index_zad_alpha=alpha_array.index(alpha_zad)
        I_zad=I_array[index_zad_alpha]
        ax.plot(alpha_opt, I_max, 'o', color='#96cdff', markersize=10)  # 'o' - это маркер круглой формы
        ax.plot(alpha_zad, I_zad, 'o', color='#0b8bff', markersize=10)  # 'o' - это маркер круглой формы

        ax.hlines(y=I_zad, xmin=min(alpha_array) * 0.98, xmax=alpha_zad, color='#0b8bff', linewidth=2, linestyle='--')
        ax.vlines(x=alpha_zad, ymin=min(I_array) * 0.98, ymax=I_zad, color='#0b8bff', linewidth=2, linestyle='--')

        ax.hlines(y=I_max, xmin=min(alpha_array) * 0.98, xmax=alpha_opt, color='#96cdff', linewidth=2, linestyle='--')
        ax.vlines(x=alpha_opt, ymin=min(I_array) * 0.98, ymax=I_max, color='#96cdff', linewidth=2, linestyle='--')

        label1 = ctk.CTkLabel(master=frame, text=f'I_опт = {round(I_max)}м/с \nI_зад = {round(I_zad)}м/с \nα_опт = {alpha_opt} \nα_зад = {alpha_zad}',font=font1)
        label1.grid(row=5, column=1, sticky='w', padx=0, pady=0)

    else:
        ax.plot(alpha_opt, I_max, 'o', color='#96cdff', markersize=10)  # 'o' - это маркер круглой формы
        ax.hlines(y=I_max, xmin=min(alpha_array) * 0.98, xmax=alpha_opt, color='#96cdff', linewidth=2, linestyle='--')
        ax.vlines(x=alpha_opt, ymin=min(I_array) * 0.98, ymax=I_max, color='#96cdff', linewidth=2, linestyle='--')

        label1 = ctk.CTkLabel(master=frame,text=f'I_опт = {round(I_max)}м/с \nα_опт = {alpha_opt}',font=font1)
        label1.grid(row=5, column=1, sticky='w', padx=0, pady=0)


    ax.set_xlabel('Коэффициент избытка окислителя', fontsize=16, fontproperties=font_props, color='white',)
    ax.set_ylabel("I, м/с", fontsize=16, rotation='horizontal',fontproperties=font_props, color='white', labelpad=30, va='bottom')
    ax.set_xlim(min(alpha_array) * 0.98, max(alpha_array) * 1.02)
    ax.set_ylim(min(I_array) * 0.98, max(I_array) * 1.01)

    # Установите форматирование для осей X и Y
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    # Получите текущие метки и примените к ним новые настройки шрифта
    ax.set_xticklabels([f"{x:.2f}" for x in ax.get_xticks()], fontproperties=font_props)
    ax.set_yticklabels([f"{x:.0f}" for x in ax.get_yticks()], fontproperties=font_props)

    # Обновите параметры тиков после изменения меток, если нужно
    ax.tick_params(axis='x', colors='white', labelsize=15)  # Используйте свой размер шрифта
    ax.tick_params(axis='y', colors='white', labelsize=15)  # Используйте свой размер шрифта
    ax.title.set_color('white')
    fig.patch.set_facecolor('#171717')
    fig.subplots_adjust(left=0.15, bottom=0.1, right=0.97, top=0.95)
    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=5, column=0, padx=30, pady=0,sticky='w')

    canvas.draw()
def donut_diagramm(mass, max, master,x,y):
    """=====Построение графика в виде круговой диаграммы====="""
    futura_pt = FontProperties(fname='data/ofont.ru_Futura PT.ttf')
    colors = ['#57A3FC', '#3468AC', '#285493', '#1A3D73', '#0F2A5A']
    el = [el[0] for el in mass[:max]]  # Названия элементов для легенды
    el.append("Др.")

    # Создание массива значений для сегментов диаграммы
    val = [val[1] for val in mass[:max]]  # Значения для сегментов диаграммы
    val.append(sum([name[1] for name in mass[max:]]))  # Сумма остальных значений

    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    # Сохраняем результаты pie в переменные для дальнейшего доступа
    wedges, texts, autotexts = ax.pie(val, labels=el, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.3),
                                      pctdistance=0.85, colors=colors)

    # Настройка фона
    fig.set_facecolor('#171717')
    ax.set_facecolor('#171717')

    # Настройка стиля autotexts (текста с процентами на самой диаграмме)
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontproperties(futura_pt)  # Установка шрифта Futura PT
        autotext.set_fontsize(14)

    # Настройка стиля текстов легенды
    for text in texts:
        text.set_fontproperties(futura_pt)
        text.set_fontsize(16)
        text.set_color('white')

    # Центральный текст
    ax.text(0, 0, 'Массовое содержание\nкомпонентов', ha='center', va='center', fontproperties=futura_pt,fontsize=18, color='white')

    # Вставка холста в интерфейс
    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas_widget = canvas.get_tk_widget()
    # Используйте grid (или любой другой менеджер геометрии, который вы используете в CTkScrollableFrame)
    canvas_widget.place(x=x,y=y)
    # Настраиваем грид менеджер, чтобы холст растягивался вместе с родительским окном
    master.grid_rowconfigure(0, weight=1)
    master.grid_columnconfigure(0, weight=1)
def plot_partial_circle_with_line(radius, x0, y0, start_angle, end_angle, line_params, start_angle_2, end_angle_2, x02, y02, radius2,frame,R_kp,l,beta_grad,R_ks):
    """=====Построение радиусно-конической сужающейся части====="""
    # Проверка на правильность задания углов
    if start_angle >= end_angle:
        raise ValueError("Начальный угол должен быть меньше конечного угла.")
    # Генерация углов в указанном диапазоне
    angles = np.linspace(np.radians(start_angle), np.radians(end_angle), 20)
    angles_2 = np.linspace(np.radians(start_angle_2), np.radians(end_angle_2), 20)

    # Вычисление координат точек на окружности
    x_circle = x0 + radius * np.cos(angles)[::-1]  # обратный порядок
    y_circle = y0 + radius * np.sin(angles)[::-1]  # обратный порядок

    x_circle_2 = x02 + radius2 * np.cos(angles_2)
    y_circle_2 = y02 + radius2 * np.sin(angles_2)
    cos_beta=np.cos(np.radians(beta_grad))
    sin_beta=np.sin(np.radians(beta_grad))
    # Вычисление координат прямой
    x_line = np.linspace(l, -radius2 * cos_beta, 5)
    y_line = -np.tan(np.radians(line_params['alpha'])) * (x_line + radius2 * np.cos(np.radians(line_params['beta']))) + \
             R_kp + radius2 - radius2 * np.sin(np.radians(line_params['beta']))

    x_line_ks = [x0]*2
    y_line_ks = np.linspace(0, R_ks, 2)

    x_line_o1 = [l] * 2
    y_line_o1 = np.linspace(0, R_ks-radius+radius*sin_beta, 2)

    x_line_o2 = [-radius2*cos_beta] * 2
    y_line_o2 = np.linspace(0, R_kp + radius2 - radius2 * sin_beta, 2)

    x_line_o3 = np.linspace(x0, 0, 2)
    y_line_o3 = [0] * 2

    x_line_o4 = [0] * 2
    y_line_o4 = np.linspace(0, R_kp, 2)

    x_total = np.concatenate([x_circle, x_line, x_circle_2])
    y_total = np.concatenate([y_circle, y_line, y_circle_2])

    fig = Figure(figsize=(7, 7), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#171717')  #171717
    ax.plot(x_circle, y_circle, color='#0094FF')
    ax.plot(x_circle_2, y_circle_2, color='#0094FF')
    ax.plot(x_line, y_line, color='white')
    ax.plot(x_line_ks, y_line_ks, color='#0094FF', linewidth=2)
    ax.plot(x_line_o1, y_line_o1, color='white', linestyle='--', linewidth=2)
    ax.plot(x_line_o2, y_line_o2, color='white', linestyle='--', linewidth=2)
    ax.plot(x_line_o3, y_line_o3, color='white', linewidth=2)
    ax.plot(x_line_o4, y_line_o4, color='#0094FF', linewidth=2)
    ax.tick_params(axis='x', colors='white',labelsize=14)
    ax.tick_params(axis='y', colors='white',labelsize=14)
    ax.grid(True, color='white', linestyle='--', linewidth=1)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=1)
    ax.grid(which='minor', color='gray', linestyle='--', linewidth=1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.title.set_color('white')
    ax.set_xlabel('x, мм', fontsize=16, fontproperties=font_props, color='white', )
    ax.set_ylabel("r, мм", fontsize=16, rotation='horizontal',fontproperties=font_props, color='white', labelpad=30, va='bottom')
    fig.patch.set_facecolor('#171717') # 171717
    fig.subplots_adjust(left=0.07, bottom=0.05, right=0.98, top=0.98)
    ax.set_xlim(x0 * 1.05, 10)
    ax.set_ylim(-10, R_ks*1.05)
    # Установите форматирование для осей X и Y
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)
    # Получите текущие метки и примените к ним новые настройки шрифта
    ax.set_xticklabels([f"{x:.0f}" for x in ax.get_xticks()], fontproperties=font_props)
    ax.set_yticklabels([f"{x:.0f}" for x in ax.get_yticks()], fontproperties=font_props)
    # Обновите параметры тиков после изменения меток, если нужно
    ax.tick_params(axis='x', colors='white', labelsize=15)  # Используйте свой размер шрифта
    ax.tick_params(axis='y', colors='white', labelsize=15)  # Используйте свой размер шрифта

    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=440,y=810)

    return x_total, y_total
def plot_subsonic_nozzle_rr(R_ks,R_kp,R_1,R_2,beta_grad,alpha_grad,x_01,y_01,x_02,y_02,frame):
    """=====Построение радиусной сужающейся части====="""
    # Генерация углов в указанном диапазоне
    angles = np.linspace(np.radians(beta_grad), np.radians(90), 20)
    angles_2 = np.linspace(np.radians(270 - alpha_grad), np.radians(270), 20)
    # Вычисление координат точек на окружности
    x_circle = x_01 + R_1 * np.cos(angles)[::-1]  # обратный порядок
    y_circle = y_01 + R_1 * np.sin(angles)[::-1]  # обратный порядок

    x_circle_2 = x_02 + R_2 * np.cos(angles_2)
    y_circle_2 = y_02 + R_2 * np.sin(angles_2)

    cos_beta=np.cos(np.radians(beta_grad))
    sin_beta=np.sin(np.radians(beta_grad))

    x_line_ks = [x_01] * 2
    y_line_ks = np.linspace(0, R_ks, 2)

    x_line_o1 = [-R_2*cos_beta] * 2
    y_line_01 = np.linspace(0, R_kp + R_2 - R_2 * sin_beta, 2)

    x_line_o2 = [0] * 2
    y_line_02 = np.linspace(0, R_kp , 2)

    x_line_o3 = np.linspace(0, x_01, 2)
    y_line_03 = [0] * 2

    x_total = np.concatenate([x_circle, x_circle_2])
    y_total = np.concatenate([y_circle, y_circle_2])

    fig = Figure(figsize=(7, 7), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#171717')  #171717
    ax.plot(x_circle, y_circle, color='#0094FF')
    ax.plot(x_circle_2, y_circle_2, color='#0094FF')
    ax.plot(x_line_ks, y_line_ks, color='#0094FF', linewidth=2)
    ax.plot(x_line_o1, y_line_01, color='#0094FF', linestyle='--', linewidth=2)
    ax.plot(x_line_o2, y_line_02, color='#0094FF', linewidth=2)
    ax.plot(x_line_o3, y_line_03, color='white', linewidth=2)
    ax.tick_params(axis='x', colors='white',labelsize=14)
    ax.tick_params(axis='y', colors='white',labelsize=14)
    ax.grid(True, color='white', linestyle='--', linewidth=1)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=1)
    ax.grid(which='minor', color='gray', linestyle='--', linewidth=1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_xlabel('x, мм', fontsize=16, fontproperties=font_props, color='white', )
    ax.set_ylabel("r, мм", fontsize=16, rotation='horizontal', fontproperties=font_props, color='white', labelpad=30,va='bottom')
    ax.title.set_color('white')
    fig.patch.set_facecolor('#171717') # 171717
    fig.subplots_adjust(left=0.07, bottom=0.05, right=0.98, top=0.98)
    ax.set_xlim(x_01 * 1.05, 10)
    ax.set_ylim(-10, R_ks*1.05)
    # Установите форматирование для осей X и Y
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)
    # Получите текущие метки и примените к ним новые настройки шрифта
    ax.set_xticklabels([f"{x:.0f}" for x in ax.get_xticks()], fontproperties=font_props)
    ax.set_yticklabels([f"{x:.0f}" for x in ax.get_yticks()], fontproperties=font_props)
    # Обновите параметры тиков после изменения меток, если нужно
    ax.tick_params(axis='x', colors='white', labelsize=15)  # Используйте свой размер шрифта
    ax.tick_params(axis='y', colors='white', labelsize=15)  # Используйте свой размер шрифта
    # Добавление легенды

    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=440,y=50)
    return x_total, y_total

def print_Combustion_Chamber(x_suzh,y_suzh,frame,L_ks):
    """=====Построение камеры сгорания====="""
    fig = Figure(figsize=(9, 9), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_aspect('equal', adjustable='box')
    ax.set_facecolor('#171717')  #171717

    x_line = np.linspace(x_suzh[0]-L_ks, x_suzh[0], 2)
    y_line = [y_suzh[0]] * 2

    x_line_1 = [x_suzh[0]-L_ks] * 2
    y_line_1 = np.linspace(y_suzh[0], 0, 2)

    x_line_2 = [x_suzh[0]] * 2
    y_line_2 = np.linspace(y_suzh[0], 0, 2)

    x_line_3 = np.linspace(x_suzh[0]-L_ks, 0, 2)
    y_line_3 = [0] * 2

    x_line_4 = [0] * 2
    y_line_4 = np.linspace(0, y_suzh[-1], 2)

    x_total = np.append(x_suzh[0]-L_ks, x_suzh)
    y_total = np.append(y_suzh[0], y_suzh)

    ax.plot(x_suzh, y_suzh, color='#0094FF')
    ax.plot(x_line, y_line, color='#0094FF')
    ax.plot(x_line_1, y_line_1, color='#0094FF')
    ax.plot(x_line_2, y_line_2, color='#0094FF')
    ax.plot(x_line_3, y_line_3, color='white')
    ax.plot(x_line_4, y_line_4, color='#0094FF')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.grid(True, color='white', linestyle='--', linewidth=1)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=1)
    ax.grid(which='minor', color='gray', linestyle='--', linewidth=1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    # ax.title.set_color('white')
    fig.patch.set_facecolor('#171717') # 171717
    fig.subplots_adjust(left=0.07, bottom=0.05, right=0.98, top=0.98)
    # Установите форматирование для осей X и Y
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)
    # Получите текущие метки и примените к ним новые настройки шрифта
    ax.set_xticklabels([f"{x:.0f}" for x in ax.get_xticks()], fontproperties=font_props)
    ax.set_yticklabels([f"{x:.0f}" for x in ax.get_yticks()], fontproperties=font_props)
    # Обновите параметры тиков после изменения меток, если нужно
    ax.tick_params(axis='x', colors='white', labelsize=15)  # Используйте свой размер шрифта
    ax.tick_params(axis='y', colors='white', labelsize=15)  # Используйте свой размер шрифта
    # Определение пределов осей
    x_min = (x_suzh[0] - L_ks)*1.05
    x_max = 10
    y_min = -10
    y_max = (y_suzh[0])*1.05

    max_range = max(x_max - x_min, y_max - y_min) / 2
    mid_x = (x_max + x_min) / 2
    mid_y = (y_max + y_min) / 2

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)

    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=100,y=657)
    return x_total,y_total
def plot_nozzle_laval(R_kp,R_a,beta_m,beta_a,frame,x_dozv,y_dozv,L_ks,L_sv):
    """=====Построение профиилированного сопла Лаваля====="""
    R_3 = R_kp * 0.45
    x_01=0
    y_01=R_kp+R_3
    alpha_m=90-beta_m
    alpha_a = 90 - beta_a
    pi=math.pi
    beta_m_rad=pi * beta_m / 180
    beta_a_rad=pi * beta_a / 180
    alpha_m_rad =pi * alpha_m / 180
    alpha_a_rad =pi * alpha_a / 180
    # Генерация углов в указанном диапазоне
    angles= np.linspace(np.radians(270), np.radians(270+beta_m), 10)
    # Вычисление координат точек на окружности
    x_circle = x_01 + R_3 * np.cos(angles)
    y_circle = y_01 + R_3 * np.sin(angles)
    beta=np.radians(beta_m)
    beta_0=beta+3*math.pi/2
    x_1=R_3 * np.cos(beta_0)
    x_2=L_sv+R_3 * np.cos(beta_0)
    y_1=R_3 * np.sin(beta_0)+y_01
    y_2=R_a
    L = x_2 - x_1
    H = y_2 - y_1
    L_1 = (H - (L * np.tan(beta_a_rad))) / (np.sin(beta_m_rad) - (np.cos(beta_m_rad) * np.tan(beta_a_rad)))
    x_0 = L_1 * np.cos(beta_m_rad)+x_1
    y_0 = L_1 * np.sin(beta_m_rad)+y_1
    A = np.array([x_1, y_1])
    B = np.array([x_0, y_0])
    C = np.array([x_2, y_2])
    t_values = np.linspace(0, 1, 40)
    curve = np.array([de_casteljau(t, [A, B, C]) for t in t_values])

    y_lav=np.linspace(R_kp+R_3-R_3*math.sin(alpha_m_rad),R_a , 40)

    x_line_o1 = [x_dozv[0]] * 2
    y_line_01 = np.linspace(0, y_dozv[0], 2)

    x_line_o2 = [x_dozv[0]+L_ks] * 2
    y_line_02 = np.linspace(0, y_dozv[0], 2)

    x_line_o3 = [0] * 2
    y_line_03 = np.linspace(0, y_dozv[-1], 2)

    x_sv = np.concatenate([x_circle, curve[:, 0]])
    y_sv = np.concatenate([y_circle, curve[:, 1]])

    x_line_o5 = np.linspace(x_dozv[0], x_sv[-1], 2)
    y_line_05 = [0] * 2

    x_line_06 = [x_sv[-1]] * 2
    y_line_06 = np.linspace(0, y_sv[-1], 2)

    x_total = np.concatenate([x_dozv, x_circle,curve[:, 0]])
    y_total = np.concatenate([y_dozv, y_circle,curve[:, 1]])

    fig = Figure(figsize=(12, 12), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#171717')  #171717
    ax.set_aspect('equal', adjustable='box')
    ax.plot(x_dozv, y_dozv, color='#0094FF')
    ax.plot(x_circle, y_circle, color='#0094FF')

    ax.plot(x_line_o1, y_line_01, color='white')
    ax.plot(curve[:, 0], curve[:, 1], color='#0094FF')
    ax.plot(x_line_06, y_line_06, color='white')
    ax.plot(x_line_o2, y_line_02, color='white')
    ax.plot(x_line_o3, y_line_03, color='white')
    ax.plot(x_line_o5, y_line_05, color='white', linestyle='--')
    ax.tick_params(axis='x', colors='white',labelsize=14)
    ax.tick_params(axis='y', colors='white',labelsize=14)
    ax.grid(True, color='white', linestyle='--', linewidth=1)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=1)
    ax.grid(which='minor', color='gray', linestyle='--', linewidth=1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    # ax.title.set_color('white')
    # Определение пределов осей
    x_min = (x_dozv[0]) * 1.05
    x_max = x_sv[-1]*1.05
    y_min = -20
    y_max = (y_lav[0]) * 1.05

    max_range = max(x_max - x_min, y_max - y_min) / 2
    mid_x = (x_max + x_min) / 2
    mid_y = (y_max + y_min) / 2

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    fig.patch.set_facecolor('#171717') # 171717
    fig.subplots_adjust(left=0.07, bottom=0.05, right=0.98, top=0.98)
    # Установите форматирование для осей X и Y
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)
    # Получите текущие метки и примените к ним новые настройки шрифта
    ax.set_xticklabels([f"{x:.0f}" for x in ax.get_xticks()], fontproperties=font_props)
    ax.set_yticklabels([f"{x:.0f}" for x in ax.get_yticks()], fontproperties=font_props)
    # Обновите параметры тиков после изменения меток, если нужно
    ax.tick_params(axis='x', colors='white', labelsize=15)  # Используйте свой размер шрифта
    ax.tick_params(axis='y', colors='white', labelsize=15)  # Используйте свой размер шрифта


    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=10,y=50)
    return x_total, y_total,x_sv,y_sv
def print_graph_p_x(x,y,l,frame,x_0,y_0,label_all,label_x,label_y,a,b):
    """=====Построение графика изменения основных параметров в зависимости от длины====="""
    x_line_1 = np.linspace(x[0]-l, x[0], 2)
    y_line_1 = [y[0]] * 2

    fig = Figure(figsize=(a,b), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#171717')  # 171717
    ax.plot(x, y, color='white')
    ax.plot(x_line_1, y_line_1, color='white')
    ax.set_title(label_all, fontproperties=custom_font)
    ax.tick_params(axis='x', colors='white', labelsize=16)
    ax.tick_params(axis='y', colors='white', labelsize=16)
    ax.grid(True, color='white', linestyle='--', linewidth=1)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=1)
    ax.grid(which='minor', color='gray', linestyle='--', linewidth=1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())

    ax.set_xlabel(label_x, fontsize=16, fontproperties=font_props, color='white', )
    ax.set_ylabel(label_y, fontsize=16, rotation='horizontal', fontproperties=font_props, color='white',labelpad=40,
                  va='bottom')
    ax.set_xlim((x[0]-l) * 1.05, max(x) * 1.02)
    ax.set_ylim(min(y) * 0.97, max(y) * 1.01)

    # Установите форматирование для осей X и Y
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    # Получите текущие метки и примените к ним новые настройки шрифта
    ax.set_xticklabels([f"{x:.0f}" for x in ax.get_xticks()], fontproperties=font_props)
    ax.set_yticklabels([f"{x:.1f}" for x in ax.get_yticks()], fontproperties=font_props)

    # Обновите параметры тиков после изменения меток, если нужно
    ax.tick_params(axis='x', colors='white', labelsize=15)  # Используйте свой размер шрифта
    ax.tick_params(axis='y', colors='white', labelsize=15)  # Используйте свой размер шрифта
    ax.title.set_color('white')
    fig.patch.set_facecolor('#171717')
    fig.subplots_adjust(left=0.25, bottom=0.1, right=0.97, top=0.95)
    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=x_0,y=y_0)

    canvas.draw()
def print_graph_phi_x(y_1,y_2,y_3,x,frame,x_0,y_0,label_all,label_x,label_y):
    """=====Построение графика изменения потерь в зависимости от угла полураскрытия конической расширяющейся части====="""
    fig = Figure(figsize=(9, 7), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#171717')  # 171717
    ax.plot(x, y_1, color='#8BCFFF', label='phi_р')
    ax.plot(x, y_2, color='#0094FF', label='phi_тр')
    ax.plot(x, y_3, color='white', label='phi_s')
    ax.set_title(label_all, fontproperties=custom_font)
    ax.tick_params(axis='x', colors='white', labelsize=16)
    ax.tick_params(axis='y', colors='white', labelsize=16)
    ax.grid(True, color='white', linestyle='--', linewidth=1)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=1)
    ax.grid(which='minor', color='gray', linestyle='--', linewidth=1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.legend()
    ax.set_xlabel(label_x, fontsize=16, fontproperties=font_props, color='white', )
    ax.set_ylabel(label_y, fontsize=16, rotation='horizontal', fontproperties=font_props, color='white',labelpad=20,
                  va='bottom')
    ax.set_xlim(4, 31)

    # Установите форматирование для осей X и Y
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    # Получите текущие метки и примените к ним новые настройки шрифта
    ax.set_xticklabels([f"{x:.0f}" for x in ax.get_xticks()], fontproperties=font_props)
    ax.set_yticklabels([f"{x:.2f}" for x in ax.get_yticks()], fontproperties=font_props)

    # Обновите параметры тиков после изменения меток, если нужно
    ax.tick_params(axis='x', colors='white', labelsize=15)  # Используйте свой размер шрифта
    ax.tick_params(axis='y', colors='white', labelsize=15)  # Используйте свой размер шрифта
    ax.title.set_color('white')
    fig.patch.set_facecolor('#171717')
    fig.subplots_adjust(left=0.25, bottom=0.1, right=0.97, top=0.95)
    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=x_0,y=y_0)

    canvas.draw()
def print_graph_kon(x,y_1,l,beta,r_a,r_kp,frame,x_0,y_0,label_all,label_x,label_y,x_sv,y_sv):
    """=====Построение конического и профиллированного сопла====="""
    x_line_1 = np.linspace(x[0] - l, x[0], 2)
    y_line_1 = [y_1[0]] * 2
    y_line_1_1 = [-(y_1[0])] * 2
    tg_beta=math.tan(beta*math.pi/180)
    x_line_2 = np.linspace(0, ((r_a-r_kp)/tg_beta), 2)
    y_line_2 = np.linspace(r_kp, r_a, 2)

    x_line_3 = np.linspace(x[0] - l, ((r_a - r_kp) / tg_beta), 2)
    y_line_3 = [0] * 2

    x_line_4 = [x[0]] * 2
    y_line_4 = np.linspace(-y_1[0], y_1[0], 2)

    x_line_5 = [0] * 2
    y_line_5 = np.linspace(-y_1[-1], y_1[-1], 2)

    x_line_6 = [x[0] - l] * 2
    y_line_6 = np.linspace(0, y_1[0], 2)
    y_line_6_1 = -(np.linspace(0, y_1[0], 2))

    x_line_7 = [((r_a-r_kp)/tg_beta)] * 2
    y_line_7 = np.linspace(0, r_a, 2)

    x_line_7_1 = [x_sv[-1]] * 2
    y_line_7_1 = -(np.linspace(0, y_sv[-1], 2))

    x_total = np.concatenate([x_line_1,x,x_line_2])
    y_total = np.concatenate([y_line_1,y_1,y_line_2])

    fig = Figure(figsize=(12, 12), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#171717')  # 171717
    ax.set_aspect('equal', adjustable='box')
    ax.plot(x, y_1, color='#0094FF')
    ax.plot(x, -(y_1), color='#0094FF')
    ax.plot(x_sv, -(y_sv), color='#0094FF')
    ax.plot(x_line_1, y_line_1, color='#0094FF')
    ax.plot(x_line_1, y_line_1_1, color='#0094FF')
    ax.plot(x_line_2, y_line_2, color='#0094FF')
    ax.plot(x_line_3, y_line_3, color='white', linestyle='--')
    ax.plot(x_line_4, y_line_4, color='white', linestyle='--')
    ax.plot(x_line_5, y_line_5, color='white', linestyle='--')
    ax.plot(x_line_6, y_line_6, color='white')
    ax.plot(x_line_6, y_line_6_1, color='white')
    ax.plot(x_line_7, y_line_7, color='white')
    ax.plot(x_line_7_1, y_line_7_1, color='white')
    ax.set_title(label_all, fontproperties=custom_font)
    ax.tick_params(axis='x', colors='white', labelsize=16)
    ax.tick_params(axis='y', colors='white', labelsize=16)
    ax.grid(True, color='white', linestyle='--', linewidth=1)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=1)
    ax.grid(which='minor', color='gray', linestyle='--', linewidth=1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_xlabel(label_x, fontsize=16, fontproperties=font_props, color='white', )
    ax.set_ylabel(label_y, fontsize=16, rotation='horizontal', fontproperties=font_props, color='white',labelpad=20,
                  va='bottom')

    # Определение пределов осей
    x_min = (x[0] - l) * 1.05
    x_max = ((r_a-r_kp)/tg_beta)*1.05
    y_min = -10
    y_max = (r_a) * 1.05

    max_range = max(x_max - x_min, y_max - y_min) / 2
    mid_x = (x_max + x_min) / 2
    mid_y = (y_max + y_min) / 2

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)

    # Установите форматирование для осей X и Y
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    # Получите текущие метки и примените к ним новые настройки шрифта
    ax.set_xticklabels([f"{x:.0f}" for x in ax.get_xticks()], fontproperties=font_props)
    ax.set_yticklabels([f"{x:.2f}" for x in ax.get_yticks()], fontproperties=font_props)

    # Обновите параметры тиков после изменения меток, если нужно
    ax.tick_params(axis='x', colors='white', labelsize=15)  # Используйте свой размер шрифта
    ax.tick_params(axis='y', colors='white', labelsize=15)  # Используйте свой размер шрифта
    ax.title.set_color('white')
    fig.patch.set_facecolor('#171717')
    fig.subplots_adjust(left=0.07, bottom=0.05, right=0.98, top=0.98)
    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=x_0,y=y_0)

    canvas.draw()
    return x_total,y_total
def de_casteljau(t, points):
    """=====Функция для построения кривой методом де Кастельжо====="""
    while len(points) > 1:
        points = [(1 - t) * points[i] + t * points[i + 1] for i in range(len(points) - 1)]
    return points[0]
def print_suzh_d(x_d,y_d,x_0,y_0,frame):
    """=====Построение графика изменения потерь в зависимости от угла полураскрытия конической расширяющейся части====="""
    x_line_1 = [x_d[0]] * 2
    y_line_1 = np.linspace(0, y_d[0], 2)

    x_line_2 = [x_0[0]] * 2
    y_line_2 = np.linspace(0, y_0[0], 2)

    x_line_3 = [x_d[1]] * 2
    y_line_3 = np.linspace(0, y_d[0], 2)

    x_line_4 = [x_0[1]] * 2
    y_line_4 = np.linspace(0, y_0[0], 2)

    x_line_5 = [x_d[-1]] * 2
    y_line_5 = np.linspace(0, y_d[-1], 2)

    x_line_6 = [x_0[-1]] * 2
    y_line_6 = np.linspace(0, y_0[-1], 2)

    fig = Figure(figsize=(12, 12), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#171717')  # 171717
    ax.set_aspect('equal', adjustable='box')
    ax.plot(x_d, y_d, color='#0094FF',label='Действительное сопло')
    ax.plot(x_0, y_0, color='white',linestyle='--',label='Сопло до учёта потерь')
    ax.plot(x_line_1, y_line_1, color='#0094FF')
    ax.plot(x_line_2, y_line_2, color='white')
    ax.plot(x_line_3, y_line_3, color='#0094FF', linestyle='--')
    ax.plot(x_line_4, y_line_4, color='white', linestyle='--')
    ax.plot(x_line_5, y_line_5, color='#0094FF')
    ax.plot(x_line_6, y_line_6, color='white')
    ax.plot(np.linspace(x_d[0], x_d[-1], 2), [0] * 2, color='#0094FF', linestyle='--')
    ax.plot([0] * 2, np.linspace(0, np.min(y_d), 2), color='#0094FF', linestyle='--')
    ax.set_title("Сопло с учётом потерь", fontproperties=custom_font)
    ax.tick_params(axis='x', colors='white', labelsize=16)
    ax.tick_params(axis='y', colors='white', labelsize=16)
    ax.grid(True, color='white', linestyle='--', linewidth=1)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=1)
    ax.grid(which='minor', color='gray', linestyle='--', linewidth=1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_xlabel("L (мм)", fontsize=16, fontproperties=font_props, color='white', )
    ax.set_ylabel("R", fontsize=16, rotation='horizontal', fontproperties=font_props, color='white', labelpad=20,va='bottom')

    # Определение пределов осей
    x_min = x_d[0] * 1.05
    x_max = x_d[-1] * 1.05
    y_min = -10
    y_max = y_d[-1] * 1.05

    max_range = max(x_max - x_min, y_max - y_min) / 2
    mid_x = (x_max + x_min) / 2
    mid_y = (y_max + y_min) / 2

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)

    # Установите форматирование для осей X и Y
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    # Получите текущие метки и примените к ним новые настройки шрифта
    ax.set_xticklabels([f"{x:.0f}" for x in ax.get_xticks()], fontproperties=font_props)
    ax.set_yticklabels([f"{x:.0f}" for x in ax.get_yticks()], fontproperties=font_props)

    # Обновите параметры тиков после изменения меток, если нужно
    ax.tick_params(axis='x', colors='white', labelsize=15)  # Используйте свой размер шрифта
    ax.tick_params(axis='y', colors='white', labelsize=15)  # Используйте свой размер шрифта
    ax.title.set_color('white')
    ax.legend()
    fig.patch.set_facecolor('#171717')
    fig.subplots_adjust(left=0.07, bottom=0.05, right=0.98, top=0.98)
    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=25, y=380)

    canvas.draw()

    canvas.draw()