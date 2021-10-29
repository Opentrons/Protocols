import math
import csv
import os
from opentrons.types import Point

metadata = {
    'protocolName': 'Agriseq Library Prep Part 1 - DNA transfer',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(protocol):

    [num_samp, m20_mount, reset_tipracks] = get_values(  # noqa: F821
        "num_samp", "m20_mount", "reset_tipracks")

    if not 1 <= num_samp <= 384:
        raise Exception("Enter a sample number between 1-384")

    num_col = math.ceil(num_samp/8)

    # Tip tracking between runs
    if not protocol.is_simulating():
        file_path = '/data/csv/tiptracking.csv'
        file_dir = os.path.dirname(file_path)
        # check for file directory
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        # check for file; if not there, create initial tip count tracking
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as outfile:
                outfile.write("0, 0\n")

    tip_count_list = []
    if protocol.is_simulating():
        tip_count_list = [0]
    elif reset_tipracks:
        tip_count_list = [0]
    else:
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            tip_count_list = next(csv_reader)

    tip_counter = int(tip_count_list[0])

    # load labware
    sample_plates = [protocol.load_labware(
                    'fisherscientific_96_wellplate_200ul',
                     str(slot), label='Sample Plate') for slot in [1, 2, 3, 4]]
    reaction_plate = protocol.load_labware(
                    'microamp_384_wellplate_100ul', '5',
                    label='Reaction Plate')
    mmx_plate = protocol.load_labware('customendura_96_wellplate_200ul', '7',
                                      label='MMX Plate')
    tiprack20 = [protocol.load_labware('opentrons_96_filtertiprack_20ul',
                                       str(slot))
                 for slot in [9, 10, 11]]

    # load instruments
    m20 = protocol.load_instrument('p20_multi_gen2', m20_mount,
                                   tip_racks=tiprack20)

    tips = [col for tipbox in tiprack20 for col in tipbox.rows()[0]]

    def touchtip(pip, well):
        knock_loc = well.top(z=-1).move(
                    Point(x=-(well.diameter/2.25)))
        knock_loc2 = well.top(z=-1).move(
                Point(x=(well.diameter/2.25)))
        pip.move_to(knock_loc)
        pip.move_to(knock_loc2)

    def pick_up():
        nonlocal tip_counter
        if tip_counter == 36:
            protocol.home()
            protocol.pause('Replace 20 ul tip racks on Slots 9, 10, and 11')
            m20.reset_tipracks()
            tip_counter = 0
            pick_up()
        else:
            m20.pick_up_tip(tips[tip_counter])
            tip_counter += 1

    sample_plate_cols = [col for plate in sample_plates
                         for col in plate.rows()[0]][:num_col]
    reaction_plate_cols = [col for j in range(2) for i in range(2)
                           for col in reaction_plate.rows()[i][j::2]][:num_col]

    # load reagents
    amplify_mix = mmx_plate.rows()[0][:2]

    # add amplification mix
    airgap = 2
    num = 0
    pick_up()
    for col in reaction_plate_cols:
        if num > 192:
            amplify_mix_well = amplify_mix[1]
        else:
            amplify_mix_well = amplify_mix[0]
        m20.aspirate(7, amplify_mix_well)
        touchtip(m20, amplify_mix_well)
        m20.air_gap(airgap)
        m20.dispense(airgap, col)
        m20.dispense(7, col)
        m20.blow_out()
        touchtip(m20, col)
        num += 8
    m20.return_tip()
    protocol.comment('\n\n\n\n')

    # add DNA
    for s, d in zip(sample_plate_cols, reaction_plate_cols):
        pick_up()
        m20.aspirate(3, s)
        touchtip(m20, s)
        m20.air_gap(airgap)
        m20.dispense(airgap, d.top())
        m20.dispense(3, d)
        m20.mix(2, 5, d)
        m20.blow_out()
        touchtip(m20, d)
        m20.return_tip()

    protocol.home()
    protocol.pause('''Protocol method complete. Please remove reaction plates
                   from deck and proceed with PCR and centrifuge steps.
                   Return reaction plates back to deck and continue to
                   Part 2 - Pre-ligation.''')

    # write updated tipcount to CSV
    new_tip_count = str(tip_counter)+", "+"\n"
    if not protocol.is_simulating():
        with open(file_path, 'w') as outfile:
            outfile.write(new_tip_count)
