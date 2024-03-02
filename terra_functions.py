from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import AutoMinorLocator
import math
import matplotlib.pyplot as plt
import cantera as ct
import bisect
import customtkinter as ctk

font1 = ("Futura PT Book", 16)

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
    plt.rcParams['font.family'] = 'Futura PT'

    fig = Figure(figsize=(9,7), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#171717') #171717
    ax.plot(alpha_array, T_array, color='white')
    ax.set_title("Зависимость газовой постоянной от к.и.о.",fontsize=16, fontname='Futura PT')
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


    ax.set_xlabel('Коэффициент избытка окислителя', fontsize=16, fontname='Futura PT', color='white',)
    ax.set_ylabel("R, Дж/(кг*К)", fontsize=16, rotation='horizontal',fontname='Futura PT', color='white', labelpad=60, va='bottom')
    ax.set_xlim(min(alpha_array) * 0.98, max(alpha_array) * 1.02)
    ax.set_ylim(min(T_array) * 0.98, max(T_array) * 1.01)
    ax.title.set_color('white')
    fig.patch.set_facecolor('#171717')
    fig.subplots_adjust(left=0.22, bottom=0.1, right=0.97, top=0.95)
    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=6, column=0, padx=0, pady=0)

    canvas.draw()
def print_graph_T_opt(T_array,alpha_array,frame,x,alpha_opt,T_opt,alpha_zad):
    plt.rcParams['font.family'] = 'Futura PT'

    fig = Figure(figsize=(9,7), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#171717') #171717
    ax.plot(alpha_array, T_array, color='white')
    ax.set_title("Зависимость Температуры в КС от к.и.о.",fontsize=16, fontname='Futura PT')
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


    ax.set_xlabel('Коэффициент избытка окислителя', fontsize=16, fontname='Futura PT', color='white',)
    ax.set_ylabel("Т, К", fontsize=16, rotation='horizontal',fontname='Futura PT', color='white', labelpad=20, va='bottom')
    ax.set_xlim(min(alpha_array) * 0.98, max(alpha_array) * 1.02)
    ax.set_ylim(min(T_array) * 0.98, max(T_array) * 1.01)
    ax.title.set_color('white')
    fig.patch.set_facecolor('#171717')
    fig.subplots_adjust(left=0.13, bottom=0.1, right=0.97, top=0.95)
    canvas = FigureCanvasTkAgg(fig, master=frame)  # frame - это контейнер, где должен быть размещен график
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=5, column=0, padx=0, pady=0)

    canvas.draw()
def print_graph_I_opt(I_array,alpha_array,frame,x,alpha_opt,I_max,alpha_zad):
    plt.rcParams['font.family'] = 'Futura PT'

    fig = Figure(figsize=(9,7), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#171717') #171717
    ax.plot(alpha_array, I_array, color='white')
    ax.set_title("Зависимость удельного пустотного импульса от к.и.о.",fontsize=16, fontname='Futura PT')
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


    ax.set_xlabel('Коэффициент избытка окислителя', fontsize=16, fontname='Futura PT', color='white',)
    ax.set_ylabel("I, м/с", fontsize=16, rotation='horizontal',fontname='Futura PT', color='white', labelpad=30, va='bottom')
    ax.set_xlim(min(alpha_array) * 0.98, max(alpha_array) * 1.02)
    ax.set_ylim(min(I_array) * 0.98, max(I_array) * 1.01)
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
    alpha_array = [i / 100 for i in range(84,87)]
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

    return properties,species_names,mass_fractions,mole_fractions
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
    return properties,species_names,mass_fractions,mole_fractions,F_kp
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
        mass_fractions = gas.Y
        mole_fractions = gas.X
        species_names = gas.species_names
    return properties,species_names,mass_fractions,mole_fractions,I_a,F_a
def donut_diagramm(mass, max, master,x,y):
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
        autotext.set_fontsize(14)
        autotext.set_weight('bold')

    # Настройка стиля текстов легенды
    for text in texts:
        text.set_fontsize(16)
        text.set_color('white')

    # Центральный текст
    ax.text(0, 0, 'Массовое содержание\nкомпонентов', ha='center', va='center', fontsize=18, color='white')

    # Вставка холста в интерфейс
    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas_widget = canvas.get_tk_widget()
    # Используйте grid (или любой другой менеджер геометрии, который вы используете в CTkScrollableFrame)
    canvas_widget.place(x=x,y=y)
    # Настраиваем грид менеджер, чтобы холст растягивался вместе с родительским окном
    master.grid_rowconfigure(0, weight=1)
    master.grid_columnconfigure(0, weight=1)