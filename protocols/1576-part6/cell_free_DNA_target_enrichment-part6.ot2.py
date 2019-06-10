from opentrons import labware, instruments

metadata = {
    'protocolName': 'Cell3 Target: Cell Free DNA Target Enrichment Part 6',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware setup
plate = labware.load('biorad-hardshell-96-PCR', '1')
tuberack = labware.load('opentrons-aluminum-block-2ml-screwcap', '8')
reg_tuberack = labware.load('opentrons-tuberack-1.5ml-eppendorf', '5')
tipracks_50 = [labware.load('opentrons-tiprack-300ul', slot)
               for slot in ['6', '9']]
tipracks_10 = [labware.load('opentrons-tiprack-10ul', slot)
               for slot in ['10', '11']]

# instrument setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=tipracks_50)
p10 = instruments.P10_Single(
    mount='right',
    tip_racks=tipracks_10)

# reagent setup
pool_sample = reg_tuberack.wells('A1')
hybridization_buffer = tuberack.wells('A1')
hybridization_enhancer = tuberack.wells('B1')
probe_set = tuberack.wells('C1')
nuclease_free_water = tuberack.wells('D1')

# add hybridization mix components to the dried-up library pool
volumes = [8.5, 2.7, 4, 1.8]
components = [hybridization_buffer, hybridization_enhancer, probe_set,
              nuclease_free_water]
for vol, component in zip(volumes, components):
    p10.transfer(vol, component, pool_sample, blow_out=True)

# mix gently
p50.set_flow_rate(aspirate=15, dispense=30)
p50.pick_up_tip()
p50.mix(10, 15, pool_sample)
p50.blow_out(pool_sample)
p50.drop_tip()
p50.set_flow_rate(aspirate=25, dispense=50)

p50.delay(minutes=10)

# transfer reaction mix to a new clean tube
p50.transfer(17, pool_sample, plate.wells('A1'))
