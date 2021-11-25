#### pip install PySimpleGUI
#### https://pysimplegui.readthedocs.io/en/latest/cookbook/
#### usage example: gather input from user
import PySimpleGUI as sg      

layout = [[sg.Text('My one-shot window.')],      
                 [sg.InputText()],      
                 [sg.Submit(), sg.Cancel()]]      

window = sg.Window('Window Title', layout)    

event, values = window.read()    
window.close()

text_input = values[0]    
sg.popup('You entered', text_input)
