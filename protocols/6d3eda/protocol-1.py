
metadata={"apiLevel": "2.0"}

#def get_values(sample_count, volume, input_labware, output_labware):
#    return 48, 50, 'corning_24_wellplate_3.4ml_flat', 'corning_24_wellplate_3.4ml_flat'

def run(ctx):

    # Add tip tracking to this protocol
    sample_count, volume, input_labware, output_labware = get_values(
            'sample_count', 'volume', 'input_labware', 'output_labware')
    sample_plates = [ctx.load_labware(input_labware, '2')] 
    target_plates = [ctx.load_labware(output_labware, '5')]
    tip_racks = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '1')]
    if sample_count > 24:
        sample_plates.append(ctx.load_labware(input_labware, '3'))
        target_plates.append(ctx.load_labware(output_labware, '6'))

    # Variable pipettes?
    p300s = ctx.load_instrument('p300_single_gen2', "right", tip_racks=tip_racks)

    for i,sample_plate in enumerate(sample_plates):
        for well_num,well in enumerate(sample_plate.wells()[:sample_count-(i*24)]):
            p300s.transfer(volume, well, target_plates[i].wells()[well_num], blow_out=True, new_tip='always')
