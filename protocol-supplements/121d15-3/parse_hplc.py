import os
import csv
from datetime import date
import tkinter as tk

path = '/Users/nickdiehl/Desktop/Opentrons Internal/Eurofins Onsite'

enter_loop = True
root = tk.Tk()
root.geometry("800x400")
batch_prompt = tk.Label(root, text='HPLC batch barcode:')
sample_prompt = tk.Label(root, text='HPLC sample barcode:')
status = tk.Label(root, text='')
end_label = tk.Label(root, text='')
batch_barcode_entry = tk.Entry(root)
sample_barcode_entry = tk.Entry(root)
first_sample = None
last_sample = None

current_sample_barcode = ''


def retrieve_files(batch, file_name):
    if not batch:
        search_path = path
    else:
        if batch not in os.listdir(path):
            status['text'] = f'invalid batch [{batch}]'
        else:
            search_path = f'{path}/{batch}'

    all_files = [file.lower() for file in os.listdir(search_path)]
    if file_name in all_files:
        return f'{search_path}/{file_name}'
    else:
        return None


def pick_fraction(fraction_data):
    fraction_lengths = []
    for line in fraction_data:
        if line[0].isnumeric():  # valid line?
            length = int(line[3])
            fraction_lengths.append(length)
    fraction_ind = fraction_lengths.index(max(fraction_lengths))
    start_ind = sum(fraction_lengths[:fraction_ind]) + 2
    return start_ind


def parse(file_content):
    content = file_content[39:]
    split_ind = None
    for i, line in enumerate(content):
        if line[:3] == ['', '', '']:
            split_ind = i
            break
    fraction_data = content[3:split_ind]
    well_data = content[split_ind+4:]

    start_ind = pick_fraction(fraction_data)
    wells = [int(line[0]) for line in well_data[start_ind:start_ind+4]]
    vols = [float(line[3])*1000 for line in well_data[start_ind:start_ind+4]]
    return({well: vol for well, vol in zip(wells, vols)})


all_wells = []


def get_barcode():
    global current_sample_barcode
    global first_sample

    current_batch_barcode = batch_barcode_entry.get()
    current_sample_barcode = sample_barcode_entry.get()
    check_file = f'{current_sample_barcode}_fraction report.txt'

    file = retrieve_files(current_batch_barcode, check_file)
    if file:
        output = f'last barcode successfully submitted: [{current_sample_barcode}]'
        if not first_sample:
            first_sample = current_sample_barcode

        with open(file, 'r') as sample_file:
            content = [line.split('\t') for line in sample_file.readlines()]
            all_wells.append(parse(content))
    else:
        output = f'No files found for [{current_sample_barcode}]'

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
    out_file_path = f'{path}/{first_sample}-{last_sample}.csv'

    with open(out_file_path, 'w') as out_file:
        writer = csv.writer(out_file)
        for well_data, well_name in zip(all_wells, well_names[:len(all_wells)]):
            for well, vol in well_data.items():
                writer.writerow([well, well_name, vol])

    all_wells = []
    end_label['text'] = f'File successfully written to [{out_file_path}]'


submit_button = tk.Button(root, text='submit barcode', highlightbackground='blue', command=get_barcode)
end_button = tk.Button(root, text='end and write file', highlightbackground='blue', command=end)
destroy_button = tk.Button(root, text="quit", highlightbackground='blue', command=root.destroy)

batch_prompt.pack()
batch_barcode_entry.pack()
sample_prompt.pack()
sample_barcode_entry.pack()
submit_button.pack()
status.pack()
end_button.pack()
end_label.pack()
destroy_button.pack()
root.mainloop()
