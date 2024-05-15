import scipy
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import AutoMinorLocator
import math
import matplotlib.pyplot as plt
import cantera as ct
import bisect
import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
import os
from scipy.interpolate import make_interp_spline
import tkinter as tk
from ctypes import windll, byref, create_string_buffer
from matplotlib.font_manager import FontProperties
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter
formatter = FuncFormatter(lambda x, _: f"{x:.2f}")

font_path = 'data/ofont.ru_Futura PT.ttf'
font_props = font_manager.FontProperties(fname=font_path)

FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20
if os.name == 'nt':
    windll.gdi32.AddFontResourceExW("data/ofont.ru_Futura PT.ttf", FR_PRIVATE, 0)
else:
    pass
font1 = ("Futura PT Book", 16)
custom_font = FontProperties(fname='data/ofont.ru_Futura PT.ttf', size=16)
def equilSoundSpeeds(gas, rtol=1.0e-6, max_iter=5000):
    gas.equilibrate('TP', rtol=rtol, max_iter=max_iter)

    s0 = gas.s
    p0 = gas.P
    r0 = gas.density
    p1 = p0*1.0001

    gas.SP = s0, p1
    gas.equilibrate('SP', rtol=rtol, max_iter=max_iter)

    aequil = math.sqrt((p1 - p0)/(gas.density - r0))
    return_condition(gas, s0, p0/10**6)
    return aequil
def findPressureInCritical(gas):

    # запоминаем параметры в КС
    s0 = gas.s
    h0 = gas.h
    p0 = gas.P
    #рассчитываем давление в критике в первом приближении
    k = gas.cp/gas.cv
    p_cr0 = p0*(2/(k+1))**(k/(k-1))
    
    mdot = 1  # задаём расход газа 1кг/с
    # задаём первое приближение для площади и давления в критике
    amin = 1.e14  # принимаем площадь F'' побольше
    p_crit = p_cr0  # принимаем давление в критике в первом приближении

    for r in range(0, 100):  
        p = p_cr0 + p_cr0 * (r + 1) / 100.0
        # рассчитываем параметры газа при заданном давлении
        gas.SP = s0, p
        gas.equilibrate('SP')
        W2 = 2.0 * (h0 - gas.h)  # h + W^2/2 = h0 - закон сохранения энергии, учебник Дорофеева стр.274 (3-изд)
        W = math.sqrt(W2)
        area = mdot / (gas.density * W)  # расчёт F'' из ур-ия неразрывности

        if (area <= amin):
            amin = area
            p_crit = p
            W_crit = W
        else:
            break
    gas.SP = s0, p_crit
    gas.equilibrate('SP')
    I_ud_kp=(W + p_crit * amin)
    return p_crit/10**6, W_crit, amin, I_ud_kp
def return_condition(gas, S, P):
    gas.SP = S, P * 10 ** 6
    gas.equilibrate('SP')
    return gas
def print_options(gas):
    print(f'Давление (p) = {gas.P / 10 ** 6:.5} МПа')
    print(f'Температура (T) = {gas.T:.2f} К')
    print(f'Удельный объём (v) = {gas.v:.2f} м3/кг')
    print(f'Энтропия (S) = {gas.s:.2f} Дж/кг*К')
    print(f'Полная энтальпия (I) = {gas.enthalpy_mass * 0.001:.2f} кДж/кг')
    print(f'Полная внутренняя энергия (U) = {gas.int_energy_mass * 0.001:.2f} кДж/кг')
    print(f"Молярная масса газовой фазы (MMg): {gas.mean_molecular_weight:.2f} г/моль")
    print(f'Газовая постоянная: {gas.cp - gas.cv:.2f}')
def print_choice(gas, S, P, choiсe):
    if choiсe == 0:
        return_condition(gas, S, P)
        T_1 = gas.T
        P_1 = gas.P
        V_1 = gas.v
        S_1 = S

        # расчёт равновесной Cv
        gas.TD = T_1 * 1.00001, 1 / V_1
        gas.equilibrate('TV')
        U2 = gas.int_energy_mass
        gas.TD = T_1, 1 / V_1
        gas.equilibrate('TV')
        U1 = gas.int_energy_mass
        CVEQ = (U2 - U1) / (0.00001 * T_1)

        # Возвращаем всё, как было
        return_condition(gas, S_1, P_1 / 10 ** 6)

        # расчёт равновесной Cp
        gas.TP = T_1 * 1.01, P_1
        gas.equilibrate('TP')
        H2 = gas.enthalpy_mass
        gas.TP = T_1 * 0.99, P_1
        gas.equilibrate('TP')
        H1 = gas.enthalpy_mass
        CPEQ = (H2 - H1) / (0.02 * T_1)

        # Возвращаем всё, как было
        return_condition(gas, S_1, P_1 / 10 ** 6)

        print("------Равновеснные параметры------")
        print(f'Удельная теплоёмкость при постоянном давлении (Cp\'\') = {CPEQ:.2f} Дж/кг*К')
        print(f'Удельная теплоёмкость при постоянном объёме (Cv\'\') =  {CVEQ:.2f} Дж/кг*К')
        print(f'Показатель адиабаты (k\'\'): {CPEQ / CVEQ:.3f}')
    else:
        print("------Замороженные параметры------")
        print(f'Удельная теплоёмкость при постоянном давлении (Cp) = {gas.cp:.2f} Дж/кг*К')
        print(f'Удельная теплоёмкость при постоянном объёме (Cv) = {gas.cv:.2f} Дж/кг*К')
        print(f'Показатель адиабаты (k): {gas.cp / gas.cv:.3f} ')
