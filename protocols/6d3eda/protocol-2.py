metadata={"apiLevel": "2.5"}

def run(ctx):
    sample_count = get_values('sample_count')
    sample_plates = [ctx.load_labware('corning_244_wellplate_3.4ml_flat', '9')] # CHANGE THIS TO CUSTOM LABWARE
    target_plates = [ctx.load_labware('corning_24_wellplate_3.4ml_flat', '8')]
    tip_racks = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '7')]


