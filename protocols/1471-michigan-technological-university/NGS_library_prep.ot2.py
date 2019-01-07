from opentrons import labware, instruments, modules

metadata = {
    'protocolName': 'NGS Library Prep',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'}

# labware setup
mag_module = modules.load('magdeck', '1')
mag_plate = labware.load('biorad-hardshell-96-PCR', '1', share=True)
plate = labware.load('biorad-hardshell-96-PCR', '2')
trough = labware.load('trough-12row', '4')

tipracks_50 = labware.load('tiprack-200ul', '3')
tipracks_300 = [labware.load('tiprack-200ul', slot)
                for slot in ['5', '6', '7', '8', '9']]

# instruments setup
m50 = instruments.P50_Multi(
    mount='left',
    tip_racks=[tipracks_50])
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks_300)

# reagent setup
beads = trough.wells('A1')
ethanol = trough.wells('A2', to='A3')
tris = trough.wells('A4')

for col in mag_plate.cols():
    m50.pick_up_tip()
    m50.transfer(20, beads, col, new_tip='never')
    m50.mix(5, 20, col)
    m50.blow_out(col)
    m50.drop_tip()

m50.delay(minutes=5)
mag_module.engage()
m50.delay(minutes=2)

for cycle in range(2):
    m300.distribute(
        200, ethanol[cycle], [col[0].top() for col in mag_plate.cols()])
    m300.delay(seconds=30)
    for col in mag_plate.cols():
        m300.transfer(300, col, m300.trash_container.top())
m300.delay(minutes=15)

mag_module.disengage()

for col in mag_plate.cols():
    m300.pick_up_tip()
    m300.transfer(52.5, tris, col, new_tip='never')
    m300.mix(5, 30, col)
    m300.blow_out(col)
    m300.drop_tip()

m300.delay(minutes=2)
mag_module.engage()
m300.delay(minutes=2)

for source, dest in zip(mag_plate.cols(), plate.cols()):
    m300.transfer(50, source, dest)

mag_module.disengage()
