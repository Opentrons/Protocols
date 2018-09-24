from opentrons import labware, instruments, robot

"""
Tagment Genomic DNA
Amplify Libraries
"""
# labware setup
gDNA_plate = labware.load('96-PCR-flat', '1')
out_plate = labware.load('96-PCR-flat', '2')
# out_plate = labware.load('biorad-hardshell-96-PCR', '2')
tuberack = labware.load('tube-rack-2ml', '5')

# reagent setup
atm = tuberack.wells('A1')  # Amplicon Tagment Mix
td = tuberack.wells('B1')  # Tagment DNA Buffer
nt = tuberack.wells('C1')  # Neutralize Tagment Buffer
npm = tuberack.wells('D1')  # Nextera PCR Master Mix
index_1 = tuberack.wells('A2', to='D4')  # Index 1 (i7) adapters
index_2 = tuberack.wells('A5', to='D6')  # Index 2 (i5) adapters

tipracks50 = [labware.load('tiprack-200ul', slot) for slot in ['3', '4']]
tipracks10 = [labware.load('tiprack-10ul', slot) for slot in ['6', '7']]

# pipette setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=tipracks50)

p10 = instruments.P10_Single(
    mount='right',
    tip_racks=tipracks10)


def run_custom_protocol(
        number_of_samples: int=24):

    # define sample locations
    samples = gDNA_plate.wells()[:number_of_samples]

    index1 = {name: [] for name in range(len(index_1))}
    index2 = {name: [] for name in range(len(index_2))}

    if number_of_samples <= 24:
        output = [well
                  for col in gDNA_plate.cols('1', to='6')
                  for well in col.wells('A', to='D')][:number_of_samples]
        for index, well in enumerate(output):
            index1[index // 4].append(well)
            index2[index % 4].append(well)
    else:
        output = [well for well in out_plate.wells()][:number_of_samples]
        for index, well in enumerate(output):
            index1[index // 8].append(well)
            index2[index % 8].append(well)

    """
    Tagment genomic DNA
    """
    # Add Tagment DNA Buffer to each well
    p50.distribute(10, td, [well.top() for well in samples])

    # Add normalized gDNA to each well
    p10.transfer(5, samples, output, new_tip='always')

    robot.comment("Centrifuge at 280 × g at 20°C for 1 minute. Place on the \
        preprogrammed thermal cycler and run the tagmentation program. \
        When the sample reaches 10°C, immediately proceed to the next step \
        because the transposome is still active. Place the plate back to \
        slot 2.")

    robot.pause()

    # Add Neutralize Tagment Buffer to each well
    p10.transfer(5, nt, output, mix_after=(5, 10), new_tip='always')

    robot.comment("Centrifuge at 280 × g at 20°C for 1 minute. Place the plate \
        back to slot 2.")

    robot.pause()

    # Incubate at RT for 5 minutes
    p10.delay(minutes=5)

    """
    Amplify Libraries
    """
    # Add each index 1 adapter down each column
    for key in index1.keys():
        if index1[key]:
            p50.distribute(
                5,
                index_1[key],
                [well.top() for well in index1[key]])

    # Add each index 2 adapter across each row
    for key in index2.keys():
        if index2[key]:
            p50.distribute(
                5,
                index_2[key],
                [well.top() for well in index2[key]])

    # Add Nextera PCR Master Mix to each well
    p50.transfer(15, npm, output, mix_after=(2, 30), new_tip='always')
