from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'PCR Preparation',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load labware
tips10 = labware.load('opentrons_96_tiprack_10ul', '2')
tips50 = labware.load('opentrons_96_tiprack_300ul', '3')
tubes = labware.load(
    'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '6')

# modules
tempdeck = modules.load('tempdeck', '5')
plate = labware.load(
    'opentrons_96_aluminumblock_biorad_wellplate_200ul', '5', share=True)
if not robot.is_simulating():
    tempdeck.set_temperature(4)
    tempdeck.wait_for_temp()

# pipettes
p10 = instruments.P10_Single(
    mount='right',
    tip_racks=[tips10]
)
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tips50]
)


def run_custom_protocol(number_of_DNA_samples: int = 21,
                        number_of_oligo_standards: int = 8):
    # check invalid parameters
    if number_of_DNA_samples + number_of_oligo_standards > 30:
        raise Exception('Too many samples and standards for one plate.')

    # master mix setup
    master_mix = tubes.wells('A1')

    # DNA sample sources setup
    DNA_samples = tubes.wells('B1', length=number_of_DNA_samples)

    # destinations setup
    dests_triplicates = [plate.rows[start][(3*i):(3*i+3)]
                         for i in range(4) for start in range(8)]

    DNA_dests = dests_triplicates[0:number_of_DNA_samples]
    pc_dests = dests_triplicates[number_of_DNA_samples]
    NTC_dests = dests_triplicates[number_of_DNA_samples+1]
    oligo_dests = dests_triplicates[(len(dests_triplicates) -
                                    number_of_oligo_standards):
                                    len(dests_triplicates)]

    # distribute master mix to all destination wells for DNA, oligo, positive
    # control, and NTC
    mm_dests = [well
                for set in [DNA_dests, [pc_dests], [NTC_dests], oligo_dests]
                for well in set]
    for trip in mm_dests:
        p50.distribute(15, master_mix, trip)

    # transfer DNA samples to corresponding triplicate locations
    for source, dests in zip(DNA_samples, DNA_dests):
        p10.transfer(5,
                     source,
                     dests,
                     new_tip='always',
                     blow_out=True)

    robot.pause('Please replace the master mix tube and DNA sample tubes with '
                'positive control, NTC and oligo standard tubes before '
                'resuming.')

    # transfer positive control to corresponding triplicate location
    positive_control = tubes.wells('C6')
    p10.transfer(5,
                 positive_control,
                 pc_dests,
                 new_tip='always',
                 blow_out=True)

    # transfer NTC to corresponding triplicate location
    NTC = tubes.wells('D6')
    p10.transfer(5,
                 NTC,
                 NTC_dests,
                 new_tip='always',
                 blow_out=True)

    # oligo standard sources setup
    oligo_standards = tubes.wells(0, length=number_of_oligo_standards)

    # transfer oligo standards to corresponding triplicate locations
    for source, dests in zip(oligo_standards, oligo_dests):
        p10.transfer(5,
                     source,
                     dests,
                     new_tip='always',
                     blow_out=True)
