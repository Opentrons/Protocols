import os
import csv
from datetime import date
import tkinter as tk
from tkinter import *

path = '\\\\us17filp002\\production_data\\DNA\\Application_Data\\Lab\\HPLC_Chromeleon_Batches\\Results_Data'
python_template_path = '\\\\us17filp002\\production_data\\Production_System_Data\\HPLC_PostPur_Picking_Template\\hplcpicking.ot2.apiv2.py'
enter_loop = True
root = tk.Tk()
root.geometry("800x400")
well_num_prompt = tk.Label(root, text='number of wells per fraction:')
batch_prompt = tk.Label(root, text='HPLC batch barcode:')
sample_prompt = tk.Label(root, text='HPLC sample barcode:')
status = tk.Label(root, text='')
end_label = tk.Label(root, text='')
well_num_entry = tk.Entry(root)
well_num_entry.insert(0, "4")
batch_barcode_entry = tk.Entry(root)
sample_barcode_entry = tk.Entry(root)
first_sample = None
last_sample = None
current_sample_barcode = ''
current_batch_barcode = ''


def retrieve_files(batch, file_name):
    if not batch:
        search_path = path
    else:
        if batch not in os.listdir(path):
            status['fg'] = 'red'
            status['text'] = f'invalid batch [{batch}]'
            return None
        else:
            search_path = f'{path}\\{batch}'
    all_files = [file.lower() for file in os.listdir(search_path)]
    if file_name in all_files:
        return f'{search_path}\\{file_name}'
    else:
        return None


def pick_fraction(fraction_data):
    fraction_lengths = {}
    for i, line in enumerate(fraction_data):
        if line[0].isnumeric():
            fraction_num = int(line[2])
            if fraction_num not in fraction_lengths.keys():
                fraction_lengths[fraction_num] = {'length': 1, 'start': i}
            else:
                fraction_lengths[fraction_num]['length'] += 1
    fraction_max = 0
    fraction_to_pick = None
    for fraction_num, data in fraction_lengths.items():
        if data['length'] > fraction_max:
            fraction_max = data['length']
            fraction_to_pick = fraction_num

    return fraction_data[
        fraction_lengths[fraction_to_pick]['start']:
        fraction_lengths[fraction_to_pick]['start'] +
            fraction_lengths[fraction_to_pick]['length']]


def choose_wells(fraction_data):
    window_length = int(well_num_entry.get())
    num_slides = len(fraction_data) - window_length + 1
    if num_slides < 1:
        status['fg'] = 'red'
        status['text'] = f'Too few samples in fraction ({len(fraction_data)})'
        raise Exception(f'Too few samples in fraction ({len(fraction_data)})')
    max_sum = 0
    window_start_ind = 0
    for slide in range(num_slides):
        window_sum = sum([float(line[8]) for line in fraction_data[slide:slide+window_length]])
        if window_sum > max_sum:
            max_sum = window_sum
            window_start_ind = slide
    lines_to_pick = fraction_data[window_start_ind:window_start_ind+window_length]
    wells = [int(line[0]) for line in lines_to_pick]
    if max(wells) - min(wells) >= window_length:
        status['fg'] = 'red'
        status['text'] = f'Wells not adjacent ({wells})'
        raise Exception(f'Wells not adjacent ({wells})')

    vols = [float(line[5])*1000 for line in lines_to_pick]
    return {well: vol for well, vol in zip(wells, vols)}


def find_start_line(content):
    start_ind = None
    for i, line in enumerate(content):
        if line[0].strip().upper() == 'UV_VIS_1':
            start_ind = i + 1
    return start_ind


def parse(file_content):
    start_ind = find_start_line(file_content)
    data = file_content[start_ind:]
    fraction_data = pick_fraction(data)
    chosen_well_data = choose_wells(fraction_data)
    return(chosen_well_data)


all_wells = []

