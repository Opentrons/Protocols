from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
from opentrons.legacy_api.modules import tempdeck
import math

"""Controlling multiple of the same module in the protocol:
1. SSH into robot
2. run $ls /dev/tty*
   you are looking for two values with the format /dev/ttyACM*
   you will use those values in lines 24-27.
If you need to know which tempdeck is hooked up to which port:
1. unplug one of the modules
2. run $ls /dev/tty* : the results correlates to the module that is plugged in
3. plug the other module in and run ls /dev/tty* again, you will be able to
   know the value of the second module
"""

# defining two Temperature Modules
tempmod1 = tempdeck.TempDeck()
tempmod2 = tempdeck.TempDeck()
tempmod3 = tempdeck.TempDeck()
tempmod4 = tempdeck.TempDeck()

tempmod1._port = '/dev/ttyACM1'
tempmod2._port = '/dev/ttyACM2'
tempmod3._port = '/dev/ttyACM3'
tempmod4._port = '/dev/ttyACM4'

if not robot.is_simulating():
    tempmod1.connect()
    tempmod2.connect()
    tempmod3.connect()
    tempmod4.connect()

metadata = {
    'protocolName': 'Cell Culture Assay',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom plate
plate_name = 'Cellvis-24-flat'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(6, 4),
        spacing=(19.3, 19.3),
        diameter=16.2,
        depth=19,
        volume=3600
    )

# load labware and modules
tempmod1 = modules.load('tempdeck', '10')
temp_plate1 = labware.load(plate_name, '10', 'plate 1', share=True)
tempmod2 = modules.load('tempdeck', '7')
temp_plate2 = labware.load(plate_name, '7', 'plate 2', share=True)
tempmod3 = modules.load('tempdeck', '4')
temp_plate3 = labware.load(plate_name, '4', 'plate 3', share=True)
tempmod4 = modules.load('tempdeck', '6')
temp_plate4 = labware.load(plate_name, '6', 'plate 4', share=True)
tips1000 = [labware.load('tiprack-1000ul', slot) for slot in ['5', '11']]
tubes = labware.load('opentrons-tuberack-15_50ml', '8')
waste = labware.load('point', '1')

tempmod1.set_temperature(37)
tempmod2.set_temperature(37)
tempmod3.set_temperature(37)
tempmod4.set_temperature(37)
tempmod4.wait_for_temp()

# reagents
media = [tubes.wells(well) for well in ['A3', 'A4']]


def run_custom_protocol(
    pipette_mount: StringSelection('right', 'left') = 'right'
):

    # height track function
    r = 13.4
    h = {
        'media1': -20,
        'media2': -20
        }

    def h_track(vol, media):
        nonlocal h
        dh = vol/(math.pi*(r**2))
        h[media] = h[media] - dh if h[media] - dh > - 112 else 112

    # pipette
    p1000 = instruments.P1000_Single(mount=pipette_mount, tip_racks=tips1000)

    # perform media transfers
    for i, well in enumerate([well for plate in [temp_plate1,
                                                 temp_plate2,
                                                 temp_plate3,
                                                 temp_plate4]
                              for well in plate]):

        # transfer out old media
        p1000.transfer(
            1000,
            well.bottom(0.5),
            waste.wells(0),
            blow_out=True
            )

        media_name = 'media1' if i < 48 else 'media2'
        media_tube = media[0] if i < 48 else media[1]
        # choose media tube, height track, and transfer new media
        h_track(750, media_name)
        p1000.transfer(
            750,
            media_tube.top(h[media_name]),
            well.top(),
            blow_out=True
            )
