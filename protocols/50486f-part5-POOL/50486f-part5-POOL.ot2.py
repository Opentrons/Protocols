from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'PCR Prep: POOL',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

pcr_plate = labware.load('biorad_96_wellplate_200ul_pcr', '6', 'PCR Plate')
pcr_well = labware.load('opentrons_96_aluminumblock_generic_pcr_strip_200ul',
                        '5', 'chilled aluminum block w/ PCR strip')
tipracks = labware.load('tiprack-10ul', '7')


def run_custom_protocol(
        p10_mount: StringSelection('left', 'right') = 'left',
        tip_strategy: StringSelection('same tip', 'different tip') = 'same tip'
):

    # create pipette

    pip10 = instruments.P10_Multi(mount=p10_mount, tip_racks=[tipracks])

    tip10_max = len(tipracks)*12
    tip10_count = 0

    def pick_up(pip):
        nonlocal tip10_count

        if tip10_count == tip10_max:
            robot.pause(
                'Replace 10ul tipracks in slot 7 before resuming.')
            pip10.reset()
            tip10_count = 0
        pip10.pick_up_tip()
        tip10_count += 1

    dest = pcr_plate.rows('A')

    # transfer 2ul of sample to 8-well PCR strip
    if tip_strategy == 'different tip':
        for d in dest:
            pick_up(pip10)
            pip10.transfer(2, d, pcr_well.wells('A1'), new_tip='never')
            pip10.blow_out(d.top())
            pip10.drop_tip()
    else:
        pick_up(pip10)
        for d in dest:
            pip10.transfer(2, d, pcr_well.wells('A1'), new_tip='never')
            pip10.blow_out(d.top())
        pip10.drop_tip()

    robot.comment("Pooling protocol now complete.")
