from opentrons import labware, instruments
import math

trough_name = 'trough-1row'
if trough_name not in labware.list():
    labware.create(
        trough_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=72,
        depth=41.5)

# labware setup
trough = labware.load(trough_name, '11')
plates = [labware.load('96-flat', slot)
          for slot in ['1', '2', '3', '4', '5']]
tipracks = [labware.load('opentrons-tiprack-300ul', slot)
            for slot in ['6', '7', '8', '9', '10']]

# reagent setup
reagent = trough.wells('A1')

# instrument setup
p1 = instruments.P300_Multi(
    mount='left',
    tip_racks=tipracks)

p2 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks)


def run_custom_protocol(
        reagent_volume: float=1000):

    tip_loc = [col for tiprack in tipracks for col in tiprack.cols()]
    plate_loc = [col for plate in plates for col in plate.cols()]

    for index, (col_1, col_2) in enumerate(zip(
            plate_loc[::2], plate_loc[1::2])):
        volume = reagent_volume
        p1.pick_up_tip(tip_loc[index*2])
        p2.pick_up_tip(tip_loc[index*2+1])
        if volume > p1.max_volume:
            cycle = math.ceil(volume / p1.max_volume)
        else:
            cycle = 1
        for index in range(cycle):
            if volume > 0 and volume < p1.max_volume:
                p1.aspirate(volume, reagent)
                p2.aspirate(volume, reagent)
                p1.dispense(volume, col_1)
                p2.dispense(volume, col_2)
            elif volume > 0:
                p1.aspirate(p1.max_volume, reagent)
                p2.aspirate(p1.max_volume, reagent)
                p1.dispense(p1.max_volume, col_1)
                p2.dispense(p1.max_volume, col_2)
                volume = volume - p1.max_volume
        p1.drop_tip()
        p2.drop_tip()
