from opentrons import labware, instruments

metadata = {
    'protocolName': 'Serial Dilution for Analytical Chemistry Part 2: GC',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load labware
tubes_50ml = labware.load('opentrons-tuberack-50ml', '1')
tubes_ep = labware.load('opentrons-tuberack-2ml-eppendorf', '2')
tips1000 = labware.load('tiprack-1000ul', '4')
tips300 = labware.load('opentrons-tiprack-300ul', '5')

# pipettes
p1000 = instruments.P1000_Single(mount='right', tip_racks=[tips1000])
p300 = instruments.P300_Single(mount='left', tip_racks=[tips300])

# solvent addition
solvent = tubes_50ml.wells('A1').top(-90)
dests = ['D4', 'A1', 'A2', 'D3', 'A3', 'A4', 'A5', 'D2', 'A6', 'B1', 'B2',
         'B3', 'D1', 'B4', 'B5', 'B6', 'C1', 'C2', 'C3']
vols = [500, 750, 900, 900, 960, 750, 900, 900, 920, 960, 800, 900, 900, 920,
        950, 800, 900, 920, 950]

p1000.pick_up_tip()
for d, vol in zip(dests, vols):
    dest = tubes_ep.wells(d)
    p1000.transfer(
        vol,
        solvent,
        dest.top(),
        blow_out=True,
        new_tip='never'
    )
p1000.drop_tip()

# stock 100 dilution
p300.transfer(
    100,
    tubes_ep.wells('D5'),
    tubes_ep.wells('D4').top(),
    blow_out=True
)
p1000.pick_up_tip()
p1000.transfer(
    400,
    tubes_ep.wells('D6'),
    tubes_ep.wells('D4'),
    new_tip='never'
)
p1000.mix(5, 1000, tubes_ep.wells('D4'))
p1000.blow_out(tubes_ep.wells('D4').top())
p1000.drop_tip()

# function for dilution from stock


def dil_from_stock(dests, vols, source):
    for d, vol in zip(dests, vols):
        dest = tubes_ep.wells(d)
        p300.pick_up_tip()
        p300.transfer(
            vol,
            tubes_ep.wells(source),
            dest,
            blow_out=True,
            new_tip='never'
        )
        p300.mix(5, 300, dest)
        p300.blow_out(dest.top())
        p300.drop_tip()


# dilution from stock 100
dil_from_stock(
    ['A1', 'A2', 'D1', 'A3'],
    [250, 100, 100, 40],
    'D4'
)

# dilution from stock 10
dil_from_stock(
    ['A4', 'A5', 'D2', 'A6', 'B1'],
    [250, 100, 100, 80, 40],
    'D3'
)

# dilution from stock 1
dil_from_stock(
    ['B2', 'B3', 'D3', 'B4', 'B5'],
    [200, 100, 100, 80, 50],
    'D2'
)

# dilution from stock 0.1
dil_from_stock(
    ['B6', 'C1', 'C2', 'C3'],
    [200, 100, 80, 50],
    'D1'
)
