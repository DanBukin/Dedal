from Dedal_functions import *
from terra_functions import *
import tkinter.messagebox as messagebox
import json
import bisect
import sys
import math
ctk.deactivate_automatic_dpi_awareness()
with open('oxigen_data.json', 'r', encoding='utf-8') as file:
    substances_data = json.load(file)
with open('fuel_data.json', 'r', encoding='utf-8') as file:
    substances_data_1 = json.load(file)
with open('alpha_data.json', 'r', encoding='utf-8') as file:
    substances_data_2 = json.load(file)
class DedalApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.font1 = ("Futura PT Book", 16)  # Настройка пользовательского шрифта 1
        self.font2 = ("Futura PT Book", 14)  # Настройка пользовательского шрифта 2

        self.title("Dedal")  # Название программы
        self.resizable(False, False)  # Запрет изменения размера окна

        screen_width = self.winfo_screenwidth()  # Устанавливаем размер и позицию окна
        screen_height = self.winfo_screenheight()
        window_width = 1305
        window_height = 734
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{1305}x{734}+{723}+{209}")

        ctk.set_appearance_mode("Dark")  # Настройка темы
        ctk.set_default_color_theme("blue")  # Цветовая палитра
        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов

        # Инициализация переменных
        self.is_running = True
        self.auto_fill_var = ctk.IntVar(value=0)  # Переменная для чекбокса "Авто"
        self.global_image = None
        self.image_label = None
        self.global_image_1 = None
        self.image_label_1 = None
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

    def combobox_callback1(self,value):
        self.oxigen = value
        self.periodic_check()

    def combobox_callback2(self,value):
        self.fuel = value
        self.periodic_check()
    def periodic_check(self):
        if self.is_running:
            self.update_enthalpy()
            self.alpha_input()

    def alpha_input(self):
        if self.is_running:
            if self.radio_var_alpha.get() == 1:  # Если выбрана первая радиокнопка
                if self.Entry_alpha:
                    self.Entry_alpha.place_forget()
            elif self.radio_var_alpha.get() == 2:  # Если выбрана вторая радиокнопка
                if self.Entry_alpha:
                    self.Entry_alpha.place(x=5, y=90)

    def update_enthalpy(self):
        self.selected_substance_oxigen = self.combobox1.get()  # Получаем выбранный оксид
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

    def get_selected_option(self):
        # Возвращает выбранный вариант
        self.selected_option = None
        if self.radio_var.get() == 1:
            self.selected_option = "Равновесный"
        elif self.radio_var.get() == 2:
            self.selected_option = "Замороженный"
        return self.selected_option

    def get_selected_option_alpha(self):
        # Возвращает выбранный вариант
        self.selected_option_alpha = None
        if self.radio_var_alpha.get() == 1:
            self.selected_option_alpha = "Оптимальный"
        elif self.radio_var_alpha.get() == 2:
            self.selected_option_alpha = "Заданный"
        return self.selected_option_alpha

    def setup_label(self):
        """--------------------Создание Надписей--------------------"""
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
        """--------------------Создание мини-окон--------------------"""
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
        """--------------------Создание окон с вводом данных--------------------"""
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
        self.combobox1 = ctk.CTkComboBox(self.frame3,values=["", "Кислород", "Озон", "АК", "АК-27", "АТ", "Перекись водорода", "Воздух"],command=self.combobox_callback1, font=self.font2, width=170)
        self.combobox2 = ctk.CTkComboBox(self.frame4,values=["", "Водород", "НДМГ", "Метан", "Аммиак", "Керосин РГ-1", "Керосин Т-1","Керосин RP-1", "Синтин", "Боктан", "Этанол", "ММГ", "Гидразин", "Анилин","Триэтиламин", "Ксилидин", ], command=self.combobox_callback2, font=self.font2,width=170)
        self.combobox1.place(x=5, y=25)
        self.combobox2.place(x=5, y=25)

    def setup_button(self):
        self.button1 = create_button(self.frame2, "Свойства окислителя", lambda: show_oxigen_properties(self),self.font1, 200, 10, 10)
        self.button2 = create_button(self.frame2, "Свойства горючего", lambda: show_fuel_properties(self), self.font1,200, 215, 10)
        self.button3 = create_button(self.frame2, "Свойства топливной пары", lambda: show_fuel_properties(self),self.font1, 210, 420, 10)
        self.close_button = create_button(self, "Дальше", self.close_window, self.font1,100,720,450)

        show_fuel_properties(self)

    def on_radio_button1_clicked(self):
        self.periodic_check()

    def on_radio_button2_clicked(self):
        self.periodic_check()

    def setup_radio(self):
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

    def setup_checkbox(self):
        self.auto_fill_var = ctk.IntVar(value=1)  # Переменная для отслеживания состояния чекбокса (0 - не нажат, 1 - нажат)
        self.auto_fill_checkbox = ctk.CTkCheckBox(self, text="Авто", variable=self.auto_fill_var, font=self.font1)
        self.auto_fill_checkbox.place(x=720, y=400)
    def close_window(self):
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
        self.destroy()
        second_window = SecondWindow(self.oxigen, self.fuel, self.p_k, self.p_a, self.alpha, self.alpha_value,
                                     self.selected_option, self.formula_gor, self.formula_ox, self.H_gor, self.H_ok)
        second_window.mainloop()
