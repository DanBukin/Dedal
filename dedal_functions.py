from dedal_graphs import *
from dedal_table_kudr import *
import scipy

def find_teta_a(p_a,p_k):
    """=====Функция, которая находит угол выхода на срезе профиллированного сопла====="""
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
def find_teta_m(w_a,T_kp,R,k,k_kp):
    """=====Функция, которая находит угол входа в критическом сечении профиллированного сопла====="""
    a_kp=(k_kp*R*T_kp)**0.5
    lambda_a=w_a/a_kp
    k_1=( (k+1)/(k-1) )**0.5
    k_2=math.atan( (((k-1)/(k+1))**0.5) * (( ((lambda_a**2)-1)/(1-( ((k-1)*(lambda_a**2))/(k+1))) )**0.5) )
    k_3=math.atan(( ((lambda_a**2)-1)/(1-( ((k-1)*(lambda_a**2))/(k+1))) )**0.5)
    psi_lambda=k_1*k_2-k_3
    teta_m_1=(psi_lambda/3)*180/math.pi
    return teta_m_1
def find_l_sv(k_a,lambda_a,R_a,R_kp):
    """=====Поиск длины расширающейся части (формулы 10.64,10.65,10.66,10.67 Кудрявцева)====="""
    x_1=math.sqrt( (k_a+1)/(k_a-1) )
    x_2=np.arctan(math.sqrt((k_a-1)/(k_a+1))*math.sqrt( ( (lambda_a**2)-1 )/ (1-( ((k_a-1)*lambda_a**2)/(k_a+1) )) ))
    x_3=np.arctan(math.sqrt( ( (lambda_a**2)-1 )/ (1-( ((k_a-1)*lambda_a**2)/(k_a+1) )) ))
    psi=x_1*x_2-x_3
    beta=(1/3)*psi
    y_a_otn=R_a/R_kp
    x_a_otn=(y_a_otn+1)*math.sqrt(1-(1/(y_a_otn**2)))
    alpha_A=1/x_3
    x_AB_otn=y_a_otn/np.tan(alpha_A)
    x_0_otn=x_a_otn+x_AB_otn
    x_0=x_0_otn*R_kp
    return beta,x_0
def find_angle(x_array,y_array):
    """=====Функция, которая находит угол в каждой точке из массива координат профиллированного сопла====="""
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
    """=====Функция, которая находит среднее значение между двумя в массиве (кроме площади)====="""
    lenght=len(array_0)
    array_1 = [0] *(lenght-1)
    for i in range(0,lenght-1):
        array_1[i]=abs((array_0[i]+array_0[i+1])/2)
    return array_1
def srednee_znachenie_F(array_0,m):
    """=====Функция, которая находит среднее значение между двумя в массиве (для площади)====="""
    lenght=len(array_0)
    array_1 = [0] *(lenght-1)
    for i in range(0,lenght-1):
        array_1[i]=m*abs(array_0[i]-array_0[i+1])
    return array_1
def est_li_soplo_rk(R_ks,R_kp,R_1,R_2,alpha_grad):
    """=====Проверка на построение радиусно-конического сопла====="""
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
    """=====Нахождение угла в радиусной сужающейся части====="""
    beta_rad=math.asin( (R_kp+R_2-R_ks+R_1)/(R_1+R_2) )
    alpha_rad=math.pi*0.5 - beta_rad
    alpha_grad=alpha_rad*180/math.pi
    return alpha_grad
def print_options_rr(R_1,R_2,R_ks,R_kp):
    """=====Расчёт всех параметров в радиусной сужающейся части====="""
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
    """=====Расчёт всех параметров в радиусно-конической сужающейся части====="""
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
    """=====Расчёт дозвуковой части (радиусно-конической)====="""
    alpha_rad = alpha_grad*math.pi/180
    beta_grad = 90 - alpha_grad
    beta_rad = beta_grad*math.pi/180
    sin_beta_rad = math.sin(beta_rad)
    cos_beta_rad=math.cos(beta_rad)
    tg_beta_rad=math.tan(alpha_rad)
    l_eb = -R_2 * cos_beta_rad - ((R_ks - (R_kp + R_2 - R_2 * sin_beta_rad + R_1 - R_1 * sin_beta_rad)) / tg_beta_rad)
    x_01 = l_eb - R_1 * cos_beta_rad
    line_params = {'alpha': alpha_grad, 'beta': beta_grad, 'r_kp': R_kp}
    x_total, y_total=plot_partial_circle_with_line(R_1, x_01, R_ks - R_1, beta_grad, 90, line_params, 270 - alpha_grad, 270, 0,
                                  R_kp + R_2, R_2,frame,R_kp,l_eb,beta_grad,R_ks)
    return x_total, y_total
