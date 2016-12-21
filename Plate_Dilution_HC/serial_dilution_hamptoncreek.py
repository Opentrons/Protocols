from opentrons import containers, instruments

p1000rack = containers.load('tiprack-1000ul', 'A1')
p200rack = containers.load('tiprack-200ul', 'A2')
trough = containers.load('trough-12row', 'C1')
tube = containers.load('tube-rack-2ml', 'D1')
plate = containers.load('96-PCR-flat', 'D2')
trash = containers.load('point', 'B2')

p200 = instruments.Pipette(
    axis="a",
    max_volume=200,
    trash_container=trash,
    tip_racks=[p200rack],
    channels=8
)

p1000 = instruments.Pipette(
    axis="b",
    max_volume=1000,
    trash_container=trash,
    tip_racks=[p1000rack]
)


def dilute_wells(wells, volume, pipette):
    pipette.pick_up_tip()
    for i in range(len(wells) - 1):  # stop before the last one
        pipette.aspirate(volume, wells[i])
        pipette.dispense(wells[i + 1])
        pipette.mix(3, volume, wells[i + 1])
    pipette.drop_tip()


def distribute_equally(source, targets, volume, pipette):
    pipette.pick_up_tip()
    aspirate_volume = volume * int(pipette.max_volume / volume)
    for well in targets:
        if pipette.current_volume < volume:
            pipette.aspirate(aspirate_volume).delay(1).touch_tip()
        pipette.dispense(volume, well).touch_tip()
    pipette.blow_out().drop_tip()


# distribute buffer to all wells
distribute_equally(trough['A1'], plate, 300, p1000)

# distribute samples in duplicate to columns A and E, 1 tube to 2 wells
for i in range(12):
    targets = [plate.cols['A'][i], plate.cols['E'][i]]
    distribute_equally(tube[i], targets, 300, p1000)

# dilute down all rows
for row in plate.rows:
    dilute_wells(row[0:4], 300, p1000)
    dilute_wells(row[4:8], 300, p1000)

# dispense 200 uL to every even row
distribute_equally(trough['A1'], plate.rows[1:12:2], 200, p200)