class SecondWindow(ctk.CTk):
    def __init__(self, oxigen, fuel, p_k, p_a, alpha, alpha_value, selected_option, formula_gor, formula_ox, H_gor, H_ok):
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

        ctk.set_appearance_mode("Dark")  # Настройка темы
        ctk.set_default_color_theme("blue")  # Цветовая палитра
        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов

        self.alpha_array = [i / 100 for i in range(50, 151)]  # [0.5, 0.51, 0.52, ..., 1.49, 1.5]
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
        self.fuel=self.formula_gor
        self.oxidizer=self.formula_ox
        self.scrollbar()
        self.place_label()
        self.graph_opt()
        self.but_exel()
    def scrollbar(self):
        self.scrollbar_frame = ctk.CTkScrollableFrame(self, width=830, height=370+95,fg_color='#171717') #171717
        self.scrollbar_frame.place(x=10, y=10)
    def place_label(self):
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame, text=f"Окислитель: {self.oxigen_naz}",font=self.font1)
        self.label1.grid(row=0, column=0,sticky='w', padx=10, pady=0)
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame, text=f"Горючее: {self.fuel_naz}",font=self.font1)
        self.label1.grid(row=1, column=0, sticky='w',padx=10, pady=0)
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame, text=f"Давление в камере: {self.p_k} МПа",font=self.font1)
        self.label1.grid(row=2, column=0, sticky='w',padx=10, pady=0)
        self.label1 = ctk.CTkLabel(master=self.scrollbar_frame, text=f"Давление на срезе: {self.p_a} МПа",font=self.font1)
        self.label1.grid(row=3, column=0, sticky='w',padx=10, pady=0)
    def graph_opt(self):
        self.alph_array,self.I_array,self.T_array,self.R_array,self.alpha_itog=optimalnaya_alpha(self.choice, self.p_k, self.p_a, self.alpha,
                          self.fuel, self.oxidizer, self.H_gor, self.H_ok, self.km0, self.scrollbar_frame,0)
    def but_exel(self):
        self.button1_I_exel = ctk.CTkButton(master=self.scrollbar_frame,text="Excel",width=60,command=lambda: save_to_excel_I_a(self.I_array, self.alph_array))
        self.button1_I_exel.place(x=615,y=460)
        self.button1_I_txt = ctk.CTkButton(master=self.scrollbar_frame, text="txt", width=50,command=lambda: save_to_txt_I_a(self.I_array, self.alph_array))
        self.button1_I_txt.place(x=620, y=490)

        self.button1_T_exel = ctk.CTkButton(master=self.scrollbar_frame, text="Excel", width=60,command=lambda: save_to_excel_T_a(self.T_array, self.alph_array))
        self.button1_T_exel.place(x=615, y=910)
        self.button1_T_txt = ctk.CTkButton(master=self.scrollbar_frame, text="txt", width=50,command=lambda: save_to_txt_T_a(self.T_array, self.alph_array))
        self.button1_T_txt.place(x=620, y=940)

        self.button1_R_exel = ctk.CTkButton(master=self.scrollbar_frame, text="Excel", width=60,command=lambda: save_to_excel_R_a(self.R_array, self.alph_array))
        self.button1_R_exel.place(x=615, y=1365)
        self.button1_R_txt = ctk.CTkButton(master=self.scrollbar_frame, text="txt", width=50,command=lambda: save_to_txt_R_a(self.R_array, self.alph_array))
        self.button1_R_txt.place(x=620, y=1395)

        self.button_close = ctk.CTkButton(master=self.scrollbar_frame, text="Дальше", width=100,command=lambda: self.close_window())
        self.button_close.place(x=725, y=1440)
    def close_window(self):
        self.destroy()
        third_window = ThirdWindow(self.formula_ox,self.formula_gor,self.p_k,self.p_a,self.alpha,self.km0,self.tech,self.H_gor,self.H_ok,self.alpha_itog,self.choice)
        third_window.mainloop()
