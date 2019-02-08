from opentrons import labware, instruments, modules
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Protein Addition',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


def run_custom_protocol(
        temperature_of_tempdeck: float=4,
        protein_volume: float=19.8,
        mixing_speed: StringSelection('Default', 'Fast', 'Slow')='Default'):

    # labware setup
    plate = labware.load('384-plate', '5')
    temp_module = modules.load('tempdeck', '4')
    temp_rack = labware.load('opentrons-aluminum-block-2ml-screwcap', '4',
                             share=True)

    tiprack_10 = [labware.load('tiprack-10ul', slot)
                  for slot in ['1', '2', '3', '6']]
    tiprack_50 = [labware.load('tiprack-200ul', slot)
                  for slot in ['7', '8', '9', '10']]

    # instruments setup
    p10 = instruments.P10_Single(
        mount='left',
        tip_racks=tiprack_10)
    p50 = instruments.P50_Single(
        mount='right',
        tip_racks=tiprack_50)

    # reagent setup
    protein = temp_rack.wells('A1')

    # set temp for temp module
    temp_module.set_temperature(temperature_of_tempdeck)
    temp_module.wait_for_temp()

    if protein_volume > 10:
        pipette = p50
        mix_vol = 10
    else:
        pipette = p10
        mix_vol = 5

    # define different speeds for mixing
    default_aspirate_speed = pipette.max_volume / 2
    default_dispense_speed = pipette.max_volume

    if mixing_speed == 'Fast':
        aspirate_speed = pipette.max_volume
        dispense_speed = pipette.max_volume * 2
    elif mixing_speed == 'Slow':
        aspirate_speed = pipette.max_volume / 4
        dispense_speed = pipette.max_voume / 2
    else:
        aspirate_speed = default_aspirate_speed
        dispense_speed = default_dispense_speed

    # define first 4 rows as protein destinations
    protein_dests = [well for row in plate.rows('A', to='D') for well in row]

    protein_volume_tracker = 1500

    # transfer protein
    for dest in protein_dests:
        # set transfer speed
        pipette.set_flow_rate(
            aspirate=default_aspirate_speed, dispense=default_dispense_speed)
        pipette.pick_up_tip()
        if protein_volume_tracker <= protein_volume:
            protein = next(protein)
            protein_volume_tracker = 1500
        pipette.transfer(protein_volume, protein, dest, new_tip='never')
        # set mixing speed
        pipette.set_flow_rate(aspirate=aspirate_speed, dispense=dispense_speed)
        pipette.mix(8, mix_vol, dest)
        pipette.blow_out(dest.top())
        pipette.drop_tip()
        protein_volume_tracker -= protein_volume
