import math

metadata = {
    'protocolName': '16S Library pooling',
    'author': 'Parrish Payne <parrish.payne@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.13'
}

    # Step 1: Use a single channel pipettor and a new tip each time, transfer 2-35 uL from the 96 well PCR plate to a single 2 mL snap tube
    # Step 2: Repeat across the entire plate according to the .csv file

def run(ctx):

    # [input_csv, p20_mount] = get_values(  # noqa: F821
    #     'input_csv', 'p20_mount')


    input_csv = """
    Sample Location,Qubits,Volume (ul) for ng: 70,,,,,,,,,,,
A1,3.5,35.0,,,,,,,,,,,
A2,15,4.7,,,,,,,,,,,
A3,20,3.5,,,,,,,,,,,
"""

    p20_mount = 'right'

    # labware

    mag_mod = ctx.load_module('magnetic module gen2', 6)   # not used during protocol
    pcr_plates = [ctx.load_labware('armadillo_96_wellplate_200ul_pcr_full_skirt', slot)
            for slot in [2, 5, 8]]

    tube_rack = ctx.load_labware('opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', 3)

    tips = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
            for slot in [1]]

    # pipettes
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=tips)

    # Helper Functions
    def pick_up(pip):
        """Function that can be used instead of .pick_up_tip() that will pause
        robot when robot runs out of tips, prompting user to replace tips
        before resuming"""
        try:
            pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            pip.home()
            ctx.pause("Replace the tips")
            pip.reset_tipracks()
            pip.pick_up_tip()

    def slow_withdraw(pip, well, delay_seconds=2.0):
        pip.default_speed /= 16
        if delay_seconds > 0:
            ctx.delay(seconds=delay_seconds)
        pip.move_to(well.top())
        pip.default_speed *= 16

    # mapping
    pool_well = tube_rack.wells()[0]

    # parse
    all_rows = [
        [val.strip().upper() for val in line.split(',')]
        for line in input_csv.splitlines()[1:]
        if line and line.split(',')[0]][1:]

    all_samples = [
        well
        for plate in pcr_plates
        for well in plate.wells()
        ]

    for row, source in zip(all_rows, all_samples):

        volume = float(row[2])

        p20.pick_up_tip()

        if volume > 20:
            num_transfers = math.ceil(volume/p20.max_volume)
            transfer_vol = volume/num_transfers
            for _ in range(num_transfers):

                p20.aspirate(transfer_vol, source)
                p20.dispense(transfer_vol, pool_well)

        else:
            p20.aspirate(volume, source)
            p20.dispense(volume, pool_well)

        p20.drop_tip()
