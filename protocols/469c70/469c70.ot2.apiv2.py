metadata = {
    'protocolName': 'Serial Dilution of Analyte Stock',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [csv, mount] = get_values(  # noqa: F821
        "csv", "mount")

    # load labware
    serial_rack1 = ctx.load_labware(
                    'opentrons_15_tuberack_falcon_15ml_conical', '1',
                    label='SERIAL RACK 1')
    serial_rack2 = ctx.load_labware(
                    'opentrons_15_tuberack_falcon_15ml_conical', '2',
                    label='SERIAL RACK 2')
    diluent_labware = ctx.load_labware('nest_1_reservoir_195ml', '3',
                                       label='DILUTION RESERVOIR')
    analyte_stock_rack = ctx.load_labware(
        'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', '4',
        label='STOCK RACK')

    tiprack = ctx.load_labware('opentrons_96_tiprack_1000ul', '6')

    # load instrument
    pip = ctx.load_instrument('p1000_single_gen2', mount, tip_racks=[tiprack])

    # protocol
    list_of_rows = [[val.strip() for val in line.split(',')]
                    for line in csv.splitlines()
                    if line.split(',')[0].strip()][1:]

    slot_num_source = 0
    tube_source = 1
    vol = 3
    slot_num_dest = 4
    tube_dest = 5
    all_labware = [serial_rack1,
                   serial_rack2,
                   diluent_labware,
                   analyte_stock_rack]

    for _ in list_of_rows:
        source = all_labware[int(_[slot_num_source])-1]
        dest = all_labware[int(_[slot_num_dest])-1]
        pip.pick_up_tip()
        pip.transfer(float(_[vol])*1000,
                     source.wells_by_name()[_[tube_source]
                     if int(_[slot_num_source]) != 3 else 'A1'],
                     dest.wells_by_name()[_[tube_dest]].top(),
                     new_tip='never',
                     blow_out=True,
                     blowout_location='destination well')
        if int(_[slot_num_source]) == 3:
            pip.mix(2, 0.6*float(_[vol])*1000
                    if 0.6*float(_[vol])*1000 < 1000 else 1000,
                    dest.wells_by_name()[_[tube_dest]].bottom(z=60))
        pip.drop_tip()
        ctx.comment('\n\n')
