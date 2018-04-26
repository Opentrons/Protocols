from opentrons import labware, instruments

p300rack = labware.load('tiprack-200ul', '11', 'p300rack')
trough = labware.load('trough-12row', '10', 'trough')
plate = labware.load('96-PCR-flat', '4', 'plate')
top_plate = labware.load('96-PCR-flat', '5', 'top_plate')
liquid_trash = labware.load('trash-box', '3')

p300_multi = instruments.P300_Multi(
    tip_racks=[p300rack],
    mount='right'
)

# Reagent locations in trough:

# trough row 1 = buffer
# trough row 2 = Ph-Ch-Iso-Amyl mix
# trough row 3 = isopropanol
# trough row 4 = ethanol


# Transfer 300uL of L buffer from trough to 96 well deep plate with same tips
p300_multi.transfer(300, trough('A1'), plate.cols('1', to='12'))

# Transfer 180uL of Ph-Ch-Iso-Amyl mixture to 96 well deep plate
p300_multi.transfer(180, trough('A2'), plate.cols('1', to='12'))

# Transfer top layer (200uL) from 96 well deep plate to new 96 deep well plate
top_source = [col[0].top(-2) for col in plate.cols('1', to='12')]
p300_multi.transfer(
    200, top_source, top_plate.cols())

# Transfer 280uL of isopropanol to this new plate with top layer
p300_multi.transfer(280, trough('A3'), top_plate.cols('1', to='12'))

# Remove the isopropanol and discard.
top_source_1 = [col[0].top(-2) for col in top_plate.cols('1', to='12')]
p300_multi.transfer(280, top_source_1, liquid_trash)

# Transfer 450uL of ethanol and wash the pellet.
p300_multi.transfer(
    450, trough('A4'), top_plate.cols('1', to='12'), mix_after=(5, 300))

# Remove the ethanol and discard
top_source_2 = [col[0].top(-2) for col in top_plate.cols('1', to='12')]
p300_multi.transfer(450, top_source_2, liquid_trash)