def find_W_F_I(gas,p,H_k):
    H_2 = gas.h
    W2 = 2.0 * (math.fabs(H_k - H_2))
    W = math.sqrt(W2)
    F = 1 / (gas.density * W)
    I_ud = (W + p * (10 ** 6) * F)
    return W, F,I_ud
def print_graph_R_opt(T_array,alpha_array,frame,x,alpha_opt,T_opt,alpha_zad):

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
        label1.grid(row=6, column=1, sticky='w', padx=0, pady=0)


    else:
        ax.plot(alpha_opt, T_opt, 'o', color='#96cdff', markersize=10)  # 'o' - это маркер круглой формы
        ax.hlines(y=T_opt, xmin=min(alpha_array) * 0.98, xmax=alpha_opt, color='#96cdff', linewidth=2, linestyle='--')
        ax.vlines(x=alpha_opt, ymin=min(T_array) * 0.98, ymax=T_opt, color='#96cdff', linewidth=2, linestyle='--')


        label1 = ctk.CTkLabel(master=frame,
                              text=f'R_опт = {round(T_opt)} Дж/кг*К \nα_опт = {alpha_opt}',
                              font=font1)
        label1.grid(row=6, column=1, sticky='w', padx=0, pady=0)


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
    canvas_widget.grid(row=6, column=0, padx=0, pady=0)

    canvas.draw()
def print_graph_T_opt(T_array,alpha_array,frame,x,alpha_opt,T_opt,alpha_zad):
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
        label1.grid(row=5, column=1, sticky='w', padx=0, pady=0)

    else:
        ax.plot(alpha_opt, T_opt, 'o', color='#96cdff', markersize=10)  # 'o' - это маркер круглой формы
        ax.hlines(y=T_opt, xmin=min(alpha_array) * 0.98, xmax=alpha_opt, color='#96cdff', linewidth=2, linestyle='--')
        ax.vlines(x=alpha_opt, ymin=min(T_array) * 0.98, ymax=T_opt, color='#96cdff', linewidth=2, linestyle='--')

        label1 = ctk.CTkLabel(master=frame,
                              text=f'T_опт = {round(T_opt)} K \nα_опт = {alpha_opt}',
                              font=font1)
        label1.grid(row=5, column=1, sticky='w', padx=0, pady=0)


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
    canvas_widget.grid(row=5, column=0, padx=0, pady=0)

    canvas.draw()
def print_graph_I_opt(I_array,alpha_array,frame,x,alpha_opt,I_max,alpha_zad):
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
        label1.grid(row=4, column=1, sticky='w', padx=0, pady=0)

    else:
        ax.plot(alpha_opt, I_max, 'o', color='#96cdff', markersize=10)  # 'o' - это маркер круглой формы
        ax.hlines(y=I_max, xmin=min(alpha_array) * 0.98, xmax=alpha_opt, color='#96cdff', linewidth=2, linestyle='--')
        ax.vlines(x=alpha_opt, ymin=min(I_array) * 0.98, ymax=I_max, color='#96cdff', linewidth=2, linestyle='--')

        label1 = ctk.CTkLabel(master=frame,text=f'I_опт = {round(I_max)}м/с \nα_опт = {alpha_opt}',font=font1)
        label1.grid(row=4, column=1, sticky='w', padx=0, pady=0)


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
    canvas_widget.grid(row=4, column=0, padx=30, pady=0,sticky='w')

    canvas.draw()
