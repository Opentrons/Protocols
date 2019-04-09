from opentrons import labware, instruments, modules, robot
import math

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
    if number_of_DNA_samples > 23:
        raise Exception('Please specify 23 or fewer DNA samples.')
    if number_of_DNA_samples + number_of_oligo_standards > 32:
        raise Exception('Too many samples and standards for one plate.')

    # DNA sample sources setup
    master_mix = tubes.wells(0)
    DNA_samples = tubes.wells(1, length=number_of_DNA_samples)

    # DNA sample destinations setup
    dests_triplicates = [plate.rows[start][(3*i):(3*i+3)]
                         for i in range(4) for start in range(8)]

    DNA_dests = dests_triplicates[0:number_of_DNA_samples]

    # distribute master mix to all destination wells
    p50.distribute(15, master_mix, plate.wells())

    # transfer DNA samples to corresponding triplicate locations
    for source, dests in zip(DNA_samples, DNA_dests):
        p10.pick_up_tip()
        p10.transfer(5,
                     source,
                     [d.top() for d in dests],
                     new_tip='never',
                     blow_out=True)
        p10.drop_tip()

    robot.pause('Please replace the master mix tube and DNA sample tubes with '
                'NTC, positive control, and oligo standard tubes before '
                'resuming.')

    # positive control and NTC setup
    num_pc_and_NTC = 32 - (number_of_DNA_samples + number_of_oligo_standards)
    num_pc = math.ceil(num_pc_and_NTC/2)
    num_NTC = math.floor(num_pc_and_NTC/2)

    positive_control = tubes.wells('A6')
    NTC = tubes.wells('B6')

    # distribute positive control
    if num_pc > 0:
        pc_dests = dests_triplicates[number_of_DNA_samples:
                                     number_of_DNA_samples+num_pc]
        p10.pick_up_tip()
        for dests in pc_dests:
            p10.transfer(5,
                         positive_control,
                         [d.top() for d in dests],
                         new_tip='never',
                         blow_out=True)
            p10.drop_tip()

    # distribute NTC
    if num_NTC > 0:
        NTC_dests = dests_triplicates[number_of_DNA_samples+num_pc:
                                      number_of_DNA_samples+num_pc+num_NTC]
        p10.pick_up_tip()
        for dests in NTC_dests:
            p10.transfer(5,
                         NTC,
                         [d.top() for d in dests],
                         new_tip='never',
                         blow_out=True)
            p10.drop_tip()

    # oligo standard sources setup
    oligo_standards = tubes.wells(0, length=number_of_oligo_standards)

    # oligo standard destinations
    oligo_dests = dests_triplicates[(32-number_of_oligo_standards):]

    # transfer oligo standards to corresponding triplicate locations
    for source, dests in zip(oligo_standards, oligo_dests):
        p10.pick_up_tip()
        p10.transfer(5,
                     source,
                     [d.top() for d in dests],
                     new_tip='never',
                     blow_out=True)
        p10.drop_tip()
