from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Heat Shock Transformation',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load labware
tuberack15 = labware.load(
    'opentrons_15_tuberack_falcon_15ml_conical', '1', 'tuberack for LB')
cold_rack = labware.load(
    'opentrons_24_aluminumblock_generic_2ml_screwcap', '2')
tiprack300 = labware.load('opentrons_96_tiprack_300ul', '3')
tempdeck = modules.load('tempdeck', '4')
tempdeck.set_temperature(42)
heat_block = labware.load(
    'opentrons_96_aluminumblock_biorad_wellplate_200ul',
    '4',
    '96-well plate on aluminum block for heat shock',
    share=True)
tiprack10 = labware.load('opentrons_96_tiprack_10ul', '6')

# reagents
lb = tuberack15.wells('A1')


def run_custom_protocol(
        p300_mount: StringSelection('left', 'right') = 'left',
        p10_mount: StringSelection('right', 'left') = 'right',
        number_of_samples: int = 6,
        DNA_volume_in_ul: float = 2,
        cell_volume_in_ul: float = 25,
        starting_volume_of_LB_tube_in_ml: float = 12
):
    # check
    if p300_mount == p10_mount:
        raise Exception('Pipette mounts cannot be the same.')
    if number_of_samples < 1 or number_of_samples > 6:
        raise Exception('Number of samples must be between 1 and 6.')

    # pipettes
    p300 = instruments.P300_Single(mount=p300_mount, tip_racks=[tiprack300])
    p10 = instruments.P10_Single(mount=p10_mount, tip_racks=[tiprack10])

    pip = p10 if DNA_volume_in_ul < 30 else p300
    # add DNA from tube column B to tube column A in cold deck
    for s, d in zip(cold_rack.rows('B')[:number_of_samples],
                    cold_rack.rows('A')[:number_of_samples]):
        pip.pick_up_tip()
        pip.transfer(
            DNA_volume_in_ul, s.bottom(4), d.bottom(4), new_tip='never')
        pip.mix(3, 9, d.bottom(4))
        pip.blow_out(d.top())
        pip.drop_tip()

    # delay 30 minutes after adding DNA
    robot.pause('Place the aluminum block containing samples in a 4C \
environment for 30 minutes. Replace the block in slot 5 and resume once \
incubation has finished.')

    # move dna/cells from cold deck to heat deck and then back
    p300.home()
    tempdeck.wait_for_temp()
    volume = DNA_volume_in_ul + cell_volume_in_ul
    pip = p10 if volume < 30 else p300
    for s, d in zip(cold_rack.rows('A')[:number_of_samples],
                    heat_block.rows('A')[:number_of_samples]):
        pip.pick_up_tip()
        pip.transfer(volume, s.bottom(4), d, new_tip='never')
        pip.touch_tip(d)

        robot.comment('Heat shock for 1 minute...')
        pip.delay(minutes=1)

        pip.transfer(volume, d, s.bottom(4), new_tip='never')
        pip.touch_tip(s)
        pip.drop_tip()

    # delay 5 minutes after heat shock
    robot.comment('Incubating at 4C for 5 minutes')
    p300.delay(minutes=5)

    # add LB to dna/cells
    if starting_volume_of_LB_tube_in_ml > 10:
        loc = lb.top(-60)
    elif starting_volume_of_LB_tube_in_ml > 5:
        loc = lb.bottom(30)
    else:
        loc = lb.bottom(5)
    p300.transfer(
        200,
        loc,
        [s.top() for s in cold_rack.rows('A')[:number_of_samples]]
    )
