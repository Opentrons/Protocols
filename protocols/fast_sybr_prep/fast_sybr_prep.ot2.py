from opentrons import containers, instruments

# tube rack holding master mix
master_mixes = containers.load('tube-rack-2ml', '1')

# tubes with master mix in rack

# can change position of master mix tubes here
master_mix1 = master_mixes.wells('A1')
# can change position
master_mix2 = master_mixes.wells('A2')

# 96 well plate
destination_plate = containers.load('96-PCR-flat', '2')

# PCR strips with cDNA
pcr_strips = containers.load('PCR-strip-tall', '3')

# tip rack for p10 pipettes
tip10_rack = containers.load('tiprack-10ul', '10')
tip10_rack2 = containers.load('tiprack-10ul', '11')



# p10 (1 - 10 uL) (single)
p10single = instruments.P10_Single(
    mount='right',
    tip_racks=[tip10_rack]
)

# p10 (1 - 10 uL) (multi)
p10multi = instruments.P10_Multi(
    mount='left',
    tip_racks=[tip10_rack2]
)


def run_custom_protocol(vol1: float=8, vol2: float=8, cdna_vol: float=8,
                        num_strips: int=6):
    # set cols of 96 well plate that get each mix
    # 1 to 6 as written, will change based on num_strips
    mix1_cols = [col for col in destination_plate.cols('1', length=num_strips)]
    # 7 to 12 as written, will change based on num_strips
    mix2_cols = [
        col
        for col
        in destination_plate.cols(12 - num_strips, length=num_strips)]

    # pcr strips location
    strips = pcr_strips.cols('1', length=num_strips)

    # transfer master mix1 to 96 plate
    for col in range(0, num_strips):
        p10single.transfer(vol1, master_mix1, mix1_cols[col], new_tip='once')

    # transfer master mix2 to 96 plate
    for col in range(0, num_strips):
        p10single.transfer(vol2, master_mix2, mix2_cols[col], new_tip='once')

    # transfer cDNA from strips to both designated rows of 96 well plate
    for col in range(0, num_strips):
        # cDNA to first designated row
        p10multi.transfer(cdna_vol, strips[col], destination_plate.cols(col))
        # cDNA to second designated row
        p10multi.transfer(
            cdna_vol, strips[col], destination_plate.cols(col + num_strips))
