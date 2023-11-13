import PySimpleGUI as sg
import os

# Define the layout of the GUI
layout = [
    [sg.Text('Open Time Clock Export: Payroll CSV'), sg.Input(key='input_file1'), sg.FileBrowse(file_types=(("CSV Files", "*.csv"),))],
    [sg.Text('Quick EMR Export: Provider Productivity CSV'), sg.Input(key='input_file2'), sg.FileBrowse(file_types=(("CSV Files", "*.csv"),))],
    [sg.Text('Output File Path'), sg.Input(key='output_file'), sg.FolderBrowse()],
    [sg.Button('Calculate Productivity', disabled=True, tooltip= "All inputs must be valid.")]
]

# Create the GUI window
window = sg.Window('Productivity Calculator', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if values['input_file1'] and values['input_file2'] and values['output_file']:
        window['Calculate Productivity'].update(disabled=False)
    else:
        window['Calculate Productivity'].update(disabled=True)
    if event == 'Calculate Productivity':
        print('Input File 1:', values['input_file1'])
        print('Input File 2:', values['input_file2'])
        print('Output File:', os.path.join(values['output_file'], 'output.csv'))

# Close the GUI window
window.close()
