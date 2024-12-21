from dedal_functions import *
from dedal_thermodynamics import *
from dedal_customtkinter import *
from dedal_save_properties import *
from dedal_table_kudr import *
import json
import sys
import math
from PIL import Image, ImageTk
from scipy.interpolate import interp1d
import warnings


warnings.filterwarnings("ignore", category=UserWarning)
ctk.deactivate_automatic_dpi_awareness()
with open('data/oxigen_data.json', 'r', encoding='utf-8') as file:
    substances_data = json.load(file)
with open('data/fuel_data.json', 'r', encoding='utf-8') as file:
    substances_data_1 = json.load(file)
with open('data/alpha_data.json', 'r', encoding='utf-8') as file:
    substances_data_2 = json.load(file)
from ctypes import windll

if os.name == 'nt':
    windll.gdi32.AddFontResourceExW("data/ofont.ru_Futura PT.ttf", 0x10, 0)
else:
    pass

class User:
    """----------------------------Храненние глобальных переменных для удобного вызова----------------------------"""
    def __init__(self):
        self.R_k=None
        self.T_k=None
        self.p_k=None
        self.m_sum=None
        self.F_kp=None
        self.F_ks=None
        self.B=None
        self.p_a=None
        self.rho_a=None
        self.w_a=None
        self.k_a=None
        self.T_kp=None
        self.R_kp = None
        self.k_kp = None
        self.Rad_a=None
        self.Rad_kp = None
        self.p_k = None
        self.p_a = None
        self.oxigen = None
        self.fuel = None
        self.alpha = None
        self.alpha_value = None
        self.selected_option = None
        self.formula_gor = None
        self.formula_ox = None
        self.H_gor = None
        self.H_ok =None
        self.p_kp=None
        self.alpha_itog=None
        self.x_suzh=None
        self.y_suzh=None
        self.F_otn_1=None
        self.x_sv=None
        self.y_sv=None
        self.L_ks=None
        self.P=None
        self.teta_a=None
        self.choice=None
        self.V_suzh=None
        self.tau_pr=None
        self.R_1 = None
        self.R_2 = None
        self.R_ks = None
        self.R_kp = None
        self.alpha_rad_kon = None
        self.aar = None
        self.teta_m = None
        self.x_dozv = None
        self.y_dozv = None
        self.I_a = None
        self.F_a = None
        self.Rad_ks=None
        self.k_k=None
        self.type_suzh=None
        self.R_1_0 = None
        self.R_2_0 = None
        self.alpha_suzh_0 = None
        self.lambda_a=None
        self.x_total = None
        self.y_total = None
        self.phi_s_prof=None
        self.I_alpha=None
        self.T_alpha=None
        self.R_alpha=None
        self.alpha_alpha=None
        self.options_ks_excel=None
        self.options_kp_excel=None
        self.options_a_excel=None
        self.l_pr=None
        self.X_graph = None
        self.P_graph = None
        self.T_graph = None
        self.Rho_graph = None
        self.W_graph = None
        self.M_graph = None
        self.Lambda_graph = None
        self.RW_graph = None
        self.Delta_P_suzh_1 = None
        self.Delta_P_rassh_1 = None
        self.Delta_P_itog = None
        self.phi_tr_prof = None
        self.phi_r_prof = None
        self.phi_s_prof = None
        self.max_phi = None
        self.beta_kon_itog = None
        self.phi_r_array = None
        self.phi_tr_array = None
        self.phi_s_array = None
        self.beta_kon_grad_array = None
        self.phi_k = None
        self.I_a_d = None
        self.m_sum_d = None
        self.F_kp_d = None
        self.F_a_d = None
        self.d_kp_d = None
        self.d_a_d = None
        self.itog_1 = None
        self.itog_2 = None
        self.itog_3 = None
        self.itog_4 = None
        self.itog_5 = None
        self.itog_6 = None
        self.itog_7 = None
        self.x_total_d = None
        self.y_total_d = None
        self.x_dzv = None
        self.r_dzv = None
        self.T_dozv = None
        self.rho_dozv = None
        self.R_dozv = None
        self.k_dozv = None
        self.w_dozv = None
        self.F_dozv = None
        self.x_svzv = None
        self.M_dozv = None
        self.r_sv = None
        self.T_sv_array = None
        self.rho_sv_array = None
        self.R_sv_array = None
        self.k_sv_array = None
        self.w_sv_array = None
        self.M_sv = None
        self.F_sv_array = None
user = User()
class DedalApp(ctk.CTk):
    """----------------------------Окно с выбором начальных параметров----------------------------"""
    def __init__(self):
        """=====Начальные значения атрибутов класса====="""
        super().__init__()

        self.font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 1
        self.font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 2

        self.title("DEDAL")  # Название программы
        self.resizable(False, False)  # Запрет изменения размера окна
        screen_width = self.winfo_screenwidth()  # Устанавливаем размер и позицию окна
        screen_height = self.winfo_screenheight()
        window_width = 1305
        window_height = 734
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        ctk.set_appearance_mode("Dark")  # Настройка темы
        ctk.set_default_color_theme("blue")  # Цветовая палитра
        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов

        self.iconbitmap('data/wings_4.ico')

        # Инициализация переменных
        self.is_running = True
        self.auto_fill_var = ctk.IntVar(value=0)  # Переменная для чекбокса "Авто"
        self.global_image = None
        self.image_label = None
        self.global_image_1 = None
        self.image_label_1 = None
        self.global_image_2 = None
        self.image_label_2 = None
        self.global_image_3 = None
        self.image_label_3 = None
        self.label_oxigen = None
        self.label_fuel = None
        self.oxigen = None
        self.fuel = None

        # Настройка интерфейса
        self.setup_frame()
        self.setup_label()
        self.setup_entry()
        self.setup_button()
        self.setup_combobox()
        self.setup_radio()
        self.setup_checkbox()

        # Привязка события к изменению переменной auto_fill_var
        self.auto_fill_var.trace_add("write", lambda *args: self.update_enthalpy())
        self.periodic_check()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """=====Действие при нажатии на крестик закрытия окна====="""
        self.destroy()
        sys.exit()  # Завершает работу программы
    def periodic_check(self):
        """=====Обновление параметров====="""
        if self.is_running:
            self.update_enthalpy()
            self.alpha_input()
    def alpha_input(self):
        """=====Обновление параметров в зависимости от нажатия радио-кнопки====="""
        if self.is_running:
            if self.radio_var_alpha.get() == 1:  # Если выбрана первая радиокнопка
                if self.Entry_alpha:
                    self.Entry_alpha.place_forget()
            elif self.radio_var_alpha.get() == 2:  # Если выбрана вторая радиокнопка
                if self.Entry_alpha:
                    self.Entry_alpha.place(x=5, y=90)

    def update_enthalpy(self):
        """=====Появляние и исчезновение объектов в заисимости от выбора пользователя====="""
        self.selected_substance_oxigen = self.combobox1.get()  # Получаем выбранный окислитель
        self.selected_substance_fuel = self.combobox2.get()  # Получаем выбранное горючее

        # Получаем данные для выбранного окислителя
        oxigen_data = substances_data.get(self.selected_substance_oxigen, {})
        self.formula_ox = oxigen_data.get('formula', None)
        self.H_ok = oxigen_data.get('H', None)
        self.enthalpy_value_oxigen = f"{self.H_ok} кДж/кг" if self.H_ok is not None else ""

        # Аналогично для горючего
        fuel_data = substances_data_1.get(self.selected_substance_fuel, {})
        self.formula_gor = fuel_data.get('formula', None)
        self.H_gor = fuel_data.get('H', None)
        self.enthalpy_value_fuel = f"{self.H_gor} кДж/кг" if self.H_gor is not None else ""


        # Обновляем или создаем лейблы для оксидов и горючих веществ
        if self.label_oxigen:
            self.label_oxigen.configure(text=self.enthalpy_value_oxigen)
        else:
            self.label_oxigen = create_label(self.frame3, self.enthalpy_value_oxigen, 20, 80)

        if self.label_fuel:
            self.label_fuel.configure(text=self.enthalpy_value_fuel)
        else:
            self.label_fuel = create_label(self.frame4, self.enthalpy_value_fuel, 20, 80)

        # Показываем лейблы
        if self.auto_fill_var.get() == 1:  # Если чекбокс "Авто" нажат
            self.Entry1.place_forget()  # Скрываем Entry1
            self.Entry2.place_forget()  # Скрываем Entry2
            self.label_oxigen.place(x=20, y=80)
            self.label_fuel.place(x=20, y=80)
        else:
            self.Entry1.place(x=5, y=80)
            self.Entry2.place(x=10, y=80)
            # Скрываем лейблы, если они созданы
            self.label_oxigen.place_forget()
            self.label_fuel.place_forget()

    def setup_label(self):
        """=====Создание Надписей====="""
        self.label1 = create_label(self, "Добро пожаловавть в программу 'Дедал' !", 400, 5)
        self.label2 = create_label(self.frame1, "Пожалуйста,\nвыберите компоненты:", 25, 5)
        self.label3 = create_label(self.frame3, "Окислитель:", x=10, y=0)
        self.label4 = create_label(self.frame4, "Горючее:", x=10, y=0)
        self.label5 = create_label(self.frame3, "Энтальпия ок.:", x=10, y=50)
        self.label6 = create_label(self.frame4, "Энтальпия гор.:", x=10, y=50)
        self.label7 = create_label(self.frame5, "Коэфф. изб. окислителя:", x=5, y=0)
        self.label8 = create_label(self.frame7, "Давление в КС:", x=5, y=0)
        self.label9 = create_label(self.frame8, "Давление на срезе:", x=5, y=0)
        self.label10 = create_label(self.frame9, "Тип течения:", x=5, y=0)
        self.label11 = create_label(self.frame7, "МПа", x=115, y=25)
        self.label12 = create_label(self.frame8, "МПа", x=115, y=25)
    def setup_frame(self):
        """=====Создание мини-окон====="""
        self.frame1 = create_frame(self,200, 470,10,10,"#2b2b2b","transparent")
        self.frame2 = create_frame(self,640, 50,220,35,"#2b2b2b","transparent")
        self.frame3 = create_frame(self,180, 120, 20,60,"#3D3D3D", '#2b2b2b')
        self.frame4 = create_frame(self,180, 120,20,190, "#3D3D3D", '#2b2b2b')
        self.frame5 = create_frame(self,180, 150,20,320, "#3D3D3D", '#2b2b2b')
        self.frame6 = create_frame(self,500, 100,215,380,"#2b2b2b","transparent")
        self.frame7 = create_frame(self,160, 60,220,400, "#3D3D3D", '#2b2b2b')
        self.frame8 = create_frame(self,160, 60, 385,400,"#3D3D3D", '#2b2b2b')
        self.frame9 = create_frame(self,150, 80, 555,390,"#3D3D3D", '#2b2b2b')

    def setup_entry(self):
        """=====Создание окон с вводом данных====="""
        self.entry1_value = ctk.StringVar()
        self.entry2_value = ctk.StringVar()
        self.entry3_value = ctk.StringVar()
        self.entry4_value = ctk.StringVar()
        self.entry5_value = ctk.StringVar()
        self.Entry1 = create_entry(self.frame3, 140, self.entry1_value,5,80)
        self.Entry2 = create_entry(self.frame4, 140, self.entry2_value,10,80)
        self.Entry3 = create_entry(self.frame7, 100, self.entry3_value,10,25)
        self.Entry4 = create_entry(self.frame8, 100, self.entry4_value,10,25)
        self.Entry_alpha = ctk.CTkEntry(master=self.frame5, width=140, textvariable=self.entry5_value)

    def setup_combobox(self):
        """=====Создание ячеек с компонентами====="""
        self.combobox1 = ctk.CTkComboBox(self.frame3,values=["", "Кислород", "Озон", "АК", "АК-27", "АТ", "Перекись водорода", "Воздух"],command=self.combobox_callback1, font=self.font2, width=170)
        self.combobox2 = ctk.CTkComboBox(self.frame4,values=["", "Водород", "НДМГ", "Метан", "Аммиак", "Керосин РГ-1", "Керосин Т-1","Керосин RP-1", "Синтин", "Боктан", "Этанол", "ММГ", "Гидразин", "Анилин","Триэтиламин", "Ксилидин", ], command=self.combobox_callback2, font=self.font2,width=170)
        self.combobox1.place(x=5, y=25)
        self.combobox2.place(x=5, y=25)
    def combobox_callback1(self,value):
        """=====Функиця, связанная с сохранением выбранного окислителя====="""
        self.oxigen = value
        self.periodic_check()
    def combobox_callback2(self,value):
        """=====Функиця, связанная с сохранением выбранного горючего====="""
        self.fuel = value
        self.periodic_check()
    def setup_button(self):
        """=====Создание кнопок====="""
        self.button0 = create_button(self, "?", lambda: show_spravka(self),self.font1, 20, 840, 5)
        self.button1 = create_button(self.frame2, "Свойства окислителя", lambda: show_oxigen_properties(self),self.font1, 200, 10, 10)
        self.button2 = create_button(self.frame2, "Свойства горючего", lambda: show_fuel_properties(self), self.font1,200, 215, 10)
        self.button3 = create_button(self.frame2, "Свойства топливной пары", lambda: show_alpha_properties(self),self.font1, 210, 420, 10)
        self.close_button = create_button(self, "Дальше", self.close_window, self.font1,100,720,450)

        show_spravka(self)

    def setup_radio(self):
        """=====Создание радио-кнопок с выбором режима и типом поиска к.и.о====="""
        self.radio_var = ctk.IntVar()
        self.radio_var_alpha = ctk.IntVar(value=2)

        self.radio_option1 = ctk.CTkRadioButton(self.frame9, text="Равновесный", variable=self.radio_var, value=1)
        self.radio_option2 = ctk.CTkRadioButton(self.frame9, text="Замороженный", variable=self.radio_var, value=2)
        self.radio_option3 = ctk.CTkRadioButton(self.frame5, text="Оптимальный", variable=self.radio_var_alpha, command=self.on_radio_button1_clicked,value=1)
        self.radio_option4 = ctk.CTkRadioButton(self.frame5, text="Заданный", variable=self.radio_var_alpha,command=self.on_radio_button2_clicked, value=2)

        self.radio_option1.place(x=10, y=25)
        self.radio_option2.place(x=10, y=50)
        self.radio_option3.place(x=10, y=30)
        self.radio_option4.place(x=10, y=60)
    def on_radio_button1_clicked(self):
        """=====Обновление параметров при нажании на радио-кнопку====="""
        self.periodic_check()

    def on_radio_button2_clicked(self):
        """=====Обновление параметров при нажании на радио-кнопку====="""
        self.periodic_check()
    def get_selected_option(self):
        """=====Возвращает тип течения потока====="""
        self.selected_option = None
        if self.radio_var.get() == 1:
            self.selected_option = "Равновесный"
        elif self.radio_var.get() == 2:
            self.selected_option = "Замороженный"
        return self.selected_option
    def get_selected_option_alpha(self):
        """=====Возвращает тип поиска к.и.о.====="""
        self.selected_option_alpha = None
        if self.radio_var_alpha.get() == 1:
            self.selected_option_alpha = "Оптимальный"
        elif self.radio_var_alpha.get() == 2:
            self.selected_option_alpha = "Заданный"
        return self.selected_option_alpha
    def setup_checkbox(self):
        """=====Выбор автоматического поиска энтальпии у компонентов====="""
        self.auto_fill_var = ctk.IntVar(value=1)  # Переменная для отслеживания состояния чекбокса (0 - не нажат, 1 - нажат)
        self.auto_fill_checkbox = ctk.CTkCheckBox(self, text="Авто", variable=self.auto_fill_var, font=self.font1)
        self.auto_fill_checkbox.place(x=720, y=400)

    def close_window(self):
        """=====Закрытие окна с предварительным сохранием данных====="""
        # Сохраняем данные перед уничтожением основного окна
        self.p_k = self.entry3_value.get()
        self.p_a = self.entry4_value.get()
        self.selected_option = self.get_selected_option()
        self.selected_option_alpha = self.get_selected_option_alpha()

        if self.label_oxigen.winfo_ismapped():
            self.kost = 1
        else:
            self.H_ok = self.entry1_value.get()
            self.H_gor = self.entry2_value.get()

        if self.Entry_alpha.winfo_ismapped():
            self.alpha = self.entry5_value.get()
        else:
            self.alpha = "Оптимальный"

        self.alpha_value = substances_data_2.get(self.fuel, {}).get(self.oxigen, None)

        # Закрываем основное окно
        self.is_running = False

        try:
            self.destroy()
        except:
            print('Ошибка')
        user.p_k = self.p_k
        user.p_a = self.p_a
        user.oxigen =self.oxigen
        user.fuel =self.fuel
        user.alpha =self.alpha
        user.alpha_value =self.alpha_value
        user.selected_option =self.selected_option
        user.formula_gor =self.formula_gor
        user.formula_ox =self.formula_ox
        user.H_gor =self.H_gor
        user.H_ok =self.H_ok
        second_window = SecondWindow(self.oxigen, self.fuel, self.p_k, self.p_a, self.alpha, self.alpha_value,
                                     self.selected_option, self.formula_gor, self.formula_ox, self.H_gor, self.H_ok)
        second_window.mainloop()
