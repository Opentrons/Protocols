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

pbs = labware.load(trough_name, '2').wells('A1')
paraform = labware.load(trough_name, '3').wells('A1')
for well in [pbs, paraform]:
    well.properties['length'] = 95
    well.properties['width'] = 75

# pipette setup
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack])


def run_custom_protocols(
        number_of_384_well_plates: int=2):

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

    # add 50 uL PBS to all wells of all plates
    m300.pick_up_tip()
    m300.aspirate(250, pbs)
    for well in targets:
        if m300.current_volume <= 50:
            m300.blow_out(pbs)
            m300.aspirate(250, pbs)
        m300.dispense(50, well)
    m300.drop_tip()

    # remove 50 uL from all wells of all plates
    m300.consolidate(50, targets, m300.trash_container.top(), new_tip='once')

    # add 50 uL paraform to all wells of all plates
    m300.pick_up_tip()
    m300.aspirate(250, paraform)
    for well in targets:
        if m300.current_volume <= 50:
            m300.blow_out(paraform)
            m300.aspirate(250, paraform)
        m300.dispense(50, well)
    m300.drop_tip()

    m300.delay(minutes=15)

    # remove 50 uL from all wells of all plates
    m300.consolidate(50, targets, m300.trash_container.top(), new_tip='once')

    # add 50 uL PBS to all wells of all plates
    m300.pick_up_tip()
    m300.aspirate(250, pbs)
    for well in targets:
        if m300.current_volume <= 50:
            m300.blow_out(pbs)
            m300.aspirate(250, pbs)
        m300.dispense(50, well)
    m300.drop_tip()
