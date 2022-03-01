import os
import csv
from datetime import date
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import *

# template_directory = '\\\\us17filp002\\production_data\\DNA\\Application_Data\\Lab\\RedoReplacement'
# output_directory = '\\\\us17filp002\\production_data\\DNA\\Application_Data\\Lab\\RedoReplacement\\RunFiles'
template_directory = '/Users/nickdiehl/protocols/protocol-supplements/121d15-2'
output_directory = '/Users/nickdiehl/protocols/protocol-supplements/121d15-2'

enter_loop = True
root = tk.Tk()
root.geometry("800x400")
plate1_file_prompt = tk.Label(root, text='plate 1 file')
plate1_scan_prompt = tk.Label(root, text='plate 1 scan')
plate1_scan = tk.Entry(root)
plate1_scan.insert(0, '')
plate1_status = tk.Label(root, text='')
tuberack1_scan_prompt = tk.Label(root, text='tuberack 1 scan')
tuberack1_scan = tk.Entry(root)
tuberack1_scan.insert(0, '')
plate2_file_prompt = tk.Label(root, text='plate 2 file')
plate2_scan_prompt = tk.Label(root, text='plate 2 scan')
plate2_scan = tk.Entry(root, text='')
plate2_scan.insert(0, '')
plate2_status = tk.Label(root, text='')
tuberack2_scan_prompt = tk.Label(root, text='tuberack 2 scan')
tuberack2_scan = tk.Entry(root)
tuberack2_scan.insert(0, '')
volume_prompt = tk.Label(root, text='volume (in ul)')
volume = tk.Entry(root)
volume.insert(0, '200')
status = tk.Label(root, text='')
end_label = tk.Label(root, text='')
first_sample = None
last_sample = None

file_map = {
    '96 0.5ml plate': 'greiner_500_redoreplacementpicking.ot2.apiv2.py',
    '96 1.2ml plate': 'greiner_1000_redoreplacementpicking.ot2.apiv2.py',
    '96 2.2ml plate': 'irish_2200_redoreplacementpicking.ot2.apiv2.py',
    '384 0.24ml plate': 'greiner_384_redoreplacementpicking.ot2.apiv2.py'
}
options = file_map.keys()
dropdown_value = tk.StringVar(root)
dropdown_value.set('Select plate type')

# initial menu text
dropdown = tk.OptionMenu(root, dropdown_value, *options)

current_sample_barcode = ''


def select_file1():
    filename = fd.askopenfilename()
    return filename


def update_file1_status(text):
    plate1_status['text'] = text


def select_file2():
    filename = fd.askopenfilename()
    return filename


def update_file2_status(text):
    plate2_status['text'] = text


def button1_press():
    update_file1_status(select_file1())


def button2_press():
    update_file2_status(select_file2())


# open button
plate1_file_button = tk.Button(
    root,
    text='open a file',
    command=button1_press
)
plate2_file_button = tk.Button(
    root,
    text='open a file',
    command=button2_press
)


def extract_csv_contents(file_path, var_name):
    content = []
    with open(file_path, 'r') as csv_file:
        all_lines = [line for line in csv_file.readlines()]
        for i, line in enumerate(all_lines):
            if i == 0:
                content.append(f'{var_name} = """{line}')
            elif i == len(all_lines) - 1:
                content.append(f'{line}"""')
            else:
                content.append(line)
    return content


def write_python_protocol(out_file_path, template_path, *args):
    template_contents = []
    with open(template_path, 'r') as template_file:
        for line in template_file.readlines():
            template_contents.append(line)
    with open(out_file_path, 'w') as out_file:
        for content in args:
            out_file.writelines(content)
            out_file.writelines(['\n\n'])
        out_file.writelines(template_contents)


def end():

    if plate1_status['text'] != '':
        if plate2_status['text'] != '':
            name_part_1 = plate1_status['text'].split('.txt')[0].split('\\')[-1]
            name_part_2 = plate2_status['text'].split('.txt')[0].split('\\')[-1]
            outfile_name = f"{name_part_1}-{name_part_2}.py"
            content1 = extract_csv_contents(plate1_status['text'], 'input_file')
            content2 = extract_csv_contents(plate2_status['text'], 'input_file2')
            plate1_info = [f"plate_scan = '{plate1_scan.get()}'"]
            plate2_info = [f"plate_scan2 = '{plate2_scan.get()}'"]
            tuberack1_info = [f"tuberack_scan1 = '{tuberack1_scan.get()}'"]
            tuberack2_info = [f"tuberack_scan2 = '{tuberack2_scan.get()}'"]
        else:
            name_part_1 = plate1_status['text'].split('.txt')[0].split('\\')[-1]
            outfile_name = f"{name_part_1}.py"
            content1 = extract_csv_contents(plate1_status['text'], 'input_file')
            content2 = ['input_file2 = ""']
            plate1_info = [f"plate_scan = '{plate1_scan.get()}'"]
            plate2_info = ["plate_scan2 = ''"]
            tuberack1_info = [f"tuberack_scan1 = '{tuberack1_scan.get()}'"]
            tuberack2_info = ["tuberack_scan2 = ''"]

        if dropdown_value.get() == 'Select plate type':
            status['text'] = 'Please select plate type'
        template = file_map[dropdown_value.get()]
        template_path = f'{template_directory}\\{template}'
        out_file_path = f"{output_directory}\\{outfile_name}"
        volume_info = [f"default_disposal_vol = {volume.get()}\n", f"default_transfer_vol = {volume.get()}"]
        write_python_protocol(out_file_path, template_path,
                              content1,
                              content2,
                              plate1_info,
                              plate2_info,
                              tuberack1_info,
                              tuberack2_info,
                              volume_info)

        status['text'] = f'File successfully written to [{out_file_path}]'


end_button = tk.Button(root, text='create protocol file', highlightbackground='blue', command=end)
destroy_button = tk.Button(root, text="quit", highlightbackground='blue', command=root.destroy)

plate1_file_prompt.grid(row=0, column=0)
plate1_file_button.grid(row=0, column=1)
plate1_scan_prompt.grid(row=1, column=0)
plate1_scan.grid(row=1, column=1)
plate1_status.grid(row=0, column=2, columnspan=5)
tuberack1_scan_prompt.grid(row=1, column=3)
tuberack1_scan.grid(row=1, column=4)
plate2_file_prompt.grid(row=2, column=0)
plate2_file_button.grid(row=2, column=1)
plate2_scan_prompt.grid(row=3, column=0)
plate2_scan.grid(row=3, column=1)
plate2_status.grid(row=2, column=2, columnspan=5)
tuberack2_scan_prompt.grid(row=3, column=3)
tuberack2_scan.grid(row=3, column=4)
volume_prompt.grid(row=4, column=0)
volume.grid(row=4, column=1)
dropdown.grid(row=5, column=1)
end_label.grid(row=6, column=1)
status.grid(row=8, column=1, columnspan=4)
end_button.grid(row=6, column=3)
end_label.grid(row=9, column=3)
destroy_button.grid(row=7, column=3)
root.mainloop()
