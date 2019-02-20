from opentrons import labware, instruments, robot

metadata = {
    'protocolName': 'PCR/qPCR Prep',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware setup
mastermix_rack = labware.load('opentrons-tuberack-2ml-eppendorf', '1')
sample_rack = labware.load('opentrons-tuberack-2ml-eppendorf', '5')
plate_1 = labware.load('opentrons-aluminum-block-96-PCR-plate', '2')
plate_2 = labware.load('opentrons-aluminum-block-96-PCR-plate', '3')

tiprack_10_1 = labware.load('tiprack-10ul', '4')
tiprack_10_2 = labware.load('tiprack-10ul', '7')
tiprack_300 = labware.load('opentrons-tiprack-300ul', '6')

# instruments setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack_10_1, tiprack_10_2])
p300 = instruments.P300_Single(
    mount='right',
    tip_racks=[tiprack_300])

# reagent setup
bacteria_mm = mastermix_rack.wells('A1')
fungi_mm = mastermix_rack.wells('B1')
bacteria_mm2 = mastermix_rack.wells('C1')
fungi_mm2 = mastermix_rack.wells('D1')

# selects PCR plate 1 wells taking into consideration edge effects
target_b = [well for col in plate_1.cols('2', to='5')
            for well in col.wells('B', to='G')]
target_f = [well for col in plate_1.cols('8', to='11')
            for well in col.wells('B', to='G')]
target_1 = target_b + target_f

# transfer bacteria mastermix 1
p10.transfer(24, bacteria_mm, target_b)

# transfer fungi mastermix 1
p10.transfer(24, fungi_mm, target_f)

# transfer samples to plate 1
for sample, dest_1, dest_2 in zip(sample_rack.wells(), target_b, target_f):
    p10.transfer(1, sample, dest_1, blow_out=True)
    p10.transfer(1, sample, dest_2, blow_out=True)

robot.pause("Spin and thermocycle on Plate 1, place it back in slot 2 before \
resuming the protocol.")

# selects PCR plate 2 wells taking into consideration edge effects
target_2b = [well for col in plate_2.cols('2', to='5')
             for well in col.wells('B', to='G')]
target_2f = [well for col in plate_2.cols('8', to='11')
             for well in col.wells('B', to='G')]
target_2 = target_2b + target_2f

# transfer bacteria mastermix 2
p300.distribute(49, bacteria_mm2, target_2b)

# transfer fungi mastermix 2
p300.distribute(49, fungi_mm2, target_2f)

# transfer samples from plate 1 to plate 2
for source, dest in zip(target_1, target_2):
    p10.transfer(1, source, dest)
