from opentrons import labware, instruments
import math

# labware setup
sample_plates = [labware.load('96-PCR-tall', slot)
                 for slot in ['1', '3']]
plate = labware.load('384-plate', '2')
strips = labware.load('PCR-strip-tall', '4')
trough = labware.load('trough-12row', '5')
tiprack_10 = [labware.load('tiprack-10ul', slot)
              for slot in ['6', '7', '8']]
tiprack_50 = labware.load('tiprack-200ul', '9')

# reagent setup
standards = strips.cols('1')
standard_pico = strips.cols('2')
TE_pico = trough.wells('A1')

# instrument setup
m10 = instruments.P10_Multi(
    mount='left',
    tip_racks=tiprack_10)

m50 = instruments.P50_Multi(
    mount='right',
    tip_racks=[tiprack_50])


def run_custom_protocol(
        number_of_samples: int=184):

    if number_of_samples > 184:
        raise Exception("Number of samples cannot exceed 184.")

    col_num = math.ceil(number_of_samples/8)

    # transfer standards in duplicate
    m10.transfer(10, standards, [well for well in plate.wells('A1', 'B1')])

    # transfer picogreen solution to each standard well
    m10.transfer(10, standard_pico, [well for well in plate.wells('A1', 'B1')])

    # transfer TE Buffer and Picogreen mix
    if col_num == 1:
        dests = [well for well in plate.cols('2')[:2]]
    else:
        dests = [well for col in plate.cols('2', length=col_num)
                 for well in col[:2]]
    m50.distribute(19, TE_pico, dests)

    # transfer samples
    sample_cols = [col for plate in sample_plates
                   for col in plate.cols()][:col_num]
    if col_num == 1:
        sample_dests = [col[:2] for col in plate.cols('2')]
    else:
        sample_dests = [col[:2] for col in plate.cols('2', length=col_num)]
    for source, dest in zip(sample_cols, sample_dests):
        m10.pick_up_tip()
        for well in dest:
            m10.transfer(1, source, well, blow_out=True, new_tip='never')
        m10.drop_tip()
