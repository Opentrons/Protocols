from opentrons import labware, instruments

# number times to mix solutions
solmix = 10  # can change here

# reagent and solutions volumes
r_vol = 295  # can change here (reagent)
x_vol = 5  # can change here (solution x)
y_vol = 5  # can change here (solution y)

# tip racks
p200rack = labware.load('tiprack-200ul', '1')
p10rack = labware.load('tiprack-10ul', '2')

# solutions X1, X2, Y1, Y2, X, and Y; reagent
solutions = labware.load('trough-12row-short', '3')
reagent = labware.load('point', '4')

# 96 well plate 1
plate1 = labware.load('96-PCR-flat', '5')
# 96 well plate 2
plate2 = labware.load('96-PCR-flat', '6')

# p10 (1 - 10 uL) (single)
p10single = instruments.P10_Single(
    mount='right',
    tip_racks=[p10rack])

# p300 (20 - 300 uL) (multi)
p300multi = instruments.P300_Multi(
    mount='left',
    tip_racks=[p200rack])

# locations of each solution
x_sols = [well for well in solutions.wells('A1', length=2)]
y_sols = [well for well in solutions.wells('A3', length=2)]
x = solutions['A5']
y = solutions['A6']

# all plate wells
wells = [col for col in plate1.cols()] + [col for col in plate2.cols()]

# wells in rows in plate 1
plate1_oddcols = [
    well for col in plate1.cols(0, length=6, step=2) for well in col]
plate1_evencols = [
    well for col in plate1.cols(1, length=6, step=2) for well in col]

# wells in columns in plate 2
plate2_oddrows = [
    well for row in plate2.rows(0, length=4, step=2) for well in row]
plate2_evenrows = [
    well for row in plate2.rows(1, length=4, step=2) for well in row]

# blue wells
blue = plate1_oddcols[0:16:2] + \
    plate1_evencols[1:8:2] + \
    [well for well in plate1.wells('A4', length=24)] + \
    plate2_oddrows[0::2] + \
    plate2_evenrows[1::2]

# orange wells
orange = [well for well in plate1.wells('A7', length=24)] + \
    plate1_evencols[32:48:2] + \
    plate1_oddcols[41:48:2] + \
    plate2_oddrows[1::2] + \
    plate2_evenrows[0::2]

# transfer x1 and x2 to X position, mix X
p300multi.transfer(125, x_sols, x, new_tip='always')
p300multi.pick_up_tip()
p300multi.mix(solmix, 250, x)
p300multi.drop_tip()

# transfer y1 and y2 to Y position, mix Y
p300multi.transfer(125, y_sols, y, new_tip='always')
p300multi.pick_up_tip()
p300multi.mix(solmix, 250, y)
p300multi.drop_tip()

# transfer reagent to all wells
p300multi.transfer(r_vol, reagent, wells)

# transfer solution x to blue wells
p10single.transfer(x_vol, x, blue, mix_after=(3, 10))

# transfer solution y to orange wells
p10single.transfer(y_vol, y, orange, mix_after=(3, 10))
