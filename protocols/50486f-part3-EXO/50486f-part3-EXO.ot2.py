from opentrons import labware, instruments, robot, modules
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'PCR Prep 3/4: EXO',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

tempdeck = modules.load('tempdeck', '4')
tempplate = labware.load('biorad_96_wellplate_200ul_pcr', '4', share=True)
tempdeck.set_temperature(4)
tempdeck.wait_for_temp()
pcr_well = labware.load('opentrons_96_aluminumblock_generic_pcr_strip_200ul',
                        '5', 'chilled aluminum block w/ PCR strip')
tipracks = labware.load('tiprack-10ul', '7')


def run_custom_protocol(
        p10_mount: StringSelection('left', 'right') = 'left',
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

    dest = tempplate.rows('A')[:12]

    # transfer 10ul of mastermix from PCR strip to plate on tempdeck

    for d in dest:
        pick_up(pip10)
        pip10.transfer(2, pcr_well.wells('A1'), d, new_tip='never')
        pip10.blow_out(d.top())
        pip10.drop_tip()

    robot.comment("Part 3/4 (EXO) complete. Please remove plate from \
    temperature module and run on PCR program. When ready, load Part 4/4 (PCR)\
     into OT-2.")