def optimalnaya_alpha(choice,p_k,p_a,alpha,fuel,oxidizer,H_gor,H_ok,alpha_value,frame,x):

    k0=alpha_value
    # Задаём газ (GRI30)
    gas = ct.Solution('gri30.yaml')
    alpha_array = [i / 100 for i in range(50,150)]
    if alpha!="Оптимальный":
        choise_2 = 1
        alpha_zad=float(alpha)
        kostyl="Не оптимальный"
        bisect.insort(alpha_array, float(alpha))
    else:
        choise_2 = 0
        alpha_zad="Оптимальный"
        kostyl = "Оптимальный"
    results_I = []
    results_T = []
    results_R = []
    for alpha in alpha_array:
        km = k0 * alpha
        # Расчёт энтальпии смеси
        m_gor = (1 / (1 + km))
        m_ok = 1 * km / (1 + km)
        H_sum = ((m_gor * H_gor) + (m_ok * H_ok)) * 1000

        # Задаём смешивание компонентов
        gas.set_equivalence_ratio(1 / (alpha), fuel, oxidizer)

        # Уравновешиваем состав при 300 К (иначе выдаёт ошибку в итерациях):
        gas.TP = 300, p_k * 10 ** 6
        gas.equilibrate('TP')

        # Уравновешиваем состав при заданной энатльпии смеси и заданном давлении:
        gas.HP = H_sum, p_k * 10 ** 6
        gas.equilibrate('HP')

        # Запоминаем параметры в камере для удобства использования в последующих расчётах
        T_k = gas.T
        results_T.append(T_k)
        R_k = gas.cp - gas.cv
        results_R.append(R_k)
        S_k = gas.s
        H_k = gas.h

        if choice == 1:
            gas.SP = None, p_a * (10 ** 6)
            W_a, F_a, I_a = find_W_F_I(gas, p_a, H_k)
            results_I.append(I_a)

        else:
            return_condition(gas, S_k, p_a)
            W_a, F_a, I_a = find_W_F_I(gas, p_a, H_k)
            results_I.append(I_a)
        x=0
    I_max = max(results_I)
    index_I_max = results_I.index(I_max)
    alpha_opt = alpha_array[index_I_max]
    T_opt = results_T[index_I_max]
    R_opt = results_R[index_I_max]
    print_graph_I_opt(results_I, alpha_array,frame,x-1,alpha_opt,I_max,alpha_zad)
    print_graph_T_opt(results_T, alpha_array, frame, x, alpha_opt, T_opt, alpha_zad)
    print_graph_R_opt(results_R, alpha_array, frame, x + 1, alpha_opt, R_opt, alpha_zad)

    if kostyl!="Оптимальный":
        kostyl=float(alpha_zad)
    else:
        kostyl=alpha_opt

    return alpha_array,results_I,results_T,results_R,kostyl
def options_ks(choice,p_k,alpha,fuel,oxidizer,H_gor,H_ok,km0):

    k0=km0
    gas = ct.Solution('gri30.yaml')
    km = k0 * alpha
    # Расчёт энтальпии смеси
    m_gor = (1 / (1 + km))
    m_ok = 1 * km / (1 + km)
    H_sum = ((m_gor * H_gor) + (m_ok * H_ok)) * 1000

    # Задаём смешивание компонентов
    gas.set_equivalence_ratio(1 / (alpha), fuel, oxidizer)

    # Уравновешиваем состав при 300 К (иначе выдаёт ошибку в итерациях):
    gas.TP = 300, p_k * 10 ** 6
    gas.equilibrate('TP')

    # Уравновешиваем состав при заданной энатльпии смеси и заданном давлении:
    gas.HP = H_sum, p_k * 10 ** 6
    gas.equilibrate('HP')

    # Запоминаем параметры в камере для удобства использования в последующих расчётах
    T_k = gas.T
    R_k = gas.cp - gas.cv
    S_k = gas.s
    H_k = gas.h

    properties = f"""Давление (p) = {gas.P / 10 ** 6:.5} МПа
Температура (T) = {gas.T:.2f} К
Удельный объём (v) = {gas.v:.2f} м3/кг
Энтропия (S) = {gas.s:.2f} Дж/кг*К
Полная энтальпия (I) = {gas.enthalpy_mass * 0.001:.2f} кДж/кг
Полная внутренняя энергия (U) = {gas.int_energy_mass * 0.001:.2f} кДж/кг
Молярная масса газовой фазы (MMg): {gas.mean_molecular_weight:.2f} г/моль
Газовая постоянная: {gas.cp - gas.cv:.2f} Дж/кг*К
"""
    if choice == 0:
        return_condition(gas, S_k, p_k)
        T_1 = gas.T
        P_1 = gas.P
        V_1 = gas.v
        S_1 = S_k

        # расчёт равновесной Cv
        gas.TD = T_1 * 1.00001, 1 / V_1
        gas.equilibrate('TV')
        U2 = gas.int_energy_mass
        gas.TD = T_1, 1 / V_1
        gas.equilibrate('TV')
        U1 = gas.int_energy_mass
        CVEQ = (U2 - U1) / (0.00001 * T_1)

        # Возвращаем всё, как было
        return_condition(gas, S_1, P_1 / 10 ** 6)

        # расчёт равновесной Cp
        gas.TP = T_1 * 1.01, P_1
        gas.equilibrate('TP')
        H2 = gas.enthalpy_mass
        gas.TP = T_1 * 0.99, P_1
        gas.equilibrate('TP')
        H1 = gas.enthalpy_mass
        CPEQ = (H2 - H1) / (0.02 * T_1)

        # Возвращаем всё, как было
        return_condition(gas, S_1, P_1 / 10 ** 6)
        properties +=f"""------------Равновеснные параметры------------
Удельная теплоёмкость при постоянном давлении (Cp\'\') = {CPEQ:.2f} Дж/кг*К
Удельная теплоёмкость при постоянном объёме (Cv\'\') =  {CVEQ:.2f} Дж/кг*К
Показатель адиабаты (k\'\'): {CPEQ / CVEQ:.3f}
"""
    else:
        properties +=f"""------------Замороженные параметры------------
Удельная теплоёмкость при постоянном давлении (Cp) = {gas.cp:.2f} Дж/кг*К
Удельная теплоёмкость при постоянном объёме (Cv) = {gas.cv:.2f} Дж/кг*К
Показатель адиабаты (k): {gas.cp / gas.cv:.3f}
"""
    # Получение и вывод массовых и мольных долей компонентов смеси
    mass_fractions = gas.Y
    mole_fractions = gas.X
    species_names = gas.species_names

    return properties,species_names,mass_fractions,mole_fractions,R_k,T_k
