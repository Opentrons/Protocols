from opentrons import labware, instruments

metadata = {
    'protocolName': 'Liquid Transfer on Custom Cartridges',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

trough_1_well_name = 'trough_1well'
if trough_1_well_name not in labware.list():
    labware.create(
        trough_1_well_name,
        grid=(1, 1),
        spacing=(0, 0),
        depth=39,
        diameter=72)

trough_2_well_name = 'trough-2well'
if trough_2_well_name not in labware.list():
    labware.create(
        trough_2_well_name,
        grid=(2, 1),
        spacing=(54, 0),
        depth=39,
        diameter=53)

xfe96_plate_name = 'XFe96-384-well'
if xfe96_plate_name not in labware.list():
    labware.create(
        xfe96_plate_name,
        grid=(24, 16),
        spacing=(4.5, 4.5),
        depth=30,
        diameter=2.85)

xfe24_plate_name = 'XFe24-96-well'
if xfe24_plate_name not in labware.list():
    labware.create(
        xfe24_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        depth=33,
        diameter=3.7)

# load XFe96 plates
xfe96_plates = [labware.load(xfe96_plate_name, slot)
                for slot in ['1', '4', '5']]
for plate in xfe96_plates:
    for well in plate:
        well.properties['height'] = 9.6

# load XFe24 plates
xfe24_plates = [labware.load(xfe24_plate_name, slot)
                for slot in ['2', '6', '9']]
for plate in xfe24_plates:
    for well in plate:
        well.properties['height'] = 12.5

# load XFp plate
xfp_plate = labware.load(xfe96_plate_name, '3').cols(
    '3', '4', '11', '12', '19', '20')
for well in xfp_plate:
    well.properties['height'] = 9.6

# load troughs and tiprack
trough_1 = labware.load(trough_1_well_name, '7')
trough_2 = labware.load(trough_2_well_name, '8')
tiprack = labware.load('opentrons-tiprack-300ul', '10')

# instruments setup
m50 = instruments.P50_Multi(
    mount='left',
    tip_racks=[tiprack])

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack])

# reagent setup
water = trough_1.wells('A1')

"""
Fill 384 injection ports in slot 1 with colored water from trough_1
"""
plate = xfe96_plates[0]
dests = [well.top() for col in plate.cols() for well in col[:2]]
m50.distribute(25, water, dests, disposal_vol=0)

"""
Fill 96 ports in slot 2 with colored water from trough_1
"""
plate = xfe24_plates[0]
dests = [col[0].top() for col in plate.cols()]
m300.start_at_tip(tiprack.cols('2'))
m300.distribute(75, water, dests, disposal_vol=0)

"""
Fill each port A in slot 6 with colored water from trough_1
"""
plate = xfe24_plates[1]
dests = [col[0].top() for col in plate.cols('1', to='12', step=2)]
m300.distribute(75, water, dests, disposal_vol=0)

"""
Fill each port B in slot 9 with colored water from trough_1
"""
plate = xfe24_plates[2]
dests = [col[0].top() for col in plate.cols('1', to='12', step=2)]
m300.distribute(75, water, dests, disposal_vol=0)

"""
Fill each port B in slot 5 with colored water from trough_1
"""
plate = xfe96_plates[2]
dests = [col[1].top() for col in plate.cols('1', to='24', step=2)]
m50.start_at_tip(tiprack.cols('5'))
m50.distribute(25, water, dests, disposal_vol=0)

"""
Fill each port A in slot 4 with colored water from trough_1
"""
plate = xfe96_plates[1]
dests = [col[0].top() for col in plate.cols('1', to='24', step=2)]
m50.distribute(25, water, dests, disposal_vol=0)

"""
Wash Pipette tips
"""
m300.start_at_tip(tiprack.cols('7'))
m300.transfer(300, trough_2.wells('A1'), trough_2.wells('A2'))
m50.start_at_tip(tiprack.cols('8'))
m50.transfer(50, trough_2.wells('A1'), trough_2.wells('A2'))

"""
Fill all ports in slot 3 with colored water from trough_1
"""
m50.pick_up_tip()
for col in xfp_plate:
    dests = [well.top() for well in col[:2]]
    m50.distribute(25, water, dests, disposal_vol=0, new_tip='never')
m50.drop_tip()
