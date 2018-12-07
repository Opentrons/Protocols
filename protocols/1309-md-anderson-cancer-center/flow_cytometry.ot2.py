from opentrons import labware, instruments, modules, robot
from otcustomizers import FileInput

# create custom labware
tuberack_name = 'custom-pyrotube-rack'
if tuberack_name not in labware.list():
    labware.create(
        tuberack_name,
        grid=(6, 4),
        spacing=(20, 20),
        diameter=11.8,
        depth=75)

# labware setup
flow_tuberacks = [labware.load(tuberack_name, slot)
                  for slot in ['1', '2', '3', '5']]
temp_deck = modules.load('tempdeck', '4')
plate = labware.load('96-flat', '4', share=True)

trough = labware.load('trough-12row', '7')
tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '8')
tiprack_10 = labware.load('tiprack-10ul', '6')
tiprack_300 = [labware.load('opentrons-tiprack-300ul', slot)
               for slot in ['9', '10', '11']]

# instrument setup
p300 = instruments.P300_Single(
    mount='left',
    tip_racks=tiprack_300)

p10 = instruments.P10_Single(
    mount='right',
    tip_racks=[tiprack_10])

# reagent setup
cell = trough.wells('A1')
DAPI_PBS = trough.wells('A2')
PBS = trough.wells('A3')

p10_tip_count = 0
p300_tip_count = 0

wells = [well for well in plate.wells()]
flowtubes = [well for tuberack in flow_tuberacks
             for col in tuberack.cols()
             for well in col]

csv_example = """
Antibody 1,Antibody 2,Antibody 3,Antibody 4,Antibody 5,Antibody 6,Antibody 7,\
Antibody 8
4,,,,5,,4,4
,4,3,,,5,,4
5,4,,3,4,4,3,5
,,4,,,,3,
,,3,,5,,4,
,3,,5,,,,3
3,,,3,,3,5,3
,,3,,,4,,4
,,4,,,3,,3
,3,,5,3,,4,5
,,,,,3,,
"""


def update_p10_tip_count(num):
    global p10_tip_count
    p10_tip_count += num
    print(p10_tip_count)
    if p10_tip_count == 96:
        robot.pause("Your P10 tips have run out. Refill tip rack before \
        resuming.")
        p10.reset_tip_tracking()
        p10_tip_count = 0


def update_p300_tip_count(num):
    global p300_tip_count
    p300_tip_count += num
    print(p300_tip_count)
    if p300_tip_count == 96:
        robot.pause("Your P300 tips have run out. Refill tip racks before \
        resuming.")
        p300.reset_tip_tracking()
        p300_tip_count = 0


def csv_to_list(csv_string):
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    new_dict = {_: [] for _ in range(len(info_list[0]))}
    for line in info_list[1:]:
        for index, cell in enumerate(line):
            if cell:
                new_dict[index].append(float(cell))
            else:
                new_dict[index].append(0)
    return new_dict, len(info_list[1:])


def run_custom_protocol(csv_file: FileInput=csv_example):
    antibody_dict, sample_num = csv_to_list(csv_file)

    temp_deck.set_temperature(4)

    # transfer 100 uL cell to the wells
    p300.distribute(100, cell, wells[:sample_num])
    update_p300_tip_count(1)

    # transfer antibodies to the wells
    for antibody_index in range(len(antibody_dict)):
        source = tuberack[antibody_index]
        vols = antibody_dict[antibody_index]
        for vol, dest in zip(vols, wells[:sample_num]):
            if vol:
                p10.pick_up_tip()
                p10.transfer(vol, source, dest.top(), new_tip='never')
                p10.mix(5, 10)
                p10.blow_out(dest.top())
                p10.drop_tip()
                update_p10_tip_count(1)

    temp_deck.wait_for_temp()
    p300.delay(minutes=20)

    # transfer 100 uL DAPI to 48 wells
    targets = [well.top() for well in wells[:sample_num]]
    p300.distribute(100, DAPI_PBS, targets, blow_out=True)
    update_p300_tip_count(1)

    temp_deck.deactivate()

    robot.pause("Remove the plate from OT-2 to for centrifugation and \
    centrifuge for 5 min at 1500RPM at 4 degree centigrade. Toss the \
    supernatant by quickly inverting the plate in the sink. Tap gently on a \
    paper towel to remove extra drops of liquid on the corners of the plate. \
    Bring the plate back to OT2. ")

    # transfer 250 uL PBS to each well
    for source, dest in zip(wells[:sample_num], flowtubes[:sample_num]):
        p300.pick_up_tip()
        p300.transfer(250, PBS, source, new_tip='never')
        p300.set_flow_rate(dispense=600)
        p300.mix(10, 200)
        p300.set_flow_rate(dispense=300)
        p300.transfer(250, source.bottom(0.5), dest, new_tip='never')
        p300.blow_out(dest)
        p300.drop_tip()
        update_p300_tip_count(1)