def options_kp(choice,p_k,alpha,fuel,oxidizer,H_gor,H_ok,km0):

    k0=km0
    gas = ct.Solution('gri30.yaml')
    km = k0 * alpha
    # Расчёт энтальпии смеси
    m_gor = (1 / (1 + km))
    m_ok = 1 * km / (1 + km)
    H_sum = ((m_gor * H_gor) + (m_ok * H_ok)) * 1000

    # Задаём смешивание компонентов
    gas.set_equivalence_ratio(1 / (alpha), fuel, oxidizer)

    # Уравновешиваем состав при 300 К (иначе выдаёт ошибку в итерациях):
    gas.TP = 300, p_k * 10 ** 6
    gas.equilibrate('TP')

    # Уравновешиваем состав при заданной энатльпии смеси и заданном давлении:
    gas.HP = H_sum, p_k * 10 ** 6
    gas.equilibrate('HP')

    # Запоминаем параметры в камере для удобства использования в последующих расчётах
    T_k = gas.T
    R_k = gas.cp - gas.cv
    S_k = gas.s
    H_k = gas.h

    if choice == 1:
        # Расчёт давления в критическом сечении для замороженного течения:
        k = gas.cp / gas.cv
        p_kp = p_k * (2 / (k + 1)) ** (k / (k - 1))

        # Выводим на экран параметры в критическом сечении:
        gas.SP = None, p_kp * (10 ** 6)
        W_kp, F_kp, I_ud_kp = find_W_F_I(gas, p_kp, H_k)
        beta_kp = p_k * (10 ** 6) * F_kp
        # print_choice(gas, S_k, p_kp, choice)
        T_kp=gas.T
        R_kp=gas.cp - gas.cv
        k_kp=gas.cp / gas.cv
        properties = f"""Давление (p) = {p_kp:.5} МПа
Температура (T) = {gas.T:.2f} К
Удельный объём (v) = {gas.v:.2f} м3/кг
Энтропия (S) = {gas.s:.2f} Дж/кг*К
Полная энтальпия (I) = {gas.enthalpy_mass * 0.001:.2f} кДж/кг
Полная внутренняя энергия (U) = {gas.int_energy_mass * 0.001:.2f} кДж/кг
Молярная масса газовой фазы (MMg): {gas.mean_molecular_weight:.2f} г/моль
Газовая постоянная: {gas.cp - gas.cv:.2f} Дж/кг*К
        
Удельный пустотный импульс в критике (I_уд_кр) = {I_ud_kp:.2f} м/с
Скорость газа: (W) = {W_kp:.2f} м/с
Удельная площадь потока (F_кр\'\') = {F_kp:.8f} м2*с/кг
Расходный комплекс (B) = {beta_kp:.2f} м/с
        
------------Замороженные параметры------------
Удельная теплоёмкость при постоянном давлении (Cp) = {gas.cp:.2f} Дж/кг*К
Удельная теплоёмкость при постоянном объёме (Cv) = {gas.cv:.2f} Дж/кг*К
Показатель адиабаты (k): {gas.cp / gas.cv:.3f}
"""
        mass_fractions = gas.Y
        mole_fractions = gas.X
        species_names = gas.species_names
    else:
        p_kp, W_kp, F_kp, I_ud_kp = findPressureInCritical(gas)
        beta_kp = p_k * (10 ** 6) * F_kp

        return_condition(gas, S_k, p_kp)
        T_1 = gas.T
        P_1 = gas.P
        V_1 = gas.v
        S_1 = S_k

        # расчёт равновесной Cv
        gas.TD = T_1 * 1.00001, 1 / V_1
        gas.equilibrate('TV')
        U2 = gas.int_energy_mass
        gas.TD = T_1, 1 / V_1
        gas.equilibrate('TV')
        U1 = gas.int_energy_mass
        CVEQ = (U2 - U1) / (0.00001 * T_1)

        # Возвращаем всё, как было
        return_condition(gas, S_1, P_1 / 10 ** 6)

        # расчёт равновесной Cp
        gas.TP = T_1 * 1.01, P_1
        gas.equilibrate('TP')
        H2 = gas.enthalpy_mass
        gas.TP = T_1 * 0.99, P_1
        gas.equilibrate('TP')
        H1 = gas.enthalpy_mass
        CPEQ = (H2 - H1) / (0.02 * T_1)

        # Возвращаем всё, как было
        return_condition(gas, S_1, P_1 / 10 ** 6)
        T_kp = gas.T
        R_kp = gas.cp - gas.cv
        k_kp = CPEQ / CVEQ
        properties = f"""Давление (p) = {p_kp:.5} МПа
Температура (T) = {gas.T:.2f} К
Удельный объём (v) = {gas.v:.2f} м3/кг
Энтропия (S) = {gas.s:.2f} Дж/кг*К
Полная энтальпия (I) = {gas.enthalpy_mass * 0.001:.2f} кДж/кг
Полная внутренняя энергия (U) = {gas.int_energy_mass * 0.001:.2f} кДж/кг
Молярная масса газовой фазы (MMg): {gas.mean_molecular_weight:.2f} г/моль
Газовая постоянная: {gas.cp - gas.cv:.2f} Дж/кг*К

Скорость газа: (W) = {W_kp:.2f} м/с
Удельный пустотный импульс в критике (I_уд_кр) = {I_ud_kp:.2f} м/с
Удельная площадь потока (F_кр\'\') = {F_kp:.8f} м2*с/кг
Расходный комплекс (B) = {beta_kp:.2f} м/с

------------Равновеснные параметры------------
Удельная теплоёмкость при постоянном давлении (Cp\'\') = {CPEQ:.2f} Дж/кг*К
Удельная теплоёмкость при постоянном объёме (Cv\'\') =  {CVEQ:.2f} Дж/кг*К
Показатель адиабаты (k\'\'): {CPEQ / CVEQ:.3f}
"""
        mass_fractions = gas.Y
        mole_fractions = gas.X
        species_names = gas.species_names
    return properties,species_names,mass_fractions,mole_fractions,F_kp,beta_kp,T_kp,R_kp,k_kp,p_kp
