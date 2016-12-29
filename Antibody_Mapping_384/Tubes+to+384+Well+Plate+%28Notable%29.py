from opentrons import containers, instruments


p200rack = containers.load('tiprack-200ul', 'A1')
trash = containers.load('point', 'A2')
tube_rack = containers.load('tube-rack-2ml', 'C2')
plate = containers.load('384-plate', 'C1')

p200 = instruments.Pipette(
    axis="b",
    max_volume=200,
    tip_racks=[p200rack],
    trash_container=trash
)

# dispense 40 uL from tube to plate, for 24 tubes
num_samples = 24
p200.transfer(
    40, tube_rack[:num_samples], plate[:num_samples], tips=num_samples)
