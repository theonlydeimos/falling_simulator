import tkinter as tk
import matplotlib
import math

matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def show_param_window():
    global is_win_shown
    global parameters

    parameters = ['' for _ in range(len(parameters_names))]

    if not is_win_shown:

        is_win_shown = True
        input_fields = []

        parameter_dialog = tk.Toplevel(root)
        parameter_dialog.geometry('500x500')
        parameter_dialog.title("Ввод параметров")

        bt_save_inputs = tk.Button(parameter_dialog, text="Сохранить данные", width=20, height=2,
                                   command=lambda: save_inputs(parameter_dialog, input_fields),
                                   font=("Helvetica", "15"))

        for param_name in parameters_names:
            label = tk.Label(parameter_dialog, text=f"{param_name}:", font=("Helvetica", "15"))
            label.pack()
            entry = tk.Entry(parameter_dialog)
            entry.pack()
            input_fields.append(entry)

        bt_save_inputs.pack()


def save_inputs(window, inputs):
    global parameters
    global is_inputs_ok
    global is_win_shown

    is_inputs_ok = True
    new_parameters = []
    # global is_error_shown
    # error_text = tk.Label(window, text='Введите числовые параметры.', fg="#B91818", font=("Helvetica", "15"))

    for i, item in enumerate(inputs):
        item = item.get().replace(',', '.')
        if item != '':
            try:
                # parameters[i] = float(item)
                new_parameters.append(float(item))
            except ValueError:
                is_inputs_ok = False
        else:
            is_inputs_ok = False
        #     if not is_error_shown:
        #         error_text.pack()
        #         is_error_shown = True

    if is_inputs_ok:
        window.destroy()
        is_win_shown = False
        parameters = new_parameters
        get_positions()
    print(parameters)


def get_positions():
    global falling_time

    if parameters != ['' for _ in range(len(parameters_names))]:
        y = parameters[0]
        velocity0 = 0

        while y > 0:
            air_force = (parameters[3] * parameters[2] * parameters[4] * velocity0) / 2
            air_acceleration = air_force / parameters[1]  # II закон Ньютона
            acceleration = air_acceleration - (-1 * parameters[5])

            velocity = velocity0 + acceleration * dt
            y = y - (velocity * dt) - ((acceleration * dt ** 2) / 2)
            if y >= 0:
                positions.append(y)
            velocity0 = velocity

    print(f'positions {positions}')
    falling_time = round(len(positions) * dt, 3)
    print(f'falling time {falling_time}s')


def start_animation():
    if parameters != ['' for _ in range(len(parameters_names))]:
        canvas.delete('all')
        current_height = tk.Label(frame_animation, text=f'Текущая высота: {parameters[0]}м')
        current_height.grid()
        body = canvas.create_oval(597, 5, 651, 55, fill='black')
        scale = round(648 / parameters[0], 5)
        ball_id = None
        index = 0

        def animate():
            isOutOfCanvas = False
            nonlocal index, ball_id, body
            canvas.delete(body)
            if ball_id is not None:
                canvas.delete(ball_id)
            if index < len(positions):
                new_height = (parameters[0] - positions[index]) * scale
                if new_height + 51 > 648:  # Если мячик пытается выйти за границы холста
                    canvas.create_oval(597, 5 + (parameters[0] - positions[index - 1]) * scale, 651,
                                       55 + (parameters[0] - positions[index - 1]) * scale, fill='black')
                    current_height['text'] = 'Текущая высота: 0м'
                    print(current_height['text'] + '*')
                    isOutOfCanvas = True
                    return
                ball_id = canvas.create_oval(597, 5 + new_height, 651, 55 + new_height, fill='black')
                lll = len(positions)
                if not isOutOfCanvas:
                    current_height['text'] = f'Текущая высота: {round(positions[index], 2)}м'
                print(current_height['text'])
                index += 1
                root.after(int(dt * 1000), animate)

        animate()