class SecondWindow(ctk.CTk):
    """----------------------------Окно с отрисовкой основных параметров в зависимости от к.и.о.----------------------------"""
    def __init__(self, oxigen, fuel, p_k, p_a, alpha, alpha_value, selected_option, formula_gor, formula_ox, H_gor, H_ok):
        """=====Начальные значения атрибутов класса====="""
        super().__init__()
        self.oxigen_naz = oxigen
        self.fuel_naz = fuel
        self.p_k = float(p_k)
        self.p_a = float(p_a)
        self.alpha = alpha
        self.km0 = float(alpha_value)
        self.tech = selected_option
        self.formula_gor = formula_gor
        self.formula_ox = formula_ox
        self.H_gor = float(H_gor)
        self.H_ok = float(H_ok)

        self.font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 1
        self.font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 2

        self.title("Оптимальный коэффициент избытка окислителя")  # Название программы
        self.resizable(False, False)  # Запрет изменения размера окна

        screen_width = self.winfo_screenwidth()  # Устанавливаем размер и позицию окна
        screen_height = self.winfo_screenheight()
        window_width = 1305
        window_height = 734
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        self.iconbitmap('data/wings_4.ico')
        ctk.set_appearance_mode("Dark")  # Настройка темы
        ctk.set_default_color_theme("blue")  # Цветовая палитра
        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов

        self.alpha_array = [i / 100 for i in range(50, 150)]  #[0.5, 0.51, 0.52, ..., 1.49, 1.5]
        if self.alpha != "Оптимальный":
            self.opisanie_alpha="Задаём число"
            self.alpha=float(self.alpha)
            bisect.insort_left(self.alpha_array, self.alpha)
        else:
            self.opisanie_alpha = "Оптимальное"
        if self.tech=="Равновесный":
            self.choice=0
        else:
            self.choice = 1
        user.choice=self.choice
        self.fuel=self.formula_gor
        self.oxidizer=self.formula_ox
        self.scrollbar()
        self.place_label()
        self.graph_opt()
        self.but_exel()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """=====Действие при нажатии на крестик закрытия окна====="""
        self.destroy()
        sys.exit()  # Завершает работу программы
    def scrollbar(self):
        """=====Создание пролистывающегося фрейма====="""
        self.scrollbar_frame = ctk.CTkScrollableFrame(self, width=830, height=370+95,fg_color='#171717') #171717
        self.scrollbar_frame.place(x=10, y=10)
    def place_label(self):
        """=====Создание Надписей====="""
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame, text=f"Окислитель: {self.oxigen_naz}",font=self.font1)
        self.label1.grid(row=0, column=0,sticky='w', padx=10, pady=0)
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame, text=f"Горючее: {self.fuel_naz}",font=self.font1)
        self.label1.grid(row=1, column=0, sticky='w',padx=10, pady=0)
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame, text=f"Давление в камере: {self.p_k} МПа",font=self.font1)
        self.label1.grid(row=2, column=0, sticky='w',padx=10, pady=0)
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame, text=f"Давление на срезе: {self.p_a} МПа",font=self.font1)
        self.label1.grid(row=3, column=0, sticky='w',padx=10, pady=0)
    def graph_opt(self):
        """=====Заполнение массивов основных параметров====="""
        self.alph_array,self.I_array,self.T_array,self.R_array,self.alpha_itog=optimalnaya_alpha(self.choice, self.p_k, self.p_a, self.alpha,
                          self.fuel, self.oxidizer, self.H_gor, self.H_ok, self.km0, self.scrollbar_frame,0)
        user.alpha_itog=self.alpha_itog
        user.I_alpha=self.I_array
        user.T_alpha=self.T_array
        user.R_alpha=self.R_array
        user.alpha_alpha=self.alph_array
    def but_exel(self):
        """=====Создание кнопок====="""
        self.button1_I_exel = ctk.CTkButton(master=self.scrollbar_frame,text="Excel",width=60,command=lambda: save_to_excel(self.I_array, self.alph_array,'Коэффициент избытка оксилителя','Импульс'))
        self.button1_I_exel.place(x=615,y=460)
        self.button1_I_txt = ctk.CTkButton(master=self.scrollbar_frame, text="txt", width=50,command=lambda: save_to_txt(self.I_array, self.alph_array))
        self.button1_I_txt.place(x=620, y=490)

        self.button1_T_exel = ctk.CTkButton(master=self.scrollbar_frame, text="Excel", width=60,command=lambda: save_to_excel(self.T_array, self.alph_array,'Коэффициент избытка оксилителя','Температура'))
        self.button1_T_exel.place(x=615, y=910)
        self.button1_T_txt = ctk.CTkButton(master=self.scrollbar_frame, text="txt", width=50,command=lambda: save_to_txt(self.T_array, self.alph_array))
        self.button1_T_txt.place(x=620, y=940)

        self.button1_R_exel = ctk.CTkButton(master=self.scrollbar_frame, text="Excel", width=60,command=lambda: save_to_excel(self.R_array, self.alph_array,'Коэффициент избытка оксилителя','Газовая постоянная'))
        self.button1_R_exel.place(x=615, y=1365)
        self.button1_R_txt = ctk.CTkButton(master=self.scrollbar_frame, text="txt", width=50,command=lambda: save_to_txt(self.R_array, self.alph_array))
        self.button1_R_txt.place(x=620, y=1395)

        self.but_back = ctk.CTkButton(master=self.scrollbar_frame, text="Назад", width=100,command=lambda: self.back_window())
        self.but_back.place(x=725, y=1440)

        self.button_close = ctk.CTkButton(master=self.scrollbar_frame, text="Дальше", width=100,command=lambda: self.close_window())
        self.button_close.place(x=725, y=1470)
    def back_window(self):
        """=====Возвращение к предыдущему окну====="""
        self.destroy()
        user.oxigen=None
        user.fuel=None
        user.p_k=None
        user.p_a=None
        user.alpha=None
        user.alpha_value=None
        user.selected_option=None
        user.formula_gor=None
        user.formula_ox=None
        user.H_gor=None
        user.H_ok=None
        user.choice=None
        user.alpha_itog =None
        user.I_alpha = None
        user.T_alpha = None
        user.R_alpha = None
        user.alpha_alpha = None
        app = DedalApp()
        app.mainloop()
    def close_window(self):
        """=====Переход к следующему окну====="""
        self.destroy()
        third_window = ThirdWindow(self.formula_ox,self.formula_gor,self.p_k,self.p_a,self.alpha,self.km0,self.tech,self.H_gor,self.H_ok,self.alpha_itog,self.choice)
        third_window.mainloop()
