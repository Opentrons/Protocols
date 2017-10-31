from opentrons import containers, instruments

# number times to mix solutions
solmix = 10  # can change here

# reagent and solutions volumes
r_vol = 295  # can change here (reagent)
x_vol = 5  # can change here (solution x)
y_vol = 5  # can change here (solution y)

# tip racks
p200rack = containers.load('tiprack-200ul', 'B2')
p10rack = containers.load('tiprack-10ul', 'D2')

# tip disposal
trash = containers.load('trash-box', 'D1')

# solutions X1, X2, Y1, Y2, X, and Y; reagent
solutions = containers.load('trough-12row-short', 'A2')
reagent = containers.load('point', 'C1')

# 96 well plate 1
plate1 = containers.load('96-PCR-flat', 'A1')
# 96 well plate 2
plate2 = containers.load('96-PCR-flat', 'B1')

# p10 (1 - 10 uL) (single)
p10single = instruments.Pipette(
    axis='b',
    name='p10single',
    max_volume=10,
    min_volume=1,
    channels=1,
    trash_container=trash,
    tip_racks=[p10rack])

# p300 (20 - 300 uL) (multi)
p300multi = instruments.Pipette(
    axis='a',
    name='p300multi',
    max_volume=300,
    min_volume=20,
    channels=8,
    trash_container=trash,
    tip_racks=[p200rack])

# locations of each solution
x_sols = [well for well in solutions.wells('A1', length=2)]
y_sols = [well for well in solutions.wells('A3', length=2)]
x = solutions['A5']
y = solutions['A6']

# all plate wells
wells = [row for row in plate1.rows()] + [row for row in plate2.rows()]

# wells in rows in plate 1
plate1_oddrows = [
    well for row in plate1.rows(0, length=6, step=2) for well in row]
plate1_evenrows = [
    well for row in plate1.rows(1, length=6, step=2) for well in row]

# wells in columns in plate 2
plate2_oddcols = [
    well for col in plate2.columns(0, length=4, step=2) for well in col]
plate2_evencols = [
    well for col in plate2.columns(1, length=4, step=2) for well in col]

# blue wells
blue = plate1_oddrows[0:16:2] + \
    plate1_evenrows[1:8:2] + \
    [well for well in plate1.wells('A4', length=24)] + \
    plate2_oddcols[0::2] + \
    plate2_evencols[1::2]

# orange wells
orange = [well for well in plate1.wells('A7', length=24)] + \
    plate1_evenrows[32:48:2] + \
    plate1_oddrows[41:48:2] + \
    plate2_oddcols[1::2] + \
    plate2_evencols[0::2]

# transfer x1 and x2 to X position, mix X
p300multi.transfer(125, x_sols, x, new_tip='always')
p300multi.mix(solmix, 250, x)

# transfer y1 and y2 to Y position, mix Y
p300multi.transfer(125, y_sols, y, new_tip='always')
p300multi.mix(solmix, 250, y)

# transfer reagent to all wells
p300multi.transfer(r_vol, reagent, wells)

# transfer solution x to blue wells
p10single.transfer(x_vol, x, blue, mix_after=(3, 10))

# transfer solution y to orange wells
p10single.transfer(y_vol, y, orange, mix_after=(3, 10))
