import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


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
