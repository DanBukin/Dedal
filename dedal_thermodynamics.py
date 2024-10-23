from dedal_graphs import *
import math
import cantera as ct
import bisect
def findPressureInCritical(gas):
    """--------------------Поиск давления в критическом сечении--------------------"""
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
    """--------------------Возвращает состояние газа при заданных P и S--------------------"""
    gas.SP = S, P * 10 ** 6
    gas.equilibrate('SP')
    return gas
def find_W_F_I(gas,p,H_k):
    """--------------------Поиск скорости, площади и удельного пустотного импульса--------------------"""
    H_2 = gas.h
    W2 = 2.0 * (math.fabs(H_k - H_2))
    W = math.sqrt(W2)
    F = 1 / (gas.density * W)
    I_ud = (W + p * (10 ** 6) * F)
    return W, F,I_ud
def optimalnaya_alpha(choice,p_k,p_a,alpha,fuel,oxidizer,H_gor,H_ok,alpha_value,frame,x):
    """--------------------Поиск осовных параметров газа при к.и.о от 0,5 до 1,5--------------------"""
    k0=alpha_value
    # Задаём газ (GRI30)
    gas = ct.Solution('gri30_highT.yaml')
    #gas = ct.Solution('gri30.yaml')
    alpha_array = [i / 100 for i in range(50,150)]
    if alpha!="Оптимальный":
        alpha_zad=float(alpha)
        kostyl="Не оптимальный"
        bisect.insort(alpha_array, float(alpha))
    else:
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
    """--------------------Поиск всех основных параметров в камере сгорания--------------------"""
    k0=km0
    gas = ct.Solution('gri30_highT.yaml')
    #gas = ct.Solution('gri30.yaml')
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
    doc_excel=[]
    properties = f"""Давление (p) = {gas.P / 10 ** 6:.5} МПа
Температура (T) = {gas.T:.2f} К
Удельный объём (v) = {gas.v:.2f} м3/кг
Энтропия (S) = {gas.s:.2f} Дж/кг*К
Полная энтальпия (I) = {gas.enthalpy_mass * 0.001:.2f} кДж/кг
Полная внутренняя энергия (U) = {gas.int_energy_mass * 0.001:.2f} кДж/кг
Молярная масса газовой фазы (MMg): {gas.mean_molecular_weight:.2f} г/моль
Газовая постоянная: {gas.cp - gas.cv:.2f} Дж/кг*К
"""
    doc_excel.append(str(gas.P / 10 ** 6))
    doc_excel.append(str(gas.T))
    doc_excel.append(str(gas.v))
    doc_excel.append(str(gas.s))
    doc_excel.append(str(gas.enthalpy_mass * 0.001))
    doc_excel.append(str(gas.int_energy_mass * 0.001))
    doc_excel.append(str(gas.mean_molecular_weight))
    doc_excel.append(str(gas.cp - gas.cv))
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
        k_k=CPEQ / CVEQ
        doc_excel.append(str(CPEQ))
        doc_excel.append(str(CVEQ))
        doc_excel.append(str(CPEQ / CVEQ))
    else:
        properties +=f"""------------Замороженные параметры------------
Удельная теплоёмкость при постоянном давлении (Cp) = {gas.cp:.2f} Дж/кг*К
Удельная теплоёмкость при постоянном объёме (Cv) = {gas.cv:.2f} Дж/кг*К
Показатель адиабаты (k): {gas.cp / gas.cv:.3f}
"""
        k_k = gas.cp / gas.cv
        doc_excel.append(str(gas.cp))
        doc_excel.append(str(gas.cv))
        doc_excel.append(str(gas.cp / gas.cv))
    # Получение и вывод массовых и мольных долей компонентов смеси
    mass_fractions = gas.Y
    mole_fractions = gas.X
    species_names = gas.species_names
    return properties,species_names,mass_fractions,mole_fractions,R_k,T_k,k_k,doc_excel
