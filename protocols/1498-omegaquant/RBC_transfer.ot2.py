from opentrons import labware, instruments

metadata = {
    'protocolName': 'RBC Transfer',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

plate_name = 'omegaquant-96-well-plate'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=9,
        depth=30)

trough_name = 'glass-trough'
if trough_name not in labware.list():
    labware.create(
        trough_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=66,
        depth=25)

tiprack_name = 'tiprack-200ul-extended'
if tiprack_name not in labware.list():
    labware.create(
        tiprack_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=3.5,
        depth=78)

tuberack_name = 'blood-tube-rack'
if tuberack_name not in labware.list():
    labware.create(
        tuberack_name,
        grid=(6, 4),
        spacing=(20, 20),
        diameter=13,
        depth=75)

# labware setup
plate = labware.load(plate_name, '2')
trough_1 = labware.load(trough_name, '3')
tiprack_300 = labware.load('opentrons-tiprack-300ul', '4')
trough_2 = labware.load(trough_name, '5')
tiprack_50 = labware.load(tiprack_name, '6')
sample_trays = [labware.load(tuberack_name, slot)
                for slot in ['7', '8', '10', '11']]

# instruments setup
p50 = instruments.P50_Single(
    mount='right',
    tip_racks=[tiprack_50])

m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack_300])

# Reagent setup and transfer
bf3 = trough_1.wells('A1')
wistd = trough_2.wells('A1')


def run_custom_protocol(
        number_of_samples: int=96,
        tip_start_column: str=1):

    if number_of_samples >= 12:
        plate_loc = [col for col in plate.cols()]
    else:
        plate_loc = [col for col in plate.cols()][:number_of_samples]

    samples = [well for tray in sample_trays for well in tray.wells()]
    outputs = [well for row in plate.rows() for well in row]

    # transfer blood from tube to 96-well plate
    for index in range(number_of_samples):
        p50.pick_up_tip()
        p50.aspirate(25, samples[index].bottom(4))
        p50.delay(seconds=3)
        p50.dispense(25, outputs[index])
        p50.blow_out()
        p50.touch_tip()
        p50.delay(seconds=1)
        p50.drop_tip()

    m300.start_at_tip(tiprack_300.cols(tip_start_column))
    # transfer 14% BF3·MeOH to wells
    m300.pick_up_tip()
    m300.mix(3, 300, bf3)
    m300.blow_out(bf3)
    for dest in plate_loc:
        m300.transfer(250, bf3, dest[0].top(), blow_out=True, new_tip='never')
    m300.drop_tip()

    # transfer WISTD to wells
    m300.pick_up_tip()
    m300.mix(3, 300, wistd)
    m300.blow_out(wistd)
    for dest in plate_loc:
        m300.transfer(250, wistd, dest[0].top(), blow_out=True,
                      new_tip='never')
    m300.drop_tip()
