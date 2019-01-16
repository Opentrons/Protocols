from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Fluorescence Polarization Assays',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'}

trough_name = 'trough-1row'
if trough_name not in labware.list():
    labware.create(
        trough_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=85,
        depth=38)

plate_name = 'puregrade-96-flat'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=11)

cooler_name = 'eppendorf-PCR-cooler'
if cooler_name not in labware.list():
    labware.create(
        cooler_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=0,
        depth=30)

cooler_plate_name = 'non-skirted-96-PCR-chimney'
if cooler_plate_name not in labware.list():
    labware.create(
        cooler_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6,
        depth=14)

# labware setup
buffer = labware.load(trough_name, '1', 'Buffer').wells('A1')
plate = labware.load(plate_name, '2', 'Plate')
cooler_1 = labware.load(cooler_name, '3')
WC1 = labware.load(cooler_plate_name, '3', 'WC1', share=True)
reagent_plate = labware.load('96-flat', '4', 'Reagent Plate')
cooler_2 = labware.load(cooler_name, '5')
inhibitors = labware.load(cooler_plate_name, '5', 'Inhibitors', share=True)
tracer = labware.load(trough_name, '6', 'Tracer').wells('A1')

tiprack_300 = labware.load('opentrons-tiprack-300ul', '7')
tiprack_10 = labware.load('tiprack-10ul', '8')

# instrument setup
m10 = instruments.P10_Multi(
    mount='left',
    tip_racks=[tiprack_10])
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack_300])

# reagent setup
protein = reagent_plate.cols('1')
DMSO = reagent_plate.cols('2')


def run_custom_protocol(protocol_type: StringSelection('A1', 'A2')='A1'):

    if protocol_type == 'A1':
        DMSO_vol = 18
        dwp = inhibitors
    else:
        DMSO_vol = 16.8
        dwp = WC1

    """
    Protocol A
    """
    m10.pick_up_tip()
    m10.transfer(DMSO_vol, DMSO, dwp.cols('4')[0].top(), new_tip='never')
    m10.transfer(10, DMSO, [col[0].top() for col in dwp.cols('5', to='12')],
                 new_tip='never')
    m10.drop_tip()

    m10.pick_up_tip()
    m10.mix(3, 10, dwp.cols('4'))
    for source, dest in zip(
            plate.cols('4', to='11'), dwp.cols('5', to='12')):
        m10.transfer(10, source, dest, new_tip='never')
        m10.mix(3, 10, dest)
    m10.drop_tip()

    """
    Protocol B
    """
    m300.pick_up_tip()
    m300.transfer(
        [200, 150],
        buffer,
        [col[0].top() for col in plate.cols('1', '2')],
        new_tip='never'
        )
    m300.distribute(
        140,
        buffer,
        [col[0].top() for col in plate.cols('3', to='12')],
        disposal_vol=20,
        blow_out=buffer,
        new_tip='never'
        )
    m300.drop_tip()

    m10.distribute(2, DMSO, [col[0].top() for col in plate.cols('1', to='3')])

    m10.transfer(
        10, protein, [col[0].top() for col in plate.cols('3', to='12')])

    m10.pick_up_tip()
    for source, dest in zip(dwp.cols('12', to='4'), plate.cols('12', to='4')):
        m10.transfer(2, source, dest, new_tip='never')
        m10.mix(3, 10, dest)
        m10.blow_out(dest[0].top())
    m10.drop_tip()

    m300.distribute(
        50,
        tracer,
        [col[0].top() for col in plate.cols('2', to='12')],
        blow_out=tracer)

    m300.pick_up_tip()
    for col in plate.cols('2', '3') + plate.cols('12', to='4'):
        m300.mix(3, 200, col)
        m300.blow_out(col.top())
    m300.drop_tip()