class ThirdWindow(ctk.CTk):
    """----------------------------Окно с выводом данных в основных сечениях камеры (Астра/Терра)----------------------------"""
    def __init__(self,formula_ox,formula_gor,p_k,p_a,alpha,km0,tech,H_gor,H_ok,alpha_itog,choice):
        """=====Начальные значения атрибутов класса====="""
        super().__init__()
        self.formula_ox = formula_ox
        self.formula_gor = formula_gor
        self.p_k = p_k
        self.p_a = p_a
        self.alpha = alpha
        self.km0 = km0
        self.tech = tech
        self.H_gor = H_gor
        self.H_ok = H_ok
        self.alpha_itog = alpha_itog
        self.choice = choice
        self.font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 1
        self.font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 2
        self.font3 = ("Futura PT Book", 20)  # Настройка пользовательского шрифта 2

        self.title("Параметры по соплу камеры")  # Название программы
        self.resizable(False, False)  # Запрет изменения размера окна

        screen_width = self.winfo_screenwidth()  # Устанавливаем размер и позицию окна
        screen_height = self.winfo_screenheight()
        window_width = 1305
        window_height = 734
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        ctk.set_appearance_mode("Dark")  # Настройка темы
        ctk.set_default_color_theme("blue")  # Цветовая палитра
        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов

        self.iconbitmap('data/wings_4.ico')
        self.scrollbar()
        self.options_KS()
        self.options_KP()
        self.options_A()
        self.place_label()
        self.donut_mass()
        self.print_engine()
        self.button_excel()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """=====Действие при нажатии на крестик закрытия окна====="""
        self.destroy()
        sys.exit()  # Завершает работу программы
    def button_excel(self):
        """=====Создание кнопок====="""
        self.but_prop_ks_txt = ctk.CTkButton(master=self.scrollbar_frame, text="txt", width=40,command=lambda: save_properties_txt(self.properties))
        self.but_prop_ks_txt.place(x=560, y=215)
        self.but_prop_kp_txt = ctk.CTkButton(master=self.scrollbar_frame, text="txt", width=40,command=lambda: save_properties_txt(self.properties_kp))
        self.but_prop_kp_txt.place(x=560, y=925)
        self.but_prop_a_txt = ctk.CTkButton(master=self.scrollbar_frame, text="txt", width=40,command=lambda: save_properties_txt(self.properties_a))
        self.but_prop_a_txt.place(x=560, y=1640)

        self.but_mass_ks_txt = ctk.CTkButton(master=self.scrollbar_frame, text="txt", width=40,command=lambda: save_mass_txt(self.species_names,self.mass_fractions,self.mole_fractions))
        self.but_mass_ks_txt.place(x=360, y=715-50-10)
        self.but_mass_kp_txt = ctk.CTkButton(master=self.scrollbar_frame, text="txt", width=40,command=lambda: save_mass_txt(self.species_names_kp,self.mass_fractions_kp,self.mole_fractions_kp))
        self.but_mass_kp_txt.place(x=360, y=1425-50-5)
        self.but_mass_a_txt = ctk.CTkButton(master=self.scrollbar_frame, text="txt", width=40,command=lambda: save_mass_txt(self.species_names_a,self.mass_fractions_a,self.mole_fractions_a))
        self.but_mass_a_txt.place(x=360, y=2140-50)

        self.but_all_txt = ctk.CTkButton(master=self.scrollbar_frame, text="Сохранить все", width=100,command=lambda: save_all_txt(self.properties,self.properties_kp,self.properties_a,self.species_names,self.mass_fractions,self.mole_fractions,self.species_names_kp,self.mass_fractions_kp,self.mole_fractions_kp,self.species_names_a, self.mass_fractions_a,self.mole_fractions_a))
        self.but_all_txt.place(x=620, y=2140 - 50)

        self.but_back = ctk.CTkButton(master=self.scrollbar_frame, text="Назад", width=100,command=lambda: self.back_window())
        self.but_back.place(x=730, y=2140 - 80)

        self.but_close = ctk.CTkButton(master=self.scrollbar_frame, text="Дальше", width=100,command=lambda:self.close_window())
        self.but_close.place(x=730, y=2140 - 50)
    def print_engine(self):
        """=====Отрисовка изображений в окне====="""
        self.original_image = Image.open("data/engine_ks.png")  # Путь к изображению
        self.resized_image = self.original_image.resize((round(421*0.9), round(231*0.9)), Image.Resampling.LANCZOS)
        self.global_image = ImageTk.PhotoImage(self.resized_image)
        self.image_label = ctk.CTkLabel(self.scrollbar_frame, image=self.global_image)
        self.image_label.place(x=560, y=60)
        self.image_label.configure(text="")

        self.original_image = Image.open("data/engine_kp.png")  # Путь к изображению
        self.resized_image = self.original_image.resize((round(406 * 1.0), round(226 * 1.0)),Image.Resampling.LANCZOS)
        self.global_image = ImageTk.PhotoImage(self.resized_image)
        self.image_label = ctk.CTkLabel(self.scrollbar_frame, image=self.global_image)
        self.image_label.place(x=560, y=760)
        self.image_label.configure(text="")

        self.original_image = Image.open("data/engine_a.png")  # Путь к изображению
        self.resized_image = self.original_image.resize((round(474 * 0.85), round(256 * 0.85)),Image.Resampling.LANCZOS)
        self.global_image = ImageTk.PhotoImage(self.resized_image)
        self.image_label = ctk.CTkLabel(self.scrollbar_frame, image=self.global_image)
        self.image_label.place(x=560, y=1480)
        self.image_label.configure(text="")
    def scrollbar(self):
        """=====Создание прокручивающихся фреймов====="""
        self.scrollbar_frame = ctk.CTkScrollableFrame(self, width=830, height=370 + 95,fg_color='#171717')  # 171717
        self.scrollbar_frame.place(x=10, y=10)
        self.scrollbar_frame_1 = ctk.CTkScrollableFrame(self.scrollbar_frame, width=520, height=30,fg_color='black')  # 520
        self.scrollbar_frame_1.grid(row=1, column=0, padx=5, pady=0, sticky='w')
        self.scrollbar_frame_2 = ctk.CTkScrollableFrame(self.scrollbar_frame, width=320, height=400,fg_color='black')  # 520
        self.scrollbar_frame_2.grid(row=2, column=0, padx=5, pady=15, sticky='w')
        self.scrollbar_frame_3 = ctk.CTkScrollableFrame(self.scrollbar_frame, width=520, height=30,fg_color='black')  # 520
        self.scrollbar_frame_3.grid(row=4, column=0, padx=5, pady=15, sticky='w')
        self.scrollbar_frame_4 = ctk.CTkScrollableFrame(self.scrollbar_frame, width=320, height=400,fg_color='black')  # 520
        self.scrollbar_frame_4.grid(row=5, column=0, padx=5, pady=15, sticky='w')
        self.scrollbar_frame_5 = ctk.CTkScrollableFrame(self.scrollbar_frame, width=520, height=30,fg_color='black')  # 520
        self.scrollbar_frame_5.grid(row=7, column=0, padx=5, pady=15, sticky='w')
        self.scrollbar_frame_6 = ctk.CTkScrollableFrame(self.scrollbar_frame, width=320, height=400,fg_color='black')  # 520
        self.scrollbar_frame_6.grid(row=8, column=0, padx=5, pady=15, sticky='w')
    def options_KS(self):
        """=====Вывод всей информации, связанной с КС====="""
        self.properties,self.species_names,self.mass_fractions,self.mole_fractions,self.R_k,self.T_k,self.k_k,self.options_ks_excel=options_ks(self.choice,self.p_k,self.alpha_itog,self.formula_gor,self.formula_ox,self.H_gor,self.H_ok,self.km0)
        user.R_k = self.R_k
        user.T_k = self.T_k
        user.k_k=self.k_k
        user.options_ks_excel=self.options_ks_excel
        self.i = 1
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_2, text="Компонент", font=self.font1, justify='left')
        self.label1.grid(row=0, column=0, sticky='w', padx=0, pady=0)
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_2, text="Мас. доли", font=self.font1,justify='left')
        self.label1.grid(row=0, column=1, sticky='w', padx=20, pady=0)
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_2, text="Мол. доли", font=self.font1,justify='left')
        self.label1.grid(row=0, column=2, sticky='w', padx=20, pady=0)
        for self.name, self.mass_frac, self.mole_frac in zip(self.species_names, self.mass_fractions, self.mole_fractions):
            if self.mass_frac != 0:
                self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_2, text=self.name, font=self.font1,justify='left')
                self.label1.grid(row=self.i, column=0, sticky='w', padx=0, pady=0)
                self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_2, text=f"{self.mass_frac:<{10}.4e}", font=self.font1,justify='left')
                self.label1.grid(row=self.i, column=1, sticky='w', padx=20, pady=0)
                self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_2, text=f"{self.mole_frac:<{10}.4e}", font=self.font1,justify='left')
                self.label1.grid(row=self.i, column=2, sticky='w', padx=20, pady=0)
                self.i +=1
    def options_KP(self):
        """=====Вывод всей информации, связанной с критическим сечением====="""
        self.properties_kp,self.species_names_kp,self.mass_fractions_kp,self.mole_fractions_kp,self.F_kp,self.beta_kp,self.T_kp,self.R_kp,self.k_kp,self.p_kp,self.options_kp_excel=options_kp(self.choice,self.p_k,self.alpha_itog,self.formula_gor,self.formula_ox,self.H_gor,self.H_ok, self.km0)
        user.B = self.beta_kp
        user.T_kp = self.T_kp
        user.R_kp = self.R_kp
        user.k_kp = self.k_kp
        user.p_kp=self.p_kp
        user.options_kp_excel=self.options_kp_excel
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_4, text="Компонент", font=self.font1, justify='left')
        self.label1.grid(row=0, column=0, sticky='w', padx=0, pady=0)
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_4, text="Мас. доли", font=self.font1, justify='left')
        self.label1.grid(row=0, column=1, sticky='w', padx=20, pady=0)
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_4, text="Мол. доли", font=self.font1, justify='left')
        self.label1.grid(row=0, column=2, sticky='w', padx=20, pady=0)
        for self.name_kp, self.mass_frac_kp, self.mole_frac_kp in zip(self.species_names_kp, self.mass_fractions_kp,
                                                             self.mole_fractions_kp):
            if self.mass_frac_kp != 0:
                self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_4, text=self.name_kp, font=self.font1,
                                           justify='left')
                self.label1.grid(row=self.i, column=0, sticky='w', padx=0, pady=0)
                self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_4, text=f"{self.mass_frac_kp:<{10}.4e}",
                                           font=self.font1, justify='left')
                self.label1.grid(row=self.i, column=1, sticky='w', padx=20, pady=0)
                self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_4, text=f"{self.mole_frac_kp:<{10}.4e}",
                                           font=self.font1, justify='left')
                self.label1.grid(row=self.i, column=2, sticky='w', padx=20, pady=0)
                self.i += 1
    def options_A(self):
        """=====Вывод всей информации, связанной со срезом сопла====="""
        self.properties_a, self.species_names_a, self.mass_fractions_a, self.mole_fractions_a,self.I_a,self.F_a,self.w_a,self.rho_a,self.k_a,self.options_a_excel = options_a(
            self.choice, self.p_k,self.p_a, self.alpha_itog, self.formula_gor, self.formula_ox, self.H_gor, self.H_ok, self.km0)
        user.w_a=self.w_a
        user.rho_a=self.rho_a
        user.k_a = self.k_a
        user.options_a_excel=self.options_a_excel
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_6, text="Компонент", font=self.font1, justify='left')
        self.label1.grid(row=0, column=0, sticky='w', padx=0, pady=0)
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_6, text="Мас. доли", font=self.font1, justify='left')
        self.label1.grid(row=0, column=1, sticky='w', padx=20, pady=0)
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_6, text="Мол. доли", font=self.font1, justify='left')
        self.label1.grid(row=0, column=2, sticky='w', padx=20, pady=0)
        for self.name_a, self.mass_frac_a, self.mole_frac_a in zip(self.species_names_a, self.mass_fractions_a,
                                                                      self.mole_fractions_a):
            if self.mass_frac_a != 0:
                self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_6, text=self.name_a, font=self.font1,
                                           justify='left')
                self.label1.grid(row=self.i, column=0, sticky='w', padx=0, pady=0)
                self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_6, text=f"{self.mass_frac_a:<{10}.4e}",
                                           font=self.font1, justify='left')
                self.label1.grid(row=self.i, column=1, sticky='w', padx=20, pady=0)
                self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_6, text=f"{self.mole_frac_a:<{10}.4e}",
                                           font=self.font1, justify='left')
                self.label1.grid(row=self.i, column=2, sticky='w', padx=20, pady=0)
                self.i += 1
    def place_label(self):
        """=====Создание надписей в окне====="""
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame, text=f"Параметры в камере сгорания",font=self.font3)
        self.label1.grid(row=0, column=0, padx=10, pady=0)
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_1, text=(self.properties), font=self.font1,justify='left')
        self.label1.grid(row=0, column=0, sticky='w', padx=10, pady=0)
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame, text=f"Параметры в критическом сечении", font=self.font3)
        self.label1.grid(row=3, column=0, padx=10, pady=0)
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_3, text=(self.properties_kp), font=self.font1,justify='left')
        self.label1.grid(row=0, column=0, sticky='w', padx=10, pady=0)
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame, text=f"Параметры на срезе сопла",font=self.font3)
        self.label1.grid(row=6, column=0, padx=10, pady=0)
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame_5, text=(self.properties_a), font=self.font1,justify='left')
        self.label1.grid(row=0, column=0, sticky='w', padx=10, pady=0)
    def donut_mass(self):
        """=====Создание круговой диаграммы====="""
        self.elements_value = {}
        for i in range(len(self.species_names)):
            self.elements_value[self.species_names[i]] = list(self.mass_fractions)[i]
        self.sorted_elements = sorted(self.elements_value.items(), key=lambda item: item[1], reverse=True)
        if self.formula_ox=={'O': 2} and self.formula_gor=={'H': 2}:
            self.max_number=2
        else:
            self.max_number = 4
        donut_diagramm(mass=self.sorted_elements, max=self.max_number, master=self.scrollbar_frame,x=550,y=370)

        self.elements_value_kp = {}
        for i in range(len(self.species_names_kp)):
            self.elements_value_kp[self.species_names_kp[i]] = list(self.mass_fractions_kp)[i]
        self.sorted_elements_kp = sorted(self.elements_value_kp.items(), key=lambda item: item[1], reverse=True)
        donut_diagramm(mass=self.sorted_elements_kp, max=self.max_number-1, master=self.scrollbar_frame, x=550, y=1440)

        self.elements_value_a = {}
        for i in range(len(self.species_names_a)):
            self.elements_value_a[self.species_names_a[i]] = list(self.mass_fractions_a)[i]
        self.sorted_elements_a = sorted(self.elements_value_a.items(), key=lambda item: item[1], reverse=True)
        donut_diagramm(mass=self.sorted_elements_a, max=self.max_number-1, master=self.scrollbar_frame, x=550, y=2515)
    def back_window(self):
        """=====Переход к предыдущему окну====="""
        user.R_k = None
        user.T_k = None
        user.k_k=None
        user.B = None
        user.T_kp = None
        user.R_kp = None
        user.k_kp = None
        user.p_kp = None
        user.w_a = None
        user.rho_a = None
        user.k_a = None
        user.options_ks_excel = None
        user.options_kp_excel = None
        user.options_a_excel = None

        self.destroy()
        second_window = SecondWindow(user.oxigen, user.fuel, user.p_k, user.p_a, user.alpha, user.alpha_value,
                                     user.selected_option, user.formula_gor, user.formula_ox, user.H_gor, user.H_ok)
        second_window.mainloop()
    def close_window(self):
        """=====Переход к следующему окну====="""
        self.destroy()
        user.I_a=self.I_a
        nozzle_window = NozzleWindow(self.I_a,self.F_kp,self.F_a,self.p_k)
        nozzle_window.mainloop()
