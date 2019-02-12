from opentrons import labware, instruments

metadata = {
    'protocolName': 'Two-solution Fames protocols',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

trough_name = 'glass-trough'
if trough_name not in labware.list():
    labware.create(
        trough_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=66,
        depth=25)

# labware setup
plate = labware.load('96-flat', '2')
trough1 = labware.load(trough_name, '5')
trough2 = labware.load(trough_name, '9')
tiprack = labware.load('opentrons-tiprack-300ul', '4')

# instrument setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack])

# reagent setup
wistd = trough1.wells('A1')
water = trough2.wells('A1')


def run_custom_protocol(
        number_of_samples: int=96,
        tip_start_column: str=2):

    if number_of_samples >= 12:
        plate_loc = [col for col in plate.cols()]
    else:
        plate_loc = [col for col in plate.cols()][:number_of_samples]

    m300.start_at_tip(tiprack.cols(tip_start_column))
    # transfer WISTD to wells
    m300.pick_up_tip()
    m300.mix(3, 300, wistd)
    m300.blow_out(wistd)
    for dest in plate_loc:
        m300.transfer(250, wistd, dest.top(), blow_out=True, new_tip='never')
    m300.drop_tip()

    # transfer water to wells
    m300.pick_up_tip()
    m300.mix(3, 300, water)
    m300.blow_out(water)
    for dest in plate_loc:
        m300.transfer(250, water, dest.top(), blow_out=True, new_tip='never')
    m300.drop_tip()
