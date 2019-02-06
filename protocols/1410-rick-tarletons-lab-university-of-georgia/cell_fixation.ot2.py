from opentrons import labware, instruments

trough_name = 'trough-1well'
if trough_name not in labware.list():
    labware.create(
        'trough-1well',
        grid=(1, 1),
        spacing=(0, 0),
        diameter=0,
        depth=25)

# labware setup
tiprack = labware.load('opentrons-tiprack-300ul', '1')
trough_1 = labware.load('trough-12row', '2')
trough_2 = labware.load('trough-12row', '3')

# pipette setup
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack])


def run_custom_protocol(
        number_of_384_well_plates: int=2):

    pbs = trough_1.wells('A1')
    paraform = trough_2.wells('A1')

    plates = [labware.load('384-plate', slot)
              for slot in ['4', '5', '6', '7', '8', '9', '10', '11'][
                :number_of_384_well_plates]]
    for plate in plates:
        plate.properties['height'] = 14.4
        for well in plate.wells():
            well.properties['depth'] = 11.5

    targets = [well for plate in plates
               for well in plate.rows(0).wells()+plate.rows(1).wells()]

    # remove 50 uL from all wells of all plates
    m300.consolidate(50, targets, m300.trash_container.top(), new_tip='once')

    pbs_volume_tracker = pbs.max_volume()
    # add 50 uL PBS to all wells of all plates
    m300.pick_up_tip()
    for well in targets:
        if pbs_volume_tracker < 300 * 8:
            pbs = next(pbs)
            pbs_volume_tracker = pbs.max_volume()
        if m300.current_volume < 50:
            m300.aspirate(300, pbs)
            pbs_volume_tracker -= 300 * 8
        m300.dispense(50, well)
    m300.drop_tip()

    # remove 50 uL from all wells of all plates
    m300.consolidate(50, targets, m300.trash_container.top(), new_tip='once')

    # add 50 uL paraform to all wells of all plates
    paraform_volume_tracker = paraform.max_volume()
    m300.pick_up_tip()
    for well in targets:
        if pbs_volume_tracker < 300 * 8:
            pbs = next(paraform)
            paraform_volume_tracker = paraform.max_volume()
        if m300.current_volume < 50:
            m300.aspirate(300, paraform)
            paraform_volume_tracker -= 300 * 8
        m300.dispense(50, well)
    m300.drop_tip()

    m300.delay(minutes=15)

    # remove 50 uL from all wells of all plates
    m300.consolidate(50, targets, m300.trash_container.top(), new_tip='once')

    # add 50 uL PBS to all wells of all plates
    m300.pick_up_tip()
    for well in targets:
        if pbs_volume_tracker < 300 * 8:
            pbs = next(pbs)
            pbs_volume_tracker = pbs.max_volume()
        if m300.current_volume < 50:
            m300.aspirate(300, pbs)
            pbs_volume_tracker -= 300 * 8
        m300.dispense(50, well)
    m300.drop_tip()
