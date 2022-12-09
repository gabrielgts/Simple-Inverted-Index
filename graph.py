from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Graph:
    def __init__(self, dictionary, canvas):
        self.dictionary = dictionary
        self.canvas = canvas
        self.draw_figure()

    def plot_graph(self):
        x, y = zip(*self.dictionary)
        plt.plot(range(len(y)), y)
        plt.xlabel('Posição')
        plt.ylabel('Frequência')
        plt.title('Meu Dicionário')
        return plt.gcf()


    def draw_figure(self):
        figure = self.plot_graph()
        figure_canvas_agg = FigureCanvasTkAgg(figure, self.canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg
