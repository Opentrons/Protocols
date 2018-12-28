from opentrons import labware, instruments, modules
from otcustomizers import FileInput

metadata = {
    'protocolName': 'PCR Prep Using CSV Input',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware setup
source_plates = [labware.load('96-flat', slot)
                 for slot in ['1', '2', '3', '4', '5']]
temp_module = modules.load('tempdeck', '6')
output_plate = labware.load('96-flat', '6', share=True)
tiprack_s = labware.load('tiprack-10ul', '7')
tiprack_m = labware.load('tiprack-10ul', '8')

# instrument setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack_s])

m10 = instruments.P10_Multi(
    mount='right',
    tip_racks=[tiprack_m])

# reagent setup
mastermixes = [col for col in output_plate.cols('11', to='12')]

csv_example = """
Destination Well,Source Plate,Source well
A01,PLATE_1,B03
A01,PLATE_2,C06
A01,PLATE_3,H08
A01,PLATE_4,F05
A01,PLATE_5,G01
B01,PLATE_1,D05
B01,PLATE_2,A02
B01,PLATE_3,C07
B11,PLATE_4,D07
"""


def csv_string_to_list(csv_string):
    global source_plates, output_plate
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    dest_list = []
    source_list = []
    for line in info_list[1:]:
        dest_well = line[0]
        source_plate = line[1]
        source_well = line[2]
        if dest_well[1] == '0':
            dest_well = dest_well[:1] + dest_well[2:]
        dest_list.append(output_plate.wells(dest_well))
        source_plate = source_plates[int(source_plate.split('_')[1])-1]
        if source_well[1] == '0':
            source_well = source_well[:1] + source_well[2:]
        source_list.append(source_plate.wells(source_well))
    return dest_list, source_list


def run_custom_protocol(
    desired_temperature: float=4,
    sample_volume: float=5,
    mastermix_volume: float=5,
    CSV_file: FileInput=csv_example
        ):

    temp_module.set_temperature(desired_temperature)
    temp_module.wait_for_temp()

    destination_well_list, source_well_list = csv_string_to_list(CSV_file)

    for source, dest in zip(source_well_list, destination_well_list):
        p10.pick_up_tip()
        p10.transfer(sample_volume, source, dest, new_tip='never')
        p10.blow_out(dest.top())
        p10.drop_tip()

    col_num = max([int(well.get_name()[1:]) for well in destination_well_list])

    for mastermix in mastermixes:
        m10.transfer(
            mastermix_volume,
            mastermix,
            [col[0] for col in output_plate.cols('1', length=col_num)],
            disposal_vol=0)
