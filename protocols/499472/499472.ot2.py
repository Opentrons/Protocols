from opentrons import labware, instruments, robot, modules
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Nucleic Acid Prep with MagBeads',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

tips300 = [labware.load('opentrons_96_tiprack_300ul', slot,
                        'Opentrons 300ul Tips')
           for slot in ['8', '9', '11']]

tips50 = [labware.load('opentrons_96_tiprack_300ul', '10',
                       'Opentrons 50ul Tips')]

tempdeck = modules.load('tempdeck', '7')
tempplate = labware.load('biorad_96_wellplate_200ul_pcr', '7', share=True)

magdeck = modules.load('magdeck', '4')
magplate = labware.load('biorad_96_wellplate_200ul_pcr', '4', share=True)

altube = labware.load('opentrons_24_aluminumblock_generic_2ml_screwcap', '1',
                      'Aluminum Tube Rack, 2mL')

res12 = labware.load('usascientific_12_reservoir_22ml', '2',
                     '12 Channel Reservoir')

res1 = labware.load('agilent_1_reservoir_290ml', '3', 'Reservoir 1')

res2 = labware.load('agilent_1_reservoir_290ml', '6', 'Reservoir 2')

liqwaste = labware.load('agilent_1_reservoir_290ml', '5', 'Liquid Waste')

HB = altube.wells('A1')
HB1 = altube.wells('B1')
magbeads = altube.wells('C1')

mm = res12.wells(0)
hrp = res12.wells(1)
subs = res12.wells(2)


