from opentrons import labware, instruments

metadata = {
    'protocolName': 'Serial Dilution for Analytical Chemistry Part 1: HPLC',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load labware
tubes_50ml = labware.load('opentrons-tuberack-50ml', '1')
tubes_ep = labware.load('opentrons-tuberack-2ml-screwcap', '2')
tips1000 = labware.load('tiprack-1000ul', '4')
tips300 = labware.load('opentrons-tiprack-300ul', '5')

# pipettes
p1000 = instruments.P1000_Single(mount='right', tip_racks=[tips1000])
p300 = instruments.P300_Single(mount='left', tip_racks=[tips300])

# solvent addition
solvent = tubes_50ml.wells('A1').top(-90)
p1000.pick_up_tip()
p1000.mix(5, 1000, solvent)
p1000.drop_tip()

dests = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'B1', 'B2', 'B3', 'B4', 'B5',
         'B6', 'C1', 'C2']
vols = [900, 920, 950, 970, 920, 950, 970, 900, 920, 950, 970, 900, 920, 950]

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

# function for dilution from stock


def dil_from_stock(mix_before, dests, vols, source):
    src = tubes_ep.wells(source)
    for d, vol in zip(dests, vols):
        dest = tubes_ep.wells(d)
        p300.pick_up_tip()
        if mix_before:
            p300.mix(5, 300, src)
            p300.blow_out(src.top())
        p300.transfer(
            vol,
            src,
            dest,
            blow_out=True,
            new_tip='never'
        )
        p300.mix(5, 300, dest)
        p300.blow_out(dest.top())
        p300.drop_tip()


# dilution from stock pest
dil_from_stock(
    False,
    ['A1', 'A2', 'A3', 'A4'],
    [100, 80, 50, 30],
    'D6'
)

# dilution from stock 100
dil_from_stock(
    True,
    ['A5', 'A6', 'B1'],
    [100, 50, 30],
    'A1'
)

# dilution from stock 10
dil_from_stock(
    True,
    ['B2', 'B3', 'B4', 'B5'],
    [100, 80, 50, 30],
    'A5'
)

# dilution from stock 1
dil_from_stock(
    True,
    ['B6', 'C1', 'C2'],
    [100, 80, 50],
    'B2'
)
