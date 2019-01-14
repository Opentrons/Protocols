from opentrons import labware, instruments
from otcustomizers import FileInput

trough_name = 'trough-1row-deep'
if trough_name not in labware.list():
    labware.create(
        trough_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=10,
        depth=40)

# labware setup
trough = labware.load(trough_name, '1')
plate_1 = labware.load('96-flat', '2')
output_1 = labware.load('96-flat', '3')
plate_2 = labware.load('96-flat', '5')
output_2 = labware.load('96-flat', '6')
tipracks_s = [labware.load('opentrons-tiprack-300ul', slot)
              for slot in ['4', '8']]
tipracks_m = [labware.load('opentrons-tiprack-300ul', slot)
              for slot in ['7', '9']]

# reagent setup
buffer = trough.wells('A1')

# instruments setup
p300 = instruments.P300_Single(
    mount='left',
    tip_racks=tipracks_s)
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks_m)

example = """
Plate,Well,Volume
1,A1,
1,A2,245
1,A3,248
1,A4,262
1,A5,300
1,A6,287
1,A7,283
1,A8,259
1,A9,289
1,A10,340
1,A11,341
1,A12,
"""


def csv_to_list(csv_string):
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    loc, vol, active_plates = [], [], []
    for line in info_list[1:]:
        if line[2]:  # if there is a volume
            if line[0] == '1' or line[0] == '2':
                if line[0] == '1':
                    plate = plate_1
                else:
                    plate = plate_2
                loc.append(plate.wells(line[1]))
                vol.append(float(line[2]))
                if plate not in active_plates:
                    active_plates.append(plate)
    return loc, vol, active_plates


def run_custom_protocol(
        volume_csv: FileInput=example,
        transfer_volume: float=100):

    locations, volumes, active_plates = csv_to_list(volume_csv)

    for loc, vol in zip(locations, volumes):
        p300.pick_up_tip()
        p300.transfer(vol, buffer, loc, new_tip='never')
        p300.mix(5, vol/2, loc)
        p300.drop_tip()

    for plate in active_plates:
        if plate == plate_1:
            output = output_1
        else:
            output = output_2
        for source, dest in zip(plate.cols(), output.cols()):
            m300.transfer(transfer_volume, source, dest, new_tips='once')
