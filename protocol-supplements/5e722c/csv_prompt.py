import os
import csv
from datetime import date
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import *

root = tk.Tk()
root.geometry("800x400")

source1_file_prompt = tk.Label(root, text='source labware 1 file')
source1_status = tk.Label(root, text='')
status = tk.Label(root, text='')
end_label = tk.Label(root, text='')
volume_prompt = tk.Label(root, text='total volume (in ul)')
volume = tk.Entry(root)
conc_prompt = tk.Label(root, text='target concentration (in ug/ul)')
conc = tk.Entry(root)


def select_file1():
    filename = fd.askopenfilename()
    return filename


def update_file1_status(text):
    source1_status['text'] = text


def button1_press():
    update_file1_status(select_file1())


# open button
source1_file_button = tk.Button(
    root,
    text='open a file',
    command=button1_press
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


def parse_file_name(file_name):
    if '.txt' in file_name:
        return f'{file_name.split(".txt")[0]}.py'
    elif '.csv' in file_name:
        return f'{file_name.split(".csv")[0]}.py'
    else:
        return f'{file_name}.py'


def end():

    outfile_path = parse_file_name(source1_status['text'])
    content1 = extract_csv_contents(source1_status['text'], 'input_file')
    content2 = [f'TOTAL_VOLUME = {volume.get()}  # ul']
    content3 = [f'DESIRED_CONCENTRATION = {conc.get()}  # ug/ml']
    write_python_protocol(outfile_path, content1, content2, content3)

    status['text'] = f'File successfully written to [{outfile_path}]'


def reset():
    source1_status['text'] = ''
    volume.delete(0, END)
    conc.delete(0, END)


end_button = tk.Button(root, text='create protocol file', highlightbackground='blue', command=end)
reset_button = tk.Button(root, text='reset', highlightbackground='blue', command=reset)
destroy_button = tk.Button(root, text='quit', highlightbackground='blue', command=root.destroy)

source1_file_prompt.grid(row=0, column=0)
source1_file_button.grid(row=0, column=1)
volume_prompt.grid(row=1, column=0)
volume.grid(row=1, column=1)
conc_prompt.grid(row=2, column=0)
conc.grid(row=2, column=1)
end_button.grid(row=3, column=0)
reset_button.grid(row=4, column=0)
status.grid(row=5, column=0, columnspan=2)
destroy_button.grid(row=6, column=0)
root.mainloop()
