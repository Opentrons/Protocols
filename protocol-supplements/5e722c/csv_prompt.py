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

template = """# metadata
metadata = {
    'protocolName': 'Normalization',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    # labware
    source_plate = ctx.load_labware('greinerbioone_96_wellplate_343ul', '1',
                                    'source plate')
    norm_plate = ctx.load_labware('greinerbioone_96_wellplate_343ul', '2',
                                  'normalization plate')
    buffer = ctx.load_labware('nest_12_reservoir_15ml', '3',
                              'buffer (channel 1)').wells()[0]
    tipracks20 = [
        ctx.load_labware('opentrons_96_tiprack_20ul', slot)
        for slot in ['4', '7']]
    tipracks300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['5', '8']]

    # pipette
    p20 = ctx.load_instrument('p20_single_gen2', 'left', tip_racks=tipracks20)
    p300 = ctx.load_instrument('p300_single_gen2', 'right',
                               tip_racks=tipracks300)

    # data
    data = [
        [val.strip().upper() for val in line.split(',')]
        for line in INPUT_CSV.splitlines()][1:]

    def get_sample_volume(initial_concentration):
        factor = initial_concentration/DESIRED_CONCENTRATION
        return round(TOTAL_VOLUME/factor, 2)

    # pre-load volume data
    well_data = {}
    for line in data:
        print(line)
        well_name = line[1]
        conc = float(line[9])
        sample_vol = get_sample_volume(conc)
        well_data[well_name] = {
            'sample-vol': sample_vol,
            'buffer-vol': TOTAL_VOLUME - sample_vol
        }

    # pre-transfer buffer with one tip
    for well_name in well_data.keys():
        buffer_vol = well_data[well_name]['buffer-vol']
        pip = p20 if buffer_vol < 20 else p300
        if not pip.has_tip:
            pip.pick_up_tip()
        pip.transfer(buffer_vol, buffer, norm_plate.wells_by_name()[well_name],
                     new_tip='never')
    [pip.drop_tip() for pip in [p20, p300] if pip.has_tip]

    # transfer sample and mix once
    for well_name in well_data.keys():
        sample_vol = well_data[well_name]['sample-vol']
        pip = p20 if buffer_vol < 20 else p300
        pip.transfer(sample_vol, source_plate.wells_by_name()[well_name],
                     norm_plate.wells_by_name()[well_name],
                     mix_after=(1, pip.min_volume))
"""


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


def write_python_protocol(out_file_path, *args):
    global template
    template_contents = [line for line in template.splitlines()]
    with open(out_file_path, 'w') as out_file:
        for content in args:
            out_file.writelines(content)
            out_file.writelines(['\n\n'])
        for line in template_contents:
            out_file.writelines(line)


def parse_file_name(file_name):
    if '.txt' in file_name:
        return f'{file_name.split(".txt")[0]}.py'
    elif '.csv' in file_name:
        return f'{file_name.split(".csv")[0]}.py'
    else:
        return f'{file_name}.py'


def end():

    outfile_path = parse_file_name(source1_status['text'])
    content1 = extract_csv_contents(source1_status['text'], 'INPUT_CSV')
    content2 = [f'TOTAL_VOLUME = {volume.get()}  # ul']
    content3 = [f'DESIRED_CONCENTRATION = {conc.get()}  # ug/ml']
    write_python_protocol(outfile_path, content1, content2, content3)

    status['text'] = f'File successfully written to [{outfile_path}]'


def reset():
    source1_status['text'] = ''
    volume.delete(0, END)
    conc.delete(0, END)
    status['text'] = ''


end_button = tk.Button(root, text='create protocol file', highlightbackground='blue', command=end)
reset_button = tk.Button(root, text='reset', highlightbackground='blue', command=reset)
destroy_button = tk.Button(root, text='quit', highlightbackground='blue', command=root.destroy)

source1_file_prompt.grid(row=0, column=0)
source1_file_button.grid(row=0, column=1)
source1_status.grid(row=0, column=2, columnspan=3)
volume_prompt.grid(row=1, column=0)
volume.grid(row=1, column=1)
conc_prompt.grid(row=2, column=0)
conc.grid(row=2, column=1)
end_button.grid(row=3, column=0)
reset_button.grid(row=4, column=0)
status.grid(row=5, column=0, columnspan=2)
destroy_button.grid(row=6, column=0)
root.mainloop()
