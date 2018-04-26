from opentrons import labware, instruments


p200rack = labware.load('tiprack-200ul', '1')
tube_rack = labware.load('tube-rack-2ml', '4')
plate = labware.load('384-plate', '2')


p200 = instruments.P300_Single(
    mount="right",
    tip_racks=[p200rack],
)

# dispense 40 uL from tube to plate, for 24 tubes
p200.transfer(
    40,
    tube_rack.wells('A1', length=24),
    plate.rows('A'),
    new_tip='always'
)
