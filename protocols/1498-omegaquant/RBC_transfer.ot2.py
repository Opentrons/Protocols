from opentrons import labware, instruments
import math

metadata = {
    'protocolName': 'RBC Transfer',
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
BTM = labware.load(trough_name, '1').wells('A1')
plate = labware.load('96-flat', '2')
BF3 = labware.load(trough_name, '3').wells('A1')
tiprack_300 = labware.load('opentrons-tiprack-300ul', '4')
WISTD = labware.load(trough_name, '5').wells('A1')
tiprack_50 = labware.load(tiprack_name, '6')
sample_trays = [labware.load(tuberack_name, slot)
                for slot in ['7', '8', '10', '11']]
water = labware.load(trough_name, '9')

# instruments setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack_50])

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack_300])


def run_custom_protocol(number_of_samples: int=96):

    col_num = math.ceil(number_of_samples/8)

    samples = [well for tray in sample_trays for well in tray.wells()]

    # transfer blood from tube to 96-well plate
    for index in range(number_of_samples):
        p50.pick_up_tip()
        p50.aspirate(25, samples[index].bottom(4))
        p50.delay(seconds=3)
        p50.dispense(25, plate[index])
        p50.drop_tip()

    # transfer BF3 to each well
    m300.pick_up_tip()
    m300.mix(3, 300, BF3)
    for col in plate.cols('1', length=col_num):
        m300.transfer(250, BF3, col[0].top(), new_tip='never')
    m300.drop_tip()

    # transfer WISTD
    m300.pick_up_tip()
    m300.mix(3, 300, WISTD)
    for col in plate.cols('1', length=col_num):
        m300.transfer(250, WISTD, col[0].top(), new_tip='never')
    m300.drop_tip()