def options_kp(choice,p_k,alpha,fuel,oxidizer,H_gor,H_ok,km0):
    """--------------------Поиск всех основных параметров в критическом сечении--------------------"""
    k0=km0
    gas = ct.Solution('gri30_highT.yaml')
    #gas = ct.Solution('gri30.yaml')
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
    doc_excel=[]
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
        doc_excel.append(str(p_kp))
        doc_excel.append(str(gas.T))
        doc_excel.append(str(gas.v))
        doc_excel.append(str(gas.s))
        doc_excel.append(str(gas.enthalpy_mass * 0.001))
        doc_excel.append(str(gas.int_energy_mass * 0.001))
        doc_excel.append(str(gas.mean_molecular_weight))
        doc_excel.append(str(gas.cp - gas.cv))
        doc_excel.append(str(I_ud_kp))
        doc_excel.append(str(W_kp))
        doc_excel.append(str(F_kp))
        doc_excel.append(str(beta_kp))
        doc_excel.append(str(gas.cp))
        doc_excel.append(str(gas.cv))
        doc_excel.append(str(gas.cp / gas.cv))

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
        doc_excel.append(str(p_kp))
        doc_excel.append(str(gas.T))
        doc_excel.append(str(gas.v))
        doc_excel.append(str(gas.s))
        doc_excel.append(str(gas.enthalpy_mass * 0.001))
        doc_excel.append(str(gas.int_energy_mass * 0.001))
        doc_excel.append(str(gas.mean_molecular_weight))
        doc_excel.append(str(gas.cp - gas.cv))
        doc_excel.append(str(W_kp))
        doc_excel.append(str(I_ud_kp))
        doc_excel.append(str(F_kp))
        doc_excel.append(str(beta_kp))
        doc_excel.append(str(CPEQ))
        doc_excel.append(str(CVEQ))
        doc_excel.append(str(CPEQ / CVEQ))

    return properties,species_names,mass_fractions,mole_fractions,F_kp,beta_kp,T_kp,R_kp,k_kp,p_kp,doc_excel
def options_a(choice,p_k,p_a,alpha,fuel,oxidizer,H_gor,H_ok,km0):
    """--------------------Поиск всех основных параметров на срезе сопла--------------------"""
    k0 = km0
    gas = ct.Solution('gri30_highT.yaml')
    #gas = ct.Solution('gri30.yaml')
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
    doc_excel=[]
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
        doc_excel.append(str(p_a))
        doc_excel.append(str(gas.T))
        doc_excel.append(str(gas.v))
        doc_excel.append(str(gas.s))
        doc_excel.append(str(gas.enthalpy_mass * 0.001))
        doc_excel.append(str(gas.int_energy_mass * 0.001))
        doc_excel.append(str(gas.mean_molecular_weight))
        doc_excel.append(str(gas.cp - gas.cv))
        doc_excel.append(str(W_a))
        doc_excel.append(str(I_a))
        doc_excel.append(str(F_a))
        doc_excel.append(str(gas.cp))
        doc_excel.append(str(gas.cv))
        doc_excel.append(str(gas.cp / gas.cv))

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
        doc_excel.append(str(p_a))
        doc_excel.append(str(gas.T))
        doc_excel.append(str(gas.v))
        doc_excel.append(str(gas.s))
        doc_excel.append(str(gas.enthalpy_mass * 0.001))
        doc_excel.append(str(gas.int_energy_mass * 0.001))
        doc_excel.append(str(gas.mean_molecular_weight))
        doc_excel.append(str(gas.cp - gas.cv))
        doc_excel.append(str(W_a))
        doc_excel.append(str(I_a))
        doc_excel.append(str(F_a))
        doc_excel.append(str(CPEQ))
        doc_excel.append(str(CVEQ))
        doc_excel.append(str(CPEQ / CVEQ))
    return properties,species_names,mass_fractions,mole_fractions,I_a,F_a,w_a,rho_a,k_a,doc_excel
def raschet_dozv(k0,alpha,H_gor,H_ok,fuel,oxidizer,p_k,selected_option,p_array):
    """--------------------Поиск основных параметров по длине сопла в зависимости от давления в этих сечениях--------------------"""
    if selected_option=="Равновесный":
        choice=0
    else:
        choice=1
    # Задаём газ (GRI30)
    gas = ct.Solution('gri30_highT.yaml')
    #gas = ct.Solution('gri30.yaml')
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