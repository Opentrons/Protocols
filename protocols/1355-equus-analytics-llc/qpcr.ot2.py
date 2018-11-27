from opentrons import labware, instruments

# labware setup
tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '1')
plate = labware.load('96-flat', '2')

tipracks = [labware.load('tiprack-10ul', slot)
            for slot in ['3', '4']]

# reagent setup
samples = tuberack.wells('A1', length=8)
assays = tuberack.wells('A3', length=12)
water = tuberack.wells('A6')
master_mix = tuberack.wells('B6')

# instrument setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=tipracks)


def run_custom_protocol(
        water_volume: float=2.5,
        master_mix_volume: float=4.5,
        assay_volume: float=1,
        sample_volume: float=1):

    # transfer water and master mix to plate
    p10.pick_up_tip()
    p10.distribute(
        water_volume,
        water,
        plate.wells(),
        blow_out=True,
        new_tip='never')
    p10.distribute(
        master_mix_volume,
        master_mix,
        plate.wells(),
        disposal_vol=0,
        blow_out=True,
        new_tip='never')
    p10.drop_tip()

    # transfer assays to plate
    for assay, dest in zip(assays, plate.cols()):
        p10.distribute(1, assay, dest)

    # transfer samples to plate
    for sample, dest in zip(samples, plate.rows()):
        for well in dest:
            p10.transfer(1, sample, well, blow_out=True)