class NozzleWindow(ctk.CTk):
    """----------------------------Окно с выбором параметров для построения сужающейся части----------------------------"""
    def __init__(self,I_a,F_kp,F_a,p_k):
        """=====Начальные значения атрибутов класса====="""
        super().__init__()
        self.I_a=float(I_a)
        self.F_kp_otn = float(F_kp)
        self.F_a_otn = float(F_a)
        self.p_k=float(p_k)*1000000
        self.font1 = ("Futura PT Book", 16)
        self.font2 = ("Futura PT Book", 14)
        self.font3 = ("Futura PT Book", 20)
        self.font4 = ("Futura PT Book", 18)

        self.title("Подготовка к проетированию сопла")  # Название программы
        self.resizable(False, False)  # Запрет изменения размера окна
        self.iconbitmap('data/wings_4.ico')
        screen_width = self.winfo_screenwidth()  # Устанавливаем размер и позицию окна
        screen_height = self.winfo_screenheight()
        window_width = 1305
        window_height = 734
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        ctk.set_appearance_mode("Dark")  # Настройка темы
        ctk.set_default_color_theme("blue")  # Цветовая палитра
        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов

        self.label3 = None
        self.P = None  # Тяга не введена
        self.kost = None  # Коэффициент не выбран
        self.R_1=None
        self.R_2=None
        self.alpha_rad_kon=None
        self.kost_1=1
        self.kost_2=1
        self.kost_3=30

        self.scrollbar()
        self.place_frame()
        self.place_label()
        self.place_entry()
        self.place_button()
        self.place_slider()
        self.print_soplo()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """=====Действие при нажатии на крестик закрытия окна====="""
        self.destroy()
        sys.exit()  # Завершает работу программы

    def scrollbar(self):
        self.scrollbar_frame_1 = ctk.CTkScrollableFrame(self, width=400, height=50,fg_color='black')  # 171717
        self.scrollbar_frame_1.place(x=440, y=220)

    def place_frame(self):
        """=====Создание мини-окон внутри основного окна====="""
        self.frame1 = create_frame(self,200, 100,10,10,"#171717","transparent")
        self.frame2 = create_frame(self, 340, 100, 220, 10, "#171717", "transparent")
        self.frame3 = create_frame(self, 300, 100, 565, 10, "black", "transparent")
        self.frame4 = create_frame(self, 275, 95, 10, 120, "#171717", "transparent")
        self.frame5 = create_frame(self, 275, 95, 290, 120, "#171717", "transparent")
        self.frame6 = create_frame(self, 275, 95, 570, 120, "#171717", "transparent")
        self.frame9 = ctk.CTkFrame(master=self.scrollbar_frame_1, width=395, height=270, fg_color="black",bg_color="transparent")
        self.frame9.grid(row=0, column=0, sticky='w', padx=1, pady=1)
        self.frame7 = create_frame(self.frame9, 265, 150, 2, 2, "#171717", "transparent")
        self.frame8 = create_frame(self.frame9, 120, 150, 270, 2, "#171717", "transparent")
    def place_label(self):
        """=====Создание надписей====="""
        self.label1 = create_label(self.frame1, "Введите пустотную тягу:", 10, 2)
        self.label1 = create_label(self.frame1, "кН", 75, 30)
        self.label2 = create_label_2(self.frame1, "Тогда расход равен:", 10, 50)
        self.label4 = create_label(self.frame2, f"Значение Fотн =: {4.00:.2f} ", 10, 60)
        self.label5 = create_label(self.frame2, "Введите относительную площадь Fкс/Fкр:", 10, 2)
        self.label6 = create_label(self.frame2, "2.00", 10, 30)
        self.label7 = create_label(self.frame2, "6.00", 205, 30)
        self.label8 = create_label(self.frame3, "Для расчета геометрии необходимо двигать", x=3, y=5)
        self.label8 = create_label(self.frame3, "ползунок. Убедитесь, что вы также ввели",x=3, y=30)
        self.label8 = create_label(self.frame3, "значение пустотной тяги в окне слева!",x=3, y=55)
        self.label10 = create_label_2(self.frame4, "", x=5, y=2)
        self.label11 = create_label_2(self.frame4, "", x=5, y=22)
        self.label12 = create_label_2(self.frame4, "", x=5, y=42)
        self.label13 = create_label_2(self.frame4, "", x=5, y=62)
        self.label14 = create_label_2(self.frame5, "", x=5, y=2)
        self.label15 = create_label_2(self.frame5, "", x=5, y=22)
        self.label16 = create_label_2(self.frame5, "", x=5, y=42)
        self.label17 = create_label_2(self.frame5, "", x=5, y=62)
        self.label18 = create_label_2(self.frame6, "", x=5, y=2)
        self.label19 = create_label_2(self.frame6, "", x=5, y=22)
        self.label20 = create_label_2(self.frame6, "", x=5, y=42)
        self.label21 = create_label_2(self.frame6, "", x=5, y=62)
        self.label22 = create_label(self.frame8, f"R_1 = R_ks*{1.00:.2f}", 5, 15)
        self.label23 = create_label(self.frame8, f"R_2 = R_кр*{1.00:.2f}", 5, 60)
        self.label24 = create_label(self.frame8, f"α/2 = {30}°", 5, 105)
        self.label25 = create_label(self.frame7, "0.8", 50, 15)
        self.label26 = create_label(self.frame7, "0.8", 50, 60)
        self.label28 = create_label(self.frame7, "1.2", 235, 15)
        self.label29 = create_label(self.frame7, "1.2", 235, 60)
        self.label31 = create_label(self.frame7, "R_1:", 10, 15)
        self.label32 = create_label(self.frame7, "R_2:", 10, 60)
        self.label33 = create_label(self.frame7, "α/2:", 10, 105)
        self.label34 = create_label(self.frame7, "25", 50, 105)
        self.label28 = create_label(self.frame7, "40", 235, 105)
        self.label28 = create_label(self.frame9, "", 10, 165)
        self.label29 = create_label(self.frame9, "", 10, 195)

    def place_entry(self):
        """=====Создание строки для ввода пустотной тяги====="""
        self.entry1_value = ctk.StringVar()
        self.Entry1 = create_entry(self.frame1, 60, self.entry1_value, 10, 30)
    def place_button(self):
        """=====Создание кнопок====="""
        self.back_button = create_button(self, "Назад", lambda: self.back_window(), self.font1, 90, 650, 450)
        self.close_button = create_button(self, "Далее", lambda: self.close_window(), self.font1, 100, 750, 450)
    def print_true_nozzle(self):
        """=====Проверка на возможность спроектировать радиусное сопло====="""
        if self.R_1 is None:
            self.R_1=self.R_ks*1.00
        if self.R_2 is None:
            self.R_2=self.R_kp*1.00
        if self.alpha_rad_kon is None:
            self.alpha_rad_kon=30
        self.blr,self.aar=est_li_soplo_rk(self.R_ks,self.R_kp,self.R_1,self.R_2,self.alpha_rad_kon)
        self.sav= est_li_soplo_rr(self.R_ks, self.R_kp, self.R_1, self.R_2)
        self.label28.configure(text=f"{self.blr}")
        self.label29.configure(text=f"Радусное сопло можно спроектировать под углом,\nравным {round(self.sav,2)}°")
    def show_qm(self):
        """=====Проверка на возможность вывода основных размеров====="""
        if self.P is not None and self.kost is not None:
            self.F_otn_1 = self.kost
            user.F_otn_1=self.F_otn_1
            self.options_geomerty()
    def options_geomerty(self):
        """=====Вывод размеров в 3-ёх основных точках ====="""
        self.F_kp = self.F_kp_otn * self.m_sum
        self.F_ks=self.F_kp*self.F_otn_1
        user.F_kp = self.F_kp
        user.F_ks = self.F_ks
        self.F_a = self.F_a_otn* self.m_sum
        self.D_ks =(4*self.F_ks*1000000/3.1415926535898)**(0.5)
        self.R_ks =0.5*self.D_ks
        user.Rad_ks = self.R_ks
        self.D_kp =(4*self.F_kp*1000000/3.1415926535898)**(0.5)
        self.R_kp =0.5*self.D_kp
        user.Rad_kp = self.R_kp
        self.D_a =(4*self.F_a*1000000/3.1415926535898)**(0.5)
        self.R_a =0.5*self.D_a
        user.Rad_a=self.R_a
        user.F_a=self.F_a

        self.label10.configure(text=f'В камере сгорания:')
        self.label11.configure(text=f'F_кс = {f"{self.F_ks*1000000:.2f}"} мм2')
        self.label12.configure(text=f'D_кс = {f"{self.D_ks:.2f}"} мм')
        self.label13.configure(text=f'R_кс = {f"{self.R_ks:.2f}"} мм')
        self.label14.configure(text=f'В критическом сечении:')
        self.label15.configure(text=f'F_kp = {f"{self.F_kp*1000000:.2f}"} мм2')
        self.label16.configure(text=f'D_кр = {f"{self.D_kp:.2f}"} мм')
        self.label17.configure(text=f'R_кр = {f"{self.R_kp:.2f}"} мм')
        self.label18.configure(text=f'На срезе сопла:')
        self.label19.configure(text=f'F_a = {f"{self.F_a*1000000:.2f}"} мм2')
        self.label20.configure(text=f'D_a = {f"{self.D_a:.2f}"} мм')
        self.label21.configure(text=f'R_a = {f"{self.R_a:.2f}"} мм')
    def show_thrust(self):
        """=====Вывод массового расхода====="""
        self.P=float(self.entry1_value.get())
        user.P=self.P*1000
        self.m_sum=(self.P*1000)/self.I_a
        user.m_sum=self.m_sum
        if self.label3:
            self.label3.configure(text=f'{f"{self.m_sum:.2f}"} кг/с')
        else:
            self.label3 = create_label_2(self.frame1, f'{f"{self.m_sum:.2f}"} кг/с', 10, 70)
    def place_slider(self):
        """=====Создание слайдеров с выбором радиусов====="""
        self.slider = ctk.CTkSlider(self.frame2, from_=2, to=6,command=self.on_slider_change,number_of_steps=80,border_width=4, width=150, height=15,fg_color=("#474747"),progress_color=("#0094FF"))
        self.slider.place(x=50,y=35)
        self.slider.set(4)
        self.slider_1 = ctk.CTkSlider(self.frame7, from_=0.8, to=1.2, command=self.on_slider_change_1, number_of_steps=40,border_width=4, width=150, height=15, fg_color=("#474747"),progress_color=("#0094FF"))
        self.slider_1.place(x=80, y=22)
        self.slider_1.set(1.0)
        self.slider_2 = ctk.CTkSlider(self.frame7, from_=0.8, to=1.2, command=self.on_slider_change_2, number_of_steps=40,border_width=4, width=150, height=15, fg_color=("#474747"),progress_color=("#0094FF"))
        self.slider_2.place(x=80, y=67)
        self.slider_2.set(1.0)
        self.slider_3 = ctk.CTkSlider(self.frame7, from_=25, to=40, command=self.on_slider_change_3,number_of_steps=15, border_width=4, width=150, height=15, fg_color=("#474747"),progress_color=("#0094FF"))
        self.slider_3.place(x=80, y=112)
        self.slider_3.set(30)
    def print_soplo(self):
        """=====Отрисовка изображения из методички Дорофеева====="""
        self.original_image = Image.open("data/soplo.png")  # Путь к изображению
        self.resized_image = self.original_image.resize((round(426*1.50), round(210*1.50)), Image.Resampling.LANCZOS)
        self.global_image = ImageTk.PhotoImage(self.resized_image)
        self.image_label = ctk.CTkLabel(self, image=self.global_image)
        self.image_label.place(x=10, y=240)
        self.image_label.configure(text="")
    def on_slider_change(self, value):
        """=====Обновлении информации при изменении положения ползунка, связанного с площадью====="""
        self.label4.configure(text=f"Значение Fотн =: {value:.2f}")
        self.kost=value
        self.show_thrust()
        self.show_qm()
        self.print_true_nozzle()
    def on_slider_change_1(self, value):
        """=====Обновлении информации при изменении положения ползунка №1====="""
        self.label22.configure(text=f"R_1 = R_ks*{value:.2f}")
        self.kost_1=value
        self.R_1=self.R_ks*self.kost_1
        self.print_true_nozzle()
    def on_slider_change_2(self, value):
        """=====Обновлении информации при изменении положения ползунка №2====="""
        self.label23.configure(text=f"R_2 = R_кр*{value:.2f}")
        self.kost_2=value
        self.R_2 = self.R_kp * self.kost_2
        self.print_true_nozzle()
    def on_slider_change_3(self, value):
        """=====Обновлении информации при изменении положения ползунка №3====="""
        self.label24.configure(text=f"α/2 = {value}°")
        self.kost_3=value
        self.alpha_rad_kon=self.kost_3
        self.print_true_nozzle()
    def back_window(self):
        """=====Переход к предыдущему окну====="""
        self.destroy()

        user.F_otn_1 = None
        user.F_kp = None
        user.F_ks = None
        user.Rad_ks = None
        user.Rad_kp = None
        user.Rad_a = None
        user.F_a = None
        user.P = None
        user.m_sum = None
        user.R_1_0 = None
        user.R_2_0 = None
        user.alpha_suzh_0 = None

        third_window = ThirdWindow(user.formula_ox, user.formula_gor, float(user.p_k), float(user.p_a), user.alpha, float(user.alpha_value),
                                   user.selected_option, user.H_gor, user.H_ok, user.alpha_itog, user.choice)
        third_window.mainloop()
    def close_window(self):
        """=====Переход к следующему окну====="""
        self.destroy()
        user.R_1_0=self.kost_1
        user.R_2_0=self.kost_2
        user.alpha_suzh_0=self.kost_3
        user.R_1=self.R_1
        user.R_2=self.R_2
        user.Rad_ks=self.R_ks
        user.Rad_kp=self.R_kp
        user.alpha_rad_kon=self.alpha_rad_kon
        user.aar=self.aar
        nozzle_subsonic_window = SubsonicWindow(self.R_1,self.R_2, self.R_ks,self.R_kp,self.alpha_rad_kon,self.aar)
        nozzle_subsonic_window.mainloop()
class SubsonicWindow(ctk.CTk):
    """----------------------------Окно с отрисовкой сужающейся части----------------------------"""
    def __init__(self, R_1,R_2,R_ks,R_kp,alpha_rad_kon,aar):
        """=====Начальные значения атрибутов класса====="""
        super().__init__()
        self.R_1 = R_1
        self.R_2 = R_2
        self.R_ks = R_ks
        self.R_kp = R_kp
        self.alpha_rad_kon=alpha_rad_kon
        self.kolvo=aar

        self.font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 1
        self.font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 2

        self.title("Дозвуковая часть сопла")  # Название программы
        self.resizable(False, False)  # Запрет изменения размера окна

        screen_width = self.winfo_screenwidth()  # Устанавливаем размер и позицию окна
        screen_height = self.winfo_screenheight()
        window_width = 1305
        window_height = 734
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        ctk.set_appearance_mode("Dark")  # Настройка темы
        ctk.set_default_color_theme("blue")  # Цветовая палитра
        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов
        self.iconbitmap('data/wings_4.ico')
        self.scrollbar_0()

        if self.kolvo==1:
            self.place_frame_1()
            self.scrollbar_1()
            self.place_label_1()
            self.place_button_1()
            self.print_subsonic_nozzle_rr()
        else:
            self.place_frame_2()
            self.scrollbar_2()
            self.place_label_2()
            self.place_button_2()
            self.setup_radio()
            self.print_subsonic_nozzle_rk()
            self.print_subsonic_nozzle_rr()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """=====Действие при нажатии на крестик закрытия окна====="""
        self.destroy()
        sys.exit()  # Завершает работу программы
    def scrollbar_0(self):
        """=====Создание прокручиващегося фрейма в окне====="""
        self.scrollbar_frame_0 = ctk.CTkScrollableFrame(self, width=835, height=468,fg_color='#171717')  # 171717
        self.scrollbar_frame_0.place(x=2, y=2)
    def place_frame_1(self):
        """=====Создание окна в в фрейме====="""
        self.frame0 = ctk.CTkFrame(master=self.scrollbar_frame_0, width=830, height=500, fg_color="#171717",bg_color="transparent")
        self.frame0.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    def place_frame_2(self):
        """=====Создание окна в в фрейме====="""
        self.frame0 = ctk.CTkFrame(master=self.scrollbar_frame_0, width=830, height=1085, fg_color="#171717",bg_color="transparent")
        self.frame0.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    def scrollbar_1(self):
        """=====Создание небольшого прокручиващегося фрейма в окне====="""
        self.scrollbar_frame_1 = ctk.CTkScrollableFrame(self.frame0, width=200, height=200,fg_color='black')  # 171717
        self.scrollbar_frame_1.place(x=2, y=60)
    def scrollbar_2(self):
        """=====Создание небольшого прокручиващегося фрейма в окне====="""
        self.scrollbar_frame_1 = ctk.CTkScrollableFrame(self.frame0, width=200, height=200,fg_color='black')  # 171717
        self.scrollbar_frame_1.place(x=2, y=60)
        self.scrollbar_frame_2 = ctk.CTkScrollableFrame(self.frame0, width=200, height=200, fg_color='black')  # 171717
        self.scrollbar_frame_2.place(x=2, y=565)
    def place_label_1(self):
        """=====Создание надписей (вариант 1)====="""
        self.options_rr,self.V_suzh_rr=print_options_rr(self.R_1,self.R_2, self.R_ks,self.R_kp)
        self.label1 = ctk.CTkLabel(self.scrollbar_frame_1, text=self.options_rr, font=font1,justify='left')
        self.label1.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.label2 = create_label_0(self.frame0, "Радиусное сопло", 350, 5)
        self.label3=create_label(self.frame0,"Геометричесчкие параметры:",10,30)
    def place_label_2(self):
        """=====Создание надписей (вариант 2)====="""
        self.options_rr,self.V_suzh_rr = print_options_rr(self.R_1, self.R_2, self.R_ks, self.R_kp)
        self.options_rk,self.V_suzh_rk = print_options_rk(self.R_1, self.R_2, self.R_ks, self.R_kp,self.alpha_rad_kon)
        self.label1 = ctk.CTkLabel(self.scrollbar_frame_1, text=self.options_rr, font=font1,justify='left')
        self.label1.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.label2 = ctk.CTkLabel(self.scrollbar_frame_2, text=self.options_rk, font=font1, justify='left')
        self.label2.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.label2 = create_label_0(self.frame0, "Радиусное сопло", 350, 5)
        self.label3 = create_label(self.frame0, "Геометричесчкие параметры:", 10, 30)
        self.label4 = create_label_0(self.frame0, "Радиусно-коническое сопло", 350, 510)
        self.label5 = create_label(self.frame0, "Геометричесчкие параметры:", 10, 535)
        self.label6 = create_label(self.frame0, "Какая сужающаяся часть будет использоваться?", 220, 1030)
    def place_button_1(self):
        """=====Создание кнопок (вариант 1)====="""
        self.back_button = create_button(self.frame0, "Назад", lambda: self.back_window(), self.font1, 80, 20, 420)
        self.close_button = create_button(self.frame0, "Далее", lambda: self.close_window(), self.font1, 80, 20, 450)
        self.button1 = create_button(self.frame0, "Сохранить параметры в txt", lambda: save_properties_txt(self.options_rr), self.font1,250, 2, 285)
        self.button2 = create_button(self.frame0, "Сохранить сопло в excel", lambda: save_to_excel(self.x_rr,self.y_rr,"X","Y"), self.font1,250, 2, 315)
        self.button3 = create_button(self.frame0, "Сохранить сопло в txt",lambda: save_to_txt(self.x_rr,self.y_rr), self.font1, 250,2, 345)
    def place_button_2(self):
        """=====Создание кнопок (вариант 2)====="""
        self.back_button = create_button(self.frame0, "Назад", lambda: self.back_window(), self.font1, 80, 750, 1020)
        self.close_button = create_button(self.frame0, "Далее", lambda: self.close_window(), self.font1, 80, 750, 1050)
        self.button1 = create_button(self.frame0, "Сохранить параметры в txt",lambda: save_properties_txt(self.options_rr), self.font1,250, 2, 285)
        self.button2 = create_button(self.frame0, "Сохранить сопло в excel", lambda: save_to_excel(self.x_rr,self.y_rr,"X","Y"), self.font1,250, 2, 315)
        self.button3 = create_button(self.frame0, "Сохранить сопло в txt", lambda:save_to_txt(self.x_rr,self.y_rr), self.font1, 250,2, 345)
        self.button4 = create_button(self.frame0, "Сохранить параметры в txt", lambda: save_properties_txt(self.options_rk), self.font1,250, 2, 790)
        self.button5 = create_button(self.frame0, "Сохранить сопло в excel", lambda: save_to_excel(self.x_rk,self.y_rk,"X","Y"), self.font1,250, 2, 820)
        self.button6 = create_button(self.frame0, "Сохранить сопло в txt",lambda:save_to_txt(self.x_rk,self.y_rk), self.font1, 250,2, 850)
    def print_subsonic_nozzle_rk(self):
        """=====Отрисовка радиусно-конического сопла====="""
        self.x_rk,self.y_rk=place_subsonic_nozzle_rk(self.R_ks, self.R_kp,self.R_1, self.R_2,self.alpha_rad_kon,self.frame0)
    def print_subsonic_nozzle_rr(self):
        """=====Отрисовка радиусного сопла====="""
        self.x_rr,self.y_rr=place_subsonic_nozzle_rr(self.R_ks, self.R_kp,self.R_1, self.R_2,self.frame0)
        if self.kolvo==1:
            self.x_suzh = self.x_rr
            self.y_suzh = self.y_rr
            self.V_suzh = self.V_suzh_rr
    def setup_radio(self):
        """=====Создание радио-кнопок выбора типа сужающегося сопла====="""
        self.radio_var = ctk.IntVar()

        self.radio_option1 = ctk.CTkRadioButton(self.frame0, text="Радиусная", variable=self.radio_var,command=self.on_radio_button_clicked,value=1)
        self.radio_option2 = ctk.CTkRadioButton(self.frame0, text="Радиусно-коническая", variable=self.radio_var,command=self.on_radio_button_clicked, value=2)

        self.radio_option1.place(x=550, y=1020)
        self.radio_option2.place(x=550, y=1050)
    def on_radio_button_clicked(self):
        """=====Сохранение и последующий расчет при выборе определённого типа сужающегося сопла====="""
        if self.radio_var.get() == 1:  # Если выбрана первая радиокнопка
            self.x_suzh=self.x_rr
            self.y_suzh = self.y_rr
            self.V_suzh=self.V_suzh_rr
            user.V_suzh = self.V_suzh
            user.type_suzh=1

        elif self.radio_var.get() == 2:  # Если выбрана вторая радиокнопка
            self.x_suzh = self.x_rk
            self.y_suzh = self.y_rk
            self.V_suzh = self.V_suzh_rk
            user.V_suzh=self.V_suzh
            user.type_suzh = 2
    def back_window(self):
        """=====Переход в предыдущее окно====="""
        self.destroy()
        user.V_suzh = None
        user.type_suzh = None
        nozzle_window = NozzleWindow(user.I_a, user.F_kp, user.F_a, float(user.p_k))
        nozzle_window.mainloop()
    def close_window(self):
        """=====Переход в следующее окно====="""
        self.p_k=user.p_k
        self.R_k =user.R_k
        self.T_k=user.T_k
        self.m_sum =user.m_sum
        self.F_ks = user.F_ks
        self.F_kp = user.F_kp
        self.B = user.B
        user.x_suzh = self.x_suzh
        user.y_suzh = self.y_suzh
        self.destroy()
        combustion_chamber_window = CombustionChamberWindow(self.p_k,self.R_k,self.T_k,self.m_sum,self.V_suzh,self.x_suzh, self.y_suzh,self.F_ks,self.F_kp,self.B)
        combustion_chamber_window.mainloop()
