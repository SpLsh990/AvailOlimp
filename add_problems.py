from control_data_base import Problem
import re


# Функция для добавления нижнего индекса и выделения курсивом переменных
def problem_variable(text):
    text = re.sub(r'\(([^)]+)\)', r'<sub>\1</sub>', text)
    text = re.sub(r'(\d+)', r'<sub>\1</sub>', text)
    return "<em>" + text + "</em>"

#TODO ДОБАВИТЬ ЕЩЕ ЗАДАНИЙ

# Сама функция заполнения базы данных заданиями
def add_problems():
    # Просто физика
    Problem.add_problem(object='physics', title='Неупругий удар',
                        condition=f"""На гладком горизонтальном столе покоятся два бруска: левый массой {problem_variable("m2")} = 0,30 кг, правый массой {problem_variable("m3")} = 0,50 кг. Бруски соединены
        идеальной пружиной жёсткостью {problem_variable("k")} = 200 Н/м.
        Слева по столу без трения скользит снаряд массой {problem_variable("m1")} = 0,20кг со
        скоростью {problem_variable("v0")} = 4,0м/с и центральным абсолютно неупругим образом
        сталкивается с левым бруском. После удара система «снаряд + левый
        брусок» движется как единое целое.<br>Определите скорость {problem_variable("u")} системы «снаряд + левый брусок» сразу после удара.<br>Ответ выразите в м/с, округлив до десятых долей.""",
                        right_answer='1,6', attachment='problems/Inelastic_impact.png')
    Problem.add_problem(object='physics', title='Неупругий удар 2',
                        condition=f"""На гладком горизонтальном столе покоятся два бруска: левый массой {problem_variable("m2")} = 0,30 кг, правый массой {problem_variable("m3")} = 0,50 кг. Бруски соединены
        идеальной пружиной жёсткостью {problem_variable("k")} = 200 Н/м.
        Слева по столу без трения скользит снаряд массой {problem_variable("m1")} = 0,20кг со
        скоростью {problem_variable("v0")} = 4,0м/с и центральным абсолютно неупругим образом
        сталкивается с левым бруском. После удара система «снаряд + левый
        брусок» движется как единое целое.<br>На сколько процентов уменьшилась механическая энергия системы при соударении?<br>Дайте ответ в процентах, округлив до целого числа.""",
                        right_answer='60', attachment='problems/Inelastic_impact.png')
    Problem.add_problem(object='physics', title='Цикл с линейным участком 1',
                        condition=f"""С одним молем идеального одноатомного газа совершают циклический процесс {problem_variable("ABCDA")}, состоящий из двух изохорных процессов {problem_variable("AB")}
        и {problem_variable("CD")}, изобарного процесса {problem_variable("DA")} и процесса {problem_variable("BC")}, в котором давление остаётся пропорциональным объёму ({problem_variable("P = kV")} ). Объём газа в процессе {problem_variable("AB")} равен 9 л, в процессе {problem_variable("CD")} — 21 л, давление в процессе {problem_variable("DA")}
        равно 30 кПа. Максимальное давление газа в цикле равно 210 кПа.
        Во всех расчётах используйте универсальную газовую постоянную
        R = 8,314 Дж/(моль·К).<br>Найдите количество теплоты, отданное газом на участке
        {problem_variable("C → D")}.<br>Ответ выразите в кДж, округлив до сотых долей.""", right_answer='5,67',
                        attachment='')
    Problem.add_problem(object='physics', title='Цикл с линейным участком 2',
                        condition=f"""С одним молем идеального одноатомного газа совершают циклический процесс {problem_variable("ABCDA")}, состоящий из двух изохорных процессов {problem_variable("AB")}
        и {problem_variable("CD")}, изобарного процесса {problem_variable("DA")} и процесса {problem_variable("BC")}, в котором давление
        остаётся пропорциональным объёму ({problem_variable("P = kV")} ). Объёмы газа в изохорных процессах составляет: {problem_variable("V(A)")} = {problem_variable("V(B)")} = 10 л и {problem_variable("V(C)")} = {problem_variable("V(D)")} = 22 л;
        давление в изобарном процессе {problem_variable("DA")} равно {problem_variable("P(A)")} = {problem_variable("P(D)")} = 90 кПа. Во
        всех расчётах используйте универсальную газовую постоянную
        R = 8,314 Дж/(моль·К).
        Экспериментально установлено, что работа газа за один цикл составляет {problem_variable("V(цикла)")} = 1,80 кДж.<br>Определите температуру газа в состоянии {problem_variable("C")}.<br>Ответ выразите в К, округлив до целого числа.
        """, right_answer='873', attachment='')
    Problem.add_problem(object='physics', title='Квадрат из зарядов',
                        condition=f"""В вакууме в вершинах {problem_variable("A")}, {problem_variable("B")} и {problem_variable("C")} квадрата {problem_variable("ABCD")} со стороной {problem_variable("a")} = 40,0 см расположены три одинаковых точечных заряда {problem_variable("q")} = +3,0 мкКл.
        Потенциал на бесконечности принят равным нулю. Действием силы тяжести можно пренебречь. Коэффициент в законе Кулона равен {problem_variable("k")} = 9,0 · 10<sup>9</sup> Н·м<sup>2</sup><br>Какой заряд {problem_variable("q(D)")} нужно поместить в вершину {problem_variable("D")}, чтобы потенциал в центре квадрата стал равен {problem_variable("φ0")} = 477 кВ?<br>Ответ выразите в мкКл, округлив до сотых долей.""",
                        right_answer='5,99', attachment='')
    Problem.add_problem(object='physics', title='Разгон. Движение. Торможение', condition=f"""На сортировочной горке вагон начинает движение из состояния покоя: сначала разгоняется на наклонном участке в течение 6 секунд, затем 9 секунд
        едет по горизонтальному участку с постоянной скоростью, после чего тормозит и останавливается. Известно, что модуль ускорения при торможении в 2
        раза больше, чем на наклонном участке. Суммарный путь вагона от начала
        движения до полной остановки составляет 113 метров.<br>Чему равна скорость вагона на горизонтальном участке?<br>Ответ выразите в м/с, округлив до десятых долей.""",
                        right_answer='8,4', attachment='')
    Problem.add_problem(object='physics', title='После перерезания',
                        condition=f"""На горизонтальном шероховатом столе лежит брусок массой {problem_variable("M")} = 5 кг, соединённый лёгкой нерастяжимой нитью с грузом массой {problem_variable("m")} = 1,5 кг. Нить перекинута через идеальный блок. Систему отпускают из состояния покоя.
        Как только груз опускается на расстояние {problem_variable("s")} = 0,6 м, нить перерезают. Коэффициент трения между бруском и столом составляет {problem_variable("µ")} = 0,25. Ускорение свободного падения примите равным {problem_variable("g")} = 10 м/с<sup>2</sup>.<br>Вычислите среднюю мощность силы натяжения, действующей на брусок, до перерезания нити.<br>Ответ выразите в Вт, округлив до сотых долей.""",
                        right_answer='4,9', attachment='problems/After_cutting.png')
    Problem.add_problem(object='physics', title='После соударения',
                        condition=f"""Гладкий шар массой {problem_variable("m1")} налетает на гладкий шар массой {problem_variable("m2")}
        такого же диаметра, движущийся с той же скоростью {problem_variable("v0")} = 8,7 м/с в противоположном направлении так, как показано на рисунке.
        В результате упругого соударения первый шар отскакивает в направлении, перпендикулярном первоначальному направлению его движения.
        <br>На какой угол {problem_variable("𝛼")}  повернётся вектор скорости второго шара в результате соударения с первым?<br>Дайте ответ в градусах с округлением до целого числа.""",
                        right_answer='131', attachment='problems/After_the_collision.png')
    Problem.add_problem(object='physics', title='Расширяющийся газ',
                        condition=f"""При расширении {problem_variable("𝜈")} = 1 моль идеального одноатомного газа в процессе,
         при котором {problem_variable("pVT = const")} ({problem_variable("p")} – давление, {problem_variable("V")} – объём,
        {problem_variable("T")} – температура газа), им была совершена работа {problem_variable("A")} = 2,74 кДж.
         Начальная температура газа {problem_variable("T1")} = 300 К. Универсальная газовая постоянная {problem_variable("R")} = 8,31 Дж/(моль∙К).
         <br>Во сколько раз изменился объём газа при расширении в данном процессе?<br>Ответ дайте с точностью до сотых долей.""",
                        right_answer='3', attachment='')
    # Просто математика
    """Problem.add_problem(object='math', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='math', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='math', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='math', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='math', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='math', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='math', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='math', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='math', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='math', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='math', title='', condition=f"""""", right_answer='', attachment='')
    """
    # Пвп физика
    Problem.add_problem(object='physics_pvp', title='Два камня', condition=f"""Два камня бросают одновременно навстречу друг другу с одинаковыми
        начальными скоростями {problem_variable("v0")} вдоль прямой, наклонённой под углом {problem_variable("𝛼")} = 30° к горизонту. Первый камень бросают с горизонтальной поверхности земли,
        а второй – с высоты {problem_variable("h")} = 100 м (см. рисунок). На землю камни падают одновременно. Ускорение свободного падения {problem_variable("g")} = 10 м/с<sup>2</sup>.<br>На каком расстоянии {problem_variable("S")} друг от друга приземляются камни?<br>
        Дайте ответ в метрах с округлением до десятых долей.""",
                        right_answer='0', attachment='problems/Stone_ocean.png')
    Problem.add_problem(object='physics_pvp', title='Перекладина',
                        condition=f"""Для перемещения готовых изделий с ленты Л конвейера, движущегося горизонтально со скоростью {problem_variable("v")} = 1,5 м/с, используется неподвижная
        горизонтальная направляющая перекладина 𝐴𝐵, установленная чуть выше ленты и образующая угол {problem_variable("𝛼")} с перпендикуляром к направлению скорости ленты (на рис. вид сверху). Коэффициент трения изделий о ленту конвейера
        равен {problem_variable("𝜇1")} = 0,40, а о направляющую перекладину – {problem_variable("𝜇2")} = 0,30. Считайте, что движение деталей носит поступательный характер, то есть они не вращаются при трении о перекладину.<br>Перекладину устанавливают под углом {problem_variable("𝛼")} = 30°. Считая перекладину достаточно длинной, а ленту достаточно широкой, найдите установившуюся
        скорость {problem_variable("u")} движения изделий вдоль неё.<br>Ответ дайте в см/с с точностью до целого числа.""",
                        right_answer='36', attachment='problems/Crossbar.png')
    Problem.add_problem(object='physics_pvp', title='Полярность, ЭДС, конденсаторы',
                        condition=f"""Электрическая цепь состоит из источника ЭДС с пренебрежимо малым сопротивлением, конденсатора ёмкостью {problem_variable("C")} = 300 мкФ, стрелочного амперметра с сопротивлением
        {problem_variable("𝑅(𝐴)")} = 5 Ом и переключателя П, способного очень быстро менять полярность подключения конденсатора в цепи.
        Полярность меняется с частотой {problem_variable("𝜈")} = 10 Гц, при этом показания амперметра составляют {problem_variable("I")} = 100 мА, а стрелка прибора практически не дрожит.
        Считайте, что показания стрелочного амперметра определяются средней величиной силы тока в цепи.<br>Какова ЭДС {problem_variable("ℰ")} источника?<br>Ответ дайте в вольтах с точностью до десятых долей.""",
                        right_answer='16,7', attachment='problems/Polarity_EMF_capacitors.png')
    """Problem.add_problem(object='physics_pvp', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='physics_pvp', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='physics_pvp', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='physics_pvp', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='physics_pvp', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='physics_pvp', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='physics_pvp', title='', condition=f"""""", right_answer='', attachment='')
    """
    # Пвп математика
    Problem.add_problem(object='math_pvp', title='Арифметическая прогрессия',
                        condition=f"""Арифметическая прогрессия, состоящая из целых чисел, содержит 2{problem_variable("n")} членов. Известно, что разность суммы последних {problem_variable("n")} и суммы первых {problem_variable("n")} членов равна 882.<br>Укажите все возможные значения {problem_variable("n")} в порядке возрастания без пробелов и запятых, если известно, что {problem_variable("n")} > 1""",
                        right_answer='3721', attachment='')
    Problem.add_problem(object='math_pvp', title='Клетки',
                        condition=f"""При каком наименьшем {problem_variable("n")} во все клетки таблицы 4 × 10 можно расставить некоторые из чисел от 1 до {problem_variable("n")}, каждое не более одного раза, так, чтобы любые два соседние по горизонтали или вертикали числа отличались хотя бы в 2 раза?""",
                        right_answer='41', attachment='')
    Problem.add_problem(object='math_pvp', title='Площадь фигуры',
                        condition=f"""В прямоугольнике {problem_variable("ABCD")} со сторонами {problem_variable("AB")} = 10, {problem_variable("BC")} = 12 отметили точку {problem_variable("M")} — середину стороны {problem_variable("CD")}. На отрезке {problem_variable("BM")} отметили точку {problem_variable("P")} так, что {problem_variable("BC")} = {problem_variable("BP")}. Найдите площадь четырехугольника {problem_variable("ABPD")}.<br>Ответ дайте с точностью до сотых долей""",
                        right_answer='87,69', attachment='')
    """Problem.add_problem(object='math_pvp', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='math_pvp', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='math_pvp', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='math_pvp', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='math_pvp', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='math_pvp', title='', condition=f"""""", right_answer='', attachment='')
    Problem.add_problem(object='math_pvp', title='', condition=f"""""", right_answer='', attachment='')
"""
