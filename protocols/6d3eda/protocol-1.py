
metadata={"apiLevel": "2.5"}

def get_values(sample_count):
    return 48

def run(ctx):

    # Add tip tracking to this protocol
    sample_count = get_values('sample_count')
    sample_plates = [ctx.load_labware('corning_24_wellplate_3.4ml_flat', '9')] # CHANGE THIS TO CUSTOM LABWARE
    target_plates = [ctx.load_labware('corning_24_wellplate_3.4ml_flat', '8')]
    tip_racks = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '7')]
    if sample_count > 24:
        sample_plates.append(ctx.load_labware('corning_24_wellplate_3.4ml_flat', '6'))
        target_plates.append(ctx.load_labware('corning_24_wellplate_3.4ml_flat', '5'))
    p300s = ctx.load_instrument('p300_single_gen2', "right", tip_racks=tip_racks)

    for i,sample_plate in enumerate(sample_plates):
        for well_num,well in enumerate(sample_plate.wells()[:sample_count-(i*24)]):
            p300s.transfer(100, well, target_plates[i].wells()[well_num], blow_out=True)
