CSV_PATH = 'path/to/your.csv'
DESIRED_CONCENTRATION = 1000  # µg/ml
TOTAL_VOLUME = 100  # µl


# metadata
metadata = {
    'protocolName': 'Normalization',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    # labware
    source_plate = ctx.load_labware('greinerbioone_96_wellplate_343ul', '1',
                                    'source plate')
    norm_plate = ctx.load_labware('greinerbioone_96_wellplate_343ul', '2',
                                  'normalization plate')
    buffer = ctx.load_labware('nest_12_reservoir_15ml', '3',
                              'buffer (channel 1)').wells()[0]
    tipracks20 = [
        ctx.load_labware('opentrons_96_tiprack_20ul', slot)
        for slot in ['4', '7']]
    tipracks300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['5', '8']]

    # pipette
    p20 = ctx.load_instrument('p20_single_gen2', 'left', tip_racks=tipracks20)
    p300 = ctx.load_instrument('p300_single_gen2', 'right',
                               tip_racks=tipracks300)

    # data
    with open(CSV_PATH, 'r') as csv_file:
        data = [
            [val.strip().upper() for val in line.split(',')]
            for line in csv_file.readlines()][1:]

    def get_sample_volume(initial_concentration):
        factor = initial_concentration/DESIRED_CONCENTRATION
        return round(TOTAL_VOLUME/factor, 2)

    # pre-load volume data
    well_data = {}
    for line in data:
        print(line)
        well_name = line[1]
        conc = float(line[9])
        sample_vol = get_sample_volume(conc)
        well_data[well_name] = {
            'sample-vol': sample_vol,
            'buffer-vol': TOTAL_VOLUME - sample_vol
        }

    # pre-transfer buffer with one tip
    for well_name in well_data.keys():
        buffer_vol = well_data[well_name]['buffer-vol']
        pip = p20 if buffer_vol < 20 else p300
        if not pip.has_tip:
            pip.pick_up_tip()
        pip.transfer(buffer_vol, buffer, norm_plate.wells_by_name()[well_name],
                     new_tip='never')
    [pip.drop_tip() for pip in [p20, p300] if pip.has_tip]

    # transfer sample and mix once
    for well_name in well_data.keys():
        sample_vol = well_data[well_name]['sample-vol']
        pip = p20 if buffer_vol < 20 else p300
        pip.transfer(sample_vol, source_plate.wells_by_name()[well_name],
                     norm_plate.wells_by_name()[well_name],
                     mix_after=(1, pip.min_volume))
