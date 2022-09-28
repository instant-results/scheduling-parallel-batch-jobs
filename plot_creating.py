import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import re
from random import randint


def create_plot(name, parameters, window):

    fig = plt.figure(figsize=(5, 4), dpi=100)
    plot = fig.add_subplot()

    with open(f'results/data_to_plot_{name}.csv', newline='') as csvfile:

        data = csv.DictReader(csvfile, delimiter=';')
        values = []
        for row in data:
            float_value = float(row['best_makespan'])
            values.append(float_value)

        box_plot_data = values
        plot.boxplot(box_plot_data)

        plt.title(parameters, fontsize=10)

        # Create a canvas widget from the figure
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


def generate_colors(size):
    colors = []
    for i in range(size):
        colors.append('#%06X' % randint(0, 0xFFFFFF))
    return colors

def get_max_task_id(tab2d):
    max_id = 0
    for row in tab2d:
        for task_id in row:
            if task_id > max_id:
                max_id = task_id
    return max_id

def parse_output(name):
    tasks_ret = []
    times_ret = []
    with open(f'results/output_{name}.csv', newline='') as csvfile:
        row_lp = 0
        for row in csvfile:
            row_lp = row_lp + 1
            if row_lp <= 2:
                continue

            times_tmp = []
            tasks_tmp = []
            row_splited = row.split(';')

            for t in row_splited:
                pair = re.findall(r"\d+\.*\d*", t)
                if len(pair) <= 1:
                    continue
                tasks_tmp.append(int(pair[0]))
                times_tmp.append(float(pair[1]))
            tasks_ret.append(tasks_tmp)
            times_ret.append(times_tmp)
    return tasks_ret, times_ret

def sum_columns_on_left(tab):
    ret = []
    for row in tab:
        sum_on_left = 0
        new_row = []
        for col in range(len(row)):
            new_row.append(sum_on_left + row[col])
            sum_on_left = sum_on_left + row[col]
        ret.append(new_row)
    return ret

def max_sum_in_row(tab2d):
    max_val = 0
    for row in tab2d:
        sum_row = 0
        for col in row:
            sum_row = sum_row + col
        if sum_row > max_val:
            max_val = sum_row
    return max_val

def draw_schedule(name):
    tasks, times = parse_output(name)
    times_cum = sum_columns_on_left(times)
    max_task_id = get_max_task_id(tasks)
    colors = generate_colors(max_task_id + 1)

    fig, ax = plt.subplots(figsize=(14, 8), label='Schedule')
    fig.subplots_adjust(left=.05, right=.99, bottom=0.05, top=1)
    ax.invert_yaxis()
    ax.xaxis.set_visible(True)
    ax.set_xlim(0, max_sum_in_row(times))

    for row in range(len(times)):
        for j in range(len(times[row])):
            starts = times_cum[row][j] - times[row][j]
            ax.barh('M' + str(row), times[row][j], left=starts, height=0.8, color=colors[tasks[row][j]])
            x_pos = times_cum[row][j] - (times[row][j] / 2)
            ax.text(x_pos, row, tasks[row][j], ha="center", va="center", color="black", size=9 )

    fig.show()