def place_subsonic_nozzle_rr(R_ks,R_kp,R_1,R_2,frame):
    """=====Расчёт дозвуковой части (радиусной)====="""
    beta_rad = math.asin((R_kp+R_2-R_ks+R_1)/(R_1+R_2))
    beta_grad=beta_rad*180/math.pi
    alpha_grad = 90 - beta_grad
    cos_beta_rad=math.cos(beta_rad)
    x_01=-R_2*cos_beta_rad-R_1*cos_beta_rad
    y_01= R_ks-R_1
    x_02=0
    y_02=R_kp+R_2
    x_total, y_total=plot_subsonic_nozzle_rr(R_ks,R_kp,R_1,R_2,beta_grad,alpha_grad,x_01,y_01,x_02,y_02,frame)
    return x_total, y_total
def find_volume_rr(R_ks,R_kp,R_1,R_2,beta_grad):
    """=====Нахождение объёма в радисуной сужающейся части====="""
    cos_beta=np.cos(np.radians(beta_grad))
    f_x_1 = lambda x: (((R_1 ** 2) - ((x - (-R_2 * cos_beta - R_1 * cos_beta)) ** 2)) ** 0.5 + (R_ks - R_1)) ** 2
    f_x_2 = lambda x: ((-((R_2 ** 2 - x ** 2) ** 0.5) + R_kp + R_2)) ** 2
    int_okr_1, _ = scipy.integrate.quad(f_x_1,-R_2 * cos_beta - R_1 * cos_beta,-R_2 * cos_beta)
    int_okr_2, _ = scipy.integrate.quad(f_x_2, -R_2 * cos_beta, 0)
    resylt_int_1 = math.pi * int_okr_1
    resylt_int_2 = math.pi * int_okr_2
    result_int_sum = (resylt_int_1 + resylt_int_2) / 1000000000
    return result_int_sum
def find_volume_rk(R_ks,R_kp,R_1,R_2,beta_grad):
    """=====Нахождение объёма в радисуно-конической сужающейся части====="""
    alpha_grad=90-beta_grad
    cos_beta=np.cos(np.radians(beta_grad))
    sin_beta=np.sin(np.radians(beta_grad))
    tg_alpha=np.tan(np.radians(alpha_grad))
    l = -R_2*cos_beta-((R_ks-(R_kp+R_2-R_2*sin_beta+R_1-R_1*sin_beta))/(tg_alpha))
    f_x_1 = lambda x: ((R_1**2-(x-(l-R_1*cos_beta))**2)**0.5+R_ks-R_1) ** 2
    f_x_2 = lambda x: (-tg_alpha*(x+R_2*cos_beta)+R_kp+R_2-R_2*sin_beta) ** 2
    f_x_3 = lambda x: (-((R_2**2)-(x**2))**0.5+R_kp+R_2) ** 2
    int_okr_1, _ = scipy.integrate.quad(f_x_1,l-R_1*cos_beta,l)
    int_okr_2, _ = scipy.integrate.quad(f_x_2,l,-R_2*cos_beta)
    int_okr_3, _ = scipy.integrate.quad(f_x_3,-R_2*cos_beta,0)
    resylt_int_1 = math.pi * int_okr_1
    resylt_int_2 = math.pi * int_okr_2
    resylt_int_3 = math.pi * int_okr_3
    result_int_sum = (resylt_int_1 + resylt_int_2+resylt_int_3)/1000000000
    return result_int_sum

def find_coord_peresech(x_1,x_2,y_1,y_2,alpha,beta):
    """=====Поиск координаты промежуточной точки для построения кривой Безье====="""
    L=x_2-x_1
    H=y_2-y_1
    L_1=(H-(L*np.tan(beta)))/(np.sin(alpha)-(np.cos(alpha)*np.tan(beta)))
    x_0=L_1*np.cos(alpha)
    y_0=L_1*np.sin(alpha)
    return x_0+x_1,y_0+y_1
def model_suzh_d_1(R_ks, R_kp,R_1, R_2):
    """=====Расчёт углов для действительной дозвуковой части (радиусной)====="""
    beta_rad = math.asin((R_kp + R_2 - R_ks + R_1) / (R_1 + R_2))
    beta_grad = beta_rad * 180 / math.pi
    alpha_grad = 90 - beta_grad
    cos_beta_rad = math.cos(beta_rad)
    x_01 = -R_2 * cos_beta_rad - R_1 * cos_beta_rad
    y_01 = R_ks - R_1
    x_02 = 0
    y_02 = R_kp + R_2
    # Генерация углов в указанном диапазоне
    angles = np.linspace(np.radians(beta_grad), np.radians(90), 100)
    angles_2 = np.linspace(np.radians(270 - alpha_grad), np.radians(270), 100)
    # Вычисление координат точек на окружности
    x_circle = x_01 + R_1 * np.cos(angles)[::-1]  # обратный порядок
    y_circle = y_01 + R_1 * np.sin(angles)[::-1]  # обратный порядок

    x_circle_2 = x_02 + R_2 * np.cos(angles_2)
    y_circle_2 = y_02 + R_2 * np.sin(angles_2)

    x_total = np.concatenate([x_circle, x_circle_2])
    y_total = np.concatenate([y_circle, y_circle_2])
    V_suzh=find_volume_rr(R_ks, R_kp,R_1, R_2,beta_grad)
    return x_total, y_total,V_suzh

