from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'MagBead Based Peptide Purification',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create and load labware
magdeck = modules.load('magdeck', '4')
tempdeck = modules.load('tempdeck', '1')
tempdeck.set_temperature(4)

mag_offset = 14.94  # based on definitions found in labware

deep_name = 'mt_96_deepwellplate_2200ul'
if deep_name not in labware.list():
    labware.create(
        deep_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8.2,
        depth=36.0,
        volume=2000
    )
deep_plate = labware.load(deep_name, '4', 'Deep Well Plate', share=True)
mag_plate = deep_plate.rows('A')

t_plate = labware.load(deep_name, '5', 'Transfer Plate')
deep_trans = t_plate.rows('A')

plate_name = 'lightcycler_96_wellplate_100ul'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.5,
        depth=14.9,
        volume=100
    )

elution_plate = labware.load(plate_name, '1', 'Elution Plate', share=True)
elutes = elution_plate.rows('A')

trough_name = 'starlabs_12_reservoir_7ml'
if trough_name not in labware.list():
    labware.create(
        trough_name,
        grid=(12, 1),
        spacing=(9, 0),
        diameter=8.2,
        depth=36.0,
        volume=7000
    )
tr12 = labware.load(trough_name, '2', '12 Channel Starlabs Res')
mag_clear = tr12.wells(3)
mag_bead = tr12.wells(5)
zyppy_el = tr12.wells(11)

res_name = 'mt_1_reservoir_200ml'
if res_name not in labware.list():
    labware.create(
        res_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=100,
        depth=36.0,
        volume=200000
    )

res1 = labware.load(res_name, '3', 'MT Reservoir w/ Zyppy Wash')
res2 = labware.load(res_name, '6', 'MT Reservoir w/ Neutralization')
liq_cont = labware.load(res_name, '7', 'Liquid Waste')

zyppy_wash = res1.wells(0)
neu_buff = res2.wells(0)
liq_waste = liq_cont.wells(0).top()

reuse_tips = labware.load('opentrons_96_tiprack_300ul', '8')
tips_once = [labware.load('opentrons_96_tiprack_300ul', str(slot))
             for slot in range(9, 12)]