def options_a(choice,p_k,p_a,alpha,fuel,oxidizer,H_gor,H_ok,km0):
    k0 = km0
    gas = ct.Solution('gri30.yaml')
    km = k0 * alpha
    # Расчёт энтальпии смеси
    m_gor = (1 / (1 + km))
    m_ok = 1 * km / (1 + km)
    H_sum = ((m_gor * H_gor) + (m_ok * H_ok)) * 1000

    # Задаём смешивание компонентов
    gas.set_equivalence_ratio(1 / (alpha), fuel, oxidizer)

    # Уравновешиваем состав при 300 К (иначе выдаёт ошибку в итерациях):
    gas.TP = 300, p_k * 10 ** 6
    gas.equilibrate('TP')

    # Уравновешиваем состав при заданной энатльпии смеси и заданном давлении:
    gas.HP = H_sum, p_k * 10 ** 6
    gas.equilibrate('HP')

    # Запоминаем параметры в камере для удобства использования в последующих расчётах
    T_k = gas.T
    R_k = gas.cp - gas.cv
    S_k = gas.s
    H_k = gas.h

    if choice == 1:
        gas.SP = None, p_a * (10 ** 6)
        W_a,F_a,I_a=find_W_F_I(gas, p_a, H_k)
        w_a=W_a
        rho_a=1/gas.v

        properties = f"""Давление (p) = {p_a:.5} МПа
Температура (T) = {gas.T:.2f} К
Удельный объём (v) = {gas.v:.2f} м3/кг
Энтропия (S) = {gas.s:.2f} Дж/кг*К
Полная энтальпия (I) = {gas.enthalpy_mass * 0.001:.2f} кДж/кг
Полная внутренняя энергия (U) = {gas.int_energy_mass * 0.001:.2f} кДж/кг
Молярная масса газовой фазы (MMg): {gas.mean_molecular_weight:.2f} г/моль
Газовая постоянная: {gas.cp - gas.cv:.2f} Дж/кг*К

Скорость газа: (W) = {W_a:.2f} м/с
Удельный пустотный импульс в критике (I_уд_a) = {I_a:.2f} м/с
Удельная площадь потока (F_a\'\') = {F_a:.8f} м2*с/кг

------------Замороженные параметры------------
Удельная теплоёмкость при постоянном давлении (Cp) = {gas.cp:.2f} Дж/кг*К
Удельная теплоёмкость при постоянном объёме (Cv) = {gas.cv:.2f} Дж/кг*К
Показатель адиабаты (k): {gas.cp / gas.cv:.3f}
"""
        k_a=gas.cp / gas.cv
        mass_fractions = gas.Y
        mole_fractions = gas.X
        species_names = gas.species_names
    else:
        return_condition(gas, S_k, p_a)
        W_a,F_a,I_a=find_W_F_I(gas, p_a, H_k)

        return_condition(gas, S_k, p_a)
        T_1 = gas.T
        P_1 = gas.P
        V_1 = gas.v
        S_1 = S_k

        # расчёт равновесной Cv
        gas.TD = T_1 * 1.00001, 1 / V_1
        gas.equilibrate('TV')
        U2 = gas.int_energy_mass
        gas.TD = T_1, 1 / V_1
        gas.equilibrate('TV')
        U1 = gas.int_energy_mass
        CVEQ = (U2 - U1) / (0.00001 * T_1)

        # Возвращаем всё, как было
        return_condition(gas, S_1, P_1 / 10 ** 6)

        # расчёт равновесной Cp
        gas.TP = T_1 * 1.01, P_1
        gas.equilibrate('TP')
        H2 = gas.enthalpy_mass
        gas.TP = T_1 * 0.99, P_1
        gas.equilibrate('TP')
        H1 = gas.enthalpy_mass
        CPEQ = (H2 - H1) / (0.02 * T_1)

        # Возвращаем всё, как было
        return_condition(gas, S_1, P_1 / 10 ** 6)

        w_a = W_a
        rho_a = 1 / gas.v
        properties = f"""Давление (p) = {p_a:.5} МПа
Температура (T) = {gas.T:.2f} К
Удельный объём (v) = {gas.v:.2f} м3/кг
Энтропия (S) = {gas.s:.2f} Дж/кг*К
Полная энтальпия (I) = {gas.enthalpy_mass * 0.001:.2f} кДж/кг
Полная внутренняя энергия (U) = {gas.int_energy_mass * 0.001:.2f} кДж/кг
Молярная масса газовой фазы (MMg): {gas.mean_molecular_weight:.2f} г/моль
Газовая постоянная: {gas.cp - gas.cv:.2f} Дж/кг*К

Скорость газа: (W) = {W_a:.2f} м/с
Удельный пустотный импульс на срезе (I_уд_a) = {I_a:.2f} м/с
Удельная площадь потока (F_a\'\') = {F_a:.8f} м2*с/кг

------------Равновеснные параметры------------
Удельная теплоёмкость при постоянном давлении (Cp\'\') = {CPEQ:.2f} Дж/кг*К
Удельная теплоёмкость при постоянном объёме (Cv\'\') =  {CVEQ:.2f} Дж/кг*К
Показатель адиабаты (k\'\'): {CPEQ / CVEQ:.3f}
"""
        k_a=CPEQ / CVEQ
        mass_fractions = gas.Y
        mole_fractions = gas.X
        species_names = gas.species_names
    return properties,species_names,mass_fractions,mole_fractions,I_a,F_a,w_a,rho_a,k_a
