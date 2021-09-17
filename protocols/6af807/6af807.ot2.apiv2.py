"""Protocol."""
import os
import csv
import math

metadata = {
    'protocolName': '384 Well Plate PCR Plate with Triplicates',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.8'
}


def run(ctx):
    """Protocol."""
    [num_gene, num_mastermix,
        reset_tipracks, p20_mount] = get_values(  # noqa: F821
        "num_gene", "num_mastermix", "reset_tipracks", "p20_mount")

    if not 1 <= num_mastermix <= 24:
        raise Exception("Enter a number of mastermixes between 1-24")
    if not 1 <= num_gene <= 24:
        raise Exception("Enter a number of cDNA 1-24")

    # Tip tracking between runs
    if not ctx.is_simulating():
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
    if ctx.is_simulating():
        tip_count_list = [0]
    elif reset_tipracks:
        tip_count_list = [0]
    else:
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            tip_count_list = next(csv_reader)

    tip_counter = int(tip_count_list[0])

    # load labware
    plate = ctx.load_labware('100ul_384_wellplate_100ul', '1')
    mastermix = ctx.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '2')
    cDNA = ctx.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '3')
    tiprack = ctx.load_labware('thermofisherart_96_tiprack_10ul', '4')

    # load instrument
    p20 = ctx.load_instrument('p20_single_gen2',
                              p20_mount, tip_racks=[tiprack])

    tips = [tip for tip in tiprack.wells()]

    def pick_up():
        nonlocal tip_counter
        if tip_counter == 96:
            ctx.home()
            ctx.pause('Replace 20ul tip rack')
            p20.reset_tipracks()
            tip_counter = 0
            pick_up()
        else:
            p20.pick_up_tip(tips[tip_counter])
            tip_counter += 1

    # ctx
    cDNA_tubes = cDNA.wells()[:num_gene]

    num_mastermix_in_row = math.floor(24/num_mastermix)
    row_stride = math.floor(24/num_mastermix_in_row)
    chopped_plate = [plate.columns()[i][:15]
                     for i in range(0, len(plate.columns()))]
    plate_map = [well for col in chopped_plate[::row_stride]
                 for i in range(0, num_gene*3, 3)
                 for well in col[i:i+3]]
    chunks = [plate_map[i:i+3] for i in range(0, len(plate_map), 3)]

    num_mastermix_in_row = int(math.floor(24/num_mastermix)/(num_mastermix*3))
    airgap = 2
    for tube, chunk in zip(cDNA_tubes, chunks):
        pick_up()
        for well in chunk:
            p20.aspirate(4, tube)
            p20.touch_tip()
            p20.air_gap(airgap)
            p20.dispense(4+airgap, well)
            p20.blow_out()
            p20.touch_tip()
        ctx.comment('\n')
        p20.drop_tip()

    num_rows_in_each_column = []
    remaining_wells = math.floor(num_gene*3 % 15)

    for i, col in enumerate(chopped_plate[:num_mastermix]):
        if num_gene > 5:
            if i != len(chopped_plate[:num_mastermix])-1:
                num_rows_in_each_column.append(15)
            else:
                if remaining_wells == 0:
                    num_rows_in_each_column.append(15)
                else:
                    num_rows_in_each_column.append(remaining_wells)
        else:
            num_rows_in_each_column.append(num_gene*3)

    for tube, column, num_rows in zip(mastermix.wells(),
                                      chopped_plate[:num_mastermix],
                                      num_rows_in_each_column):
        pick_up()
        for i, well in enumerate(column[:num_rows]):
            p20.aspirate(10, tube, rate=0.5)
            ctx.delay(seconds=1)
            p20.dispense(10, well.top(), rate=0.5)
            p20.blow_out()

            p20.aspirate(6, tube, rate=0.5)
            ctx.delay(seconds=1)
            p20.dispense(10, well.top(), rate=0.5)
            p20.blow_out()

        p20.drop_tip()
        ctx.comment('\n')
