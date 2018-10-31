from opentrons import labware, instruments

# labware setup
plate_in = labware.load('96-flat', '1')
plate_out = labware.load('96-flat', '2')
trough = labware.load('trough-12row', '3')
tiprack = labware.load('tiprack-10ul', '5')

# reagent setup
water = trough.wells('A1')
dye = trough.wells('A2')

# instrument setup
m10 = instruments.P10_Multi(
    mount='left',
    tip_racks=[tiprack])


def run_custom_protocol(
        sample_volume: float=10.0,
        dye_volume: float=5):

    m10.pick_up_tip()
    for source, dest in zip(plate_in.cols(), plate_out.cols()):
        m10.transfer(
            sample_volume, source, dest, blow_out=True, new_tip='never')
        m10.mix(5, 10, water)
        m10.blow_out(water)
    m10.drop_tip()

    m10.pick_up_tip()
    for well in plate_out.rows(0).wells():
        m10.transfer(
            dye_volume, dye, well.top(), blow_out=True, new_tip='never')
    m10.drop_tip()
