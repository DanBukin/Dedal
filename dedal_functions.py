from dedal_graphs import *
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
def find_teta_m(w_a,T_kp,R,k):
    """=====Функция, которая находит угол входа в критическом сечении профиллированного сопла====="""
    a_kp=(k*R*T_kp)**0.5
    lambda_a=w_a/a_kp
    k_1=( (k+1)/(k-1) )**0.5
    k_2=math.atan( (((k-1)/(k+1))**0.5) * (( ((lambda_a**2)-1)/(1-( ((k-1)*(lambda_a**2))/(k+1))) )**0.5) )
    k_3=math.atan(( ((lambda_a**2)-1)/(1-( ((k-1)*(lambda_a**2))/(k+1))) )**0.5)
    psi_lambda=k_1*k_2-k_3
    teta_m_1=(psi_lambda/3)*180/math.pi
    return teta_m_1
def find_coef_par(R_kp,R_a,teta_a,teta_m):
    """=====Функция, которая находит коэффициенты для построения профиллированного сопла====="""
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