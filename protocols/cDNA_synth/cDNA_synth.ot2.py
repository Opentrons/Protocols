from opentrons import labware, instruments

# tube rack holding reagents
reagents = labware.load('tube-rack-2ml', '1')

# 96 well plate
cdna_plate = labware.load('96-PCR-flat', '2')
qpcr_plate = labware.load('96-PCR-flat', '3')
samples = labware.load('96-PCR-flat', '4')

# pcr strip for AffinityScript RT/ RNase Block enzyme mixture
strip = labware.load('PCR-strip-tall', '5')

# tip rack for p50 pipette
tip200_rack = labware.load('tiprack-200ul', '6')
tip200_rack2 = labware.load('tiprack-200ul', '8')
tip200_rack3 = labware.load('tiprack-200ul', '9')

tip200_rack5 = labware.load('tiprack-200ul', '7')
tip200_rack6 = labware.load('tiprack-200ul', '10')
tip200_rack7 = labware.load('tiprack-200ul', '11')

# p50 (5 - 50 uL) (single)
p50single = instruments.Pipette(
    mount='right',
    name='p50single',
    max_volume=50,
    min_volume=5,
    channels=1,
    tip_racks=[tip200_rack, tip200_rack2, tip200_rack3])

# p50 (5 - 50 uL) (multi)
p50multi = instruments.Pipette(
    mount='left',
    name='p50multi',
    max_volume=50,
    min_volume=5,
    channels=8,
    tip_racks=[tip200_rack5, tip200_rack6, tip200_rack7])

water = reagents.wells('A1')
first_mix = reagents.wells('B1')
oligodT = reagents.wells('C1')
affinity = reagents.wells('D1')
qpcr_mm = reagents.wells('A2')
primermix = reagents.wells('B2')

# Step 1: Transfer 5ul of nuclease free water from 2ml tube rack to all wells
# in 96 well plate (same tip) (this is cDNA sythesis plate)
p50single.transfer(5, water, cdna_plate.wells(), new_tip='once')

# Step2: Transfer 10.0 μl of first strand master mix (2×)  from 2ml tube rack
# to all wells in 96 well plate (same tip) (cDNA sythesis plate)
p50single.transfer(10, first_mix, cdna_plate.wells(), new_tip='once')

# Step3:  Tranfer   3.0 μl of oligo(dT) primer  from 2ml tube rack
# to all wells in 96 well plate (same tip)(cDNA sythesis plate)
p50single.transfer(3, oligodT, cdna_plate.wells(), new_tip='once')

# Step4: Use single channel to add 12 μl of AffinityScript RT/ RNase Block
# enzyme mixture from 2ml tube rack to all wells to PCR strips (A to H)
p50single.transfer(12, affinity, strip.cols(0), new_tip='once')

# Step5: Use multichannel to add 1 μl of AffinityScript RT/ RNase Block
# enzyme mixture from PCR strip to 96 well plate.(cDNA sythesis plate)
p50multi.transfer(1, strip.cols(0), cdna_plate.cols(), new_tip='once')

# Step6: Use multichannel to add 1ul of sample from 96 well plate to
# 96 well plate (well A1 to A1, B1 to B1)===== cDNA synthesis plate
p50multi.transfer(1, samples.cols(), cdna_plate.cols(), new_tip='always')

#  HOLD for 1.5hr for cDNA Synthesis
p50single.delay(minutes=90)

# Step7: Transfer 1 μl  of cDNA to another 96 well plate using multichannel
# such well A1 to A1, B1 to B1. (QPCR Plate)
p50multi.transfer(1, cdna_plate.cols(), qpcr_plate.cols(), new_tip='always')

# Step8: Transfer 12.5 μl of 2× Brilliant II SYBR Green QPCR master mix
# to 96 well plate (QPCR plate) (Different tip)
p50single.transfer(12.5, qpcr_mm, qpcr_plate.cols(), new_tip='always')

# Step9: Transfer 2.5 μl of Primer mix from 2ml tube rack to all wells
# in 96 well plate (QPCR plate) (Different tip)
p50single.transfer(2.5, primermix, qpcr_plate.cols(), new_tip='always')
