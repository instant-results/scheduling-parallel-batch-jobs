import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
from tkinter.messagebox import showerror

import Michigan
import Pitt_direct
import Pitt_perm
import Common


def close(win):
    """
    Close window function
    """
    global app_running
    if messagebox.askokcancel("Exit", "Do you want to exit?"):
        app_running = False
        win.destroy()


def choices(x):
    if x == 1:
        Pitt_perm.main(),
        time.sleep(1)
    elif x == 2:
        Pitt_direct.main(),
        time.sleep(1)
    elif x == 3:
        Michigan.main(),
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


def calculate(algorithm_variables, list_algorithms):
    """
    Getting all needed parameters and activating calculation process with particular algorithm
    """
    try:
        chosen_alg = algorithm_variables.get()
        index = int(list_algorithms.get(chosen_alg))
        if type(index) == 'NonType':
            raise TypeError

        print(
            f"Algorithm: {chosen_alg}\n"
            f"Scheduling mode: {Common.scheduling_modes[Common.scheduling_mode]}\n"
            f"Output mode: {Common.output_modes[Common.output_mode]}\n")

        choices(index)

    except TypeError:
        showerror(title="Error!", message="You need to choose an algorithm!")

    result_window = tk.Toplevel(main)
    result_window.title("Results")
    result_window.geometry('800x600')


def get_current_value():
    return '{}'.format(current_num_iter.get())


def slider_change(event):
    current_number_iterations.configure(text=f"Number of iterations: {get_current_value()}")


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

    current_number_iterations = ttk.Label(iterations_num_frame, text=f'Number of iterations: {1}')
    current_number_iterations.grid(column=1, row=1, sticky=tk.NSEW, **options)

    iter_num_scale = ttk.Scale(iterations_num_frame, from_=1, to=100, orient='horizontal', command=slider_change,
                               variable=current_num_iter, length=200)
    iter_num_scale.grid(column=1, row=0, **options)

    run_button = ttk.Button(calculate_btn_frame, text="Calculate", style='Accentbutton',
                            command=lambda: calculate(algorithm_var, algorithms), width=30)
    run_button.grid(column=1, row=1, **options)

    data_generator = ttk.LabelFrame(right_frame, text="Data Generator")
    data_generator.grid(column=0, row=0, **options)

    lab = ttk.Label(data_generator, text='Generator')
    lab.grid(column=0, row=0, **options)

    main.mainloop()
