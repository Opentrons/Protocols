from opentrons import labware, instruments

# labwaer setup
plate384 = labware.load('384-plate', '1')
plates96 = [labware.load('96-flat', slot, 'Plate ' + name)
            for slot, name in zip(['2', '3', '5', '6'], ['1', '2', '3', '4'])]
trough = labware.load('trough-12row', '4')
tipracks10 = [labware.load('tiprack-10ul', slot)
              for slot in ['7', '9', '10', '11']]
tiprack50 = labware.load('tiprack-200ul', '8')

# pipette setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=tipracks10)

p50 = instruments.P50_Single(
    mount='right',
    tip_racks=[tiprack50])


def run_custom_protocol(
        reagent_volume: float=9.36,
        primer_volume: float=2.3):

    # add reagent from trough to all wells in 384-well plate
    p50.pick_up_tip()
    for well in plate384.wells():
        if p50.current_volume < reagent_volume:
            p50.aspirate(trough.wells('A1'))
        p50.dispense(reagent_volume, well.top())
    p50.blow_out(trough.wells('A1'))
    p50.drop_tip()

    # define locations of the primers
    primers_loc = [well for plate in plates96 for well in plate.wells()]

    # transfer primer stock to the appropriate well
    p10.transfer(primer_volume, primers_loc, plate384.wells(),
                 new_tip='always')