def run_custom_protocol(
        p50_single_mount: StringSelection('left', 'right') = 'left',
        p300_multi_mount: StringSelection('right', 'left') = 'right'
):

    # checks
    if p50_single_mount == p300_multi_mount:
        raise Exception('Mounts must be different.')

    # create pipette
    s50 = instruments.P50_Single(mount=p50_single_mount, tip_racks=tips50)
    m300 = instruments.P300_Multi(mount=p300_multi_mount, tip_racks=tips300)
    mag300 = magplate.rows('A')

    # pipette tip function
    tip50_count = 0
    tip300_count = 0
    tip50_max = len(tips50)*96
    tip300_max = len(tips300)*12

    def pick_up(pip):
        nonlocal tip50_count
        nonlocal tip300_count

        if pip == s50:
            if tip50_count == tip50_max:
                robot.pause('Replace 50/300ul tipracks in slots 10 \
                before resuming.')
                s50.reset()
                tip50_count = 0
            s50.pick_up_tip()
            tip50_count += 1
        else:
            if tip300_count == tip300_max:
                robot.pause('Replace 50/300ul tipracks in slots 5, 8, 9, and 11 \
                before resuming.')
                m300.reset()
                tip300_count = 0
            m300.pick_up_tip()
            tip300_count += 1

    """Control Preparation"""
    sampwells = range(16, 96)
    # add 20ul of HB in 'A' and HB1 in 'B'
    tipvol = 0
    for well in range(16):
        if tipvol == 0:
            if not s50.tip_attached:
                pick_up(s50)
            if well < 8:
                s50.aspirate(40, HB1)
            else:
                s50.aspirate(40, HB)
            tipvol = 40
        s50.dispense(20, magplate.wells(well).top())
        tipvol -= 20
        if tipvol == 0 and well > 6:
            s50.drop_tip()

    pick_up(s50)
    for well in sampwells:
        if tipvol == 0:
            s50.aspirate(40, HB)
            tipvol = 40
        s50.dispense(20, magplate.wells(well).top())
        tipvol -= 20
    s50.drop_tip()

    s50.delay(minutes=1)

    """Bead Dispensing"""
    # dispense 5ul of magbeads into each well
    tipvol = 0
    for well in magplate:
        if tipvol == 0:
            pick_up(s50)
            s50.aspirate(40, magbeads)
            tipvol = 40
        s50.dispense(5, well)
        tipvol -= 5
        if tipvol == 0:
            s50.drop_tip()

    for col in mag300:
        pick_up(m300)
        m300.mix(5, 30, col)
        m300.blow_out(col.top())
        m300.drop_tip()

    for _ in range(3):
        m300.delay(minutes=20)
        robot._driver.run_flag.wait()
        for col in mag300:
            pick_up(m300)
            m300.mix(5, 30, col)
            m300.blow_out(col.top())
            m300.drop_tip()

    """Reaction"""
    magdeck.engage()
    m300.delay(minutes=1)

    def remove_supernatant(plate, vol):
        m300.set_flow_rate(aspirate=50)
        for col in plate:
            if not m300.tip_attached:
                pick_up(m300)
            m300.transfer(vol, col, liqwaste, new_tip='never')
            m300.drop_tip()
        m300.set_flow_rate(aspirate=150)

    remove_supernatant(mag300, 35)

    # add PBS-T
    def PBStransfer(vol):
        pick_up(m300)
        for col in mag300:
            m300.transfer(vol, res1, col.top(), new_tip='never')
            m300.blow_out(col.top())

    # magdeck mixing
    def magmix(time):
        for i in range(6):
            if i % 2 == 0:
                magdeck.disengage()
            else:
                magdeck.engage()
            m300.delay(seconds=time)
            robot._driver.run_flag.wait()

        magdeck.engage()
        m300.delay(minutes=1)
        robot._driver.run_flag.wait()

    for t in [10, 15, 20]:
        PBStransfer(150)

        magmix(t)

        if t == 20:
            robot.pause('Add the reducing agent to the master mix. When ready \
            to continue, click RESUME.')
        remove_supernatant(mag300, 150)

    # add 50ul of Master Mix to each well
    tipvol = 0
    pick_up(m300)
    for col in mag300:
        if tipvol == 0:
            m300.aspirate(300, mm)
            tipvol = 300
        m300.dispense(50, col.top())
        tipvol -= 50

    magdeck.disengage()

    # mix the wells
    for col in mag300:
        if not m300.tip_attached:
            pick_up(m300)
        m300.mix(5, 50, col)
        m300.blow_out(col.top())
        m300.drop_tip()

    robot.pause('Please remove the plate from the Magnetic Module and place on \
    the Temperature Module. When ready, click RESUME.')

    tempdeck.set_temperature(41)
    m300.delay(minutes=60)
    robot._driver.run_flag.wait()

    robot.pause('Please remove the plate from the Temperature Module and place \
    on the Magnetic Module. When ready, click RESUME.')

    # remove master mix supernatant
    magdeck.engage()
    m300.delay(minutes=1)
    remove_supernatant(mag300, 50)

    stepvol = [150, 150, 150, 100, 150, 150]
    stepsrc = [res2, res2, res1, hrp, res1, res1]
    # add vol (stepvol) from source (stepsrc)
    for vol, src in zip(stepvol, stepsrc):
        pick_up(m300)
        for col in mag300:
            m300.transfer(vol, src, col.top(), new_tip='never')
            m300.blow_out(col.top())

        # mag deck mixing
        if src == res1:
            magmix(15)
        else:
            for _ in range(2):
                magmix(15)
                magdeck.disengage()
                m300.delay(minutes=4)
                robot._driver.run_flag.wait()

        magdeck.engage()
        m300.delay(minutes=1)
        remove_supernatant(mag300, vol)

    pick_up(m300)
    for col in mag300:
        m300.transfer(150, res1, col.top(), new_tip='never')
        m300.blow_out(col.top())

    magmix(15)

    magdeck.engage()
    m300.delay(minutes=1)
    robot._driver.run_flag.wait()

    robot.pause('Prepare the substrate and load it into the 22mL Reservoir \
    (Column 3). When ready, click RESUME.')

    for col in mag300:
        if not m300.tip_attached:
            pick_up(m300)
        m300.set_flow_rate(aspirate=50, dispense=300)
        m300.transfer(150, col, liqwaste, new_tip='never')
        m300.blow_out()
        m300.drop_tip()
        pick_up(m300)
        m300.set_flow_rate(aspirate=150, dispense=150)
        m300.transfer(100, subs, col, new_tip='never')
        m300.drop_tip()
        robot.pause('Substrate added. Waiting for measurement... When ready \
        for next column, click RESUME.')

    robot.comment('Congratulations, the protocol is now complete.')