def get_barcode(event):
    global current_sample_barcode
    global first_sample
    global current_batch_barcode
    current_batch_barcode = batch_barcode_entry.get()
    current_sample_barcode = sample_barcode_entry.get()
    check_file = f'{current_sample_barcode}_fraction report.txt'
    file = retrieve_files(current_batch_barcode, check_file)

    if file:
        output = f'last barcode successfully submitted: [{current_sample_barcode}]'
        status['fg'] = 'green'
        if not first_sample:
            first_sample = current_sample_barcode
        with open(file, 'r') as sample_file:
            content = [line.split('\t') for line in sample_file.readlines()]
            all_wells.append(parse(content))
    else:
        if current_sample_barcode:
            output = f'No files found for [{current_sample_barcode}]'
        else:
            output = ''
        status['fg'] = 'red'
    sample_barcode_entry.delete(0, 'end')
    status['text'] = output


def get_barcode_click():
    global current_sample_barcode
    global current_batch_barcode
    global first_sample
    current_batch_barcode = batch_barcode_entry.get()
    current_sample_barcode = sample_barcode_entry.get()
    check_file = f'{current_sample_barcode}_fraction report.txt'
    file = retrieve_files(current_batch_barcode, check_file)

    if file:
        output = f'last barcode successfully submitted: [{current_sample_barcode}]'
        status['fg'] = 'green'
        if not first_sample:
            first_sample = current_sample_barcode
        with open(file, 'r') as sample_file:
            content = [line.split('\t') for line in sample_file.readlines()]
            all_wells.append(parse(content))
    else:
        if current_sample_barcode:
            output = f'No files found for [{current_sample_barcode}]'
        else:
            output = ''
        status['fg'] = 'red'
    sample_barcode_entry.delete(0, 'end')
    status['text'] = output


def end():
    global all_wells
    global last_sample

    def take_lowest_well_index(d):
        return min(d.keys())

    def sort_pick_sets():
        global all_wells
        all_wells = sorted(all_wells, key=take_lowest_well_index)
    well_names = [f'{let}{num}' for num in range(1, 13) for let in 'ABCDEFGH']
    last_sample = current_sample_barcode
    if batch_barcode_entry.get():
        folder = f'{path}\\{batch_barcode_entry.get()}'
    else:
        folder = f'{path}'
    out_file_path = f'{folder}\\{first_sample}-{last_sample}.csv'
    with open(out_file_path, 'w') as out_file:
        writer = csv.writer(out_file)
        for well_data, well_name in zip(all_wells, well_names[:len(all_wells)]):
            for well, vol in well_data.items():
                writer.writerow([well, well_name, vol])
    end_label['text'] = f'File successfully written to [{out_file_path}]'

    with open(python_template_path, 'r') as py_file:
        content = py_file.readlines()

    with open(f'{folder}\\{first_sample}-{last_sample}.py', 'w') as py_out_file:
        py_out_file.writelines('INPUT_FILE = """')

        for i, (well_data, well_name) in enumerate(zip(all_wells, well_names[:len(all_wells)])):
            for well, vol in well_data.items():
                py_out_file.writelines(f'{well},{well_name},{vol}\n')
            if i == len(all_wells) - 1:
                py_out_file.writelines('"""\n\n')

        py_out_file.writelines('DEFAULT_TRANSFER_VOL = 300.0\n\n')

        for c in content:
            py_out_file.writelines(c)

    all_wells = []

root.bind('<Return>', get_barcode)


def reset():
    global first_sample
    global last_sample
    global status
    global end_label
    global current_sample_barcode
    global current_batch_barcode
    status = tk.Label(root, text='')
    end_label = tk.Label(root, text='')
    batch_barcode_entry.delete(0, END)
    sample_barcode_entry.delete(0, END)
    well_num_entry.delete(0, END)
    well_num_entry.insert(0, "4")
    first_sample = None
    last_sample = None
    current_sample_barcode = ''
    current_batch_barcode = ''


submit_button = tk.Button(root, text='submit barcode', highlightbackground='blue', command=get_barcode_click)
end_button = tk.Button(root, text='end and write file', highlightbackground='blue', command=end)
reset_button = tk.Button(root, text='reset all fields', highlightbackground='blue', command=reset)
destroy_button = tk.Button(root, text="quit", highlightbackground='blue', command=root.destroy)
well_num_prompt.pack()
well_num_entry.pack()
batch_prompt.pack()
batch_barcode_entry.pack()
sample_prompt.pack()
sample_barcode_entry.pack()
submit_button.pack()
status.pack()
end_button.pack()
reset_button.pack()
end_label.pack()
destroy_button.pack()
root.mainloop()
