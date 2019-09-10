from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'NEB Next Ultra II FS Library Prep: Adaptor Ligation',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
pcr_name = 'biorad_96_wellplate_350ul_pcr'
if pcr_name not in labware.list():
    labware.create(
        pcr_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.5,
        depth=19.85,
        volume=350
    )

res_name = 'axygen_12_reservoir_22ml'
if res_name not in labware.list():
    labware.create(
        res_name,
        grid=(12, 1),
        spacing=(9, 0),
        diameter=8.3,
        depth=39,
        volume=22000
    )

strips_name = 'generic_96_aluminumblock_pcr_strip_200ul'
if strips_name not in labware.list():
    labware.create(
        strips_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.5,
        depth=21.4,
        volume=200
    )

# load labware
mag_plate = labware.load(pcr_name, '1', 'reaction plate')
res12 = labware.load(res_name, '2', 'reagent reservoir')
strips = labware.load(strips_name, '3', 'strips (after move)')
tempdeck = modules.load('tempdeck', '4')
temp_strips = labware.load(strips_name, '4', 'strips (initial)', share=True)
tempdeck.set_temperature(20)
tempdeck.wait_for_temp()
tips10 = [
    labware.load('opentrons_96_tiprack_10ul', str(slot))
    for slot in range(5, 8)
]
tips300 = [
    labware.load('opentrons_96_tiprack_300ul', str(slot))
    for slot in range(8, 12)
]

# reagents
etoh = res12.wells('A1', length=2)
te = res12.wells('A3')
spri_beads = res12.wells('A5')
liquid_waste = [well.top() for well in res12.wells('A10', length=3)]

mm = temp_strips.wells('A1')
lig_enhancer = temp_strips.wells('A2')
adaptor = temp_strips.wells('A3')

user_enzyme = strips.wells('A4')


def run_custom_protocol(
        p300_multi_mount: StringSelection('right', 'left') = 'right',
        p10_multi_mount: StringSelection('left', 'right') = 'left',
        number_of_sample_to_process: int = 96
):
    # check
    if p300_multi_mount == p10_multi_mount:
        raise Exception('Input different mounts for P10 and P300 pipettes.')
    if number_of_sample_to_process > 96 or number_of_sample_to_process < 1:
        raise Exception('Invalid number of samples to process (should be \
between 1 and 96)')

    # pipettes
    m300 = instruments.P300_Multi(mount=p300_multi_mount, tip_racks=tips300)
    m10 = instruments.P10_Single(mount=p10_multi_mount, tip_racks=tips10)

    # setup
    num_cols = math.ceil(number_of_sample_to_process/8)
    mag_samples_multi = mag_plate.rows('A')[:num_cols]

    tip10_count = 0
    tip300_count = 0
    tip10_max = len(tips10)*12
    tip300_max = len(tips300)*12

    def pick_up(pip):
        nonlocal tip10_count
        nonlocal tip300_count

        if pip == m300:
            if tip300_count == tip300_max:
                robot.pause('Refill 300ul tip racks before resuming.')
                tip300_count = 0
                m300.reset()
            tip300_count += 1
        else:
            if tip10_count == tip10_max:
                robot.pause('Refill 10ul tip racks before resuming.')
                tip10_count = 0
                m10.reset()
            tip10_count += 1
        pip.pick_up_tip()

    def mix(reps, vol, loc, pip, disp_perc=0.5):
        if pip == m10:
            a, d = 2.5, 10*disp_perc
        else:
            a, d = 75, 300*disp_perc
        pip.set_flow_rate(aspirate=a, dispense=d)
        for _ in range(reps):
            pip.aspirate(vol, loc)
            pip.delay(seconds=3)
            pip.dispense(vol, loc)
            pip.delay(seconds=3)
        pip.set_flow_rate(aspirate=2*a, dispense=d/disp_perc)

    # transfer adapter ligation reagents one at a time to each well
    for vol, reagent in zip([30, 1, 2.5], [mm, lig_enhancer, adaptor]):
        pip = m300 if vol > 10 else m10
        for m in mag_samples_multi:
            pick_up(pip)
            pip.transfer(vol, reagent, m, new_tip='never')
            pip.blow_out()
            pip.drop_tip()

    # mix new reactions
    for m in mag_samples_multi:
        pick_up(m300)
        mix(10, 40, m, m300)
        m300.blow_out(m.top())
        m300.drop_tip()

    robot.pause('Move strips block from the temperature module to slot 3 and \
place the reaction plate from slot 1 onto the temperature module. Allow to \
incubate for 15 minutes and then replace in slot 1. Place the USER enzyme \
strip in column 4 of the strips block (now in slot 3).')

    robot._driver.run_flag.wait()
    tempdeck.set_temperature(37)

    # transfer USER enzyme
    for m in mag_samples_multi:
        pick_up(m10)
        m10.transfer(3, user_enzyme, m, new_tip='never')
        m10.blow_out()
        m10.drop_tip()

    # mix new reactions
    for m in mag_samples_multi:
        pick_up(m300)
        mix(5, 40, m, m300)
        m300.blow_out(m.top())
        m300.drop_tip()

    tempdeck.wait_for_temp()
    robot._driver.run_flag.wait()
    robot.pause('Move reaction plate from slot 1 onto the temperature module. \
Allow to incubate for 15 minutes and resume to finish and continue to size \
selection of adaptor-ligated DNA.')
    m300.home()
