from opentrons import labware, instruments, robot
from otcustomizers import FileInput, StringSelection

metadata = {
    'protocolName': 'Cherrypicking Transfer and Sample Normalization from CSV',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load labware
plate1X = labware.load(
    'biorad_96_wellplate_200ul_pcr', '1', '1X DNA Plate')
plate10X = labware.load(
    'biorad_96_wellplate_200ul_pcr', '3', '1/10X DNA Plate')
dest_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr', '2', 'Destination Plate')
tips10 = [
    labware.load('opentrons_96_tiprack_10ul', slot) for slot in ['4', '7']
]
tips50 = [
    labware.load('opentrons_96_tiprack_300ul', slot) for slot in ['6', '9']
]
TrisHCl_container = labware.load(
    'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', '5',
    '4-in-1 Tube Rack')

TrisHCl = TrisHCl_container.wells('A3')

example_csv = """
A1,1/10X,0
A2,1X,5.2
A3,1/10X,50

"""


def run_custom_protocol(
        picking_csv: 'FileInput' = example_csv,
        p10_mount: StringSelection('left', 'right') = 'left',
        p50_mount: StringSelection('left', 'right') = 'right',
        number_of_samples_to_process: int = 96
        ):

    # check
    if p10_mount == p50_mount:
        raise Exception('Input different mounts for P10 and P50 pipettes')
    if number_of_samples_to_process > 96 or number_of_samples_to_process < 1:
        raise Exception('Invalid number of samples to process (must be between \
        1 and 96).')

    # create pipettes
    pip10 = instruments.P10_Single(mount=p10_mount, tip_racks=tips10)
    pip50 = instruments.P50_Single(mount=p50_mount, tip_racks=tips50)

    tip10_max = len(tips10)*96
    tip50_max = len(tips50)*96
    tip10_count = 0
    tip50_count = 0

    def pick_up(pip):
        nonlocal tip10_count
        nonlocal tip50_count

        if pip == pip50:
            if tip50_count == tip50_max:
                robot.pause('Replace 300ul tipracks in slots 6 and 9\
                 before resuming.')
                pip50.reset()
                tip50_count = 0
            pip50.pick_up_tip()
            tip50_count += 1
        else:
            if tip10_count == tip10_max:
                robot.pause('Replace 10 tipracks in slots 4 and 7\
                before resuming.')
                pip10.reset()
                tip10_count = 0
            pip10.pick_up_tip()
            tip10_count += 1

    data = [
      [well.strip(), plate.strip(), float(volume)]
      for well, plate, volume in
      [row.split(',') for row in picking_csv.splitlines() if row]
        ]

    def tris_transfer(pip, vol, dest):
        pip.transfer(vol, TrisHCl, dest, new_tip='never')
        pip.blow_out(dest.top())
        pip.drop_tip()

    for d in data:
        if d[1] == '1/10X':
            plate = plate10X
        else:
            plate = plate1X

        pick_up(pip50)
        pip50.transfer(10, plate.wells(d[0]),
                       dest_plate.wells(d[0]), new_tip='never')
        pip50.blow_out(dest_plate.wells(d[0]).top())
        pip50.drop_tip()

        if d[2] > 0.1:
            pip = pip50 if d[2] > 9 else pip10
            pick_up(pip)
            tris_transfer(pip, d[2], dest_plate.wells(d[0]))

    robot.comment('Congratulations, the protocol is now complete.')