def run_custom_protocol(
        p300_mount: StringSelection('right', 'left') = 'right',
        incubation_time: int = 10
        ):

    # create pipettes
    p300 = instruments.P300_Multi(mount=p300_mount, tip_racks=tips_once)

    tip_count = 0
    tip_max = len(tips_once)*12

    def pick_up():
        nonlocal tip_count

        if tip_count == tip_max:
            p300.home()
            robot.pause('Out of single use tips. Please replace tips in slots \
            9, 10, and 11.')
            p300.reset()
            tip_count = 0
        p300.pick_up_tip()
        tip_count += 1

    used_tips = reuse_tips.rows('A')

    # add 100ul deep blue lysis buffer
    blue_wells = ([0]*6)+([1]*6)
    for tips, mag, well in zip(used_tips, mag_plate, blue_wells):
        p300.pick_up_tip(tips)
        p300.transfer(100, tr12.wells(well), mag, new_tip='never')
        p300.mix(10, 280, mag)
        p300.blow_out(mag.top())
        p300.return_tip()

    p300.delay(minutes=5)

    def part1_trans(src, vol):

        pick_up()

        for mag in mag_plate():
            p300.transfer(vol, src, mag.top(), new_tip='never')
            p300.blow_out(mag.top())

        p300.drop_tip()

        for tips, mag in zip(used_tips, mag_plate):
            p300.pick_up_tip(tips)
            p300.mix(5, 280, mag)
            p300.blow_out(mag.top())
            p300.return_tip()

    part1_trans(neu_buff, 450)  # adding neutralization buffer; mix

    part1_trans(mag_clear, 50)  # adding mag clearing beads; mix

    magdeck.engage(height=mag_offset)

    p300.delay(minutes=5)

    # transfer supernatant to clean plate
    p300.set_flow_rate(aspirate=75)
    for src, dest in zip(mag_plate, deep_trans):
        pick_up()
        for _ in range(3):
            p300.transfer(250, src, dest, new_tip='never')
        p300.blow_out(dest.top())
        p300.drop_tip()
    p300.set_flow_rate(aspirate=150)

    magdeck.disengage()

    robot.pause('Part 1 complete. Please remove plate on magdeck and replace \
    with sample plate in slot 5. Please replace tips in slot 8. Finally, dump \
    the liquid waste in slot 7 and replace the reservoir. When ready to \
    resume, click RESUME.')

    # transfer mag beads and mix
    for tips, mag in zip(used_tips, mag_plate):
        p300.pick_up_tip(tips)
        p300.mix(5, 30, mag_bead)
        p300.set_flow_rate(aspirate=75)
        p300.transfer(30, mag_bead, mag, new_tip='never')
        p300.set_flow_rate(aspirate=150)
        p300.mix(10, 280, mag)
        p300.blow_out(mag.top())
        p300.return_tip()

    for _ in range(10):
        p300.delay(seconds=30)
        for tips, mag in zip(used_tips, mag_plate):
            p300.pick_up_tip(tips)
            p300.mix(10, 280, mag)
            p300.blow_out(mag.top())
            p300.return_tip()

    magdeck.engage(height=mag_offset)

    p300.delay(minutes=5)

    p300.set_flow_rate(aspirate=75)
    for mag in mag_plate:
        pick_up()
        for _ in range(3):
            p300.transfer(260, mag, liq_waste, new_tip='never')
        p300.drop_tip()

    magdeck.disengage()
    p300.set_flow_rate(aspirate=150)

    wash_wells = ([7]*4)+([8]*4)+([9]*4)
    for mag, well in zip(mag_plate, wash_wells):
        pick_up()
        p300.transfer(200, tr12.wells(well), mag, new_tip='never')
        p300.mix(10, 200, mag)
        p300.blow_out(mag.top())
        p300.drop_tip()

    magdeck.engage(height=mag_offset)
    p300.delay(minutes=2)
    p300.set_flow_rate(aspirate=75)

    for mag in mag_plate:
        pick_up()
        p300.transfer(200, mag, liq_waste, new_tip='never')
        p300.drop_tip()

    magdeck.disengage()
    p300.set_flow_rate(aspirate=150)

    for _ in range(2):
        for mag in mag_plate:
            pick_up()
            p300.transfer(400, zyppy_wash, mag.top(), new_tip='never')
            p300.mix(10, 280, mag)
            p300.blow_out(mag.top())
            p300.drop_tip()
        magdeck.engage(height=mag_offset)
        p300.delay(minutes=2)
        p300.set_flow_rate(aspirate=75)
        for mag in mag_plate:
            pick_up()
            p300.transfer(400, mag, liq_waste, new_tip='never')
            p300.drop_tip()
        magdeck.disengage()

    inc_cmmt = 'Incubating for '+str(incubation_time)+' minutes.'
    robot.comment(inc_cmmt)
    robot.comment('While incubating, please replace tips in slot 8.')
    p300.set_flow_rate(aspirate=150)

    p300.delay(minutes=incubation_time)

    # add elution buffer and mix
    for tips, mag in zip(used_tips, mag_plate):
        p300.pick_up_tip(tips)
        p300.transfer(40, zyppy_el, mag, new_tip='never')
        p300.mix(10, 40, mag)
        p300.blow_out(mag.top())
        p300.return_tip()

    for _ in range(10):
        p300.delay(seconds=30)
        for tips, mag in zip(used_tips, mag_plate):
            p300.pick_up_tip(tips)
            p300.mix(10, 40, mag)
            p300.blow_out(mag.top())
            p300.return_tip()

    magdeck.engage(height=mag_offset)
    p300.delay(minutes=1)
    p300.set_flow_rate(aspirate=50, dispense=100)

    for src, dest in zip(mag_plate, elutes):
        pick_up()
        p300.transfer(30, src, dest, new_tip='never')
        p300.blow_out(dest.top())
        p300.drop_tip()

    robot.pause('Protocol complete. Samples are on the temperature module in \
    slot 1.')
