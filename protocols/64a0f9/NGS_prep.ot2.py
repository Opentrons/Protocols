from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Swift Biosciences Swift 25 Turbo NGS Library Prep',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load modules and labware
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load('biorad_96_wellplate_200ul_pcr', '1', share=True)
elution_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr', '2', 'elution plate')
reagent_rack = labware.load(
    'opentrons_24_aluminumblock_generic_2ml_screwcap',
    '3',
    'reagent tuberack (for mastermixes)'
)
tempdeck = modules.load('tempdeck', '4')
temp_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr',
    '4',
    'temperature module plate',
    share=True
)
reagent_res = labware.load(
    'usascientific_12_reservoir_22ml', '5', 'reagent reservoir')
tempdeck.set_temperature(4)
tempdeck.wait_for_temp()
tips10 = [
    labware.load('opentrons_96_tiprack_10ul', slot)
    for slot in ['6', '7', '8']
]
tips300 = [
    labware.load('opentrons_96_tiprack_300ul', slot)
    for slot in ['9', '10', '11']
]


def run_custom_protocol(
        number_of_samples: int = 96,
        p10_single_mount: StringSelection('right', 'left') = 'right',
        p300_multi_mount: StringSelection('left', 'right') = 'left'
):
    # check
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Invalid sample number.')
    if p10_single_mount == p300_multi_mount:
        raise Exception('Input different mounts for pipettes.')

    # pipettes
    p10 = instruments.P10_Single(mount=p10_single_mount, tip_racks=tips10)
    m300 = instruments.P300_Multi(mount=p300_multi_mount, tip_racks=tips300)

    # reagents
    e_mm = reagent_rack.wells('A1')
    l_mm = [
        well
        for well in reagent_rack.wells()[2:2+math.ceil(number_of_samples/48)]
    ]
    pcr_mm = [
        well
        for well in reagent_rack.wells()[4:4+math.ceil(number_of_samples/48)]
    ]

    beads = reagent_res.wells('A1')
    etoh = [
        well for well in reagent_res.wells(
            'A2', length=math.ceil(number_of_samples/48)*2)
    ]
    edta_buffer = reagent_res.wells('A6')
    te_buffer = reagent_res.wells('A7')
    liquid_trash = [well for well in reagent_res.wells('A8', length=5)]

    t_samples = temp_plate.wells()[:number_of_samples]
    m_samples = mag_plate.wells()[:number_of_samples]
    m_cols = mag_plate.rows('A')[:math.ceil(number_of_samples/8)]
    e_samples = elution_plate.wells()[:number_of_samples]

    tip10_count = 0
    tip300_count = 0
    tip10_max = len(tips10)*96
    tip300_max = len(tips300)*12

    def pick_up(pip):
        nonlocal tip10_count
        nonlocal tip300_count

        if pip == 'p10':
            if tip10_count == tip10_max:
                robot.pause('Replace 10ul tipracks before resuming.')
                p10.reset()
                tip10_count = 0
            p10.pick_up_tip()
            tip10_count += 1
        else:
            if tip300_count == tip300_max:
                robot.pause('Replace 300ul tipracks before resuming')
                m300.reset()
                tip300_count = 0
            m300.pick_up_tip()
            tip300_count += 1

    wash_count = 0

    def cleanup(vol_beads, buffer):
        nonlocal wash_count

        # bead addition
        pick_up('m300')
        m300.mix(10, 200, beads)
        m300.blow_out(beads.top())
        for c in m_cols:
            if not m300.tip_attached:
                pick_up('m300')
            m300.transfer(vol_beads, beads, c, new_tip='never')
            m300.mix(10, 40, c)
            m300.blow_out(c.top())
            m300.drop_tip()

        m300.delay(minutes=5)
        robot._driver.run_flag.wait()
        magdeck.engage(height=18)
        m300.delay(minutes=2)

        # remove supernatant
        m300.set_flow_rate(aspirate=50)
        for c in m_cols:
            pick_up('m300')
            m300.transfer(100, c, liquid_trash[-1], new_tip='never')
            m300.drop_tip()
        m300.set_flow_rate(aspirate=150)

        # etoh washes
        for _ in range(2):
            m300.set_flow_rate(dispense=100)
            pick_up('m300')
            for c in m_cols:
                wash_ind = wash_count // 96
                wash_count += 1
                m300.transfer(180, etoh[wash_ind], c, new_tip='never')
                m300.blow_out(c.top())
            m300.delay(seconds=30)

            # remove supernatant
            m300.set_flow_rate(aspirate=50, dispense=300)
            for c in m_cols:
                if not m300.tip_attached:
                    pick_up('m300')
                m300.transfer(200, c, liquid_trash[wash_ind], new_tip='never')
                m300.drop_tip()
            m300.set_flow_rate(aspirate=150)

        robot.pause('Quick spin the samples in a tabletop microfuge and replace \
    the plate on the magnetic module.')

        magdeck.disengage()

        # resuspend in buffer
        for s in m_samples:
            pick_up('p10')
            for vol in [8, 8, 6]:
                p10.transfer(vol, buffer, s.bottom(5), new_tip='never')
                p10.blow_out(s.bottom(5))
            p10.mix(5, 9, s)
            p10.blow_out(s.bottom(3))
            p10.drop_tip()

        magdeck.engage(height=18)
        m300.delay(minutes=2)

        # transfer elution to fresh plate
        for s, d in zip(m_samples, e_samples):
            pick_up('p10')
            p10.transfer(20, s, d, new_tip='never')
            p10.blow_out(d)
            p10.drop_tip()

    """ Enzymatic Prep """

    # transfer enzymatic mastermix
    for s in t_samples:
        pick_up('p10')
        for vol in [5.5, 5]:
            p10.transfer(vol, e_mm, s, new_tip='never')
        p10.blow_out(s.bottom(3))
        p10.mix(5, 8, s)
        p10.blow_out(s.bottom(3))
        p10.drop_tip()

    robot.pause('Vortex, and spin down the sample plate in a microfuge and \
immediately place in the chilled thermocycler, and advance the program to the \
32˚C step.')

    """ Ligation """
    for i, s in enumerate(t_samples):
        pick_up('p10')
        for _ in range(3):
            p10.transfer(10, l_mm[i//48], s.bottom(5), new_tip='never')
            p10.blow_out(s.top())
        p10.drop_tip()

    tempdeck.set_temperature(20)
    tempdeck.wait_for_temp()
    robot._driver.run_flag.wait()
    m300.delay(minutes=20)
    robot._driver.run_flag.wait()
    tempdeck.set_temperature(4)
    tempdeck.wait_for_temp()
    robot._driver.run_flag.wait()
    robot.pause('Transfer the sample plate from the temperature module to the \
magnetic module.')

    tempdeck.deactivate()

    cleanup(48, edta_buffer)

    """ Indexing PCR """

    robot.pause('Program the thermocycler according the parameters outlined \
in the protocol manual. Place the index plate on the now disengaged \
temperature module in slot 4.')

    indexes = t_samples

    # sample indexing
    for i, e in zip(indexes, e_samples):
        pick_up('p10')
        p10.transfer(5, i, e, new_tip='never')
        p10.blow_out(e)
        p10.drop_tip()

    # transfer pcr mastermix
    for i, s in enumerate(t_samples):
        pick_up('p10')
        for vol in [10, 10, 5]:
            p10.transfer(vol, pcr_mm[i//48], s.bottom(5), new_tip='never')
            p10.blow_out(s.top())
        p10.drop_tip()

    robot.pause('Spin down the samples in a microfuge and run in the indexing \
PCR pre-programmed thermocycler. Samples can be stored in thermocycler \
overnight at 4 °C. Place samples on magnetic module in slot 1, and place a \
fresh elution plate in slot 5 before resuming.')

    """ Bead Cleanup """

    cleanup(32.5, te_buffer)
