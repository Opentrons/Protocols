from itertools import groupby

metadata = {
    'protocolName': 'Normalization with Input .CSV File',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):
    [csv_samp, tip_start, p20_mount, p300_mount] = get_values(  # noqa: F821
        "csv_samp", "tip_start", "p20_mount", "p300_mount")

    # load labware
    source_plates = [ctx.load_labware('biorad_96_wellplate_200ul_pcr', slot)
                     for slot in ['3', '6', '9']]
    dest_plates = [ctx.load_labware('biorad_96_wellplate_200ul_pcr', slot)
                   for slot in ['2', '5', '8']]
    tiprack20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
                 for slot in ['1', '4', '7']]
    tiprack200 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '11')]
    diluent_rack = ctx.load_labware(
                    'opentrons_6_tuberack_50000ul', '10')

    # load instrument
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount,
                              tip_racks=tiprack20)
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=tiprack200)
    p300.starting_tip = tiprack200[0].wells()[tip_start-1]

    plate_map = [[val.strip() for val in line.split(',')]
                 for line in csv_samp.splitlines()
                 if line.split(',')[0].strip()][1:]

    # csv numbers
    plate_num = 0
    well = 1
    dil_vol = 4
    sample_vol = 5

    plate_lengths = []
    for row in plate_map:
        plate_lengths.append(row[plate_num])

    grouped_plates = [list(b) for a, b in groupby(plate_lengths)]

    # transfer diluent
    p300.pick_up_tip()
    for row in plate_map:
        p300.aspirate(int(row[dil_vol]), diluent_rack.wells()[0])
        p300.dispense(int(row[dil_vol]),
                      dest_plates[int(row[plate_num])-1].wells_by_name()[
                        row[well]])
        p300.blow_out()
    p300.drop_tip()
    ctx.comment('\n\n\n')

    ctx.pause('''
                 Diluent is transferred to all plates.
                 Place the first sample source plate in slot 3 to begin
                 after selecting "Resume" on the Opentrons App.
             ''')

    row_ctr = 0
    for i, chunk in enumerate(grouped_plates):
        for row, plate in zip(plate_map[row_ctr:], chunk):
            p20.pick_up_tip()
            p20.distribute(int(row[sample_vol]),
                           source_plates[int(row[plate_num])-1].wells_by_name()
                           [row[well]],
                           dest_plates[int(row[plate_num])-1].wells_by_name()[
                              row[well]],
                           new_tip='never',
                           blowout_location='source well')
            p20.blow_out()
            p20.drop_tip()
            row_ctr += 1
        if i < 2:
            ctx.pause(f'''Source plate {i+1} is transferred,
                    please load source plate {i+2}
                    and select "Resume on the Opentrons App."
                    ''')
