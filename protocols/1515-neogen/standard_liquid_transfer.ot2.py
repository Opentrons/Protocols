from opentrons import labware, instruments, robot

metadata = {
    'protocolName': 'Standard Liquid Transfer',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware
tips = labware.load('opentrons-tiprack-300ul', '10')
trough = labware.load('trough-12row', '11')

# create custom 96-well plate
plate_name = 'custom_96_well'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=27,
        volume=800)

# instruments
m50 = instruments.P50_Multi(
    mount='left',
    tip_racks=[tips]
)

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tips]
)


def transfer_plates(vol, pip, plate):

    # transfer from trough to all wells of all plates on the deck
    rowA = [well for well in plate.rows('A')]

    for ind, col in enumerate(rowA):

        # transfers specified volume to all wells in the plate
        pip.aspirate(vol, trough[ind])
        pip.dispense(vol, col.top(-2))
        pip.blow_out()

        # custom touch tip to only one edge for improved runtime
        well_edge = col.from_center(r=1.0, theta=0, h=0.9)
        destination = (col, well_edge)
        pip.move_to(destination)


def run_custom_protocol(
    tip_start: str = '1',
    num_plates: int = 8,
    volume: float = 50,
):

    # initially loads up to 8 plates
    if num_plates >= 8:
        count = 8
    else:
        count = num_plates
    plates = [labware.load('custom_96_well', str(slot+1))
              for slot in range(count)]

    # choose proper pipette based on volume
    if volume > 50:
        pipette = m300
    else:
        pipette = m50

    # pick up tips for entire transfer process
    pipette.pick_up_tip(tips.cols(tip_start))

    # perform transfer for as many plates as input
    for p in range(num_plates):
        plate_loc = p % 8
        if plate_loc == 0 and p > 0:
            robot.pause('Reload up to 8 more plates from slot 1 to slot 8. '
                        'Ensure all plates have consistent dimensions.')
        transfer_plates(volume, pipette, plates[plate_loc])

    # drop tip after entire process has executed
    pipette.drop_tip()
