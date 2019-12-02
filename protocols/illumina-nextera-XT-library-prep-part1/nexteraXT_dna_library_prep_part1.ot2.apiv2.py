metadata = {
    'protocolName': 'Illumina Nextera XT NGS Prep 1: Tagment Genomic DNA & \
Amplify Libraries',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library'
    }


def run(protocol_context):
    [pipette_setup, number_of_samples] = get_values(  # noqa: F821
        'pipette_setup', 'number_of_samples')

    # labware setup
    gDNA_plate = protocol_context.load_labware(
        'biorad_96_wellplate_200ul_pcr', '1', 'gDNA plate')
    out_plate = protocol_context.load_labware(
        'biorad_96_wellplate_200ul_pcr', '2', 'output plate')
    tuberack = protocol_context.load_labware(
        'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap',
        '5',
        'reagent rack'
    )

    # reagent setup
    atm = tuberack.wells()[0]  # Amplicon Tagment Mix
    td = tuberack.wells()[1]  # Tagment DNA Buffer
    nt = tuberack.wells()[2]  # Neutralize Tagment Buffer
    npm = tuberack.wells()[3]  # Nextera PCR Master Mix
    index_7 = tuberack.wells()[4:12]  # Index 1 (i7) adapters
    index_5 = tuberack.wells()[16:]  # Index 2 (i5) adapters

    # pipette setup
    pip_names = pipette_setup.split(',')
    if len(pip_names) > 1:
        tipracks50 = [
            protocol_context.load_labware('opentrons_96_tiprack_300ul', slot)
            for slot in ['3', '4']
        ]
        tipracks10 = [
            protocol_context.load_labware('opentrons_96_tiprack_10ul', slot)
            for slot in ['6', '7', '8', '9']
        ]
        racksets = [tipracks50, tipracks10]
        pip_l, pip_s = [
            protocol_context.load_instrument(pip, mount, tip_racks=rack)
            for pip, mount, rack in zip(pip_names, ['left', 'right'], racksets)
        ]
    else:
        tipracks20 = [
            protocol_context.load_labware('opentrons_96_tiprack_20ul', slot)
            for slot in ['3', '4', '6', '7', '8', '9']
        ]
        p20 = protocol_context.load_instrument(
            pip_names[0], mount='right', tip_racks=tipracks20)
        pip_l = p20
        pip_s = p20

    # define sample locations
    samples = gDNA_plate.wells()[:number_of_samples]

    if number_of_samples <= 24:
        # index7 = 6
        index5 = 4
        output = [well for col in out_plate.columns() for well in col[:4]]
    else:
        # index7 = 12
        index5 = 8
        output = [well for well in out_plate.wells()][:number_of_samples]

    cols = number_of_samples // index5
    remainder = number_of_samples % index5

    """
    Tagment genomic DNA
    """
    # Add Tagment DNA Buffer to each well
    pip_l.transfer(10, td, output, blow_out=True)

    # Add normalized gDNA to each well
    pip_s.transfer(5, samples, output, new_tip='always')

    # Add ATM to each well
    for well in output:
        pip_s.transfer(5, atm, well, mix_after=(5, 10))

    protocol_context.pause("Centrifuge at 280 × g at 20°C for 1 minute. Place \
on the preprogrammed thermal cycler and run the tagmentation program. When \
the sample reaches 10°C, immediately proceed to the next step because the \
transposome is still active. Place the plate back to slot 2.")

    # Add Neutralize Tagment Buffer to each well
    pip_s.transfer(5, nt, output, mix_after=(5, 10), new_tip='always')

    protocol_context.pause("Centrifuge at 280 × g at 20°C for 1 minute. Place \
the plate back on slot 2.")

    # Incubate at RT for 5 minutes
    protocol_context.delay(minutes=5)

    """
    Amplify Libraries
    """
    # Add each index 1 adapter down each column
    for index, loc in enumerate(range(0, number_of_samples, index5)[:cols]):
        pip_s.transfer(
            5,
            index_7[index],
            [well.top() for well in output[loc: loc+index5]],
            blow_out=True
        )

    if remainder:
        index = range(0, number_of_samples, index5)[cols]
        pip_s.transfer(
            5,
            index_7[cols],
            [well.top() for well in output[index:index+remainder]],
            blow_out=True
        )

    # Add each index 2 adapter across each row
    for index in range(0, index5):
        if remainder and index < remainder:
            loc = [loc for loc in range(
                index, number_of_samples, index5)][:cols+1]
            dest = [output[i].top() for i in loc]
        else:
            dest = [output[i].top() for i in range(
                index, number_of_samples, index5)][:cols]
        pip_s.transfer(5, index_5[index], dest, blow_out=True)

    # Add Nextera PCR Master Mix to each well
    for d in output:
        mix_vol = pip_l.max_volume if pip_l.max_volume == 20 else 30
        pip_l.transfer(15, npm, d, mix_after=(2, mix_vol))
