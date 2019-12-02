from opentrons import labware, instruments, robot
from otcustomizers import FileInput

tipracks_10 = [labware.load('tiprack-10ul', slot)
               for slot in ['1', '2']]
tiprack_200 = labware.load('tiprack-200ul', '3')
tuberack_1 = labware.load('opentrons-tuberack-2ml-screwcap', '4')
tuberack_2 = labware.load('opentrons-tuberack-2ml-screwcap', '5')
plates = [labware.load('96-deep-well', slot)
          for slot in ['6', '7', '8', '9', '10', '11']]

plates_name = ['plate '+i for i in ['1', '2', '3', '7', '10', '11']]
source = {'tube rack 1': tuberack_1, 'tube rack 2': tuberack_2}
source.update({name: plate for name, plate in zip(plates_name, plates)})

# instrument setup
p10 = instruments.P10_Single(
    mount='right',
    tip_racks=tipracks_10)

p300 = instruments.P300_Single(
    mount='left',
    tip_racks=[tiprack_200])

# reagent setup
sample_1 = tuberack_1.wells('A6')
sample_2 = tuberack_1.wells('B6')
sample_3 = tuberack_1.wells('C6')
sample_4 = tuberack_1.wells('D6')

p10_tip_count = 0
p300_tip_count = 0


example_1 = """
Tube Rack Name,Tube Position ,Sample Name,Volume (uL)
Tube Rack 2,A01,Water,282
Tube Rack 2,B1,Tris,25
Tube Rack 2,C1,Mg2+,6.25
Tube Rack 2,D1,EDTA,1
Tube Rack 1,A1,Bundle 1,10
Tube Rack 1,C1,Bundle 3,10
Tube Rack 1,D1,Bundle 4,10
"""

example_2 = """
"""

example_3 = """
"""

example_4 = """
"""


def update_tip_count(pipette):
    global p10_tip_count, p300_tip_count
    if pipette == p10:
        p10_tip_count += 1
        if p10_tip_count == 2 * 96:
            robot.pause("P10 tips have run out. Resume after the tips have been\
             replenished.")
            p10.reset_tip_tracking()
            p10_tip_count = 0
    else:
        p300_tip_count += 1
        if p300_tip_count == 96:
            robot.pause("P300 tips have run out. Resume after the tips have \
            been replenished.")
            p300.reset_tip_tracking()
            p300_tip_count = 0


def csv_to_list(csv_string):
    global source
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    source_list = []
    volume_list = []
    for line in info_list[1:]:
        well = line[1]
        if line[1][1] == "0":
            well = well.replace("0", "")
        source_well = source[line[0].lower()].wells(well)
        volume = float(line[3])
        source_list.append(source_well)
        volume_list.append(volume)
    return source_list, volume_list


def custom_mix_sample(volume_list, source_list, dest):
    for vol, source in zip(volume_list, source_list):
        if vol < 30:
            pipette = p10
            pipette.set_flow_rate(aspirate=3, dispense=5)
        else:
            pipette = p300
        pipette.pick_up_tip()
        pipette.transfer(
            vol, source, dest, new_tip='never')
        pipette.drop_tip()
        update_tip_count(pipette)


def run_custom_protocol(
        sample_1_csv: FileInput=example_1,
        sample_2_csv: FileInput=example_2,
        sample_3_csv: FileInput=example_3,
        sample_4_csv: FileInput=example_4):

    source_list, volume_list = csv_to_list(sample_1_csv)
    custom_mix_sample(volume_list, source_list, sample_1)
    robot.comment("Sample 1 finished mixing.")

    source_list, volume_list = csv_to_list(sample_2_csv)
    custom_mix_sample(volume_list, source_list, sample_2)
    robot.comment("Sample 2 finished mixing.")

    source_list, volume_list = csv_to_list(sample_3_csv)
    custom_mix_sample(volume_list, source_list, sample_3)
    robot.comment("Sample 3 finished mixing.")

    source_list, volume_list = csv_to_list(sample_4_csv)
    custom_mix_sample(volume_list, source_list, sample_4)
    robot.comment("Sample 4 finished mixing.")