class CombustionChamberWindow(ctk.CTk):
    """----------------------------Окно с выбором времени пребывания для построения КС----------------------------"""
    def __init__(self, p_k,R_k,T_k,m_sum,V_suzh,x_suzh,y_suzh,F_ks,F_kp,B):
        """=====Начальные значения атрибутов класса====="""
        super().__init__()
        self.p_k = p_k
        self.R_k = R_k
        self.T_k = T_k
        self.m_sum = m_sum
        self.V_suzh=V_suzh
        self.x_suzh=x_suzh
        self.y_suzh = y_suzh
        self.F_ks=F_ks
        self.F_kp=F_kp
        self.B=B


        self.font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 1
        self.font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 2

        self.title("Камера сгорания")  # Название программы
        self.resizable(False, False)  # Запрет изменения размера окна
        self.iconbitmap('data/wings_4.ico')
        screen_width = self.winfo_screenwidth()  # Устанавливаем размер и позицию окна
        screen_height = self.winfo_screenheight()
        window_width = 1305
        window_height = 734
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        ctk.set_appearance_mode("Dark")  # Настройка темы
        ctk.set_default_color_theme("blue")  # Цветовая палитра
        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов

        self.place_scrollbar()
        self.place_frame()
        self.place_button()
        self.print_engine()
        self.place_label()
        self.print_entry()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """=====Действие при нажатии на крестик закрытия окна====="""
        self.destroy()
        sys.exit()  # Завершает работу программы
    def place_scrollbar(self):
        """=====Создание прокручивающегося фрейма в окне====="""
        self.scrollbar_frame_0 = ctk.CTkScrollableFrame(self, width=835, height=468,fg_color='#171717')  # 171717
        self.scrollbar_frame_0.place(x=2, y=2)
    def place_frame(self):
        """=====Создание полотна в фрейме====="""
        self.frame0 = ctk.CTkFrame(master=self.scrollbar_frame_0, width=830, height=1085, fg_color="#171717",bg_color="transparent")
        self.frame0.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    def print_engine(self):
        """=====Отрисовка изображения====="""
        self.original_image = Image.open("data/tau_pr.png")  # Путь к изображению
        self.resized_image = self.original_image.resize((round(524*2.35), round(214*2.35)), Image.Resampling.LANCZOS)
        self.global_image = ImageTk.PhotoImage(self.resized_image)
        self.image_label = ctk.CTkLabel(self.frame0, image=self.global_image)
        self.image_label.place(x=2, y=2)
        self.image_label.configure(text="")
    def print_entry(self):
        """=====Создание строки для ввода времени пребывания====="""
        self.entry1_value = ctk.StringVar()
        self.Entry1 = create_entry(self.frame0, 60, self.entry1_value, 320, 340)

    def enter_change(self):
        """=====Расчёт и вывод характеристических параметров камеры сгорания====="""
        # Обновление текста метки в соответствии со значением ползунка
        self.tau_pr=float(self.entry1_value.get())
        self.label1.configure(text=f"Условное время пребывания: {self.tau_pr:.2f} мс")
        self.L_ks=1000*(((self.tau_pr*0.001*self.R_k*self.T_k*self.F_kp)/self.B)-self.V_suzh)/self.F_ks
        self.label4.configure(text=f"Длина камеры сгорания: {self.L_ks:.2f} мм")
        self.l_pr=math.pi*(self.R_k**2)*self.L_ks*(10**(-9))/self.F_kp
        self.label5.configure(text=f"Приведённая (характеристическая) длина: {self.l_pr:.2f} м")
        self.x_dozv,self.y_dozv=print_Combustion_Chamber(self.x_suzh,self.y_suzh,self.frame0,self.L_ks)
        user.tau_pr=self.tau_pr
        user.l_pr=self.l_pr
    def place_label(self):
        """=====Создание надписей====="""
        self.label = create_label_0(self.frame0, "Введите условное время пребывания (мс):", 10, 340)
        self.label1 = create_label_0(self.frame0, f"Условное время пребывания:", 10, 365)
        self.label4 = create_label_0(self.frame0, f"Длина камеры сгорания:", 10, 390)
        self.label5 = create_label_0(self.frame0, f"Приведённая (характеристическая) длина:", 10, 415)
    def place_button(self):
        """=====Создание кнопок====="""
        self.back_button = create_button(self.frame0, "Назад", lambda: self.back_window(), self.font1, 80, 750, 1020)
        self.close_button = create_button(self.frame0, "Далее", lambda: self.close_window(), self.font1, 80, 750, 1050)
        self.enter_button = create_button(self.frame0, "Ввод", lambda: self.enter_change(), self.font1, 80, 390, 340)
    def back_window(self):
        """=====Переход в предыдущее окно====="""
        self.destroy()
        user.L_ks = None
        user.teta_a = None
        user.tau_pr=None
        user.l_pr = None
        nozzle_subsonic_window = SubsonicWindow(user.R_1, user.R_2, user.Rad_ks, user.Rad_kp, user.alpha_rad_kon, user.aar)
        nozzle_subsonic_window.mainloop()
    def close_window(self):
        """=====Переход в следующее окно====="""
        self.teta_a=find_teta_a(float(user.p_a),float(user.p_k))
        # self.teta_m = find_teta_m(float(user.w_a),float(user.T_kp),float(user.R_kp),float(user.k_a),float(user.k_kp))
        self.Rad_kp=user.Rad_kp
        self.Rad_a=user.Rad_a
        self.teta_m, self.l_ras_otn = find_teta_m_1(self.Rad_a / self.Rad_kp, float(user.k_a), self.teta_a)
        user.teta_a = self.teta_a
        user.L_ks = self.L_ks
        user.teta_m=self.teta_m
        user.x_dozv=self.x_dozv
        user.y_dozv=self.y_dozv
        self.destroy()
        nozzle_laval_window = LavalWindow(self.teta_a,self.teta_m,self.Rad_kp,self.Rad_a,self.x_dozv,self.y_dozv,self.L_ks,self.l_ras_otn)
        nozzle_laval_window.mainloop()
class LavalWindow(ctk.CTk):
    """----------------------------Окно с отрисовкой профилированного сопла Лаваля----------------------------"""
    def __init__(self, teta_a,teta_m,Rad_kp,Rad_a,x_dozv,y_dozv,L_ks,l_ras_otn):
        """=====Начальные значения атрибутов класса====="""
        super().__init__()
        self.teta_a=teta_a
        self.teta_m=teta_m
        self.Rad_kp=Rad_kp
        self.Rad_a=Rad_a
        self.x_dozv=x_dozv
        self.y_dozv=y_dozv
        self.L_ks=L_ks
        self.l_ras_otn=l_ras_otn

        self.font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 1
        self.font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 2

        self.title("Расщиряющаяся часть сопла. Сопло Лаваля")  # Название программы
        self.resizable(False, False)  # Запрет изменения размера окна
        self.iconbitmap('data/wings_4.ico')
        screen_width = self.winfo_screenwidth()  # Устанавливаем размер и позицию окна
        screen_height = self.winfo_screenheight()
        window_width = 1305
        window_height = 734
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        ctk.set_appearance_mode("Dark")  # Настройка темы
        ctk.set_default_color_theme("blue")
        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов

        self.place_scrollbar()
        self.place_frame()
        self.place_button()
        self.a_kp=math.sqrt(user.k_kp*user.R_kp*user.T_kp)
        self.lambda_a=user.w_a/self.a_kp
        user.lambda_a=self.lambda_a
        self.beta=self.teta_m
        self.L_sv=self.l_ras_otn*user.Rad_kp
        self.x_total, self.y_total,self.x_sv,self.y_sv=plot_nozzle_laval(self.Rad_kp, self.Rad_a, np.rad2deg(self.beta), self.teta_a, self.frame0,self.x_dozv,self.y_dozv,self.L_ks,self.L_sv)
        user.x_sv=self.x_sv
        user.y_sv =self.y_sv
        user.x_total=self.x_total
        user.y_total = self.y_total
        self.place_label()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def on_closing(self):
        """=====Действие при нажатии на крестик закрытия окна====="""
        self.destroy()
        sys.exit()  # Завершает работу программы

    def place_scrollbar(self):
        """=====Создание прокручивающегося фрейма в окне====="""
        self.scrollbar_frame_0 = ctk.CTkScrollableFrame(self, width=835, height=468,fg_color='#171717')  # 171717
        self.scrollbar_frame_0.place(x=2, y=2)
    def place_frame(self):
        """=====Создание полотна в фрейме====="""
        self.frame0 = ctk.CTkFrame(master=self.scrollbar_frame_0, width=830, height=910, fg_color="#171717",bg_color="transparent")
        self.frame0.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    def place_label(self):
        """=====Создание надписей====="""
        self.label = create_label_0(self.frame0, "Проектирование сопла прошло успешно, поздравляем!", 100, 10)
        self.label_1 = create_label_0(self.frame0, f"β_m={np.rad2deg(self.beta):.2f}°", 10, 840)
        self.label_2 = create_label_0(self.frame0, f"β_a={self.teta_a:.2f}°", 10, 870)
        self.label_3 = create_label_0(self.frame0, f"Относит. длина расш. части равна: {self.l_ras_otn:.2f} мм.", 150, 840)
        self.label_4 = create_label_0(self.frame0, f"Длина расш. части равна: {self.x_total[-1]:.2f} мм.", 150, 870)
    def place_button(self):
        """=====Создание кнопок====="""
        self.save_nozzle = create_button(self.frame0, "Сохранить в excel",
                                         lambda: save_to_excel(self.x_total, self.y_total,"X","R"), self.font1, 100, 500,
                                         840)
        self.save_nozzle_txt = create_button(self.frame0, "Сохранить в txt",
                                             lambda: save_to_txt(self.x_total, self.y_total), self.font1, 100,
                                             500, 870)
        self.back_button = create_button(self.frame0, "Назад", lambda: self.back_window(), self.font1, 80, 750, 840)
        self.close_button = create_button(self.frame0, "Далее", lambda: self.close_window(), self.font1, 80, 750, 870)
    def back_window(self):
        """=====Переход в предыдущее окно====="""
        self.destroy()
        user.x_sv = None
        user.y_sv = None
        user.lambda_a = None
        user.x_total = None
        user.y_total = None
        combustion_chamber_window = CombustionChamberWindow(float(user.p_k), user.R_k, user.T_k, user.m_sum, user.V_suzh,
                                                            user.x_suzh, user.y_suzh, user.F_ks, user.F_kp, user.B)
        combustion_chamber_window.mainloop()

    def close_window(self):
        """=====Переход в следующее окно====="""
        self.destroy()
        Graph_po_dline = GraphWindow(user.oxigen, user.fuel, user.p_k, user.p_a, user.alpha_itog, user.alpha_value,
                                     user.selected_option, user.formula_gor, user.formula_ox, user.H_gor, user.H_ok,user.p_kp)
        Graph_po_dline.mainloop()
