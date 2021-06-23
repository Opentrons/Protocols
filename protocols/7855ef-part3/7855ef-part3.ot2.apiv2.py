import math
import csv
import os


metadata = {
    'protocolName': 'Agriseq Library Prep Part 3 - Barcoding',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.7'
}


def run(protocol):

    [num_samp, m20_mount, reset_tipracks] = get_values(  # noqa: F821
        "num_samp", "m20_mount", "reset_tipracks")

    if not 1 <= num_samp <= 288:
        raise Exception("Enter a sample number between 1-288")

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
    barcode_plate = [protocol.load_labware('customendura_96_wellplate_200ul',
                                           str(slot),
                                           label='Ion Barcode Plate')
                     for slot in [1, 2, 3]]
    reaction_plates = [protocol.load_labware('customendura_96_wellplate_200ul',
                       str(slot), label='Reaction Plate')
                       for slot in [4, 5, 6]]
    mmx_plate = protocol.load_labware('customendura_96_wellplate_200ul', '7',
                                      label='MMX Plate')
    tiprack20 = [protocol.load_labware('opentrons_96_filtertiprack_20ul',
                 str(slot))
                 for slot in [9, 10, 11]]

    # load instruments
    m20 = protocol.load_instrument('p20_multi_gen2', m20_mount,
                                   tip_racks=tiprack20)

    tips = [col for tipbox in tiprack20 for col in tipbox.rows()[0]]

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

    # load reagents
    barcode_rxn_mix = mmx_plate.rows()[0][2]
    reaction_plate_cols = [col for plate in reaction_plates
                           for col in plate.rows()[0]][:num_col]
    barcode_plate_cols = [col for plate in barcode_plate
                          for col in plate.rows()[0]]

    # add barcode adapter
    airgap = 5
    for s, d in zip(barcode_plate_cols, reaction_plate_cols):
        pick_up()
        m20.aspirate(1, s)
        m20.air_gap(airgap)
        m20.dispense(1+airgap, d)
        m20.mix(2, 8, d)
        m20.blow_out()
        m20.return_tip()

    # add barcode reaction mix
    for col in reaction_plate_cols:
        pick_up()
        m20.aspirate(3, barcode_rxn_mix)
        m20.air_gap(airgap)
        m20.dispense(1+airgap, col)
        m20.mix(2, 8, col)
        m20.blow_out()
        m20.return_tip()

    protocol.comment('''Barcoding sample libraries complete. Store at -20C after
                   centrifuge and PCR steps if needed as a break point''')

    # write updated tipcount to CSV
    new_tip_count = str(tip_counter)+", "+"\n"
    if not protocol.is_simulating():
        with open(file_path, 'w') as outfile:
            outfile.write(new_tip_count)