def show_more_info_window():
    global max_velo

    info_window = tk.Toplevel(root)
    info_window.geometry('700x700')
    info_window.title("Подробные данные")

    frame_top = tk.Frame(info_window, width=700, height=100, bg='#FBFDEE')
    frame_top.pack(fill=tk.X)

    title_info_win_label = tk.Label(frame_top, text="Подробные данные", font=('Trebuchet MS', 26, "bold"), bg='#FBFDEE',
                                    anchor='center')
    title_info_win_label.pack()

    time_falling_text = f'Время падения: {falling_time} секунд;'
    time_falling_label = tk.Label(frame_top, text=time_falling_text, font=('Trebuchet MS', 20), bg='#FBFDEE',
                                  anchor='w')
    time_falling_label.pack(side=tk.LEFT, fill=tk.Y)

    max_velo = round(math.sqrt((2 * parameters[1] * parameters[5]) / (parameters[4] * parameters[2] * parameters[3])),
                     3)
    max_velo_text = f'Предельная скорость: {max_velo} м/с'
    max_velo_label = tk.Label(frame_top, text=max_velo_text, font=('Trebuchet MS', 20), bg='#FBFDEE',
                              anchor='w')
    max_velo_label.pack(side=tk.BOTTOM, fill=tk.Y)

    frame_middle = tk.Frame(info_window, width=700, height=500, bg='#FBFDEE')
    frame_middle.pack(fill=tk.X)

    fig = Figure(figsize=(5, 5), dpi=100)
    axes = fig.add_subplot(111)

    # print(get_pos_before_zero(positions))
    # y_graph_list = get_pos_before_zero(positions)
    print(parameters)
    y_graph_list = positions
    t_graph_list = [dt * i for i in range(len(positions))]
    axes.plot(t_graph_list, y_graph_list)

    axes.set_title('Зависимость координаты тела от времени')
    axes.set_xlabel('Время, с')
    axes.set_ylabel('Высота, м')

    canvas = FigureCanvasTkAgg(fig, master=frame_middle)
    canvas.draw()

    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


parameters_names = ['Высота падения [м]', 'Масса тела [кг]', 'Лобовая площадь тела [м2]',
                    'Коэффициент обтекаемости тела [Н*с2/(м*кг)]', 'Плотность среды [кг/м3]',
                    'Ускорение свободного падения [м/с2]']
parameters = ['' for _ in range(len(parameters_names))]
# parameters = [2.055, 0.06518, 0.057, 0.47, 1.18, 9.81]
# parameters = [3.14, 0.00277, 0.011, 0.47, 1.29, 9.81]
is_win_shown = False
is_inputs_ok = True

positions = []
dt = 1 / 24
falling_time = -1
max_velo = -1
get_positions()

WIDTH = 1240
HEIGHT = 1080
RES = f"{str(WIDTH)}x{str(HEIGHT)}"

root = tk.Tk()
root.geometry(RES)  # width x height
root.title('Симулятор падения')
root.resizable(False, False)

frame_title = tk.Frame(root, width=WIDTH + 13, height=HEIGHT * 0.1, bg='#FBFDEE', highlightbackground="#E4E5DC",
                       highlightthickness=2)
frame_title.grid(row=0, column=0)
title_label = tk.Label(frame_title, text="СИМУЛЯТОР ПАДЕНИЯ", font=('Trebuchet MS', 52, "bold"), bg='#FBFDEE')
title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

frame_buttons_top = tk.Frame(root, width=WIDTH, height=HEIGHT * 0.2, bg='#FBFDEE', highlightbackground="#E4E5DC",
                             highlightthickness=2)
frame_buttons_top.grid(row=1, column=0)
bt_start = tk.Button(frame_buttons_top, text='Запустить анимацию', width=50, height=5,
                     font=('Trebuchet MS', 18, "bold"), command=start_animation)
bt_start.grid(row=0, column=0, padx=(71, 0), pady=10)
bt_open_params = tk.Button(frame_buttons_top, text='Параметры', width=50, height=5, font=('Trebuchet MS', 18, "bold"),
                           command=show_param_window)
bt_open_params.grid(row=0, column=1, padx=(0, 71), pady=10)

frame_animation = tk.Frame(root, width=WIDTH, height=HEIGHT * 0.6, bg="#E7F4E6", highlightbackground="#E4E5DC",
                           highlightthickness=1.5)
frame_animation.grid(row=2, column=0)
canvas = tk.Canvas(frame_animation, width=WIDTH, height=HEIGHT * 0.6, bg='white')
canvas.grid(row=0, column=0)

frame_bottom = tk.Frame(root, width=WIDTH, height=HEIGHT * 0.2, bg='#FBFDEE')
frame_bottom.grid(row=3, column=0)
bt_more_info = tk.Button(frame_bottom, text='Подробные данные', width=60, height=5, font=('Trebuchet MS', 18, "bold"),
                         command=show_more_info_window)
bt_more_info.grid(pady=10)

root.mainloop()
