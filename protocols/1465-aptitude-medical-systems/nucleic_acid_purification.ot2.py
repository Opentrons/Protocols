from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'Nucleic Acid Purification',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware setup
dna_plate = labware.load('biorad-hardshell-96-PCR', '1', 'DNA Plate')
out_plate = labware.load('biorad-hardshell-96-PCR', '2', 'Out Plate')
mag_module = modules.load('magdeck', '4')
mag_plate = labware.load('biorad-hardshell-96-PCR', '4', share=True)
trough = labware.load('trough-12row', '5')

tipracks = [labware.load('opentrons-tiprack-300ul', str(slot))
            for slot in range(8, 12)]

# instruments setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=tipracks)

# reagent setup
butanol = trough.wells('A1')

mag_module.disengage()

m300.set_flow_rate(aspirate=90)
m300.pick_up_tip()
for col in dna_plate.cols('1', to='4'):
    m300.transfer(95, col[0].bottom(2), m300.trash_container.top(),
                  new_tip='never')
    m300.blow_out(m300.trash_container.top())
m300.drop_tip()
m300.set_flow_rate(aspirate=150)

dests = [col[0].top() for col in dna_plate.cols('1', to='4')]
m300.distribute(30, butanol, dests, disposal_vol=10)

m300.set_flow_rate(aspirate=300, dispense=600)
m300.pick_up_tip()
for col in dna_plate.cols('1', to='4'):
    m300.mix(20, 50, col)
    m300.blow_out(col)
m300.set_flow_rate(aspirate=150, dispense=300)
m300.consolidate(
    60, dna_plate.cols('1', to='4'), out_plate.cols('1'), new_tip='never')
m300.drop_tip()

robot.pause("After inspection, let plate sit for 10 minutes before resuming.")

m300.set_flow_rate(aspirate=90)
m300.transfer(
    100, out_plate.cols('1')[0].bottom(2), m300.trash_container.top())
m300.transfer(100, out_plate.cols('1'), mag_plate.cols('1'))
