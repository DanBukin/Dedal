# DEDAL

![wings (3)](https://github.com/DanBukin/Dedal/assets/161983114/924e0fad-ecfc-45b5-bae1-0a088cc605d2)

Цель проекта:

Разработка программы для автоматизированного расчета и анализа термодинамических и геометрических характеристик жидкостных ракетных двигателей.


Основные функции:

Термодинамический расчет:
  
Использование библиотеки Cantera для моделирования химических реакций и расчета термодинамических параметров ракетного топлива.
    
Учет термического равновесия, состава смеси, температуры и давления.
    
Геометрический расчет:
  
Определение параметров сопловой системы, включая форму и размеры сопла.
    
Расчет диаметра и длины камеры сгорания.
    
Визуализация результатов:
  
Интеграция с библиотекой CustomTkinter для создания графического интерфейса пользователя (GUI).
    
Отображение результатов расчетов в виде графиков, таблиц и диаграмм.
    
Ввод пользовательских данных:
  
Возможность ввода параметров топлива, окружающей среды, начальных условий и других важных данных.
    
Экспорт результатов:
  
Возможность сохранения результатов расчетов в файлы различных форматов для последующего анализа и документации.

    
Технологический стек:

Язык программирования: Python.
  
Библиотеки: Cantera для термодинамических расчетов, CustomTkinter для GUI.
  
Другие библиотеки (numpy, matplotlib) для обработки данных и визуализации.

  
Преимущества проекта:

Удобный и интуитивно понятный интерфейс пользователя.
  
Высокая точность расчетов за счет использования библиотеки Cantera.
  
Возможность легкого масштабирования и расширения функционала.

  
Примечание: 

  Важно регулярно обновлять базу данных топлив и параметров для обеспечения актуальности программы.
  
  Программа работает с версиями python не выше 3.11

Расчет термодинамических и геометрических параметров камер жидкостных ракетных двигателей является сложным и трудоемким. Однако современные методы программирования позволяют значительно упростить и автоматизировать этот процесс. Целью работы было создание программы, выполняющее следующие задачи: 1) программа должна проводить расчеты термодинамических параметров, таких как температура газа, давление, скорость продуктов сгорания и другие характеристики, которые существенно влияют на работу камеры ЖРД; 2) путем автоматизированного анализа различных термодинамических параметров программа должна рассчитать основные геометрические параметры и предоставить пользователю результаты для дальнейшего использования; 3) автоматизация расчетов позволяет сократить время на проектирование новых конфигураций камер ЖРД, что в свою очередь способствует повышению общей скорости разработки изделий. 

Самая важная библиотека, которая есть в программе и выполняет все процессы, связанные с термодинамикой – библиотека Cantera. Библиотеке необходимы такие же параметры, что при расчёте в программном комплексе «АСТРА» или «Терра». Дальше программа должна рассчитать равновесное состояние. Для этого используется метод «gas.equilibrate(SP)». Данный метод оптимизирует состояние газа таким образом, чтобы свободная энергия Гиббса была минимизирована, то есть старается свести количество энергии в системе, доступное для совершения работы, к нулю. Оптимизирует таким образом, оставляя давление и энтропию постоянной, потому что изменение происходит именно при заданных давлениях, а камера считается изоэнтропической. То есть по сути процесс расчёта аналогичен программным комплексам «Астра» и «Терра». 

Программа DEDAL, использующая библиотеку «Cantera», выполняет следующие задачи: 1) Автоматизированное задание исходных данных: На выбор в программе даны 15 видов окислителей и 7 горючих с вложенных в них энтальпией и стехиометрическим соотношением. Также, при необходимости, можно добавить другие компоненты, при условии, что в составе компонента не находится ничего, кроме водорода, углерода, кислорода и азота. 2) Поиск оптимального коэффициента избытка окислителя: Программа рассчитывает пустотный удельный импульс в большом диапазоне коэффициента избытка окислителя и находит среди них максимальное значение 3) Расчёт геометрии камеры ЖРД: Базируясь на методиках расчёта камер ЖРД, предоставленных при обучении и применяемых для выполнения курсовых проектов, рассчитывается сужающаяся часть (радиусная или радиусно-коническая), камера сгорания (по условному времени пребывания) и расширяющаяся часть (сопло Лаваля). 4) Расчёт потерь на трение. С известной геометрией камеры просчитываются потери на трение и рассеивание. Также, при необходимости, дополнительно рассчитано коническое сопло и его потери соответственно. 

Использование программы DEDAL, написанной на языке на Python с использованием библиотеки Cantera, демонстрирует значительное ускорение и повышение эффективности проектирования благодаря автоматизации расчётов. Сравнение результатов с программой ASTRA показало высокую степень соответствия, что подтверждает точность и надёжность разработанного программного решения. Внедрение программы DEDAL способно существенно ускорить процессы проектирования ЖРД. Это открывает новые перспективы для исследований и разработок в области ракетостроения, способствуя более быстрому внедрению инноваций и сокращению времени от идеи до реализации. В качестве дальнейшего направления развития данного программного комплекса рассматривается возможность реализации и внедрения расчёта теплозащиты и прочности камер ЖРД.



