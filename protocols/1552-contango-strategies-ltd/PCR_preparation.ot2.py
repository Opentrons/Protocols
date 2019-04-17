from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'PCR Preparation',
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
if not robot.is_simulating():
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


def run_custom_protocol(number_of_DNA_samples: int = 22,
                        number_of_oligo_standards: int = 8):
    # check invalid parameters
    if number_of_DNA_samples > 22:
        raise Exception('Please specify 22 or fewer DNA samples.')
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
    oligo_dests = dests_triplicates[32-number_of_oligo_standards:]

    # distribute master mix to all destination wells for DNA, oligo, positive
    # control, and NTC
    mm_dests = [well
                for set in [DNA_dests, [pc_dests], [NTC_dests], oligo_dests]
                for well in set]
    all_mm_wells = [well for trip in mm_dests for well in trip]
    p50.distribute(15, master_mix, all_mm_wells)

    # transfer DNA samples to corresponding triplicate locations
    for source, dests in zip(DNA_samples, DNA_dests):
        p10.pick_up_tip()
        p10.transfer(5,
                     source,
                     [d.top() for d in dests],
                     new_tip='never',
                     blow_out=True)
        p10.drop_tip()

    # transfer positive control to corresponding triplicate location
    positive_control = tubes.wells('D6')
    p10.pick_up_tip()
    p10.transfer(5,
                 positive_control,
                 [d.top() for d in pc_dests],
                 new_tip='never',
                 blow_out=True)
    p10.drop_tip()

    robot.pause('Please replace the master mix tube and DNA sample tubes with '
                'NTC and oligo standard tubes before resuming.')

    # transfer NTC to corresponding triplicate location
    NTC = tubes.wells('D6')
    p10.pick_up_tip()
    p10.transfer(5,
                 NTC,
                 [d.top() for d in NTC_dests],
                 new_tip='never',
                 blow_out=True)
    p10.drop_tip()

    # oligo standard sources setup
    oligo_standards = tubes.wells(0, length=number_of_oligo_standards)

    # transfer oligo standards to corresponding triplicate locations
    for source, dests in zip(oligo_standards, oligo_dests):
        p10.pick_up_tip()
        p10.transfer(5,
                     source,
                     [d.top() for d in dests],
                     new_tip='never',
                     blow_out=True)
        p10.drop_tip()
