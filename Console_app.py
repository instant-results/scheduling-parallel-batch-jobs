import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import time

import Michigan
import Pitt_direct
import Pitt_perm
import Common


def close():
    """
    Close window function
    """
    global app_running
    if messagebox.askokcancel("Exit", "Do you want to exit?"):
        app_running = False
        root.destroy()


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


def calculate():
    index = algorithm_dropdown.current() + 1
    algorithm = algorithm_dropdown.get()  # for optional algorithm window name

    print(
        f"==================================\n"
        f"Algorithm: {algorithm}\n"
        f"Scheduling mode: {Common.scheduling_modes[Common.scheduling_mode]}\n"
        f"Output mode: {Common.output_modes[Common.output_mode]}\n"
        f"==================================")

    choices(index)


if __name__ == "__main__":
    root = tk.Tk()
    app_running = True

    root.protocol("WM_DELETE_WINDOW", close)
    root.title("Scheduling parallel batch jobs")
    root.geometry('500x300')
    options = {'padx': 10, 'pady': 10}

    root.resizable(False, False)

    algorithm_list_label = ttk.Label(root, text="Choose an algorithm:")
    algorithm_list_label.grid(column=0, row=0, sticky=tk.W, **options)

    var = tk.StringVar()
    algorithm_dropdown = ttk.Combobox(root, width=34, textvariable=var)
    algorithm_dropdown['values'] = (
        "Permutation-based Pitt",
        "Direct Pitt",
        "Michigan")

    algorithm_dropdown['state'] = 'readonly'
    algorithm_dropdown.grid(column=1, row=0, columnspan=3, **options)

    scheduling_mode_label = ttk.Label(root, text="Scheduling mode")
    scheduling_mode_label.grid(column=0, row=1, sticky=tk.W, **options)

    scheduling_mode_status = ttk.Label(root, text="Status: " + Common.scheduling_modes[Common.scheduling_mode])
    scheduling_mode_status.place(x=150, y=50)

    change_scheduling_mode_button = ttk.Button(root, text="Change", command=lambda: choices(4))
    change_scheduling_mode_button.place(x=300, y=47)

    output_mode_label = ttk.Label(root, text="Output mode")
    output_mode_label.grid(column=0, row=2, sticky=tk.W, **options)

    output_mode_status = ttk.Label(root, text="Status: " + Common.output_modes[Common.output_mode])
    output_mode_status.place(x=150, y=90)

    change_output_mode_button = ttk.Button(root, text="Change", command=lambda: choices(5))
    change_output_mode_button.place(x=300, y=87)

    run_button = tk.Button(root, text="Calculate", command=calculate)
    run_button.grid(column=2, row=3, **options)
    root.mainloop()
