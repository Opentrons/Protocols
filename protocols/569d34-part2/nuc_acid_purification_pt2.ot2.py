from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math
import time

metadata = {
    'protocolName': 'Nucleic Acid Purification: Part 2/2',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

res_name = 'biomek_4_reservoir_40ml'
if res_name not in labware.list():
    labware.create(
        res_name,
        grid=(4, 1),
        spacing=(7.4325, 0),
        diameter=23.65,
        depth=36,
        volume=40700
    )

# create custom labware
deep_name = 'thermofisherscientific_96_wellplate_2.2ml'
if deep_name not in labware.list():
    labware.create(
        deep_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8.4,
        depth=39.3,
        volume=2200
    )

rxn_name = 'thermofisherscientific_96_wellplate_200ul'
if rxn_name not in labware.list():
    labware.create(
        rxn_name,
        grid=(12, 8),
        spacing=(9.025, 9.025),
        diameter=5.494,
        depth=23.24,
        volume=200
    )

tube_name = 'qiagen_96_tuberack_collection_1.2ml_round'
if tube_name not in labware.list():
    labware.create(
        tube_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=0,
        depth=0,
        volume=1200
    )

# load modules and labware
elution_plate = labware.load(rxn_name, '1', 'elution plate')
reservoirs = [
    labware.load(res_name, slot, 'reagent reservoir ' + str(i))
    for i, slot in enumerate(['2', '3'])
]
magdeck = modules.load('magdeck', '4')
mag_plate = labware.load(deep_name, '4', share=True)
elution_buffer = labware.load(
    res_name, '5', 'elution buffer').wells(0)
mix_tips = labware.load('opentrons_96_tiprack_300ul', '6')
slots300 = [str(slot) for slot in range(7, 12)]
tips300 = [labware.load('opentrons_96_tiprack_300ul', slot)
           for slot in slots300]


def run_custom_protocol(
        p300_multi_mount: StringSelection('right', 'left') = 'right',
        number_of_samples: int = 96,
        volume_of_elution_buffer_in_ul: float = 100
):
    # checks
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Invalid sample number (must be in [1, 96])')

    # reagents
    all_chan = [well for res in reservoirs for well in res.wells()]
    num_bead_buff_chan = 2 if number_of_samples > 72 else 1
    bead_buff = all_chan[:num_bead_buff_chan]
    num_cspw1_chan = 2 if number_of_samples > 72 else 1
    cspw1 = all_chan[2:2+num_cspw1_chan]
    num_cspw2_chan = 2 if number_of_samples > 72 else 1
    cspw2 = all_chan[4:4+num_cspw2_chan]
    num_spm_chan = 2 if number_of_samples > 72 else 1
    spm_buff = all_chan[6:6+num_spm_chan]

    # pipettes
    m300 = instruments.P300_Multi(mount=p300_multi_mount, tip_racks=tips300)
    liquid_waste = m300.trash_container.top()

    mag_multi = mag_plate.rows('A')[:math.ceil(number_of_samples/8)]
    elution_multi = elution_plate.rows('A')[:math.ceil(number_of_samples/8)]

    separator = ', '
    slot300_str = separator.join(slots300)

    tip300_count = 0
    tip300_max = len(tips300)*12

    def pick_up(pip):
        nonlocal tip300_count

        if tip300_count == tip300_max:
            robot.pause('Replace 300ul tips in slots ' + slot300_str + ' \
before resuming.')
            m300.reset()
            tip300_count = 0

        m300.pick_up_tip()
        tip300_count += 1

    def remove_supernatant(vol):
        for m in mag_multi:
            m300.set_flow_rate(aspirate=50)
            pick_up('m300')
            m300.transfer(
                vol,
                mag_multi,
                liquid_waste,
                new_tip='never'
            )
            m300.drop_tip()
            m300.set_flow_rate(aspirate=150)

    # mix and distribute bead buffer to magnetic module deep plate
    for i, s in enumerate(mag_multi):
        pick_up('m300')
        bead_chan = bead_buff[i*num_bead_buff_chan//len(mag_multi)]
        m300.mix(5, 250, bead_chan)
        m300.blow_out(bead_chan.top())
        m300.transfer(520, bead_chan, s.top(), new_tip='never')
        m300.mix(10, 250, s)
        m300.blow_out(s.top())
        m300.drop_tip()

    # iterative mixing
    for mix_rep in range(3):
        t_start = time.time()
        for tip, s in zip(
                mix_tips.rows('A')[:math.ceil(number_of_samples)], mag_multi):
            m300.pick_up_tip(tip)
            m300.mix(5, 250, s)
            m300.blow_out(s.top())
            if mix_rep == 2:
                m300.drop_tip()
            else:
                m300.return_tip()
                t_stop = time.time()
            dt = t_stop - t_start
            if dt < 180:
                m300.delay(seconds=180-dt)

    magdeck.engage(height=15)
    m300.delay(minutes=3)
    # remove supernatant
    remove_supernatant(1200)
    magdeck.disengage()

    # CSPW1 wash
    for i, s in enumerate(mag_multi):
        pick_up('m300')
        m300.transfer(
            500,
            cspw1[i*num_cspw1_chan//len(mag_multi)],
            s.top(),
            new_tip='never'
        )
        m300.mix(10, 250, s)
        m300.blow_out(s.top())
        m300.drop_tip()
    magdeck.engage(height=15)
    m300.delay(minutes=3)
    # remove supernatant
    remove_supernatant(600)
    magdeck.disengage()

    # CSPW2 wash
    for i, s in enumerate(mag_multi):
        pick_up('m300')
        m300.transfer(
            500,
            cspw2[i*num_cspw2_chan//len(mag_multi)],
            s.top(),
            new_tip='never'
        )
        m300.mix(10, 250, s)
        m300.blow_out(s.top())
        m300.drop_tip()
    magdeck.engage(height=15)
    m300.delay(minutes=3)
    # remove supernatant
    remove_supernatant(600)
    magdeck.disengage()

    # SPM wash
    for i, s in enumerate(mag_multi):
        pick_up('m300')
        m300.transfer(
            500,
            spm_buff[i*num_spm_chan//len(mag_multi)],
            s.top(),
            new_tip='never'
        )
        m300.mix(10, 250, s)
        m300.blow_out(s.top())
        m300.drop_tip()
    magdeck.engage(height=15)
    m300.delay(minutes=3)
    # remove supernatant
    remove_supernatant(600)

    # airdry beads for 10 minutes
    m300.delay(minutes=10)
    robot._driver.run_flag.wait()
    magdeck.disengage()

    robot.pause('Place the elution plate (heated to 65C) in slot 1.')

    # elution buffer addition
    for i, s in enumerate(mag_multi):
        pick_up('m300')
        m300.transfer(
            volume_of_elution_buffer_in_ul,
            elution_buffer,
            s,
            new_tip='never'
        )
        m300.mix(10, 80, s)
        m300.blow_out(s.top())
        m300.drop_tip()

    robot.pause('Incubate the deepwell plate from the magnetic module at 65C \
off the deck. Replace on the magnetic module after 5 minutes of incubation.')

    robot._driver.run_flag.wait()
    magdeck.engage(height=15)
    m300.delay(minutes=3)

    # transfer elution to new plate
    for source, dest in zip(mag_multi, elution_multi):
        pick_up('m300')
        m300.transfer(
            volume_of_elution_buffer_in_ul, source, dest, new_tip='never')
        m300.blow_out()
        m300.drop_tip()

    magdeck.disengage()
