import math

metadata = {
    'protocolName': 'PCR/qPCR prep: distribute samples to 384 well plate',
    'author': 'Steve Plonk <protocols@opentrons.com>',
    'apiLevel': '2.9'
}


def run(ctx):

    # bring in constant values from json string above
    [labware_384_well_plate, patient_sample_vol, disposal_vol,
     patient_sample_count
     ] = get_values(  # noqa: F821
      'labware_384_well_plate', 'patient_sample_vol', 'disposal_vol',
      'patient_sample_count')

    ctx.set_rail_lights(True)

    # p20 multi channel, tips
    tips20 = [ctx.load_labware("opentrons_96_filtertiprack_20ul", '3')]

    p20m = ctx.load_instrument(
        "p20_multi_gen2", "right", tip_racks=tips20)

    # source and destination plates
    patient_samples = ctx.load_labware("nunc_96_wellplate_1000ul", '2')
    three_eighty_four = ctx.load_labware(
     labware_384_well_plate, '4')

    # number of patient sample columns
    num_cols = math.ceil(patient_sample_count / 8)

    # to yield next 384 column
    next_col = (column for column in three_eighty_four.columns())

    # distribute sample in "384 plate map.png" arrangement
    for column in patient_samples.columns()[:num_cols]:
        p20m.distribute(
         patient_sample_vol, column, [
          next(next_col), next(next_col)], disposal_volume=disposal_vol)
