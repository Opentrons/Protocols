from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Biofilm Assay',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = 'sarstedt_96_wellplate_200ul_flat'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.9,
        depth=11.2,
        volume=200
    )

tiprack_name = 'sarstedt_96_tiprack_300ul'
if tiprack_name not in labware.list():
    labware.create(
        tiprack_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.23,
        depth=59.3
    )

res_name = 'axygen_1_reservoir_240ml'
if res_name not in labware.list():
    labware.create(
        res_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=70,
        depth=33,
        volume=240000
    )

# load labware and modules
distilled_h2o = labware.load(res_name, '1', 'distilled H2O').wells(0)
crystal_violet = labware.load(res_name, '2', 'crystal violet').wells(0)
tipracks300 = [labware.load(tiprack_name, '3', '300ul tiprack')]
tempdeck = modules.load('tempdeck', '4')
plate = labware.load(plate_name, '4', 'culture plate', share=True)
tempdeck.set_temperature(37)
tempdeck.wait_for_temp()
ethanol = labware.load(res_name, '5', '70% ethanol').wells(0)
waste = labware.load(res_name, '7', 'liquid waste').wells(0).top()


def run_custom_protocol(
        p300_multi_mount: StringSelection('right', 'left') = 'right',
        number_of_samples: int = 96
):
    # pipette
    m300 = instruments.P300_Multi(
        mount=p300_multi_mount, tip_racks=tipracks300)

    num_cols = math.ceil(number_of_samples/8)
    samples = plate.rows('A')[:num_cols]

    m300.home()
    robot.pause('Incubating on 37C tempdeck. Resume once ready.')

    # remove initial supernatant
    m300.pick_up_tip()
    for s in samples:
        m300.transfer(160, s.bottom(0.5), waste, new_tip='never', air_gap=30)
        m300.blow_out()
    m300.drop_tip()

    # 3x distilled H2O wash
    for _ in range(3):
        m300.pick_up_tip()
        for s in samples:
            m300.transfer(
                170, distilled_h2o, s.top(), new_tip='never', air_gap=30)
            m300.blow_out()
        for s in samples:
            m300.transfer(
                180, s.bottom(0.5), waste, new_tip='never', air_gap=30)
            m300.blow_out()
        m300.drop_tip()

    # stain with crystal violet
    m300.pick_up_tip()
    for s in samples:
        m300.transfer(
            190, crystal_violet, s.top(), new_tip='never', air_gap=30)
        m300.blow_out()
    m300.drop_tip()
    robot.comment('Delaying 10 minutes for staining...')
    m300.delay(minutes=10)
    m300.pick_up_tip()
    for s in samples:
        m300.transfer(200, s.bottom(0.5), waste, new_tip='never', air_gap=30)
        m300.blow_out()
    m300.drop_tip()

    # 5x distilled H2O wash
    for _ in range(5):
        m300.pick_up_tip()
        for s in samples:
            m300.transfer(
                200, distilled_h2o, s.top(), new_tip='never', air_gap=30)
            m300.blow_out()
        for s in samples:
            m300.transfer(
                210, s.bottom(0.5), waste, new_tip='never', air_gap=30)
            m300.blow_out()
        m300.drop_tip()
    robot.pause('Pausing for drying. Resume once dry.')

    # ethanol addition
    m300.pick_up_tip()
    for s in samples:
        m300.transfer(230, ethanol, s.top(), new_tip='never', air_gap=30)
        m300.blow_out()
    m300.drop_tip()
