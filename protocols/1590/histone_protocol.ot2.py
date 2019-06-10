from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'Histone Sample Prep',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create labware
plate_name = 'Axygen-PCR-96'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.5,
        depth=15.0,
        volume=200
    )

# load labware and tempdeck
plate = labware.load(plate_name, '1')
trough = labware.load('trough-12row', '3')
tempdeck = modules.load('tempdeck', '6')
block = labware.load('opentrons-aluminum-block-2ml-eppendorf', '6', share=True)
if not robot.is_simulating():
    tempdeck.set_temperature(4)
    tempdeck.wait_for_temp()
tips300 = [labware.load('opentrons-tiprack-300ul', slot)
           for slot in ['2', '4', '5', '7', '8', '9']]
tips1000 = [labware.load('tiprack-1000ul', slot) for slot in ['10', '11']]

# pipettes
m50 = instruments.P50_Multi(mount='left', tip_racks=tips300)
p1000 = instruments.P1000_Single(mount='right', tip_racks=tips1000)

# reagents
ammonium_bicarbonate = block.rows('A')[0:2]
acetonitrile = block.wells('B1')
propionic_anhydride = block.rows('C')[0:2]
ammonium_hydroxide = block.rows('D')[0:2]
trypsin = block.wells('A5')

samples = plate.rows('A')[0:6]


def air_gap_transfer(vol, reagent, trough_spot):
    p1000.pick_up_tip()
    for _ in range(2):
        p1000.transfer(1500/2,
                       reagent,
                       trough_spot,
                       air_gap=100,
                       new_tip='never')
    p1000.drop_tip()

    m50.pick_up_tip()
    m50.aspirate(vol*6, trough_spot).air_gap(10)
    m50.dispense(10, plate.wells('A12'))
    for s in samples:
        m50.dispense(vol, s.top())
    m50.drop_tip()

    for s in samples:
        m50.pick_up_tip()
        m50.mix(5, 20, s)
        m50.drop_tip()


def ammonium_hydroxide_transfer(reagent):
    p1000.pick_up_tip()
    for _ in range(2):
        p1000.transfer(1500/2,
                       reagent,
                       trough.wells('A4'),
                       air_gap=100,
                       new_tip='never')
    p1000.drop_tip()

    for s in samples:
        m50.pick_up_tip()
        m50.transfer(18, trough.wells('A4'), s, air_gap=5, new_tip='never')
        m50.mix(10, 30, s)
        m50.drop_tip()


def repeat_chunk():
    # transfer acetonitrile
    air_gap_transfer(5, acetonitrile, trough.wells('A2'))

    # transfer propionic anhydride
    air_gap_transfer(5, propionic_anhydride[0], trough.wells('A3'))

    # transfer ammonium hydroxide
    ammonium_hydroxide_transfer(ammonium_hydroxide[0])

    # delay 15 minutes and repeat propionic anhydride
    # and ammonium hydroxide transfers
    m50.delay(minutes=15)
    air_gap_transfer(5, propionic_anhydride[1], trough.wells('A3'))
    ammonium_hydroxide_transfer(ammonium_hydroxide[1])


# transfer ammonium bicarbonate
p1000.transfer(1500, ammonium_bicarbonate[0], trough.wells('A1'))
m50.distribute(20, trough.wells('A1'), samples.top(), disposal_vol=0)

# transfer acetonitrile, propionic anhydride, and ammonium anhydride
repeat_chunk()

robot.pause('Resume once ready...')

# transfer trypsin-ammonium bicarbonate solution
p1000.transfer(1400, ammonium_bicarbonate[1], trough.wells('A5'))
p1000.pick_up_tip()
p1000.transfer(100, trypsin, trough.wells('A5'), new_tip='never')
p1000.mix(10, 200, trough.wells('A5'))
p1000.drop_tip()

for s in samples:
    m50.pick_up_tip()
    m50.transfer(20, trough.wells('A5'), s, new_tip='never')
    m50.mix(10, 50, s)
    m50.drop_tip()

# delay 12 hours
m50.delay(minutes=720)

m50.move_to(plate.wells('A1').top(20))

robot.pause('Please replace P50 Multi tip racks before resuming.')
m50.reset()

# repeat transfer of acetonitrile, propionic anhydride, and ammonium anhydride
repeat_chunk()
