from opentrons import labware, instruments

plate_dna = labware.load('96-flat', '1')
plate_y = labware.load('96-PCR-tall', '2')
plate_x = labware.load('96-flat', '3')
trough = labware.load('trough-12row', '4')
plate_1 = labware.load('96-flat', '5')
plate_2 = labware.load('96-flat', '6')


tiprack_50 = labware.load('opentrons-tiprack-300ul', '11')
tipracks_10 = [labware.load('tiprack-10ul', slot)
               for slot in ['7', '8', '9', '10']]

# reagent setup
water = trough.wells('A1')
mastermix = trough.wells('A2')

# instrument setup
m50 = instruments.P50_Multi(
    mount='left',
    tip_racks=[tiprack_50])

m10 = instruments.P10_Multi(
    mount='right',
    tip_racks=tipracks_10)


def run_custom_protocol(
        water_volume: float=180,
        primer_1_volume: float=10,
        primer_2_volume: float=10,
        mixture_volume: float=2,
        DNA_volume: float=3,
        mastermix_volume: float=23):

    m50.transfer(water_volume, water, plate_x.cols(), new_tip='once')

    for source, dest in zip(plate_1.cols(), plate_x.cols()):
        m10.transfer(primer_1_volume, source, dest)

    for source, dest in zip(plate_2.cols(), plate_x.cols()):
        m10.transfer(primer_2_volume, source, dest, mix_after=(10, 10))

    for source, dest in zip(plate_x.cols(), plate_y.cols()):
        m10.transfer(mixture_volume, source, dest, blow_out=True)

    for source, dest in zip(plate_dna.cols(), plate_y.cols()):
        m10.transfer(DNA_volume, source, dest, blow_out=True)

    m50.pick_up_tip()
    for col in plate_y.cols():
        if m50.current_volume < mastermix_volume:
            m50.aspirate(mastermix)
        m50.dispense(mastermix_volume, col.top())
    m50.drop_tip()
