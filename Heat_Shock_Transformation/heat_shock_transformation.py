from opentrons import containers, instruments


tiprack200 = containers.load('tiprack-200ul', 'A1')
tiprack10 = containers.load('tiprack-10ul', 'B2')
tube_rack = containers.load('tube-rack-2ml', 'D1')
cold_deck = containers.load('tube-rack-2ml', 'D2')
trash = containers.load('point', 'A1')
heat_deck = containers.load('tube-rack-2ml', 'B3')

p200 = instruments.Pipette(
    name="p200",
    trash_container=trash,
    tip_racks=[tiprack200],
    max_volume=200,
    axis="b"
)

p10 = instruments.Pipette(
    name="p10",
    trash_container=trash,
    tip_racks=[tiprack10],
    max_volume=10,
    axis="a"
)

# six sample protocol
num_samples = 6

DNA_vol = 2
cell_vol = 25


# add DNA from tube column B to tube column A in cold deck
p10.transfer(
    DNA_vol,
    cold_deck.cols('B').wells('1', length=num_samples),
    cold_deck.cols('A').wells('1', length=num_samples),
    mix_after=(3, 10),
    new_tip='always'
)

# delay 30 minutes after adding DNA
p10.delay(minutes=30)

# move dna/cells from cold deck to heat deck and then back
volume = DNA_vol + cell_vol
for i in range(num_samples):
    p200.pick_up_tip()

    p200.aspirate(volume, cold_deck.cols('A').wells(i))
    p200.dispense(heat_deck.cols('A').wells(i))
    p200.touch_tip()

    p200.delay(minutes=1)

    p200.aspirate(volume, heat_deck.cols('A').wells(i))
    p200.dispense(cold_deck.cols('A').wells(i))
    p200.touch_tip()

    p200.drop_tip()

# delay 5 minutes after heat shock
p200.delay(minutes=5)

# add LB to dna/cells
p200.distribute(
    200,
    tube_rack.wells('A1'),
    cold_deck.cols('A').wells('1', length=num_samples)
)
