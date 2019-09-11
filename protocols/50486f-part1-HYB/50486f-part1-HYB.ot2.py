from opentrons import labware, instruments, robot, modules
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'PCR Prep 1/4: HYB',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

tempdeck = modules.load('tempdeck', '4')
tempplate = labware.load('biorad_96_wellplate_200ul_pcr', '4', share=True)
tempdeck.set_temperature(4)
tempdeck.wait_for_temp()
pcr_well = labware.load('opentrons_96_aluminumblock_generic_pcr_strip_200ul',
                        '5', 'chilled aluminum block w/ PCR strip')
sample_plate = labware.load(
            'biorad_96_wellplate_200ul_pcr', '6', 'sample plate')
tipracks = [
    labware.load('tiprack-10ul', slot) for slot in ['7', '8']
]


def run_custom_protocol(
        p10_mount: StringSelection('left', 'right') = 'left',
):

    # create pipette

    pip10 = instruments.P10_Multi(mount=p10_mount, tip_racks=tipracks)

    tip10_max = len(tipracks)*12
    tip10_count = 0

    def pick_up(pip):
        nonlocal tip10_count

        if tip10_count == tip10_max:
            robot.pause(
                'Replace 10ul tipracks in slots 7 and 8 before resuming.')
            pip10.reset()
            tip10_count = 0
        pip10.pick_up_tip()
        tip10_count += 1

    dest = tempplate.rows('A')[:12]

    # step 1

    mm_count = 0

    pick_up(pip10)

    for d in dest:
        if mm_count == 0:
            pip10.aspirate(8, pcr_well.wells('A1'))
        pip10.dispense(2, d)
        mm_count += 1
        if mm_count > 3:
            mm_count = 0

    pip10.drop_tip()

    # step 2

    samps = sample_plate.rows('A')[:12]

    for d, s in zip(dest, samps):
        pick_up(pip10)
        pip10.transfer(8, s, d, new_tip='never')
        pip10.blow_out(d.top())
        pip10.drop_tip()

    robot.comment("Part 1/4 (HYB) complete. Please remove plate from \
    temperature module and run on PCR program. When ready, load Part 2/4 (GAP)\
     into OT-2.")
