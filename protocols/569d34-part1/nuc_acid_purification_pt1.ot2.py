from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Nucleic Acid Purification: Part 1/2',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
res_name = 'biomek_4_reservoir_40ml'
if res_name not in labware.list():
    labware.create(
        res_name,
        grid=(4, 1),
        spacing=(7.4325, 0),
        diameter=23.65,
        depth=3.5,
        volume=40700
    )

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
        diameter=7,
        depth=45,
        volume=1200
    )

# load modules and labware
strip_rack = labware.load(tube_name, '1', 'collection strip tubes (racked)')
res = labware.load(res_name, '2', 'reagent reservoir')
magdeck = modules.load('magdeck', '4')
mag_plate = labware.load(
    deep_name, '4', 'deepwell plate on magdeck', share=True)
slots300 = ['6', '7']
tips300 = [
    labware.load('opentrons_96_tiprack_300ul', slot) for slot in slots300]


def run_custom_protocol(
        p300_multi_mount: StringSelection('right', 'left') = 'right',
        number_of_samples: int = 96,
        volume_of_lysate_to_transfer_in_ul: float = 500
):
    # checks
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Invalid sample number (must be in [1, 96])')

    # reagents
    num_lysis_buff_chan = 2 if number_of_samples > 48 else 1
    lysis_buff = res.wells(0, length=num_lysis_buff_chan)

    # pipettes
    m300 = instruments.P300_Multi(mount=p300_multi_mount, tip_racks=tips300)

    strips_multi = strip_rack.rows('A')[:math.ceil(number_of_samples/8)]
    mag_multi = mag_plate.rows('A')[:math.ceil(number_of_samples/8)]

    slot300_str = ''
    for i, s in enumerate(slots300):
        temp = s + ', ' if i < len(slots300)-1 else s
        slot300_str += temp

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

    # distribute lysis buffer to collection tubes containing sample
    pick_up('m300')
    for i, s in enumerate(strips_multi):
        m300.transfer(
            720,
            lysis_buff[i*num_lysis_buff_chan//len(strips_multi)],
            s.top(),
            new_tip='never'
        )
        m300.blow_out(s.top())
    m300.drop_tip()

    robot.pause('Off robot steps: mix plant sample and lysis buffer in \
collection tubes on slot 2 using TissueLyserII, incubate at 56°C for 30 \
minutes, and centrifuge at 4,000 x g for 10 minutes')

    # carefully transfer lysate from collection tubes to corresponding wells of
    # magnetic module deep plate
    m300.set_flow_rate(aspirate=50)
    for s, d in zip(strips_multi, mag_multi):
        pick_up('m300')
        m300.transfer(
            volume_of_lysate_to_transfer_in_ul, s, d.top(), new_tip='never')
        m300.mix(10, 250, d)
        m300.blow_out(d.top())
        m300.drop_tip()
    m300.set_flow_rate(aspirate=150)

    robot.comment('Let sit at room temperature for 5 minutes, and continue \
with part 2.')
