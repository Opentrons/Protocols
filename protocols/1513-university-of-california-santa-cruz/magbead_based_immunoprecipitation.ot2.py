from opentrons import labware, instruments, modules

metadata = {
    'protocolName': 'Magbead-based Immunoprecipitation',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware setup
trough = labware.load('trough-12row', '1')
mag_module = modules.load('magdeck', '4')
plate = labware.load('biorad-hardshell-96-PCR', '4', share=True)
tiprack_50 = labware.load('opentrons-tiprack-300ul', '2')
tiprack_300 = labware.load('opentrons-tiprack-300ul', '3')

# instruments setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack_50])

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack_300])

# reagent setup
pbs = trough.wells('A1')
antigen = plate.wells('A3')

# turn on magnet for 3 seconds
mag_module.engage()
p50.delay(seconds=3)

# discard supernatant in well A2
p50.transfer(25, plate.wells('A2').bottom(0.5), p50.trash_container.top())

# transfer from A1 to A2
p50.pick_up_tip()
p50.transfer(10, plate.wells('A1'), plate.wells('A2'), new_tip='never')
mag_module.disengage()  # turn off magnet
# mix 3 times at 5 uL every 2 minutes for 30 times using the same tip
for _ in range(30):
    p50.mix(3, 5, plate.wells('A2'))
    p50.blow_out(plate.wells('A2').top())
    p50.delay(minutes=2)
p50.mix(3, 5, plate.wells('A2'))
p50.blow_out(plate.wells('A2').top())
mag_module.engage()  # turn on magnet for 5 seconds
p50.delay(seconds=5)
p50.transfer(12, plate.wells('A2').bottom(0.5), p50.trash_container.top(),
             new_tip='never')  # discard supernatant
p50.drop_tip()

# wash well with PBS twice
for _ in range(2):
    mag_module.disengage()  # turn off magnet
    m300.pick_up_tip()
    m300.transfer(200, pbs, plate.wells('A2'), new_tip='never')  # add pbs
    m300.mix(3, 100, plate.wells('A2'))
    m300.blow_out(plate.wells('A2').top())
    mag_module.engage()  # turn on magnet
    m300.delay(seconds=3)
    m300.transfer(
        250, plate.wells('A2').bottom(0.5), m300.trash_container.top(),
        new_tip='never')  # discard supernatant
    m300.drop_tip()

# turn off magnet
mag_module.disengage()

# resuspend the antibody coated in 100 uL PBS
p50.pick_up_tip()
p50.transfer(100, pbs, plate.wells('A2').top(), blow_out=True, new_tip='never')
p50.mix(5, 50, plate.wells('A2'))
# transfer well A2 to B1
p50.transfer(10, plate.wells('A2'), plate.wells('B1'), new_tip='never')
p50.move_to(plate.wells('B1').top())
mag_module.engage()  # turn on magnet for 2 seconds
p50.delay(seconds=2)
p50.transfer(120, plate.wells('B1').bottom(0.5), p50.trash_container.top(),
             new_tip='never')  # discard supernatant
p50.drop_tip()

# turn off magnetic module
mag_module.disengage()

# transfer antigen solution
m300.pick_up_tip()
m300.transfer(200, antigen, plate.wells('B1'), new_tip='never')
# mix 3 times at 150 uL every 2 minutes for 15 times using the same tip
for _ in range(15):
    m300.mix(3, 150, plate.wells('B1'))
    m300.blow_out(plate.wells('B1').top())
    m300.delay(minutes=2)
m300.mix(3, 150, plate.wells('B1'))
m300.blow_out(plate.wells('B1').top())
mag_module.engage()  # turn on magnet for 2 minutes
m300.delay(minutes=2)
m300.transfer(250, plate.wells('B1').bottom(0.5), m300.trash_container.top(),
              new_tip='never')  # discard supernatant
m300.drop_tip()

# turn off magnet
mag_module.disengage()

# wash well with PBS twice
for _ in range(3):
    mag_module.disengage()
    m300.pick_up_tip()
    m300.transfer(200, pbs, plate.wells('A2'), new_tip='never')
    m300.mix(3, 100, plate.wells('A2'))
    m300.blow_out(plate.wells('A2').top())
    mag_module.engage()
    m300.delay(seconds=3)
    m300.transfer(
        250, plate.wells('A2').bottom(0.5), m300.trash_container.top(),
        new_tip='never')
    m300.drop_tip()

# turn off magnetic module
mag_module.disengage()

# resuspend well B1 in PBS and transfer to well B2
m300.pick_up_tip()
m300.transfer(200, pbs, plate.wells('B1'), new_tip='never')
m300.mix(5, 150, plate.wells('B1'))
m300.transfer(250, plate.wells('B1').bottom(0.5), plate.wells('B2'),
              new_tip='never')
m300.drop_tip()