class ThirdWindow(ctk.CTk):
    def __init__(self,formula_ox,formula_gor,p_k,p_a,alpha,km0,tech,H_gor,H_ok,alpha_itog,choice):
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


        self.scrollbar()
        self.options_KS()
        self.options_KP()
        self.options_A()
        self.place_label()
        self.donut_mass()
        self.print_engine()
        self.button_excel()
    def button_excel(self):
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

        self.but_close = ctk.CTkButton(master=self.scrollbar_frame, text="Дальше", width=100,command=lambda:self.close_window())
        self.but_close.place(x=730, y=2140 - 50)
    def print_engine(self):
        self.original_image = Image.open("engine_ks.png")  # Путь к изображению
        self.resized_image = self.original_image.resize((round(421*0.9), round(231*0.9)), Image.Resampling.LANCZOS)
        self.global_image = ImageTk.PhotoImage(self.resized_image)
        self.image_label = ctk.CTkLabel(self.scrollbar_frame, image=self.global_image)
        self.image_label.place(x=560, y=60)
        self.image_label.configure(text="")

        self.original_image = Image.open("engine_kp.png")  # Путь к изображению
        self.resized_image = self.original_image.resize((round(406 * 1.0), round(226 * 1.0)),Image.Resampling.LANCZOS)
        self.global_image = ImageTk.PhotoImage(self.resized_image)
        self.image_label = ctk.CTkLabel(self.scrollbar_frame, image=self.global_image)
        self.image_label.place(x=560, y=760)
        self.image_label.configure(text="")

        self.original_image = Image.open("engine_a.png")  # Путь к изображению
        self.resized_image = self.original_image.resize((round(474 * 0.85), round(256 * 0.85)),Image.Resampling.LANCZOS)
        self.global_image = ImageTk.PhotoImage(self.resized_image)
        self.image_label = ctk.CTkLabel(self.scrollbar_frame, image=self.global_image)
        self.image_label.place(x=560, y=1480)
        self.image_label.configure(text="")
    def scrollbar(self):
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
        self.properties,self.species_names,self.mass_fractions,self.mole_fractions =options_ks(self.choice,self.p_k,self.alpha_itog,self.formula_gor,self.formula_ox,self.H_gor,self.H_ok,self.km0)
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
        self.properties_kp,self.species_names_kp,self.mass_fractions_kp,self.mole_fractions_kp,self.F_kp=options_kp(self.choice,self.p_k,self.alpha_itog,self.formula_gor,self.formula_ox,self.H_gor,self.H_ok, self.km0)
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
        self.properties_a, self.species_names_a, self.mass_fractions_a, self.mole_fractions_a,self.I_a,self.F_a = options_a(
            self.choice, self.p_k,self.p_a, self.alpha_itog, self.formula_gor, self.formula_ox, self.H_gor, self.H_ok, self.km0)
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
        self.elements_value = {}
        for i in range(len(self.species_names)):
            self.elements_value[self.species_names[i]] = list(self.mass_fractions)[i]
        self.sorted_elements = sorted(self.elements_value.items(), key=lambda item: item[1], reverse=True)
        donut_diagramm(mass=self.sorted_elements, max=4, master=self.scrollbar_frame,x=550,y=370)

        self.elements_value_kp = {}
        for i in range(len(self.species_names_kp)):
            self.elements_value_kp[self.species_names_kp[i]] = list(self.mass_fractions_kp)[i]
        self.sorted_elements_kp = sorted(self.elements_value_kp.items(), key=lambda item: item[1], reverse=True)
        donut_diagramm(mass=self.sorted_elements_kp, max=3, master=self.scrollbar_frame, x=550, y=1440)

        self.elements_value_a = {}
        for i in range(len(self.species_names_a)):
            self.elements_value_a[self.species_names_a[i]] = list(self.mass_fractions_a)[i]
        self.sorted_elements_a = sorted(self.elements_value_a.items(), key=lambda item: item[1], reverse=True)
        donut_diagramm(mass=self.sorted_elements_a, max=3, master=self.scrollbar_frame, x=550, y=2515)
    def close_window(self):
        self.destroy()
        nozzle_window = NozzleWindow(self.I_a,self.F_kp,self.F_a,self.p_k)
        nozzle_window.mainloop()
class NozzleWindow(ctk.CTk):
    def __init__(self,I_a,F_kp,F_a,p_k):
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

        self.place_frame()
        self.place_label()
        self.place_entry()
        self.place_button()
        self.place_slider()
        self.print_soplo()
    def place_frame(self):
        self.frame1 = create_frame(self,200, 110,10,10,"#171717","transparent")
        self.frame2 = create_frame(self, 340, 100, 220, 10, "#171717", "transparent")
        self.frame3 = create_frame(self, 300, 100, 565, 10, "black", "transparent")
        self.frame4 = create_frame(self, 275, 120, 10, 150, "#171717", "transparent")
        self.frame5 = create_frame(self, 275, 120, 290, 150, "#171717", "transparent")
        self.frame6 = create_frame(self, 275, 120, 570, 150, "#171717", "transparent")
        self.frame7 = create_frame(self, 275, 150, 450, 290, "#171717", "transparent")
        self.frame8 = create_frame(self, 130, 150, 730, 290, "#171717", "transparent")
    def place_label(self):
        self.label1 = create_label(self.frame1, "Введите пустотную тягу:", 10, 2)
        self.label1 = create_label(self.frame1, "кН", 75, 30)
        self.label2 = create_label(self.frame1, "Тогда расход равен:", 10, 55)
        self.label4 = create_label(self.frame2, "Значение q_m':", 10, 60)
        self.label5 = create_label(self.frame2, "Введите относительную расходонапряжённость:", 10, 2)
        self.label6 = create_label(self.frame2, "0.07", 10, 30)
        self.label7 = create_label(self.frame2, "0.29", 205, 30)
        self.label8 = create_label(self.frame3, "Для расчета геометрии необходимо двигать", x=3, y=5)
        self.label8 = create_label(self.frame3, "ползунок. Убедитесь, что вы также ввели",x=3, y=30)
        self.label8 = create_label(self.frame3, "значение пустотной тяги в окне слева!",x=3, y=55)
        self.label9 = create_label(self, "Геометрические параметры:", x=10, y=120)
        self.label10 = create_label(self.frame4, "", x=5, y=5)
        self.label11 = create_label(self.frame4, "", x=5, y=30)
        self.label12 = create_label(self.frame4, "", x=5, y=55)
        self.label13 = create_label(self.frame4, "", x=5, y=80)
        self.label14 = create_label(self.frame5, "", x=5, y=5)
        self.label15 = create_label(self.frame5, "", x=5, y=30)
        self.label16 = create_label(self.frame5, "", x=5, y=55)
        self.label17 = create_label(self.frame5, "", x=5, y=80)
        self.label18 = create_label(self.frame6, "", x=5, y=5)
        self.label19 = create_label(self.frame6, "", x=5, y=30)
        self.label20 = create_label(self.frame6, "", x=5, y=55)
        self.label21 = create_label(self.frame6, "", x=5, y=80)
        self.label22 = create_label(self.frame8, "", 10, 15)
        self.label23 = create_label(self.frame8, "", 10, 60)
        self.label24 = create_label(self.frame8, "", 15, 105)
        self.label25 = create_label(self.frame7, "0.8", 50, 15)
        self.label26 = create_label(self.frame7, "0.8", 50, 60)
        self.label28 = create_label(self.frame7, "1.2", 235, 15)
        self.label29 = create_label(self.frame7, "1.2", 235, 60)
        self.label31 = create_label(self.frame7, "R_1:", 10, 15)
        self.label32 = create_label(self.frame7, "R_2:", 10, 60)
        self.label33 = create_label(self.frame7, "α:", 10, 105)
    def place_entry(self):
        self.entry1_value = ctk.StringVar()
        self.Entry1 = create_entry(self.frame1, 60, self.entry1_value, 10, 30)
    def place_button(self):
        self.angle_button = create_button(self.frame7, "рассчитать", lambda: self.return_angle(), self.font1, 100, 50, 105)
        self.close_button = create_button(self, "Далее", lambda: self.close_window(), self.font1, 100, 750, 450)
    def show_qm(self):
        if self.P is not None and self.kost is not None:
            self.q_m_otn = self.kost
            self.options_geomerty()
        else:
            messagebox.showwarning("Извините :( ", "Необходимо ввести значение тяги и выбрать коэффициент. Попробуйте еще раз!")
    def options_geomerty(self):
        self.F_ks=self.m_sum*1000/(self.p_k*self.q_m_otn)
        self.F_kp=self.F_kp_otn * self.m_sum
        self.F_a = self.F_a_otn* self.m_sum
        self.D_ks =(4*self.F_ks*1000000/3.1415926535898)**(0.5)
        self.R_ks =0.5*self.D_ks
        self.D_kp =(4*self.F_kp*1000000/3.1415926535898)**(0.5)
        self.R_kp =0.5*self.D_kp
        self.D_a =(4*self.F_a*1000000/3.1415926535898)**(0.5)
        self.R_a =0.5*self.D_a

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
        self.P=float(self.entry1_value.get())
        self.m_sum=(self.P*1000)/self.I_a
        if self.label3:
            self.label3.configure(text=f'{f"{self.m_sum:.2f}"} кг/с')
        else:
            self.label3 = create_label(self.frame1, f'{f"{self.m_sum:.2f}"} кг/с', 10, 80)
    def place_slider(self):
        self.slider = ctk.CTkSlider(self.frame2, from_=0.07, to=0.29,command=self.on_slider_change,number_of_steps=22,border_width=4, width=150, height=15,fg_color=("#474747"),progress_color=("#0094FF"))
        self.slider.place(x=50,y=35)
        self.slider_1 = ctk.CTkSlider(self.frame7, from_=0.8, to=1.2, command=self.on_slider_change_1, number_of_steps=40,border_width=4, width=150, height=15, fg_color=("#474747"),progress_color=("#0094FF"))
        self.slider_1.place(x=80, y=22)
        self.slider_2 = ctk.CTkSlider(self.frame7, from_=0.8, to=1.2, command=self.on_slider_change_2, number_of_steps=40,border_width=4, width=150, height=15, fg_color=("#474747"),progress_color=("#0094FF"))
        self.slider_2.place(x=80, y=67)
    def print_soplo(self):
        self.original_image = Image.open("soplo.png")  # Путь к изображению
        self.resized_image = self.original_image.resize((round(426*1.50), round(210*1.50)), Image.Resampling.LANCZOS)
        self.global_image = ImageTk.PhotoImage(self.resized_image)
        self.image_label = ctk.CTkLabel(self, image=self.global_image)
        self.image_label.place(x=10, y=275)
        self.image_label.configure(text="")
    def on_slider_change_1(self, value):
        # Обновление текста метки в соответствии со значением ползунка
        self.label22.configure(text=f"R_1 = R_ks*{value:.2f}")
        self.kost_1=value
    def on_slider_change_2(self, value):
        # Обновление текста метки в соответствии со значением ползунка
        self.label23.configure(text=f"R_2 = R_кр*{value:.2f}")
        self.kost_2=value
    def return_angle(self):
        self.R_1 = self.kost_1 * self.R_ks
        self.R_2 = self.kost_2 * self.R_kp

        self.beta = math.asin((self.R_kp + self.R_2 - self.R_ks + self.R_1) / (self.R_1 + self.R_2))
        self.alpha_angl = 1.5708 - self.beta
        self.alpha_angl_itog = (self.alpha_angl * 180) / math.pi
        self.label24.configure(text=f"α = {self.alpha_angl_itog:.1f}°")

    def on_slider_change(self, value):
        # Обновление текста метки в соответствии со значением ползунка
        self.label4.configure(text=f"Значение q_m' (*1000): {value:.2f}")
        self.kost=value
        self.show_thrust()
        self.show_qm()


    def close_window(self):
        if self.alpha_angl_itog<50:
            messagebox.showwarning("Упс!", "Данный угол недопустим. Попробуйте ещё раз")
        else:
            self.destroy()
            nozzle_subsonic_window = SubsonicWindow(self.R_1,self.R_2, self.R_ks,self.R_kp,self.alpha_angl)
            nozzle_subsonic_window.mainloop()
class SubsonicWindow(ctk.CTk):
    def __init__(self, R_1,R_2,R_ks,R_kp,alpha_angl):
        super().__init__()
        self.R_1 = R_1
        self.R_2 = R_2
        self.R_ks = R_ks
        self.R_kp = R_kp
        self.alpha_angl = alpha_angl


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

        ctk.set_appearance_mode("Dark")  # Настройка темы
        ctk.set_default_color_theme("blue")  # Цветовая палитра
        ctk.set_widget_scaling(1.5)  # Увеличение размера виджетов

        self.place_button()
    def place_button(self):
        self.close_button = create_button(self, "Далее", lambda: self.close_window(), self.font1, 100, 750, 450)
    def close_window(self):
        print(self.R_1, self.R_2, self.R_ks, self.R_kp, self.alpha_angl)
        sys.exit()
if __name__ == "__main__":
    app = DedalApp()
    app.mainloop()