def donut_diagramm(mass, max, master,x,y):
    futura_pt = FontProperties(fname='data/ofont.ru_Futura PT.ttf')
    colors = ['#57A3FC', '#3468AC', '#285493', '#1A3D73', '#0F2A5A']
    el = [el[0] for el in mass[:max]]  # Названия элементов для легенды
    el.append("Остальные")

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
def est_li_soplo_rk(R_ks,R_kp,R_1,R_2,alpha_grad):
    alpha_rad=alpha_grad*math.pi/180
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
def plot_partial_circle_with_line(radius, x0, y0, start_angle, end_angle, line_params, start_angle_2, end_angle_2, x02, y02, radius2,frame,R_kp,l,beta_grad,R_ks):
    # Проверка на правильность задания углов
    if start_angle >= end_angle:
        raise ValueError("Начальный угол должен быть меньше конечного угла.")
    # Генерация углов в указанном диапазоне
    angles = np.linspace(np.radians(start_angle), np.radians(end_angle), 100)
    angles_2 = np.linspace(np.radians(start_angle_2), np.radians(end_angle_2), 100)

    # Вычисление координат точек на окружности
    x_circle = x0 + radius * np.cos(angles)[::-1]  # обратный порядок
    y_circle = y0 + radius * np.sin(angles)[::-1]  # обратный порядок

    x_circle_2 = x02 + radius2 * np.cos(angles_2)
    y_circle_2 = y02 + radius2 * np.sin(angles_2)

    # Вычисление координат прямой
    x_line = np.linspace(l, -radius2 * np.cos(np.radians(beta_grad)), 10)
    y_line = -np.tan(np.radians(line_params['alpha'])) * (x_line + radius2 * np.cos(np.radians(line_params['beta']))) + \
             R_kp + radius2 - radius2 * np.sin(np.radians(line_params['beta']))

    x_line_ks = [x0]*2
    y_line_ks = np.linspace(0, R_ks, 2)

    x_line_o1 = [l] * 2
    y_line_o1 = np.linspace(0, R_ks-radius+radius*np.sin(np.radians(beta_grad)), 2)

    x_line_o2 = [-radius2*np.cos(np.radians(beta_grad))] * 2
    y_line_o2 = np.linspace(0, R_kp + radius2 - radius2 * np.sin(np.radians(beta_grad)), 2)

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

    # Генерация углов в указанном диапазоне
    angles = np.linspace(np.radians(beta_grad), np.radians(90), 100)
    angles_2 = np.linspace(np.radians(270 - alpha_grad), np.radians(270), 100)

    # Вычисление координат точек на окружности
    x_circle = x_01 + R_1 * np.cos(angles)[::-1]  # обратный порядок
    y_circle = y_01 + R_1 * np.sin(angles)[::-1]  # обратный порядок

    x_circle_2 = x_02 + R_2 * np.cos(angles_2)
    y_circle_2 = y_02 + R_2 * np.sin(angles_2)

    x_line_ks = [x_01] * 2
    y_line_ks = np.linspace(0, R_ks, 2)

    x_line_o1 = [-R_2*np.cos(np.radians(beta_grad))] * 2
    y_line_01 = np.linspace(0, R_kp + R_2 - R_2 * np.sin(np.radians(beta_grad)), 2)

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
def print_Combustion_Chamber(x_suzh,y_suzh,frame,L_ks):


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
    canvas_widget.place(x=100,y=650)
    return x_total,y_total
