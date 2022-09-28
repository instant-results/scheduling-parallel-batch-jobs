import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
from tkinter.messagebox import showerror

import Michigan
import Pitt_direct
import Pitt_perm
import Common
import plot_creating


def close(win):
    """
    Close window function
    """
    global app_running
    if messagebox.askokcancel("Exit", "Do you want to exit?"):
        app_running = False
        win.destroy()


def choices(x, num_iter=1):
    if x == 1:
        Pitt_perm.main(num_iter)
        time.sleep(1)
    elif x == 2:
        Pitt_direct.main(num_iter)
        time.sleep(1)
    elif x == 3:
        Michigan.main(num_iter)
        time.sleep(1)
    elif x == 4:
        Common.scheduling_mode = Common.ENERGY_MODE if Common.scheduling_mode == Common.MAKESPAN_MODE else Common.MAKESPAN_MODE
        scheduling_mode_status['text'] = "Status: " + Common.scheduling_modes[Common.scheduling_mode]
    elif x == 5:
        Common.output_mode = (Common.output_mode + 1) % len(Common.output_modes)
        output_mode_status['text'] = "Status: " + Common.output_modes[Common.output_mode]
    else:
        print('Wrong choice')
        time.sleep(1)


def change_state():
    if run_button['state'] == "DISABLED":
        run_button.config(text="Calculate")
        run_button['state'] = "ACTIVE"
    else:
        run_button.config(text="Calculating...")
        run_button['state'] = "DISABLED"

    main.update_idletasks()
    main.update()


def calculate(algorithm_variables, list_algorithms):
    """
    Getting all needed parameters and activating calculation process with particular algorithm
    """

    try:
        if validate_iterations():
            raise ValueError
        num_iter = current_num_iter.get()
        chosen_alg = algorithm_variables.get()
        index = int(list_algorithms.get(chosen_alg))
        if type(index) == 'NonType':
            raise TypeError

        change_state()

        parameters = f"Algorithm: {chosen_alg}\n" \
                     f"Scheduling mode: {Common.scheduling_modes[Common.scheduling_mode]}\n" \
                     f"Output mode: {Common.output_modes[Common.output_mode]}\n"
        print(parameters)

        choices(index, num_iter)

        list_alg = ['pitt_perm', 'pitt_direct', 'michigan']

        result_window = tk.Toplevel(main)
        result_window.title("Results")
        result_window.geometry('800x600')
        plot_creating.create_plot(list_alg[index-1], parameters, result_window)

        plot_creating.draw_schedule(list_alg[index - 1])

        change_state()

    except TypeError:
        showerror(title="Error!", message="You need to choose an algorithm!")
    except ValueError:
        showerror(title="Error!", message="Number of iterations must be an INTEGER in range from 1 to 100!")


def get_current_value():
    return '{}'.format(current_num_iter.get())


def get_max_sum_in_row(tab2d):
    max = 0
    max_machine_lp = 0;
    for row in tab2d:
        sum = 0
        for pair in row:
            if pair[0] > max_machine_lp:
                max_machine_lp = pair[0]
            sum = sum + pair[1]
        if sum > max:
            max = sum
    return max, max_machine_lp + 1


def generate_colors(size):
    from random import randint
    colors = []
    for i in range(size):
        colors.append('#%06X' % randint(0, 0xFFFFFF))
    return colors


def validate_iterations():
    try:
        value = int(iter_num_var.get())
        if 0 >= value or value > 100:
            return True
    except ValueError:
        return True
    return False


if __name__ == "__main__":
    app_title = "Genetic algorithm simulator"
    app_running = True
    options = {'padx': 15, 'pady': 15}

    main = tk.Tk()
    main.protocol("WM_DELETE_WINDOW", lambda: close(main))

    main.title(app_title)
    main.geometry('800x550')
    style = ttk.Style(main)

    main.tk.call('source', 'azure/azure.tcl')
    style.theme_use('azure')

    main.resizable(False, False)

    current_num_iter = tk.IntVar()

    left_frame = ttk.Frame(main)
    left_frame.grid(column=0, row=0, padx=10, pady=10)

    middle_frame = ttk.Frame(main)
    middle_frame.grid(column=1, row=0, sticky=tk.N, padx=10, pady=10)

    right_frame = ttk.Frame(main)
    right_frame.grid(column=2, row=0, sticky=tk.N, padx=10, pady=10)

    algorithm_frame = ttk.LabelFrame(left_frame, text='Choose an algorithm')
    algorithm_frame.grid(column=0, row=0, **options)

    algorithm_var = tk.StringVar()
    algorithms = {'Permutation-based Pitt': '1', 'Direct Pitt': '2', 'Michigan': '3'}

    grid_row = 0
    for algorithm in algorithms:
        radio = ttk.Radiobutton(algorithm_frame, text=algorithm, value=algorithm, variable=algorithm_var)
        radio.grid(column=0, row=grid_row, sticky=tk.W, ipadx=10, ipady=10, padx=10)

        grid_row += 1

    scheduling_mode_frame = ttk.Labelframe(left_frame, text="Scheduling mode")
    scheduling_mode_frame.grid(column=0, row=1, sticky=tk.NSEW, **options)

    scheduling_mode_status = ttk.Label(scheduling_mode_frame, width=23, anchor=tk.CENTER,
                                       text="Status: " + Common.scheduling_modes[Common.scheduling_mode])
    scheduling_mode_status.grid(column=0, row=0, **options)

    change_scheduling_mode_button = ttk.Button(scheduling_mode_frame, text="Change", command=lambda: choices(4))
    change_scheduling_mode_button.grid(column=0, row=1, **options)

    output_mode_frame = ttk.Labelframe(left_frame, text="Output mode")
    output_mode_frame.grid(column=0, row=2, sticky=tk.NSEW, **options)

    output_mode_status = ttk.Label(output_mode_frame, width=23, anchor=tk.CENTER,
                                   text="Status: " + Common.output_modes[Common.output_mode])
    output_mode_status.grid(column=0, row=0, sticky=tk.NSEW, **options)

    change_output_mode_button = ttk.Button(output_mode_frame, text="Change", command=lambda: choices(5))
    change_output_mode_button.grid(column=0, row=1, **options)

    iterations_num_frame = ttk.Labelframe(middle_frame, text="Simulation size")
    iterations_num_frame.grid(column=1, row=0, **options)

    calculate_btn_frame = ttk.Frame(middle_frame)
    calculate_btn_frame.grid(column=1, row=1, sticky=tk.NSEW, **options)

    current_number_iterations = ttk.Label(iterations_num_frame, text=f'Enter the number of iterations:')
    current_number_iterations.grid(column=1, row=0, sticky=tk.NSEW, **options)

    iter_num_var = ttk.Entry(iterations_num_frame, textvariable=current_num_iter, justify="right")
    iter_num_var.grid(column=1, row=1, **options)

    run_button = ttk.Button(calculate_btn_frame, text="Calculate", style='Accentbutton',
                            command=lambda: calculate(algorithm_var, algorithms), width=30)
    run_button.grid(column=1, row=1, **options)

    data_generator = ttk.LabelFrame(right_frame, text="Data Generator")
    data_generator.grid(column=0, row=0, **options)

    lab = ttk.Label(data_generator, text='Generator')
    lab.grid(column=0, row=0, **options)

    main.mainloop()