class GraphWindow(ctk.CTk):
    """----------------------------Окно с выводом всех основных параметров по длине сопла----------------------------"""
    def __init__(self,oxigen,fuel,p_k, p_a, alpha_itog, alpha_value,selected_option,formula_gor,formula_ox,H_gor,H_ok,p_kp):
        """=====Начальные значения атрибутов класса====="""
        super().__init__()
        self.p_k = float(p_k)
        self.p_a = float(p_a)
        self.oxigen = oxigen
        self.fuel = fuel
        self.alpha_itog = alpha_itog
        self.alpha_value = alpha_value
        self.selected_option = selected_option
        self.formula_gor = formula_gor
        self.formula_ox = formula_ox
        self.H_gor = float(H_gor)
        self.H_ok = float(H_ok)
        self.p_kp=float(p_kp)
        self.x_suzh = user.x_suzh
        self.y_suzh = user.y_suzh
        self.x_sv = user.x_sv
        self.y_sv = user.y_sv
        self.x_dzv = []
        self.x_svzv = []

        self.font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 1
        self.font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 2

        self.title("Изменение параметров по длине сопла")  # Название программы
        self.resizable(False, False)  # Запрет изменения размера окна
        self.iconbitmap('data/wings_4.ico')
        screen_width = self.winfo_screenwidth()  # Устанавливаем размер и позицию окна
        screen_height = self.winfo_screenheight()
        window_width = 1305
        window_height = 734
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        ctk.set_appearance_mode("Dark")  # Настройка темы
        ctk.set_default_color_theme("blue")  # Цветовая палитра
        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов

        self.slice_p()
        self.place_scrollbar()
        self.place_frame()
        self.calculation_dozv()
        self.place_button()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """=====Действие при нажатии на крестик закрытия окна====="""
        self.destroy()
        sys.exit()  # Завершает работу программы
    def slice_p(self):
        """=====Деление массива даления на точки для построения графиков====="""
        self.p_dozv_array_0 = np.linspace(self.p_k, (self.p_k+self.p_kp)*0.5, 10)
        self.p_dozv_array = np.linspace((self.p_k+self.p_kp)*0.5, self.p_kp, 10)
        self.p_cverhzv_array = np.geomspace(self.p_kp, self.p_a, 50)
    def place_scrollbar(self):
        """=====Создание прокручивающегося фрейма в окне====="""
        self.scrollbar_frame_0 = ctk.CTkScrollableFrame(self, width=835, height=468,fg_color='#171717')  # 171717
        self.scrollbar_frame_0.place(x=2, y=2)

    def place_frame(self):
        """=====Создание полотна в фрейме====="""
        self.frame0 = ctk.CTkFrame(master=self.scrollbar_frame_0, width=830, height=3300, fg_color="#171717",bg_color="transparent")
        self.frame0.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    def place_button(self):
        """=====Создание кнопок====="""
        self.back_button = create_button(self.frame0, "Назад", lambda: self.back_window(), self.font1, 80, 735, 3220)
        self.close_button = create_button(self.frame0, "Далее", lambda: self.close_window(), self.font1, 80, 735, 3250)
        self.save_exel_1 = create_button(self.frame0, "Excel",lambda: save_to_excel(self.x_graph, self.p_graph,"X","Y"), self.font1, 70,660, 390)
        self.save_exel_2 = create_button(self.frame0, "Excel",lambda: save_to_excel(self.x_graph, self.T_array,"X","Y"), self.font1, 70, 660,850)
        self.save_exel_3 = create_button(self.frame0, "Excel",lambda: save_to_excel(self.x_graph, self.rho_array,"X","Y"), self.font1, 70, 660,1330)
        self.save_exel_4 = create_button(self.frame0, "Excel",lambda: save_to_excel(self.x_graph, self.w_array,"X","Y"), self.font1, 70, 660,1800)
        self.save_exel_5 = create_button(self.frame0, "Excel",lambda: save_to_excel(self.x_graph, self.M_array,"X","Y"), self.font1, 70, 660,2260)
        self.save_exel_6 = create_button(self.frame0, "Excel",lambda: save_to_excel(self.x_graph, self.labda_w,"X","Y"), self.font1, 70, 660,2740)
        self.save_exel_7 = create_button(self.frame0, "Excel",lambda: save_to_excel(self.x_graph, self.rw,"X","Y"), self.font1, 70, 660,3200)

        self.save_txt_1 = create_button(self.frame0, "txt", lambda: save_to_txt(self.x_graph, self.p_graph),self.font1, 40, 675, 420)
        self.save_txt_2 = create_button(self.frame0, "txt", lambda: save_to_txt(self.x_graph, self.T_array),self.font1, 40, 675, 880)
        self.save_txt_3 = create_button(self.frame0, "txt", lambda: save_to_txt(self.x_graph, self.rho_array),self.font1, 40, 675, 1360)
        self.save_txt_4 = create_button(self.frame0, "txt", lambda: save_to_txt(self.x_graph, self.w_array),self.font1, 40, 675, 1830)
        self.save_txt_5 = create_button(self.frame0, "txt", lambda: save_to_txt(self.x_graph, self.M_array),self.font1, 40, 675, 2290)
        self.save_txt_6 = create_button(self.frame0, "txt", lambda: save_to_txt(self.x_graph, self.labda_w),self.font1, 40, 675, 2770)
        self.save_txt_7 = create_button(self.frame0, "txt", lambda: save_to_txt(self.x_graph, self.rw),self.font1, 40, 675, 3230)
    def calculation_dozv(self):
        """=====Расчёт основных параметров в дозвуковой и сверхзвуковой частях и отображение графиков====="""
        self.T_dozv_array_0, self.rho_dozv_array_0, self.R_dozv_array_0, self.k_dozv_array_0, self.w_dozv_array_0, self.F_dozv_array_0 = raschet_dozv(
            self.alpha_value, self.alpha_itog, self.H_gor, self.H_ok, self.formula_gor, self.formula_ox, self.p_k,
            self.selected_option, self.p_dozv_array_0)
        self.T_dozv_array,self.rho_dozv_array,self.R_dozv_array,self.k_dozv_array,self.w_dozv_array,self.F_dozv_array=raschet_dozv(self.alpha_value,self.alpha_itog,self.H_gor,self.H_ok,self.formula_gor,self.formula_ox,self.p_k,self.selected_option,self.p_dozv_array) #k0,alpha,H_gor,H_ok,fuel,oxidizer,p_k,choice,p_array
        self.T_sv_array, self.rho_sv_array, self.R_sv_array, self.k_sv_array, self.w_sv_array, self.F_sv_array = raschet_dozv(self.alpha_value, self.alpha_itog, self.H_gor, self.H_ok, self.formula_gor, self.formula_ox, self.p_k,self.selected_option, self.p_cverhzv_array)
        self.w_dozv_array_0[0]=0
        self.F_dozv_array_0[0]=user.F_ks/user.m_sum
        self.r_dozv_0 = []
        self.r_dozv = []
        self.r_sv = []
        for F in self.F_dozv_array_0:
            self.r_dozv_0.append(((4*user.m_sum*F/(math.pi))**0.5)*1000/2)
        for F in self.F_dozv_array:
            self.r_dozv.append(((4 * F*user.m_sum / (math.pi)) ** 0.5)*1000/2)
        for F in self.F_sv_array:
            self.r_sv.append(((4 * F*user.m_sum / (math.pi)) ** 0.5)*1000/2)
        self.T_dozv=np.concatenate((self.T_dozv_array_0, self.T_dozv_array))
        self.rho_dozv=np.concatenate((self.rho_dozv_array_0, self.rho_dozv_array))
        self.R_dozv=np.concatenate((self.R_dozv_array_0, self.R_dozv_array))
        self.k_dozv=np.concatenate((self.k_dozv_array_0, self.k_dozv_array))
        self.w_dozv=np.concatenate((self.w_dozv_array_0, self.w_dozv_array))
        self.F_dozv = np.concatenate((self.F_dozv_array_0, self.F_dozv_array))
        self.r_dzv = np.concatenate((self.r_dozv_0, self.r_dozv))

        self.M_dozv=[]
        self.M_sv = []
        for R,T,k,w in zip(self.T_dozv, self.R_dozv,self.k_dozv,self.w_dozv):
            self.M_dozv.append(w/((R*T*k)**0.5))
        for R,T,k,w in zip(self.T_sv_array, self.R_sv_array,self.k_sv_array,self.w_sv_array):
            self.M_sv.append(w/((R*T*k)**0.5))
        self.T_array = np.concatenate((self.T_dozv, self.T_sv_array))
        self.rho_array = np.concatenate((self.rho_dozv, self.rho_sv_array))
        self.R_array = np.concatenate((self.R_dozv, self.R_sv_array))
        self.k_array = np.concatenate((self.k_dozv, self.k_sv_array))
        self.w_array = np.concatenate((self.w_dozv, self.w_sv_array))
        self.F_array = np.concatenate((self.F_dozv, self.F_sv_array))
        self.M_array= np.concatenate((self.M_dozv, self.M_sv))

        self.f=interp1d(user.y_suzh, user.x_suzh, kind='linear') #nearest
        self.f_1 = interp1d(user.y_sv, user.x_sv, kind='linear')
        self.r_dzv[0]=user.y_suzh[0]
        self.r_dzv[-1] = user.y_suzh[-1]
        self.r_sv[0]=self.y_sv[0]
        self.r_sv[-1]=self.y_sv[-1]
        for r in self.r_dzv:
            self.x_dzv.append(self.f(r))
        for r in self.r_sv:
            self.x_svzv.append(self.f_1(r))
        self.x_graph = np.concatenate((self.x_dzv, self.x_svzv))
        self.p_graph_1 = np.concatenate((self.p_dozv_array_0, self.p_dozv_array))
        self.p_graph = np.concatenate((self.p_graph_1, self.p_cverhzv_array))
        self.a_kp=(user.k_kp*user.R_kp*user.T_kp)**0.5
        self.labda_w=[]
        for w in self.w_array:
            self.labda_w.append(w/self.a_kp)
        self.rw=[]
        for r,w in zip(self.rho_array, self.w_array):
            self.rw.append(r*w)
        print_graph_p_x(self.x_graph,self.p_graph,user.L_ks,self.frame0,30,50,"Изменение давления по длине сопла",'х, мм',"p, МПа",9,7)
        print_graph_p_x(self.x_graph,self.T_array,user.L_ks,self.frame0,30,750,"Изменение температуры по длине сопла",'х, мм',"Т, К",9,7)
        print_graph_p_x(self.x_graph,self.rho_array,user.L_ks,self.frame0,30,1450,"Изменение плотности по длине сопла",'х, мм',"rho, кг/м3",9,7)
        print_graph_p_x(self.x_graph,self.w_array,user.L_ks,self.frame0,30,2150,"Изменение скорости по длине сопла",'х, мм',"w, м/с",9,7)
        print_graph_p_x(self.x_graph, self.M_array, user.L_ks, self.frame0, 30, 2850,"Изменение числа Маха по длине сопла", 'х, мм', "М",9,7)
        print_graph_p_x(self.x_graph, self.labda_w, user.L_ks, self.frame0, 30, 3550,"Изменение приведённой скорости по длине сопла", 'х, мм', "lambda",9,7)
        print_graph_p_x(self.x_graph, self.rw, user.L_ks, self.frame0, 30, 4250,"Изменение расходонапряжённости по длине сопла", 'х, мм', "rw, кг/м2с",9,7)
        user.X_graph=self.x_graph
        user.P_graph=self.p_graph
        user.T_graph=self.T_array
        user.Rho_graph=self.rho_array
        user.W_graph=self.w_array
        user.M_graph=self.M_array
        user.Lambda_graph=self.labda_w
        user.RW_graph=self.rw
    def back_window(self):
        """=====Переход в предыдущее окно====="""
        self.destroy()
        user.X_graph = None
        user.P_graph = None
        user.T_graph = None
        user.Rho_graph = None
        user.W_graph = None
        user.M_graph = None
        user.Lambda_graph = None
        user.RW_graph = None
        nozzle_laval_window = LavalWindow(user.teta_a, user.teta_m, user.Rad_kp, user.Rad_a, user.x_dozv, user.y_dozv,user.L_ks)
        nozzle_laval_window.mainloop()
    def close_window(self):
        """=====Переход в следующее окно====="""
        self.destroy()
        user.x_dzv=self.x_dzv
        user.r_dzv = self.r_dzv
        user.T_dozv = self.T_dozv
        user.rho_dozv = self.rho_dozv
        user.R_dozv = self.R_dozv
        user.k_dozv = self.k_dozv
        user.w_dozv = self.w_dozv
        user.F_dozv = self.F_dozv
        user.x_svzv = self.x_svzv
        user.M_dozv = self.M_dozv
        user.r_sv = self.r_sv
        user.T_sv_array = self.T_sv_array
        user.rho_sv_array = self.rho_sv_array
        user.R_sv_array = self.R_sv_array
        user.k_sv_array = self.k_sv_array
        user.w_sv_array = self.w_sv_array
        user.M_sv = self.M_sv
        user.F_sv_array = self.F_sv_array
        Losses_window = LossesWindow(self.x_dzv,self.r_dzv,self.T_dozv,self.rho_dozv,self.R_dozv,self.k_dozv,self.w_dozv,self.F_dozv,self.x_svzv,self.M_dozv,self.r_sv,self.T_sv_array,self.rho_sv_array,self.R_sv_array,self.k_sv_array,self.w_sv_array,self.M_sv,self.F_sv_array)
        Losses_window.mainloop()
