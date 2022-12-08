from bs4 import BeautifulSoup
from database import Database
from invertedindex import InvertedIndex
from matplotlib import pyplot as plt
import plotly.express as px
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

base_path = './corpus'

def getHTMLdocument(url):
   with open('{}/{}'.format(base_path, url), encoding='ISO-8859-1') as fp:
    return BeautifulSoup(fp, 'html.parser')

def plot_graph(dictionary):
    x, y = zip(*dictionary)
    plt.plot(range(len(y)), y)
    plt.xlabel('Posição')
    plt.ylabel('Frequência')
    plt.title('Meu Dicionário')
    return plt.gcf()

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def index_site(site_index, index):
    id = 1
    index.index_document({
        'id': id,
        'text': site_index.get_text()
    })

    for item in site_index.select('a'):
        id += 1
        item_link = item.get('href') if item else None
        try:
            content = getHTMLdocument(item_link)

            index.index_document({
                'id': id,
                'text': content.get_text(),
            })
        except FileNotFoundError:
            continue
    return index

def search_window(index):
    names, ocorrencies = zip(*index)

    layout = [[sg.Text('UEMG Search')],
              [sg.Input(size=(200, 1), enable_events=True, key='-INPUT-')],
              [sg.Listbox(names, size=(200, 10),
                          enable_events=True, key='-LIST-')],
              [sg.Canvas(size=(200, 450), key='-CANVAS-')],
              [sg.Button('Exit')]]

    window = sg.Window('UEMG Search', layout, finalize=True)

    draw_figure(window['-CANVAS-'].TKCanvas, plot_graph(index))

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if values['-INPUT-'] != '':
            search = values['-INPUT-']
            new_values = [x for x in names if search in x]
            window['-LIST-'].update(new_values)
        else:
            window['-LIST-'].update(names)
        if event == '-LIST-' and len(values['-LIST-']):
            sg.popup('Selected ', values['-LIST-'])

    window.close()


def main():
    html_soup = getHTMLdocument('index.html')

    db = Database()
    index = InvertedIndex(db)

    index_site(html_soup, index)

    search_window(index.get_data_frame().items())

main()
