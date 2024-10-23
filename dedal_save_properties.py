import xlsxwriter
import tkinter as tk
from tkinter import filedialog


def save_all_properties(user):
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно tkinter
    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                             filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:  # Если путь был выбран

        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet()
        data_format = workbook.add_format({'bg_color': '#1F6AA5'})
        for i in range(0, 8):
            worksheet.write_string(i, 2, "", cell_format=data_format)  # Столбец
        for i in range(0, 9):
            worksheet.write_string(8, i, "", cell_format=data_format)  # Строка
        worksheet.write(0, 0, 'Горючее:')
        worksheet.write(0, 1, str(user.formula_gor))
        worksheet.write(1, 0, 'Энтальпия горючего:')
        worksheet.write(1, 1, float(user.H_gor))
        worksheet.write(2, 0, 'Окислитель:')
        worksheet.write(2, 1, str(user.formula_ox))
        worksheet.write(3, 0, 'Энтальпия окислителя:')
        worksheet.write(3, 1, float(user.H_ok))
        worksheet.write(4, 0, 'Давление в камере (МПа):')
        worksheet.write(4, 1, float(user.p_k))
        worksheet.write(5, 0, 'Стехиометрия:')
        worksheet.write(5, 1, float(user.alpha_value))
        worksheet.write(6, 0, 'Оптимальный к.и.о:')
        worksheet.write(6, 1, float(user.alpha_itog))
        worksheet.write(7, 0, 'Тип течения:')
        worksheet.write(7, 1, str(user.selected_option))
        worksheet.write(9, 0, 'Пустотный удельный испульс')
        worksheet.write(9, 3, 'Газовая пост.')
        worksheet.write(9, 6, "Температура")
        worksheet.write(10, 1, 'I, м/с')
        worksheet.write(10, 0, 'alpha')
        worksheet.write(10, 4, "R, Дж/кг*К")
        worksheet.write(10, 3, 'alpha')
        worksheet.write(10, 7, 'T, К')
        worksheet.write(10, 6, "alpha")
        i = 11
        for alpha, I, T, R in zip(user.alpha_alpha, user.I_alpha, user.T_alpha, user.R_alpha):
            worksheet.write(i, 1, I)
            worksheet.write(i, 0, alpha)
            worksheet.write(i, 4, R)
            worksheet.write(i, 3, alpha)
            worksheet.write(i, 7, T)
            worksheet.write(i, 6, alpha)
            i += 1
        for j in range(9, i):
            worksheet.write_string(j, 2, "", cell_format=data_format)  # Строка
            worksheet.write_string(j, 5, "", cell_format=data_format)  # Строка
            worksheet.write_string(j, 8, "", cell_format=data_format)  # Строка
        for j in range(0, 9):
            worksheet.write_string(i, j, "", cell_format=data_format)  # Строка
        worksheet.set_row(i, 7)
        chart1 = workbook.add_chart({'type': 'scatter', 'subtype': 'smooth'})
        chart1.add_series({
            'name': '= Sheet1!$A$10',
            'categories': f'= Sheet1!$A$12:$A${i}',
            'values': f'= Sheet1!$B$12:$B${i}',
        })
        chart1.set_title({'name': 'Зависимость пустотного удельного импульса от к.и.о'})
        chart1.set_style(10)
        chart1.set_size({'width': 720, 'height': 500})
        chart1.set_x_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'к.и.о (б/р)'
        })
        chart1.set_y_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'Удельный пустотный импульс (м/с)'
        })
        worksheet.insert_chart('K11', chart1)

        chart2 = workbook.add_chart({'type': 'scatter', 'subtype': 'smooth'})
        chart2.add_series({
            'name': '= Sheet1!$D$10',
            'categories': f'= Sheet1!$D$12:$D${i}',
            'values': f'= Sheet1!$E$12:$E${i}',
        })
        chart2.set_title({'name': 'Зависимость газовой постоянной от к.и.о'})
        chart2.set_style(10)
        chart2.set_size({'width': 720, 'height': 500})
        chart2.set_x_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'к.и.о (б/р)'
        })
        chart2.set_y_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'R, Дж/кг*К'
        })
        worksheet.insert_chart('K38', chart2)

        chart3 = workbook.add_chart({'type': 'scatter', 'subtype': 'smooth'})
        chart3.add_series({
            'name': '= Sheet1!$G$10',
            'categories': f'= Sheet1!$G$12:$G${i}',
            'values': f'= Sheet1!$H$12:$H${i}',
        })
        chart3.set_title({'name': 'Зависимость температуры в КС от к.и.о'})
        chart3.set_style(10)
        chart3.set_size({'width': 720, 'height': 500})
        chart3.set_x_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'к.и.о (б/р)'
        })
        chart3.set_y_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'T, К'
        })
        worksheet.insert_chart('K65', chart3)
        i += 4
        j = i
        for x_1 in user.options_ks_excel:
            worksheet.write(i, 1, float(x_1))
            i += 1
        i = j
        worksheet.write(i - 3, 0, "Основные параметры")
        worksheet.write(i - 2, 0, "Камера")
        worksheet.write(i - 2, 3, "Критика")
        worksheet.write(i - 2, 6, "Срез")
        worksheet.write(i - 1, 0, "Параметр")
        worksheet.write(i - 1, 1, "Значение")
        worksheet.write(i - 1, 3, "Параметр")
        worksheet.write(i - 1, 4, "Значение")
        worksheet.write(i - 1, 6, "Параметр")
        worksheet.write(i - 1, 7, "Значение")
        worksheet.write(i, 0, "P, МПа")
        worksheet.write(i + 1, 0, "T, K")
        worksheet.write(i + 2, 0, "v, м3/кг")
        worksheet.write(i + 3, 0, "S, Дж/кг*К")
        worksheet.write(i + 4, 0, "I, кДж/кг")
        worksheet.write(i + 5, 0, "U, кДж/кг")
        worksheet.write(i + 6, 0, "MMg, г/моль")
        worksheet.write(i + 7, 0, "R, Дж/кг*К")
        worksheet.write(i + 8, 0, "Cp, Дж/кг*К")
        worksheet.write(i + 9, 0, "Cv, Дж/кг*К")
        worksheet.write(i + 10, 0, "k")
        worksheet.write(i, 3, "P, МПа")
        worksheet.write(i + 1, 3, "T, K")
        worksheet.write(i + 2, 3, "v, м3/кг")
        worksheet.write(i + 3, 3, "S, Дж/кг*К")
        worksheet.write(i + 4, 3, "I, кДж/кг")
        worksheet.write(i + 5, 3, "U, кДж/кг")
        worksheet.write(i + 6, 3, "MMg, г/моль")
        worksheet.write(i + 7, 3, "R, Дж/кг*К")
        worksheet.write(i + 8, 3, "I_уд_кр, м/с")
        worksheet.write(i + 9, 3, "W, м/с")
        worksheet.write(i + 10, 3, "F_кр_уд, м2*с/кг")
        worksheet.write(i + 11, 3, "В, м/с")
        worksheet.write(i + 12, 3, "Cp, Дж/кг*К")
        worksheet.write(i + 13, 3, "Cv, Дж/кг*К")
        worksheet.write(i + 14, 3, "k")
        worksheet.write(i, 6, "P, МПа")
        worksheet.write(i + 1, 6, "T, K")
        worksheet.write(i + 2, 6, "v, м3/кг")
        worksheet.write(i + 3, 6, "S, Дж/кг*К")
        worksheet.write(i + 4, 6, "I, кДж/кг")
        worksheet.write(i + 5, 6, "U, кДж/кг")
        worksheet.write(i + 6, 6, "MMg, г/моль")
        worksheet.write(i + 7, 6, "R, Дж/кг*К")
        worksheet.write(i + 8, 6, "W, м/с")
        worksheet.write(i + 9, 6, "I_уд, м/с")
        worksheet.write(i + 10, 6, "F_a_уд, м2*с/кг")
        worksheet.write(i + 11, 6, "Cp, Дж/кг*К")
        worksheet.write(i + 12, 6, "Cv, Дж/кг*К")
        worksheet.write(i + 13, 6, "k")
        worksheet.set_row(i + 15, 7)
        worksheet.set_row(i + 15 + 10, 7)
        for j in range(i - 3, i + 15 + 10):
            worksheet.write_string(j, 2, "", cell_format=data_format)  # Строка
            worksheet.write_string(j, 5, "", cell_format=data_format)  # Строка
            worksheet.write_string(j, 8, "", cell_format=data_format)  # Строка
        for h in range(0, 9):
            worksheet.write_string(i + 15, h, "", cell_format=data_format)  # Столбец
            worksheet.write_string(i + 15 + 10, h, "", cell_format=data_format)  # Столбец
        k = 0
        for x_2 in user.options_kp_excel:
            worksheet.write(i, 4, float(x_2))
            i += 1
            k += 1
        i = i - k
        for x_3 in user.options_a_excel:
            worksheet.write(i, 7, float(x_3))
            i += 1
        worksheet.write(i + 2, 0, "Тяга, кН")
        worksheet.write(i + 2, 1, float(user.P))
        worksheet.write(i + 3, 0, "Массовый расход, кг/с")
        worksheet.write(i + 3, 1, float(user.m_sum))
        worksheet.write(i + 4, 0, "Отношение F_кс/F_кр")
        worksheet.write(i + 4, 1, float(user.F_otn_1))
        worksheet.write(i + 5, 0, "Геометрические параметры")
        worksheet.write(i + 6, 0, "Камера")
        worksheet.write(i + 6, 3, "Критика")
        worksheet.write(i + 6, 6, "Срез")
        worksheet.write(i + 7, 0, "Параметр")
        worksheet.write(i + 7, 3, "Параметр")
        worksheet.write(i + 7, 6, "Параметр")
        worksheet.write(i + 7, 1, "Значение")
        worksheet.write(i + 7, 4, "Значение")
        worksheet.write(i + 7, 7, "Значение")
        worksheet.write(i + 8, 0, "F_кс, м^2")
        worksheet.write(i + 8, 1, float(user.F_ks))
        worksheet.write(i + 9, 0, "d_кс, мм")
        worksheet.write(i + 9, 1, float(2 * float(user.Rad_ks)))
        worksheet.write(i + 10, 0, "R_кс, мм")
        worksheet.write(i + 10, 1, float(user.Rad_ks))
        worksheet.write(i + 8, 3, "F_кр, м^2")
        worksheet.write(i + 8, 4, float(user.F_kp))
        worksheet.write(i + 9, 3, "d_кр, мм")
        worksheet.write(i + 9, 4, float(2 * user.Rad_kp))
        worksheet.write(i + 10, 3, "R_кр, мм")
        worksheet.write(i + 10, 4, float(user.Rad_kp))
        worksheet.write(i + 8, 6, "F_а, м^2")
        worksheet.write(i + 8, 7, float(user.F_a))
        worksheet.write(i + 9, 6, "d_а, мм")
        worksheet.write(i + 9, 7, float(2 * float(user.Rad_a)))
        worksheet.write(i + 10, 6, "R_а, мм")
        worksheet.write(i + 10, 7, float(user.Rad_a))

        worksheet.write(i + 12, 0, "R_1, мм")
        worksheet.write(i + 12, 1, float(user.R_1))
        worksheet.write(i + 13, 0, "R_2, мм")
        worksheet.write(i + 13, 1, float(user.R_2))
        worksheet.write(i + 14, 0, "Угол наклона суж. части, град")
        worksheet.write(i + 14, 1, float(user.alpha_suzh_0))
        worksheet.write(i + 15, 0, "Тип суж. части:")
        if float(user.type_suzh) == 1:
            worksheet.write(i + 15, 1, "Радиусная")
        else:
            worksheet.write(i + 15, 1, "Радиусно-коническая")
        worksheet.set_row(i + 16, 7)
        worksheet.write(i + 17, 0, "X, мм")
        worksheet.write(i + 17, 1, "R, мм")
        for j in range(i + 12, i + 17):
            worksheet.write_string(j, 2, "", cell_format=data_format)  # Строка
            worksheet.write_string(j, 5, "", cell_format=data_format)  # Строка
            worksheet.write_string(j, 8, "", cell_format=data_format)  # Строка
        for h in range(0, 18):
            worksheet.write_string(i + 16, h, "", cell_format=data_format)  # Столбец
        i_1 = i + 18
        i_1_0 = i_1
        i_1_2 = i_1
        for x, y in zip(user.x_suzh, user.y_suzh):
            worksheet.write(i_1, 0, float(x))
            worksheet.write(i_1, 1, float(y))
            i_1 += 1
        for x, y in zip(user.x_sv, user.y_sv):
            worksheet.write(i_1_2, 6, float(x))
            worksheet.write(i_1_2, 7, float(y))
            i_1_2 += 1
        i_1_1 = i_1
        chart4 = workbook.add_chart({'type': 'scatter', 'subtype': 'smooth'})
        chart4.add_series({
            'name': 'Сужающаяся часть',
            'categories': f'= Sheet1!$A${i_1_0 + 1}:$A${i_1_1}',
            'values': f'= Sheet1!$B${i_1_0 + 1}:$B${i_1_1}',
        })
        chart4.set_title({'name': 'Сопло Лаваля'})
        chart4.set_style(10)
        chart4.set_size({'width': 1100, 'height': 500})
        chart4.set_x_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'x, мм'
        })
        chart4.set_y_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'R, мм'
        })
        worksheet.insert_chart(f'S{i_1_0}', chart4)
        i = i_1_0 - 6
        worksheet.write(i, 3, "Камера сгорания")
        worksheet.write(i, 6, "Расш. часть")
        worksheet.write(i + 1, 3, "Усл. время преб. (мс):")
        worksheet.write(i + 1, 4, float(user.tau_pr))
        worksheet.write(i + 2, 3, "Длина КС (мм):")
        worksheet.write(i + 2, 4, float(user.L_ks))
        worksheet.write(i + 3, 3, "Приведнная длина КС (м):")
        worksheet.write(i + 3, 4, float(user.l_pr))

        worksheet.write(i + 1, 6, "β_m (°):")
        worksheet.write(i + 1, 7, float(user.teta_m))
        worksheet.write(i + 2, 6, "β_a (°):")
        worksheet.write(i + 2, 7, float(user.teta_a))
        worksheet.write(i + 3, 6, "Длина расш. ч. (мм):")
        worksheet.write(i + 3, 7, float(user.x_total[-1]))
        worksheet.write(i + 5, 3, "X,мм")
        worksheet.write(i + 5, 4, "R,мм")
        worksheet.write(i + 6, 3, float(user.x_dozv[0]))
        worksheet.write(i + 6, 4, float(user.y_dozv[0]))
        worksheet.write(i + 7, 3, float(user.x_dozv[1]))
        worksheet.write(i + 7, 4, float(user.y_dozv[1]))
        worksheet.write(i + 5, 6, "X,мм")
        worksheet.write(i + 5, 7, "R,мм")
        worksheet.write(i + 5, 9, "L,мм")
        worksheet.write(i + 5, 10, "P (МПа)")
        worksheet.write(i + 5, 11, "T (К)")
        worksheet.write(i + 5, 12, "rho (кг/м3)")
        worksheet.write(i + 5, 13, "W (м/с)")
        worksheet.write(i + 5, 14, "М (б/р)")
        worksheet.write(i + 5, 15, "lambda (б/р)")
        worksheet.write(i + 5, 16, "rw (кг/м2*с)")
        o = i + 6
        o_0 = o
        for x, y_1, y_2, y_3, y_4, y_5, y_6, y_7 in zip(user.X_graph, user.P_graph, user.T_graph, user.Rho_graph,
                                                        user.W_graph, user.M_graph, user.Lambda_graph, user.RW_graph):
            worksheet.write(o, 9, float(x))
            worksheet.write(o, 10, float(y_1))
            worksheet.write(o, 11, float(y_2))
            worksheet.write(o, 12, float(y_3))
            worksheet.write(o, 13, float(y_4))
            worksheet.write(o, 14, float(y_5))
            worksheet.write(o, 15, float(y_6))
            worksheet.write(o, 16, float(y_7))
            o += 1
        o_1=o
        for j in range(o_0 - 2, o_1):
            worksheet.write_string(j, 2, "", cell_format=data_format)  # Строка
            worksheet.write_string(j, 5, "", cell_format=data_format)  # Строка
            worksheet.write_string(j, 8, "", cell_format=data_format)  # Строка
            worksheet.write_string(j, 17, "", cell_format=data_format)  # Строка
        for h in range(0, 18):
            worksheet.write_string(o_1, h, "", cell_format=data_format)  # Столбец
        chart5 = workbook.add_chart({'type': 'scatter', 'subtype': 'smooth'})
        chart5.add_series({
            'name': 'Давление',
            'categories': f'= Sheet1!$J${o_0 + 1}:$J${o}',
            'values': f'= Sheet1!$K${o_0 + 1}:$K${o}',
        })
        chart5.set_title({'name': 'Давление'})
        chart5.set_style(10)
        chart5.set_size({'width': 550, 'height': 500})
        chart5.set_x_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'x, мм'
        })
        chart5.set_y_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'P, МПа'
        })
        worksheet.insert_chart(f'S{o_0 + 26}', chart5)

        chart6 = workbook.add_chart({'type': 'scatter', 'subtype': 'smooth'})
        chart6.add_series({
            'name': 'Температура',
            'categories': f'= Sheet1!$J${o_0 + 1}:$J${o}',
            'values': f'= Sheet1!$L${o_0 + 1}:$L${o}',
        })
        chart6.set_title({'name': 'Температура'})
        chart6.set_style(10)
        chart6.set_size({'width': 550, 'height': 500})
        chart6.set_x_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'x, мм'
        })
        chart6.set_y_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'T, K'
        })
        worksheet.insert_chart(f'AB{o_0 + 26}', chart6)

        chart7 = workbook.add_chart({'type': 'scatter', 'subtype': 'smooth'})
        chart7.add_series({
            'name': 'Плотность',
            'categories': f'= Sheet1!$J${o_0 + 1}:$J${o}',
            'values': f'= Sheet1!$M${o_0 + 1}:$M${o}',
        })
        chart7.set_title({'name': 'Плотность'})
        chart7.set_style(10)
        chart7.set_size({'width': 550, 'height': 500})
        chart7.set_x_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'x, мм'
        })
        chart7.set_y_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'rho, кг/м3'
        })
        worksheet.insert_chart(f'AK{o_0}', chart7)

        chart8 = workbook.add_chart({'type': 'scatter', 'subtype': 'smooth'})
        chart8.add_series({
            'name': 'Скорость',
            'categories': f'= Sheet1!$J${o_0 + 1}:$J${o}',
            'values': f'= Sheet1!$N${o_0 + 1}:$N${o}',
        })
        chart8.set_title({'name': 'Скорость'})
        chart8.set_style(10)
        chart8.set_size({'width': 550, 'height': 500})
        chart8.set_x_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'x, мм'
        })
        chart8.set_y_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'W, м/с'
        })
        worksheet.insert_chart(f'AK{o_0 + 26}', chart8)

        chart10 = workbook.add_chart({'type': 'scatter', 'subtype': 'smooth'})
        chart10.add_series({
            'name': 'Мах',
            'categories': f'= Sheet1!$J${o_0 + 1}:$J${o}',
            'values': f'= Sheet1!$O${o_0 + 1}:$O${o}',
        })
        chart10.add_series({
            'name': 'Прив. скорость',
            'categories': f'= Sheet1!$J${o_0 + 1}:$J${o}',
            'values': f'= Sheet1!$P${o_0 + 1}:$P${o}',
        })
        chart10.set_title({'name': 'Скорость Маха и приведенная скорость'})
        chart10.set_style(10)
        chart10.set_size({'width': 550, 'height': 500})
        chart10.set_x_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'x, мм'
        })
        chart10.set_y_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'б/р'
        })
        worksheet.insert_chart(f'AT{o_0 + 26}', chart10)

        chart11 = workbook.add_chart({'type': 'scatter', 'subtype': 'smooth'})
        chart11.add_series({
            'name': 'Расходонапряжённость',
            'categories': f'= Sheet1!$J${o_0 + 1}:$J${o}',
            'values': f'= Sheet1!$Q${o_0 + 1}:$Q${o}',
        })
        chart11.set_title({'name': 'Расходонапряжённость'})
        chart11.set_style(10)
        chart11.set_size({'width': 550, 'height': 500})
        chart11.set_x_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'x, мм'
        })
        chart11.set_y_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'rw (кг/м2*с)'
        })
        worksheet.insert_chart(f'AT{o_0}', chart11)

        chart4.add_series({
            'name': 'Расширяющаяся часть',
            'categories': f'= Sheet1!$G${i_1_0 + 1}:$G${i_1_2}',
            'values': f'= Sheet1!$H${i_1_0 + 1}:$H${i_1_2}',
        })
        chart4.add_series({
            'name': 'Камера сгорания',
            'categories': f'= Sheet1!$D${i_1_0 + 1}:$D${i_1_0 + 2}',
            'values': f'= Sheet1!$E${i_1_0 + 1}:$E${i_1_0 + 2}',
        })
        worksheet.insert_chart(f'K{i_1_0}', chart4)
        worksheet.set_row(o_1, 7)
        i = o_1 + 1
        worksheet.write(i, 0, "Потери")
        worksheet.write(i + 1, 0, "Профиллированное сопло")
        worksheet.write(i + 1, 3, "Коническое сопло")
        worksheet.write(i + 2, 0, "Потери в суж. части, Н")
        worksheet.write(i + 2, 1, float(user.Delta_P_suzh_1))
        worksheet.write(i + 2, 3, "Суммарный коэфф. потерь")
        worksheet.write(i + 2, 4, float(user.max_phi))
        worksheet.write(i + 3, 0, "Потери в расш. части, Н")
        worksheet.write(i + 3, 1, float(user.Delta_P_rassh_1))
        worksheet.write(i + 3, 3, "Угол полураскрытия сопла")
        worksheet.write(i + 3, 4, float(user.beta_kon_itog))
        worksheet.write(i + 4, 0, "Суммарные потери, Н")
        worksheet.write(i + 4, 1, float(user.Delta_P_itog))
        worksheet.write(i + 5, 0, "Коэфф. потерь на трение")
        worksheet.write(i + 5, 1, float(user.phi_tr_prof))
        worksheet.write(i + 6, 0, "Коэфф. потерь на рассеивание")
        worksheet.write(i + 6, 1, float(user.phi_r_prof))
        worksheet.write(i + 7, 0, "Суммарный коэфф. потерь")
        worksheet.write(i + 7, 1, float(user.phi_s_prof))
        worksheet.write(i + 9, 1, "φ_расс")
        worksheet.write(i + 9, 4, "φ_тр")
        worksheet.write(i + 9, 7, "φ_сум")
        worksheet.write(i + 9, 0, "β")
        worksheet.write(i + 9, 3, "β")
        worksheet.write(i + 9, 6, "β")
        j = i + 10
        j_0 = j
        for b, x_1, x_2, x_3 in zip(user.beta_kon_grad_array, user.phi_r_array, user.phi_tr_array, user.phi_s_array):
            worksheet.write(j, 0, float(b))
            worksheet.write(j, 3, float(b))
            worksheet.write(j, 6, float(b))
            worksheet.write(j, 1, float(x_1))
            worksheet.write(j, 4, float(x_2))
            worksheet.write(j, 7, float(x_3))
            j += 1
        j_1 = j

        chart12 = workbook.add_chart({'type': 'scatter', 'subtype': 'smooth'})
        chart12.add_series({
            'name': 'Коэф. потерь на рассеивание',
            'categories': f'= Sheet1!$A${j_0 + 1}:$A${j_1}',
            'values': f'= Sheet1!$B${j_0 + 1}:$B${j_1}',
        })
        chart12.add_series({
            'name': 'Коэф. потерь на трение',
            'categories': f'= Sheet1!$D${j_0 + 1}:$D${j_1}',
            'values': f'= Sheet1!$E${j_0 + 1}:$E${j_1}',
        })
        chart12.add_series({
            'name': 'Суммарный коэф. потерь',
            'categories': f'= Sheet1!$G${j_0 + 1}:$G${j_1}',
            'values': f'= Sheet1!$H${j_0 + 1}:$H${j_1}',
        })
        chart12.set_title({'name': 'Коэффициенты потерь'})
        chart12.set_style(10)
        chart12.set_size({'width': 900, 'height': 600})
        chart12.set_x_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'град'
        })
        chart12.set_y_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'б/р)'
        })
        worksheet.insert_chart(f'K{j_0 - 7}', chart12)
        for i in range(j_0 - 10, j_1):
            worksheet.write_string(i, 2, "", cell_format=data_format)  # Строка
            worksheet.write_string(i, 5, "", cell_format=data_format)  # Строка
            worksheet.write_string(i, 8, "", cell_format=data_format)  # Строка
        for h in range(0, 9):
            worksheet.write_string(j_0 - 2, h, "", cell_format=data_format)  # Столбец
            worksheet.write_string(j_1, h, "", cell_format=data_format)  # Столбец
        worksheet.set_row(j_0 - 2, 7)
        worksheet.set_row(j_1, 7)
        i = j_1 + 1
        worksheet.write(i, 0, "Потери в камере")
        worksheet.write(i + 1, 0, "Действ. уд. имупльс, м/с")
        worksheet.write(i + 2, 0, "Действительный расход, кг/с")
        worksheet.write(i + 3, 0, "Действительные площади:")
        worksheet.write(i + 4, 0, "F_кр, м2")
        worksheet.write(i + 5, 0, "F_а, м2")
        worksheet.write(i + 6, 0, "Действительные диаметры:")
        worksheet.write(i + 7, 0, "D_кр, мм")
        worksheet.write(i + 8, 0, "D_а, мм")
        worksheet.write(i + 9, 0, "Потери в суж. части, Н")
        worksheet.write(i + 10, 0, "Потери в расш. части, Н")
        worksheet.write(i + 11, 0, "Суммарные потери, Н")
        worksheet.write(i + 12, 0, "Коэфф. потерь на трение")
        worksheet.write(i + 13, 0, "Коэфф. потерь на рас.")
        worksheet.write(i + 14, 0, "Суммарный коэф. потерь")
        worksheet.write(i + 15, 0, "Погрешность, %")
        worksheet.write(i + 17, 0, "X, мм")
        worksheet.write(i + 17, 1, "R, мм")

        worksheet.write(i, 1, float(user.phi_k))
        worksheet.write(i + 1, 1, float(user.I_a_d))
        worksheet.write(i + 2, 1, float(user.m_sum_d))
        worksheet.write(i + 4, 1, float(user.F_kp_d))
        worksheet.write(i + 5, 1, float(user.F_a_d))
        worksheet.write(i + 7, 1, float(user.d_kp_d))
        worksheet.write(i + 8, 1, float(user.d_a_d))
        worksheet.write(i + 9, 1, float(user.itog_1))
        worksheet.write(i + 10, 1, float(user.itog_2))
        worksheet.write(i + 11, 1, float(user.itog_3))
        worksheet.write(i + 12, 1, float(user.itog_4))
        worksheet.write(i + 13, 1, float(user.itog_5))
        worksheet.write(i + 14, 1, float(user.itog_6))
        worksheet.write(i + 15, 1, float(user.itog_7))
        i=i+18
        i_0=i
        for x,y in zip(user.x_total_d,user.y_total_d):
            worksheet.write(i, 0, float(x))
            worksheet.write(i, 1, float(y))
            i+=1
        i_1=i
        chart13 = workbook.add_chart({'type': 'scatter', 'subtype': 'smooth'})
        chart13.add_series({
            'name': 'Действительное сопло',
            'categories': f'= Sheet1!$A${i_0 + 1}:$A${i_1}',
            'values': f'= Sheet1!$B${i_0 + 1}:$B${i_1}',
        })
        chart13.set_title({'name': 'Действительное сопло'})
        chart13.set_style(10)
        chart13.set_size({'width': 1200, 'height': 500})
        chart13.set_x_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'x, мм'
        })
        chart13.set_y_axis({
            'major_gridlines': {'visible': True, 'line': {'width': 1.00}},
            'minor_gridlines': {'visible': True, 'line': {'width': 0.75}},
            'name': 'R, мм'
        })
        worksheet.insert_chart(f'E{i_0-16}', chart13)
        for u in range(i_0 - 18, i_1):
            worksheet.write_string(u, 2, "", cell_format=data_format)  # Строка

        for h in range(0, 3):
            worksheet.write_string(i_0 - 2, h, "", cell_format=data_format)  # Столбец
            worksheet.write_string(i_1, h, "", cell_format=data_format)  # Столбец
        worksheet.set_row(i_0 - 2, 7)
        worksheet.set_row(i_1, 7)
        worksheet.set_column(0, 0, 28)
        worksheet.set_column(1, 1, 12)
        worksheet.set_column(2, 2, 0.7)
        worksheet.set_column(3, 3, 23)
        worksheet.set_column(4, 4, 12)
        worksheet.set_column(5, 5, 0.7)
        worksheet.set_column(6, 6, 18)
        worksheet.set_column(7, 7, 12)
        worksheet.set_column(8, 8, 0.7)
        worksheet.set_column(9, 9, 12)
        worksheet.set_column(10, 16, 11.23)
        worksheet.set_column(17, 17, 0.7)
        worksheet.set_row(8, 7)
        workbook.close()
