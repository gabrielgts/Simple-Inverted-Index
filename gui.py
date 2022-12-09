import PySimpleGUI as sg
from graph import Graph


class Gui:
    # simple window appearance
    def __init__(self, index):
        self.index = index
        self.search_window()

    def search_window(self):
        names, ocorrencies = zip(*self.index)
        layout = [[sg.Text('UEMG Search')],
                [sg.Input(size=(200, 1), enable_events=True, key='-INPUT-')],
                [sg.Listbox(names, size=(200, 10),
                            enable_events=True, key='-LIST-')],
                [sg.Canvas(size=(200, 450), key='-CANVAS-')],
                [sg.Button('Exit')]]

        window = sg.Window('UEMG Search', layout, finalize=True)
        Graph(self.index, window['-CANVAS-'].TKCanvas)

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
