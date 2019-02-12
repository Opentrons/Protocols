from opentrons import labware, instruments

metadata = {
    'protocolName': 'One-solution Fames protocols',
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
trough = labware.load(trough_name, '1')
tiprack = labware.load('opentrons-tiprack-300ul', '4')

# instrument setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack])

# reagent setup
source = trough.wells('A1')


def run_custom_protocol(
        number_of_samples: int=96,
        tip_start_column: str=1):

    if number_of_samples >= 12:
        plate_loc = [col for col in plate.cols()]
    else:
        plate_loc = [col for col in plate.cols()][:number_of_samples]

    m300.start_at_tip(tiprack.cols(tip_start_column))
    m300.pick_up_tip()
    m300.mix(3, 300, source)
    m300.blow_out(source)
    for dest in plate_loc:
        m300.transfer(250, source, dest.top(), blow_out=True, new_tip='never')
    m300.drop_tip()