class LossesWindow(ctk.CTk):
    """----------------------------Окно, связанное с потерями и коническим соплом----------------------------"""
    def __init__(self,x_dzv,r_dzv,T_dozv,rho_dozv,R_dozv,k_dozv,w_dozv,F_dozv,x_svzv,M_dozv,r_sv,T_sv_array,rho_sv_array,R_sv_array,k_sv_array,w_sv_array,M_sv,F_sv_array):
        """=====Начальные значения атрибутов класса====="""
        super().__init__()

        self.x_dzv=x_dzv
        self.r_dzv=r_dzv
        self.T_dozv=T_dozv
        self.rho_dozv=rho_dozv
        self.R_dozv=R_dozv
        self.k_dozv=k_dozv
        self.w_dozv=w_dozv
        self.x_svzv=x_svzv
        self.M_dozv=M_dozv
        self.r_sv=r_sv
        self.T_sv_array=T_sv_array
        self.rho_sv_array=rho_sv_array
        self.R_sv_array=R_sv_array
        self.k_sv_array=k_sv_array
        self.w_sv_array=w_sv_array
        self.M_sv=M_sv
        self.F_dozv=F_dozv
        self.F_sv_array=F_sv_array

        self.font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 1
        self.font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 2

        self.title("Расчет потерь. Коническое сопло")  # Название программы
        self.resizable(False, False)  # Запрет изменения размера окна
        self.iconbitmap('data/wings_1.ico')
        screen_width = self.winfo_screenwidth()  # Устанавливаем размер и позицию окна
        screen_height = self.winfo_screenheight()
        window_width = 1305
        window_height = 734
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        ctk.set_appearance_mode("Dark")  # Настройка темы
        ctk.set_default_color_theme("blue")  # Цветовая палитра
        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов

        self.place_scrollbar()
        self.place_frame()
        self.poteri_dozvuk()
        self.poteri_sverhzvuk_profil()
        self.poteri_konich()
        self.place_label()
        self.place_button()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """=====Действие при нажатии на крестик закрытия окна====="""
        self.destroy()
        sys.exit()  # Завершает работу программы
    def place_scrollbar(self):
        """=====Создание прокручивающегося фрейма в окне====="""
        self.scrollbar_frame_0 = ctk.CTkScrollableFrame(self, width=835, height=468,fg_color='#171717')  # 171717
        self.scrollbar_frame_0.place(x=2, y=2)
    def place_frame(self):
        """=====Создание мини-окон====="""
        self.frame0 = ctk.CTkFrame(master=self.scrollbar_frame_0, width=830, height=1590, fg_color="#171717",bg_color="transparent")
        self.frame0.grid(row=0, column=0, sticky='w', padx=1, pady=1)
        self.scrollbar_frame_1 = ctk.CTkScrollableFrame(self.frame0, width=650, height=170,fg_color='black')  # 520
        self.scrollbar_frame_1.place(x=2, y=2)
    def place_button(self):
        """=====Создание кнопок====="""
        self.back_button = create_button(self.frame0, "Назад", lambda: self.back_window(), self.font1, 80, 750, 1530)
        self.close_button = create_button(self.frame0, "Дальше", lambda: self.close_window(), self.font1, 80, 750, 1560)
        self.but_save_txt_optoins = create_button(self.frame0, "txt", lambda: save_properties_txt(self.text), self.font1, 80, 700, 190)
        self.but_save_txt_poteri = create_button(self.frame0, "txt", lambda: save_txt_graph_poteri(self.phi_r,self.phi_tr,self.phi_s, self.beta_kon_grad), self.font1, 80, 700, 600)
        self.but_save_excel_poteri = create_button(self.frame0, "excel", lambda: save_excel_graph_poteri(self.phi_r,self.phi_tr,self.phi_s, self.beta_kon_grad), self.font1, 80, 700, 630)
        self.but_save_txt_kon = create_button(self.frame0, "txt", lambda: save_to_txt(self.x_total_kon,self.y_total_kon), self.font1, 80, 20,1530)
        self.but_save_excel_kon = create_button(self.frame0, "excel", lambda: save_to_excel(self.x_total_kon,self.y_total_kon,"X","R"), self.font1, 80,20, 1560)
    def poteri_dozvuk(self):
        """=====Расчёт потерь в дозвуковой части====="""
        self.x_dzv_1=[]
        self.r_dzv_1=[]
        self.rho_dozv_1=[]
        self.w_dozv_1=[]
        self.T_dozv_1=[]
        self.M_dozv_1=[]
        self.k_dozv_1=[]
        self.F_dozv_1=[]
        self.Delta_P_suzh_1 = 0
        for i in range(0,len(self.x_dzv)-1):
            if self.x_dzv[i]!=self.x_dzv[i+1]:
                self.x_dzv_1.append(self.x_dzv[i])
                self.r_dzv_1.append(self.r_dzv[i])
                self.rho_dozv_1.append(self.rho_dozv[i])
                self.w_dozv_1.append(self.w_dozv[i])
                self.T_dozv_1.append(self.T_dozv[i])
                self.M_dozv_1.append(self.M_dozv[i])
                self.k_dozv_1.append(self.k_dozv[i])
                self.F_dozv_1.append(self.F_dozv[i])
        self.beta_j_dozv_1 = find_angle(self.x_dzv_1, self.r_dzv_1)
        self.rho_j_1 = srednee_znachenie(self.rho_dozv_1)
        self.w_j_1 = srednee_znachenie(self.w_dozv_1)
        self.T_j_1 = srednee_znachenie(self.T_dozv_1)
        self.M_j_1 = srednee_znachenie(self.M_dozv_1)
        self.k_j_1 = srednee_znachenie(self.k_dozv_1)
        self.F_j_1 = srednee_znachenie_F(self.F_dozv_1, user.m_sum)
        self.C_fi_dozv_1 = [0] * len(self.rho_j_1)
        self.tau_tr_dozv_1 = [0] * len(self.rho_j_1)
        self.delta_P_suzh_j_1 = [0] * len(self.rho_j_1)

        for i in range(0,len(self.rho_j_1)):
            self.C_fi_dozv_1[i]=(0.005*((1000/self.T_j_1[i])**(-0.35))*((1+0.44*(self.k_j_1[i]-1)*(self.M_j_1[i]**2))**(-0.55)))
            self.tau_tr_dozv_1[i]=self.C_fi_dozv_1[i]*self.rho_j_1[i]*(self.w_j_1[i]**2)*0.5
            self.delta_P_suzh_j_1[i]=self.F_j_1[i]*self.tau_tr_dozv_1[i]*(1/math.tan(self.beta_j_dozv_1[i]))
            self.Delta_P_suzh_1+=self.delta_P_suzh_j_1[i]

    def poteri_sverhzvuk_profil(self):
        """=====Расчёт потерь в профилированном сопле в расширяющейся части====="""
        self.x_svzv_1=[]
        self.r_sv_1=[]
        self.rho_sv_array_1=[]
        self.w_sv_array_1=[]
        self.T_sv_array_1=[]
        self.M_sv_1=[]
        self.k_sv_array_1=[]
        self.F_sv_array_1=[]
        for i in range(0,len(self.x_svzv)-1):
            if self.x_svzv[i]!=self.x_svzv[i+1]:
                self.x_svzv_1.append(self.x_svzv[i])
                self.r_sv_1.append(self.r_sv[i])
                self.rho_sv_array_1.append(self.rho_sv_array[i])
                self.w_sv_array_1.append(self.w_sv_array[i])
                self.T_sv_array_1.append(self.T_sv_array[i])
                self.M_sv_1.append(self.M_sv[i])
                self.k_sv_array_1.append(self.k_sv_array[i])
                self.F_sv_array_1.append(self.F_sv_array[i])
        self.beta_j_sv_1 = find_angle(self.x_svzv_1, self.r_sv_1)
        self.rho_j_sv_1 = srednee_znachenie(self.rho_sv_array_1)
        self.w_j_sv_1 = srednee_znachenie(self.w_sv_array_1)
        self.T_j_sv_1 = srednee_znachenie(self.T_sv_array_1)
        self.M_j_sv_1 = srednee_znachenie(self.M_sv_1)
        self.k_j_sv_1 = srednee_znachenie(self.k_sv_array_1)
        self.F_j_sv_1 = srednee_znachenie_F(self.F_sv_array_1, user.m_sum)
        self.C_fi_sv_1 = [0] * len(self.rho_sv_array_1)
        self.tau_tr_sv_1 = [0] * len(self.rho_sv_array_1)
        self.delta_P_sv_1 = [0] * len(self.rho_sv_array_1)
        self.Delta_P_rassh_1 = 0
        for i in range(0,len(self.rho_j_sv_1)):
            self.C_fi_sv_1[i]=(0.005*((1000/self.T_j_sv_1[i])**(-0.35))*((1+0.44*(self.k_j_sv_1[i]-1)*(self.M_j_sv_1[i]**2))**(-0.55)))
            self.tau_tr_sv_1[i]=self.C_fi_sv_1[i]*self.rho_j_sv_1[i]*(self.w_j_sv_1[i]**2)*0.5
            self.delta_P_sv_1[i]=self.F_j_sv_1[i]*self.tau_tr_sv_1[i]*(1/math.tan(self.beta_j_sv_1[i]))
            self.Delta_P_rassh_1+=self.delta_P_sv_1[i]
        # self.Delta_P_itog=self.Delta_P_rassh+self.Delta_P_suzh
        self.Delta_P_itog = self.Delta_P_rassh_1 + self.Delta_P_suzh_1
        self.phi_r_prof=(1+math.cos(user.teta_a*(math.pi/180)))*0.5
        self.phi_tr_prof=(1-(self.Delta_P_itog/user.P))
        self.phi_s_prof=self.phi_r_prof*self.phi_tr_prof
    def poteri_konich(self):
        """=====Расчёт потерь в коническом сопле в расширяющейся части====="""
        self.beta_kon=[]
        self.beta_kon_grad=[]
        for i in range(5,31):
            self.beta_kon.append(i*math.pi/180)
            self.beta_kon_grad.append(i)
        self.Delta_P_kon=[]
        self.C_fi_kon=[0]*len(self.rho_j_sv_1)
        self.tau_tr_kon=[0]*len(self.rho_j_sv_1)
        self.Delta_P_rassh_kon=0
        self.delta_P_kon=[0]*len(self.rho_j_sv_1)
        for beta in self.beta_kon:
            for i in range(0, len(self.rho_j_sv_1)):
                self.C_fi_kon[i]=(0.005*((1000/self.T_j_sv_1[i])**(-0.35))*((1+0.44*(self.k_j_sv_1[i]-1)*(self.M_j_sv_1[i]**2))**(-0.55)))
                self.tau_tr_kon[i]=self.C_fi_kon[i]*self.rho_j_sv_1[i]*(self.w_j_sv_1[i]**2)*0.5
                self.delta_P_kon[i]=self.F_j_sv_1[i]*self.tau_tr_kon[i]*(1/math.tan(beta))
                self.Delta_P_rassh_kon+=self.delta_P_kon[i]
            self.Delta_P_kon.append(self.Delta_P_rassh_kon)
            self.Delta_P_rassh_kon=0
        self.phi_r=[0]*len(self.Delta_P_kon)
        self.phi_tr= [0]*len(self.Delta_P_kon)
        self.phi_s = [0]*len(self.Delta_P_kon)
        for i in range(0,len(self.Delta_P_kon)):
            self.phi_r[i]=(1+math.cos(self.beta_kon[i]))*0.5
            self.phi_tr[i]=1-(self.Delta_P_kon[i]/user.P)
            self.phi_s[i]=self.phi_r[i]*self.phi_tr[i]
        self.max_phi=max(self.phi_s)
        self.index_max_phi=self.phi_s.index(self.max_phi)
        self.beta_kon_itog=self.beta_kon_grad[self.index_max_phi]
        print_graph_phi_x(self.phi_r,self.phi_tr,self.phi_s, self.beta_kon_grad, self.frame0, 50, 340, "Коэффициенты потерь",'', "phi")
        self.x_total_kon,self.y_total_kon=print_graph_kon(user.x_suzh,user.y_suzh,user.L_ks,self.beta_kon_itog,user.Rad_a,user.Rad_kp,self.frame0, 5, 1080,"Сопло с конической расширяющейся частью", 'х,мм', "r,мм",user.x_sv,user.y_sv)
        user.phi_r_array=self.phi_r
        user.phi_tr_array = self.phi_tr
        user.phi_s_array = self.phi_s
        user.beta_kon_grad_array = self.beta_kon_grad
    def place_label(self):
        self.text=f'''================Профилированное сопло================
Потери в сужающейся части равны = {self.Delta_P_suzh_1:.1f} Н
Потери в расширяющейся части для профиллированного сопла равны ={self.Delta_P_rassh_1:.1f} Н
Суммарные потери для профиллированного сопла равны ={self.Delta_P_itog:.1f} Н
Коэффициент потерь на трение для профиллированного сопла равен = {self.phi_tr_prof:6.4f}
Коэффициент потерь на рассеивание для профиллированного сопла равен = {self.phi_r_prof:6.4f}
Суммарный коэффициент потерь для профиллированного сопла равен={self.phi_s_prof:6.4f}

================Коническое сопло ================
Суммарный коэффициент потерь для конического сопла равен ={self.max_phi:6.4f}
Угол полураскрытия для конического сопла равен = {self.beta_kon_itog} градусов'''

        user.Delta_P_suzh_1=self.Delta_P_suzh_1
        user.Delta_P_rassh_1=self.Delta_P_rassh_1
        user.Delta_P_itog=self.Delta_P_itog
        user.phi_tr_prof=self.phi_tr_prof
        user.phi_r_prof=self.phi_r_prof
        user.phi_s_prof=self.phi_s_prof
        user.max_phi=self.max_phi
        user.beta_kon_itog=self.beta_kon_itog
        self.label = ctk.CTkLabel(self.scrollbar_frame_1, text=self.text, font=self.font1,justify='left')
        self.label.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    def back_window(self):
        """=====Переход в предыдущее окно====="""
        self.destroy()
        user.Delta_P_suzh_1 = None
        user.Delta_P_rassh_1 = None
        user.Delta_P_itog = None
        user.phi_tr_prof = None
        user.phi_r_prof = None
        user.phi_s_prof = None
        user.max_phi = None
        user.beta_kon_itog = None
        user.phi_r_array = None
        user.phi_tr_array = None
        user.phi_s_array = None
        user.beta_kon_grad_array = None
        Graph_po_dline = GraphWindow(user.oxigen, user.fuel, user.p_k, user.p_a, user.alpha_itog, user.alpha_value,
                                     user.selected_option, user.formula_gor, user.formula_ox, user.H_gor, user.H_ok,
                                     user.p_kp)
        Graph_po_dline.mainloop()
    def close_window(self):
        """=====Завершение работы. Выход====="""
        self.destroy()
        window_10 = Window_10(user.F_kp,user.m_sum,user.F_a,user.I_a,self.phi_s_prof)
        window_10.mainloop()