def model_suzh_d_2(R_ks,R_kp,R_1,R_2,alpha_grad):
    """=====Расчёт действительной дозвуковой части (радиусно-конической)====="""
    alpha_rad = alpha_grad * math.pi / 180
    beta_grad = 90 - alpha_grad
    beta_rad = beta_grad * math.pi / 180
    sin_beta_rad = math.sin(beta_rad)
    cos_beta_rad = math.cos(beta_rad)
    tg_beta_rad = math.tan(alpha_rad)
    l_eb = -R_2 * cos_beta_rad - ((R_ks - (R_kp + R_2 - R_2 * sin_beta_rad + R_1 - R_1 * sin_beta_rad)) / tg_beta_rad)
    x_01 = l_eb - R_1 * cos_beta_rad
    line_params = {'alpha': alpha_grad, 'beta': beta_grad, 'r_kp': R_kp}
    x_total, y_total = model_suzh_d_2_points(R_1, x_01, R_ks - R_1, beta_grad, 90, line_params,270 - alpha_grad, 270, 0,R_kp + R_2, R_2, R_kp, l_eb, beta_grad)
    V_suzh=find_volume_rk(R_ks,R_kp,R_1,R_2,beta_grad)
    return x_total, y_total,V_suzh
def model_suzh_d_2_points(radius, x0, y0, start_angle, end_angle, line_params, start_angle_2, end_angle_2, x02, y02, radius2,R_kp,l,beta_grad):
    """=====Построение радиусно-конической сужающейся части====="""

    # Генерация углов в указанном диапазоне
    angles = np.linspace(np.radians(start_angle), np.radians(end_angle), 100)
    angles_2 = np.linspace(np.radians(start_angle_2), np.radians(end_angle_2), 100)

    # Вычисление координат точек на окружности
    x_circle = x0 + radius * np.cos(angles)[::-1]  # обратный порядок
    y_circle = y0 + radius * np.sin(angles)[::-1]  # обратный порядок

    x_circle_2 = x02 + radius2 * np.cos(angles_2)
    y_circle_2 = y02 + radius2 * np.sin(angles_2)
    cos_beta = np.cos(np.radians(beta_grad))
    # Вычисление координат прямой
    x_line = np.linspace(l, -radius2 * cos_beta, 10)
    y_line = -np.tan(np.radians(line_params['alpha'])) * (x_line + radius2 * np.cos(np.radians(line_params['beta']))) + \
             R_kp + radius2 - radius2 * np.sin(np.radians(line_params['beta']))

    x_total = np.concatenate([x_circle, x_line, x_circle_2])
    y_total = np.concatenate([y_circle, y_line, y_circle_2])
    return x_total, y_total
def model_ks_d(tau_pr, R_k, T_k, F_kp_d, B, V_suzh_d,F_ks_d,x_sush,y_suzh):
    L_ks=1000 * (((tau_pr * 0.001 * R_k * T_k * F_kp_d) / B) - V_suzh_d) / F_ks_d
    x_total=[]
    y_total=[]
    x_total.append(x_sush[0]-L_ks)
    y_total.append(y_suzh[0])
    x_total.append(x_sush[0])
    y_total.append(y_suzh[0])
    return x_total, y_total
def model_sv_d(k_a, lambda_a, R_a, R_kp,beta_a):

    R_otn=R_a/R_kp
    beta_m, L_sv_0=find_teta_m_1(R_otn, k_a, beta_a)
    L_sv=L_sv_0*R_kp
    beta_m=np.rad2deg(beta_m)
    R_3 = R_kp * 0.45
    x_01 = 0
    y_01 = R_kp + R_3

    pi = math.pi
    beta_m_rad = pi * beta_m / 180
    beta_a_rad = pi * beta_a / 180

    # Генерация углов в указанном диапазоне
    angles = np.linspace(np.radians(270), np.radians(270 + beta_m), 20)
    # Вычисление координат точек на окружности
    x_circle = x_01 + R_3 * np.cos(angles)
    y_circle = y_01 + R_3 * np.sin(angles)
    beta = np.radians(beta_m)
    beta_0 = beta + 3 * math.pi / 2
    x_1 = R_3 * np.cos(beta_0)
    x_2 = L_sv + R_3 * np.cos(beta_0)
    y_1 = R_3 * np.sin(beta_0) + y_01
    y_2 = R_a
    L = x_2 - x_1
    H = y_2 - y_1
    L_1 = (H - (L * np.tan(beta_a_rad))) / (np.sin(beta_m_rad) - (np.cos(beta_m_rad) * np.tan(beta_a_rad)))
    x_0 = L_1 * np.cos(beta_m_rad) + x_1
    y_0 = L_1 * np.sin(beta_m_rad) + y_1
    A = np.array([x_1, y_1])
    B = np.array([x_0, y_0])
    C = np.array([x_2, y_2])
    t_values = np.linspace(0, 1, 100)
    curve = np.array([de_casteljau(t, [A, B, C]) for t in t_values])

    x_sv = np.concatenate([x_circle, curve[:, 0]])
    y_sv = np.concatenate([y_circle, curve[:, 1]])

    return x_sv,y_sv