def plot_nozzle_laval(R_kp,R_a,beta_m,beta_a,frame,a,b,c,x_dozv,y_dozv,L_ks):
    R_3 = R_kp * 0.45
    x_01=0
    y_01=R_kp+R_3
    alpha_m=90-beta_m
    alpha_a = 90 - beta_a
    beta_m_rad=math.pi * beta_m / 180
    beta_a_rad=math.pi * beta_a / 180
    alpha_m_rad =math.pi * alpha_m / 180
    alpha_a_rad =math.pi * alpha_a / 180
    # Генерация углов в указанном диапазоне
    angles= np.linspace(np.radians(270), np.radians(270+beta_m), 20)
    # Вычисление координат точек на окружности
    x_circle = x_01 + R_3 * np.cos(angles)
    y_circle = y_01 + R_3 * np.sin(angles)

    y_lav=np.linspace(R_kp+R_3-R_3*math.sin(alpha_m_rad),R_a , 100)
    x_lav=(a*(y_lav**2))+(b*y_lav)+(c)

    x_line_o1 = [x_dozv[0]] * 2
    y_line_01 = np.linspace(0, y_dozv[0], 2)

    x_line_o2 = [x_dozv[0]+L_ks] * 2
    y_line_02 = np.linspace(0, y_dozv[0], 2)

    x_line_o3 = [0] * 2
    y_line_03 = np.linspace(0, y_dozv[-1], 2)

    x_line_o4 = [x_lav[-1]] * 2
    y_line_04 = np.linspace(0, y_lav[-1], 2)

    x_line_o5 = np.linspace(x_dozv[0], x_lav[-1], 2)
    y_line_05 = [0] * 2

    x_sv = np.concatenate([x_circle, x_lav])
    y_sv = np.concatenate([y_circle, y_lav])

    x_total = np.concatenate([x_dozv, x_circle,x_lav])
    y_total = np.concatenate([y_dozv, y_circle,y_lav])

    fig = Figure(figsize=(12, 12), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#171717')  #171717
    ax.set_aspect('equal', adjustable='box')
    ax.plot(x_dozv, y_dozv, color='#0094FF')
    ax.plot(x_circle, y_circle, color='#0094FF')
    ax.plot(x_lav, y_lav, color='#0094FF')
    ax.plot(x_line_o1, y_line_01, color='white')
    ax.plot(x_line_o2, y_line_02, color='white')
    ax.plot(x_line_o3, y_line_03, color='white')
    ax.plot(x_line_o4, y_line_04, color='white')
    ax.plot(x_line_o5, y_line_05, color='white', linestyle='--')
    # ax.legend(fontsize=14)
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
    x_max = x_lav[-1]*1.05
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
def raschet_dozv(k0,alpha,H_gor,H_ok,fuel,oxidizer,p_k,selected_option,p_array):
    if selected_option=="Равновесный":
        choice=0
    else:
        choice=1
    # Задаём газ (GRI30)
    gas = ct.Solution('gri30.yaml')

    # Расчёт стехометрии:

    km = k0 * alpha

    # Расчёт энтальпии смеси
    m_gor = (1 / (1 + km))
    m_ok = 1 * km / (1 + km)
    H_sum = ((m_gor * H_gor) + (m_ok * H_ok)) * 1000

    # Задаём смешивание компонентов
    gas.set_equivalence_ratio(1 / (alpha), fuel, oxidizer)

    # Уравновешиваем состав при 300 К (иначе выдаёт ошибку в итерациях):
    gas.TP = 300, p_k * 10 ** 6
    gas.equilibrate('TP')

    # Уравновешиваем состав при заданной энатльпии смеси и заданном давлении:
    gas.HP = H_sum, p_k * 10 ** 6
    gas.equilibrate('HP')

    # Запоминаем параметры в камере для удобства использования в последующих расчётах
    T_k = gas.T
    R_k = gas.cp - gas.cv
    V_k = gas.v
    S_k = gas.s
    H_k = gas.h
    T_array=[]
    rho_array=[]
    R_array=[]
    k_array=[]
    w_array=[]
    F_dozv_array=[]
    for p in p_array:
        if choice == 1:
            gas.SP = None, p * (10 ** 6)
            T_array.append(gas.T)
            rho_array.append(1/gas.v)
            R_array.append(gas.cp - gas.cv)
            k_array.append(gas.cp / gas.cv)

            H_2 = gas.h
            W2 = 2.0 * (math.fabs(H_k - H_2))
            W = math.sqrt(W2)
            F = 1 / (gas.density * W)

            w_array.append(W)
            F_dozv_array.append(F)

        else:
            return_condition(gas, S_k, p)

            T_array.append(gas.T)
            rho_array.append(1/gas.v)
            R_array.append(gas.cp - gas.cv)

            T_1 = gas.T
            P_1 = gas.P
            V_1 = gas.v
            S_1 = S_k

            # расчёт равновесной Cv
            gas.TD = T_1 * 1.00001, 1 / V_1
            gas.equilibrate('TV')
            U2 = gas.int_energy_mass
            gas.TD = T_1, 1 / V_1
            gas.equilibrate('TV')
            U1 = gas.int_energy_mass
            CVEQ = (U2 - U1) / (0.00001 * T_1)

            # Возвращаем всё, как было
            return_condition(gas, S_1, P_1 / 10 ** 6)

            # расчёт равновесной Cp
            gas.TP = T_1 * 1.01, P_1
            gas.equilibrate('TP')
            H2 = gas.enthalpy_mass
            gas.TP = T_1 * 0.99, P_1
            gas.equilibrate('TP')
            H1 = gas.enthalpy_mass
            CPEQ = (H2 - H1) / (0.02 * T_1)
            k_array.append(CPEQ / CVEQ)
            # Возвращаем всё, как было
            return_condition(gas, S_1, P_1 / 10 ** 6)

            H_2 = gas.h
            W2 = 2.0 * (math.fabs(H_k - H_2))
            W = math.sqrt(W2)
            F = 1 / (gas.density * W)

            w_array.append(W)
            F_dozv_array.append(F)
    return T_array,rho_array,R_array,k_array,w_array,F_dozv_array
def print_graph_p_x(x,y,l,frame,x_0,y_0,label_all,label_x,label_y):
    x_line_1 = np.linspace(x[0]-l, x[0], 2)
    y_line_1 = [y[0]] * 2

    fig = Figure(figsize=(9, 7), dpi=100)
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
def print_graph_kon(x,y_1,l,beta,r_a,r_kp,frame,x_0,y_0,label_all,label_x,label_y):
    x_line_1 = np.linspace(x[0] - l, x[0], 2)
    y_line_1 = [y_1[0]] * 2

    x_line_2 = np.linspace(0, ((r_a-r_kp)/math.tan(beta*math.pi/180)), 2)
    y_line_2 = np.linspace(r_kp, r_a, 2)

    x_line_3 = np.linspace(x[0] - l, ((r_a - r_kp) / math.tan(beta * math.pi / 180)), 2)
    y_line_3 = [0] * 2

    x_line_4 = [x[0]] * 2
    y_line_4 = np.linspace(0, y_1[0], 2)

    x_line_5 = [0] * 2
    y_line_5 = np.linspace(0, y_1[-1], 2)

    x_line_6 = [x[0] - l] * 2
    y_line_6 = np.linspace(0, y_1[0], 2)

    x_line_7 = [((r_a-r_kp)/math.tan(beta*math.pi/180))] * 2
    y_line_7 = np.linspace(0, r_a, 2)

    x_total = np.concatenate([x_line_1,x,x_line_2])
    y_total = np.concatenate([y_line_1,y_1,y_line_2])

    fig = Figure(figsize=(12, 12), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#171717')  # 171717
    ax.set_aspect('equal', adjustable='box')
    ax.plot(x, y_1, color='#0094FF')

    ax.plot(x_line_1, y_line_1, color='#0094FF')
    ax.plot(x_line_2, y_line_2, color='#0094FF')
    ax.plot(x_line_3, y_line_3, color='white', linestyle='--')
    ax.plot(x_line_4, y_line_4, color='white', linestyle='--')
    ax.plot(x_line_5, y_line_5, color='white', linestyle='--')
    ax.plot(x_line_6, y_line_6, color='white')
    ax.plot(x_line_7, y_line_7, color='white')
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
    x_max = ((r_a-r_kp)/math.tan(beta*math.pi/180))*1.05
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