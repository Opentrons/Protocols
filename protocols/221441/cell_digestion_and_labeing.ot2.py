from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Cell Digestion and Labeling',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
tiprack300_name = 'tipone_96_tiprack_300ul'
if tiprack300_name not in labware.list():
    labware.create(
        tiprack300_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.23,
        depth=59.30
    )

tiprack10_name = 'tipone_96_tiprack_10ul'
if tiprack10_name not in labware.list():
    labware.create(
        tiprack10_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6,
        depth=34
    )

plate_name = 'corning_96_wellplate_v_320ul'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.86,
        depth=11.12,
        volume=320
    )

transwell_name = 'corning_96_wellplate_transwell_360ul'
if transwell_name not in labware.list():
    labware.create(
        transwell_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=4.89,
        depth=11.81,
        volume=360
    )

# load modules and labware
tips10 = labware.load(tiprack10_name, '1', '10ul tiprack')
sus_plate = labware.load(
    plate_name, '2', 'suspension plate with HTS transwell')
res12 = labware.load(
    'usascientific_12_reservoir_22ml', '3', 'reagent reservoir')
tempdeck = modules.load('tempdeck', '4')
transwell_plate = labware.load(
    transwell_name, '4', 'HTS transwell plate', share=True)
strips = labware.load(
    'opentrons_96_aluminumblock_generic_pcr_strip_200ul', '5', 'PCR strips')
tips300 = [
    labware.load(tiprack300_name, str(slot), '300ul tiprack')
    for slot in range(6, 9)
]


def run_custom_protocol(
        P300_multi_mount: StringSelection('right', 'left') = 'right',
        P10_multi_mount: StringSelection('left', 'right') = 'left',
        number_of_sample_columns_to_process: int = 8,
        temperature_module_set_temperature_in_degrees_c: int = 37
):
    # check
    if P300_multi_mount == P10_multi_mount:
        raise Exception('Pipette mounts must be distinct.')
    if (
        number_of_sample_columns_to_process > 12
        or number_of_sample_columns_to_process < 1
       ):
        raise Exception('Number of sample columns to process must be between 1 \
and 12.')
    if (
        temperature_module_set_temperature_in_degrees_c > 95
        or temperature_module_set_temperature_in_degrees_c < 4
       ):
        raise Exception('Temperature module set temperature must be between \
4 and 95C.')

    # temperature module
    tempdeck.set_temperature(temperature_module_set_temperature_in_degrees_c)
    robot.comment('Temperature module reaching set temperature...')
    tempdeck.wait_for_temp()

    # pipettes
    m300 = instruments.P300_Multi(mount=P300_multi_mount, tip_racks=tips300)
    m10 = instruments.P10_Multi(mount=P10_multi_mount, tip_racks=[tips10])

    # sample setup
    trans_samples = transwell_plate.rows(
        'A')[:number_of_sample_columns_to_process]
    sus_samples = sus_plate.rows('A')[:number_of_sample_columns_to_process]

    # mix transwell plate contents
    m300.set_flow_rate(aspirate=15, dispense=15)
    for i, t in enumerate(trans_samples):
        m300.pick_up_tip()
        m300.mix(10, 100, t.bottom(3))
        m300.blow_out(t.top())
        m300.drop_tip()
        if i == len(trans_samples) - 1:
            robot.pause('Suspend HTS transwell plate in Corning 3894 96-well \
plate in slot 2. Resume when ready...')
        else:
            robot.pause('Resume when ready...')

    # transfer to HTS transwell in suspension plate
    m300.set_flow_rate(aspirate=150, dispense=50)
    m300.pick_up_tip()
    m300.distribute(
        150,
        res12.wells(0),
        [s.top(5) for s in sus_samples],
        disposal_vol=0,
        new_tip='never'
    )

    # puncture membrane
    for s in sus_samples:
        if not m300.tip_attached:
            m300.pick_up_tip()
        m300.move_to(s.bottom(1))
        m300.drop_tip()

    robot.pause('Resume when ready...')

    # transfer from PCR strip and mix
    for s in sus_samples:
        m10.pick_up_tip()
        m10.aspirate(2, strips.wells(0))
        m10.aspirate(8, s)
        m10.dispense(10, s)
        m10.blow_out()
        m10.mix(5, 9, s)
        m10.blow_out(s.top(-1))
        m10.drop_tip()
