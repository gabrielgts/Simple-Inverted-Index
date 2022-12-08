import PySimpleGUI as sg

names = ['Roberta', 'Kylie', 'Jenny', 'Helen',
         'Andrea', 'Meredith', 'Deborah', 'Pauline',
         'Belinda', 'Wendy']

layout = [[sg.Text('UEMG Search')],
          [sg.Input(size=(200, 1), enable_events=True, key='-INPUT-')],
          [sg.Listbox(names, size=(200, 20), enable_events=True, key='-LIST-')],
          [sg.Button('Exit')]]

window = sg.Window('UEMG Search', layout)
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