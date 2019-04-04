from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'CSV Plate Filling',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = 'biorad-low-profile-96'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.4,
        depth=15.5,
        volume=200
    )

# load labware
tubes = labware.load('opentrons-aluminum-block-2ml-eppendorf', '2')
tips10 = labware.load('tiprack-10ul', '4')
tips50 = labware.load('opentrons-tiprack-300ul', '5')

# modules
tempdeck = modules.load('tempdeck', '1')
plate = labware.load(plate_name, '1', share=True)
tempdeck.set_temperature(4)
tempdeck.wait_for_temp()

# pipettes
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tips10]
)
p50 = instruments.P50_Single(
    mount='right',
    tip_racks=[tips50]
)

# DNA sample sources setup
master_mix = tubes.wells(0)
DNA_samples = tubes.wells(1, length=22)

# DNA sample destinations setup
set1 = [plate.rows[start][0:3] for start in range(8)]
set2 = [plate.rows[start][3:6] for start in range(8)]
set3 = [plate.rows[start][6:9] for start in range(6)]
DNA_dests_triplicates = set1 + set2 + set3

# distribute master mix to all destination wells
p50.distribute(15, master_mix, plate.wells())

# transfer DNA samples to corresponding triplicate locations
for source, dests in zip(DNA_samples, DNA_dests_triplicates):
    p10.pick_up_tip()
    p10.transfer(5,
                 source,
                 [d.top() for d in dests],
                 new_tip='never',
                 blow_out=True)
    p10.drop_tip()

robot.pause("Please replace the master mix tube and DNA sample tubes with "
            "oligo standard tubes before resuming.")

# oligo standard sources setup
oligo_standards = tubes.wells(0, length=8)

# oligo standard destinations
oligo_dests_triplicates = [plate.rows[start][9:12] for start in range(8)]

# transfer oligo standards to corresponding triplicate locations
for source, dests in zip(oligo_standards, oligo_dests_triplicates):
    p10.pick_up_tip()
    p10.transfer(5,
                 source,
                 [d.top() for d in dests],
                 new_tip='never',
                 blow_out=True)
    p10.drop_tip()