class Window_10(ctk.CTk):
    """----------------------------Окно, рассчитвающее действительное сопло----------------------------"""
    def __init__(self,F_kp,m_sum,F_a,I_a,phi_s_prof):
        """=====Начальные значения атрибутов класса====="""
        super().__init__()

        self.font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 1
        self.font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 2

        self.title("Расчёт параметров с учётом потерь")  # Название программы
        self.resizable(False, False)  # Запрет изменения размера окна
        self.iconbitmap('data/wings_1.ico')
        screen_width = self.winfo_screenwidth()  # Устанавливаем размер и позицию окна
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (1305 / 2))
        y_cordinate = int((screen_height / 2) - (734 / 2))
        self.geometry(f"{1305}x{734}+{x_cordinate}+{y_cordinate}")

        ctk.set_appearance_mode("Dark")  # Настройка темы
        ctk.set_default_color_theme("blue")  # Цветовая палитра
        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов

        self.F_kp=float(F_kp)
        self.m_sum=float(m_sum)
        self.F_a=F_a
        self.I_a=I_a
        self.phi_s_prof=phi_s_prof

        self.place_scrollbar()
        self.place_frame()
        self.print_label()
        self.print_button()
        self.print_entry()
        self.print_image()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """=====Действие при нажатии на крестик закрытия окна====="""
        self.destroy()
        sys.exit()  # Завершает работу программы
    def print_image(self):
        """=====Отрисовка изображений в окне====="""
        self.original_image = Image.open("data/image.png")  # Путь к изображению
        self.resized_image = self.original_image.resize((round(576*0.85), round(417*0.85)), Image.Resampling.LANCZOS)
        self.global_image = ImageTk.PhotoImage(self.resized_image)
        self.image_label = ctk.CTkLabel(self.frame0, image=self.global_image)
        self.image_label.place(x=500, y=2)
        self.image_label.configure(text="")
    def place_scrollbar(self):
        """=====Создание прокручивающегося фрейма в окне====="""
        self.scrollbar_frame_0 = ctk.CTkScrollableFrame(self, width=835, height=468,fg_color='#171717')  # 171717
        self.scrollbar_frame_0.place(x=2, y=2)
    def place_frame(self):
        """=====Создание мини-окон====="""
        self.frame0 = ctk.CTkFrame(master=self.scrollbar_frame_0, width=830, height=1370, fg_color="#171717",bg_color="transparent")
        self.frame0.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    def print_label(self):
        '''=====Вывод надписейв окно====='''
        self.label_1 = create_label(self.frame0, "Общие потери в камере сгорания находятся в диапазоне 0,95-0,99:", 10, 0)
        self.label_2 = create_label(self.frame0, "φ_к:", 10, 25)
        self.label_3 = create_label(self.frame0,f"Значение удельного пустотного действительного импульса: ",10, 50)
        self.label_4 = create_label(self.frame0, f"Действительный расход топлива:", 10, 75)
        self.label_5 = create_label(self.frame0,f"Действительные площади критического и выходного сечений:",10, 100)
        self.label_5_1 = create_label(self.frame0,f"F_кр= ... м^2",40, 125)
        self.label_5_2 = create_label(self.frame0, f"F_a= ... м^2 ", 40, 150)
        self.label_6 = create_label(self.frame0,f"Действительные диаметры критического и выходного сечений:",10, 170)
        self.label_6_1 = create_label(self.frame0,f"d_кр= ... мм",40, 195)
        self.label_6_2 = create_label(self.frame0,f"d_a= ... мм ",40, 220)
    def print_entry(self):
        '''=====Создание окна с вводом потерь в камере====='''
        self.entry1_value = ctk.StringVar()
        self.Entry1 = create_entry(self.frame0, 60, self.entry1_value, 45, 25)
    def print_button(self):
        '''=====Кнопка, выполняющая расчёт нового действительного сопла====='''
        self.entry_button = create_button(self.frame0, "Ввод", lambda: self.entry_change(), self.font1, 80, 115, 25)
        self.txt_button_1=create_button(self.frame0, "txt", lambda: save_properties_txt(self.text_2), self.font1, 80, 400, 220)
        self.txt_button_2 = create_button(self.frame0, "txt", lambda: save_to_txt(self.y_total_d, self.x_total_d), self.font1, 80, 20, 1060)
        self.txt_button_3 = create_button(self.frame0, "txt", lambda: save_properties_txt(self.text), self.font1, 80, 690, 1290)
        self.excel_button = create_button(self.frame0, "excel", lambda: save_to_excel(self.y_total_d, self.x_total_d,'R','X'), self.font1, 80, 110, 1060)
        self.excel_all_button = create_button(self.frame0, "Сохранить все параметры в excel", lambda: save_all_properties(user), self.font1, 300, 300, 1330)
        self.back_button = create_button(self.frame0, "Назад", lambda: self.back(), self.font1, 80, 5, 1330)
        self.close_button = create_button(self.frame0, "Выход", lambda: self.exit(), self.font1, 80, 750, 1330)
    def back(self):
        user.phi_k = None
        user.I_a_d = None
        user.m_sum_d = None
        user.F_kp_d = None
        user.F_a_d = None
        user.d_kp_d = None
        user.d_a_d = None
        user.itog_1 = None
        user.itog_2 = None
        user.itog_3 = None
        user.itog_4 = None
        user.itog_5 = None
        user.itog_6 = None
        user.itog_7 = None
        user.x_total_d = None
        user.y_total_d = None
        self.destroy()
        Losses_window = LossesWindow(user.x_dzv, user.r_dzv, user.T_dozv, user.rho_dozv, user.R_dozv, user.k_dozv,
                                     user.w_dozv, user.F_dozv, user.x_svzv, user.M_dozv, user.r_sv, user.T_sv_array,
                                     user.rho_sv_array, user.R_sv_array, user.k_sv_array, user.w_sv_array, user.M_sv,
                                     user.F_sv_array)
        Losses_window.mainloop()
    def exit(self):
        self.destroy()
        sys.exit()
    def entry_change(self):
        '''=====Расчёт нового действительного сопла====='''
        self.phi_k=float(self.entry1_value.get())
        self.I_a_d=self.I_a*self.phi_k*self.phi_s_prof
        self.m_sum_d=(self.m_sum)/(self.phi_k*self.phi_s_prof)
        self.F_kp_d=self.F_kp/self.phi_s_prof
        self.F_a_d=self.F_a/(self.phi_s_prof**2)
        self.d_kp_d=math.sqrt((4*self.F_kp_d)/math.pi)*1000
        self.d_a_d =math.sqrt((4*self.F_a_d)/math.pi)*1000
        self.F_ks_d=self.F_kp_d*user.F_otn_1
        self.d_ks_d=math.sqrt((4*self.F_ks_d)/math.pi)*1000
        self.label_3.configure(text=f"Значение удельного пустотного действительного импульса: {self.I_a_d:.2f} м/с")
        self.label_4.configure(text=f"Действительный расход топлива: {self.m_sum_d:.2f} кг/с")
        self.label_5_1.configure(text=f"F_кр={self.F_kp_d:.6f} м^2")
        self.label_5_2.configure(text=f"F_a={self.F_a_d:.6f} м^2")
        self.label_6_1.configure(text=f"d_кр={self.d_kp_d:.3f} мм")
        self.label_6_2.configure(text=f"d_a={self.d_a_d:.3f} мм")
        self.text_2=(f'''Общие потери в камере сгорания: {self.phi_k}
Значение удельного пустотного действительного импульса: {self.I_a_d:.2f} м/с
Действительный расход топлива: {self.m_sum_d:.2f} кг/с
F_кр={self.F_kp_d:.6f} м^2
F_a={self.F_a_d:.6f} м^2
d_кр={self.d_kp_d:.3f} мм
d_a={self.d_a_d:.3f} мм
''')
        user.phi_k = self.phi_k
        user.I_a_d=self.I_a_d
        user.m_sum_d = self.m_sum_d
        user.F_kp_d = self.F_kp_d
        user.F_a_d = self.F_a_d
        user.d_kp_d = self.d_kp_d
        user.d_a_d = self.d_a_d

        self.print_nozzle_d()
        self.slice_p()
        self.find_termodynamics_array()
        self.poteri_dozvuk()
        self.poteri_sverhzvuk()
        self.print_scrollbar()
    def print_scrollbar(self):
        self.scrollbar_frame_1 = ctk.CTkScrollableFrame(self.frame0, width=650, height=170, fg_color='black')  # 520
        self.scrollbar_frame_1.place(x=2, y=1100)
        self.text=(f'''================Действительное профилированное сопло================
Потери в сужающейся части равны = {self.Delta_P_suzh_1:.1f} Н
Потери в расширяющейся части для профиллированного сопла равны ={self.Delta_P_rassh_1:.1f} Н
Суммарные потери для профиллированного сопла равны ={self.Delta_P_itog:.1f} Н
Коэффициент потерь на трение для профиллированного сопла равен = {self.phi_tr_prof:6.4f}
Коэффициент потерь на рассеивание для профиллированного сопла равен = {self.phi_r_prof:6.4f}
Суммарный коэффициент потерь для профиллированного сопла равен={self.phi_s_prof:6.4f}
Погрешность составила {abs(self.phi_s_prof-user.phi_s_prof)*100/user.phi_s_prof:.3f} %
''')
        self.label = ctk.CTkLabel(self.scrollbar_frame_1, text=self.text, font=self.font1, justify='left')
        self.label.grid(row=0, column=0, sticky='w', padx=1, pady=1)

        user.itog_1=self.Delta_P_suzh_1
        user.itog_2 = self.Delta_P_rassh_1
        user.itog_3 = self.Delta_P_itog
        user.itog_4 = self.phi_tr_prof
        user.itog_5 = self.phi_r_prof
        user.itog_6 = self.phi_s_prof
        user.itog_7 = abs(self.phi_s_prof-user.phi_s_prof)*100/user.phi_s_prof
    def print_nozzle_d(self):
        '''=====Построение в окне нового сопла====='''
        if user.type_suzh==1:
            self.x_suzh_d,self.y_suzh_d,self.V_suzh_d=model_suzh_d_1(self.d_ks_d/2, self.d_kp_d/2,(self.d_ks_d/2)*user.R_1_0, (self.d_kp_d/2)*user.R_2_0)
        else:
            self.x_suzh_d,self.y_suzh_d,self.V_suzh_d=model_suzh_d_2(self.d_ks_d/2, self.d_kp_d/2,(self.d_ks_d/2)*user.R_1_0, (self.d_kp_d/2)*user.R_2_0,user.alpha_suzh_0)
        self.x_ks_d, self.y_ks_d = model_ks_d(user.tau_pr, user.R_k, user.T_k, self.F_kp_d, user.B, self.V_suzh_d,self.F_ks_d,self.x_suzh_d,self.y_suzh_d)
        self.x_sv_d,self.y_sv_d=model_sv_d(user.k_a, user.lambda_a, self.d_a_d/2, self.d_kp_d/2,user.teta_a)

        self.x_total_d = np.concatenate([self.x_ks_d,self.x_suzh_d,self.x_sv_d])
        self.y_total_d = np.concatenate([self.y_ks_d,self.y_suzh_d,self.y_sv_d])
        print_suzh_d(self.x_total_d,self.y_total_d,user.x_total,user.y_total,self.frame0)
        user.x_total_d=self.x_total_d
        user.y_total_d=self.y_total_d
    def slice_p(self):
        '''=====Деление давления на сегменты====='''
        self.p_k=float(user.p_k)
        self.p_kp = float(user.p_kp)
        self.p_a = float(user.p_a)
        self.p_dozv_array_0_d = np.linspace(self.p_k, (self.p_k + self.p_kp) * 0.5, 10)
        self.p_dozv_array_0_d=self.p_dozv_array_0_d[:-1]
        self.p_dozv_array_d = np.linspace((self.p_k + self.p_kp) * 0.5, self.p_kp, 10)
        self.p_cverhzv_array_d = np.geomspace(self.p_kp, self.p_a, 40)
        self.p_cverhzv_array_d =self.p_cverhzv_array_d[1:]
        self.p_dozv_array_d = np.concatenate((self.p_dozv_array_0_d, self.p_dozv_array_d))
    def find_termodynamics_array(self):
        self.T_dozv_array_d, self.rho_dozv_array_d, self.R_dozv_array_d, self.k_dozv_array_d, self.w_dozv_array_d, self.F_dozv_array_d = raschet_dozv(
            user.alpha_value, user.alpha_itog, user.H_gor, user.H_ok, user.formula_gor, user.formula_ox, self.p_k,
            user.selected_option, self.p_dozv_array_d)
        self.T_sv_array_d, self.rho_sv_array_d, self.R_sv_array_d, self.k_sv_array_d, self.w_sv_array_d, self.F_sv_array_d = raschet_dozv(
            user.alpha_value, user.alpha_itog, user.H_gor, user.H_ok, user.formula_gor, user.formula_ox, self.p_k,
            user.selected_option, self.p_cverhzv_array_d)
        self.w_dozv_array_d[0] = 0
        self.F_dozv_array_d[0] = self.F_ks_d/self.m_sum_d
        self.r_dozv_d = []
        self.r_sv_d = []
        for F in self.F_dozv_array_d:
            self.r_dozv_d.append(((4 * F*self.m_sum_d / (math.pi)) ** 0.5)*1000/2)
        for F in self.F_sv_array_d:
            self.r_sv_d.append(((4 * F*self.m_sum_d / (math.pi)) ** 0.5)*1000/2)
        self.M_dozv_array_d = []
        self.M_sv_array_d = []
        for R, T, k, w in zip(self.T_dozv_array_d, self.R_dozv_array_d, self.k_dozv_array_d, self.w_dozv_array_d):
            self.M_dozv_array_d.append(w / ((R * T * k) ** 0.5))
        for R, T, k, w in zip(self.T_sv_array_d, self.R_sv_array_d, self.k_sv_array_d, self.w_sv_array_d):
            self.M_sv_array_d.append(w / ((R * T * k) ** 0.5))
        self.T_array_d = np.concatenate((self.T_dozv_array_d, self.T_sv_array_d))
        self.rho_array_d = np.concatenate((self.rho_dozv_array_d, self.rho_sv_array_d))
        self.R_array_d = np.concatenate((self.R_dozv_array_d, self.R_sv_array_d))
        self.k_array_d = np.concatenate((self.k_dozv_array_d, self.k_sv_array_d))
        self.w_array_d = np.concatenate((self.w_dozv_array_d, self.w_sv_array_d))
        self.F_array_d = np.concatenate((self.F_dozv_array_d, self.F_sv_array_d))
        self.M_array_d = np.concatenate((self.M_dozv_array_d, self.M_sv_array_d))

        self.f_d = interp1d(self.y_suzh_d, self.x_suzh_d, kind='nearest')
        self.f_1_d = interp1d(self.y_sv_d, self.x_sv_d, kind='nearest')
        self.r_dozv_d[0] = self.y_suzh_d[0]
        self.r_dozv_d[-1] = self.y_suzh_d[-1]
        self.r_sv_d[0] = self.y_sv_d[0]
        self.r_sv_d[-1] = self.y_sv_d[-1]
        self.x_dzv_d=[]
        self.x_svzv_d=[]
        for r in self.r_dozv_d:
            self.x_dzv_d.append(self.f_d(r))
        for r in self.r_sv_d:
            self.x_svzv_d.append(self.f_1_d(r))
        self.x_graph_d = np.concatenate((self.x_dzv_d, self.x_svzv_d))
        self.p_graph_d = np.concatenate((self.p_dozv_array_d, self.p_cverhzv_array_d))
        self.a_kp_d = (user.k_kp * user.R_kp * user.T_kp) ** 0.5
        self.labda_w_d = []
        for w in self.w_array_d:
            self.labda_w_d.append(w/self.a_kp_d)
        self.rw_d=[]
        for r,w in zip(self.rho_array_d, self.w_array_d):
            self.rw_d.append(r*w)
    def poteri_dozvuk(self):
        """=====Расчёт потерь в дозвуковой части====="""
        self.x_dzv_1 = []
        self.r_dzv_1 = []
        self.rho_dozv_1 = []
        self.w_dozv_1 = []
        self.T_dozv_1 = []
        self.M_dozv_1 = []
        self.k_dozv_1 = []
        self.F_dozv_1 = []
        self.Delta_P_suzh_1 = 0
        for i in range(0, len(self.x_dzv_d) - 1):
            if self.x_dzv_d[i] != self.x_dzv_d[i + 1]:
                self.x_dzv_1.append(self.x_dzv_d[i])
                self.r_dzv_1.append(self.r_dozv_d[i])
                self.rho_dozv_1.append(self.rho_dozv_array_d[i])
                self.w_dozv_1.append(self.w_dozv_array_d[i])
                self.T_dozv_1.append(self.T_dozv_array_d[i])
                self.M_dozv_1.append(self.M_dozv_array_d[i])
                self.k_dozv_1.append(self.k_dozv_array_d[i])
                self.F_dozv_1.append(self.F_dozv_array_d[i])
        self.beta_j_dozv_1_d = find_angle(self.x_dzv_1, self.r_dzv_1)
        self.rho_j_1_d = srednee_znachenie(self.rho_dozv_1)
        self.w_j_1_d = srednee_znachenie(self.w_dozv_1)
        self.T_j_1_d = srednee_znachenie(self.T_dozv_1)
        self.M_j_1_d = srednee_znachenie(self.M_dozv_1)
        self.k_j_1_d = srednee_znachenie(self.k_dozv_1)
        self.F_j_1_d = srednee_znachenie_F(self.F_dozv_1, self.m_sum_d)
        self.C_fi_dozv_1_d = [0] * len(self.rho_j_1_d)
        self.tau_tr_dozv_1_d = [0] * len(self.rho_j_1_d)
        self.delta_P_suzh_j_1_d = [0] * len(self.rho_j_1_d)

        for i in range(0,len(self.rho_j_1_d)):
            self.C_fi_dozv_1_d[i]=(0.005*((1000/self.T_j_1_d[i])**(-0.35))*((1+0.44*(self.k_j_1_d[i]-1)*(self.M_j_1_d[i]**2))**(-0.55)))
            self.tau_tr_dozv_1_d[i]=self.C_fi_dozv_1_d[i]*self.rho_j_1_d[i]*(self.w_j_1_d[i]**2)*0.5
            self.delta_P_suzh_j_1_d[i]=self.F_j_1_d[i]*self.tau_tr_dozv_1_d[i]*(1/math.tan(self.beta_j_dozv_1_d[i]))
            self.Delta_P_suzh_1+=self.delta_P_suzh_j_1_d[i]
    def poteri_sverhzvuk(self):
        """=====Расчёт потерь в профилированном сопле в расширяющейся части====="""
        self.x_svzv_1=[]
        self.r_sv_1=[]
        self.rho_sv_array_1=[]
        self.w_sv_array_1=[]
        self.T_sv_array_1=[]
        self.M_sv_1=[]
        self.k_sv_array_1=[]
        self.F_sv_array_1=[]
        for i in range(0,len(self.x_svzv_d)-1):
            if self.x_svzv_d[i]!=self.x_svzv_d[i+1]:
                self.x_svzv_1.append(self.x_svzv_d[i])
                self.r_sv_1.append(self.r_sv_d[i])
                self.rho_sv_array_1.append(self.rho_sv_array_d[i])
                self.w_sv_array_1.append(self.w_sv_array_d[i])
                self.T_sv_array_1.append(self.T_sv_array_d[i])
                self.M_sv_1.append(self.M_sv_array_d[i])
                self.k_sv_array_1.append(self.k_sv_array_d[i])
                self.F_sv_array_1.append(self.F_sv_array_d[i])
        self.beta_j_sv_1 = find_angle(self.x_svzv_1, self.r_sv_1)
        self.rho_j_sv_1 = srednee_znachenie(self.rho_sv_array_1)
        self.w_j_sv_1 = srednee_znachenie(self.w_sv_array_1)
        self.T_j_sv_1 = srednee_znachenie(self.T_sv_array_1)
        self.M_j_sv_1 = srednee_znachenie(self.M_sv_1)
        self.k_j_sv_1 = srednee_znachenie(self.k_sv_array_1)
        self.F_j_sv_1 = srednee_znachenie_F(self.F_sv_array_1, user.m_sum)
        self.C_fi_sv_1 = [0] * len(self.rho_sv_array_1)
        self.tau_tr_sv_1 = [0] * len(self.rho_sv_array_1)
        self.delta_P_sv_1 = [0] * len(self.rho_sv_array_1)
        self.Delta_P_rassh_1 = 0
        for i in range(0,len(self.rho_j_sv_1)):
            self.C_fi_sv_1[i]=(0.005*((1000/self.T_j_sv_1[i])**(-0.35))*((1+0.44*(self.k_j_sv_1[i]-1)*(self.M_j_sv_1[i]**2))**(-0.55)))
            self.tau_tr_sv_1[i]=self.C_fi_sv_1[i]*self.rho_j_sv_1[i]*(self.w_j_sv_1[i]**2)*0.5
            self.delta_P_sv_1[i]=self.F_j_sv_1[i]*self.tau_tr_sv_1[i]*(1/math.tan(self.beta_j_sv_1[i]))
            self.Delta_P_rassh_1+=self.delta_P_sv_1[i]
        self.Delta_P_itog = self.Delta_P_rassh_1 + self.Delta_P_suzh_1
        self.phi_r_prof=(1+math.cos(user.teta_a*(math.pi/180)))*0.5
        self.phi_tr_prof=(1-(self.Delta_P_itog/user.P))
        self.phi_s_prof=self.phi_r_prof*self.phi_tr_prof

if __name__ == "__main__":
    app = DedalApp()
    app.mainloop()