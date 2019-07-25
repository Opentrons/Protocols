from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'ProtocolName': 'Arcis Sample Prep Demo Kit Protocol',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library'
    }


def run_custom_protocol(
        left_pipette: StringSelection(
            'P10_Single', 'P50_Single', 'none')='P10_Single',
        sample_number: int=12,
        reaction_container: StringSelection(
            'PCR-strip-tall',
            'biorad_96_wellplate_200ul_pcr')='PCR-strip-tall',
        extract_volume: float=5,
        extract_reagent2_ratio: StringSelection(
            '1:4', '1:3', '1:2', '1:1')='1:4'):

    if sample_number > 12:
        raise Exception("This protocol can only support 12 reactions. \
Protocol for the Bulk Kit coming soon.")

    if extract_volume < 30 and left_pipette == 'none':
        raise Exception("You must attach a second pipette, as there are \
volumes in your protocol that are outside of the P300 working volume \
range. (30-300 uL)")

    def mount_pipette(pipette_type, mount, tiprack_slot):
        pipette_size = pipette_type.split('_')[0]
        vol = 10 if pipette_size == 'p10' else 300
        tipracks = [labware.load('opentrons-tiprack-{}ul'.format(vol), slot)
                    for slot in tiprack_slot]
        pipette = getattr(instruments, pipette_type)(
            mount=mount,
            tip_racks=tipracks)
        return pipette

    # labware setup
    reaction_plate = labware.load(reaction_container, '1', 'Reaction Plate')
    # stage_1_plate = labware.load(stage_1_container, '2', 'Stage 1 Plate')
    # stage_2_plate = labware.load(stage_2_container, '3', 'Stage 2 Plate')
    tuberack = labware.load('opentrons_24_tuberack_generic_2ml_screwcap', '5')

    # instrument setup
    pipL = mount_pipette(left_pipette, 'left', ['4', '7'])
    pipR = mount_pipette('P300_Single', 'right', ['6', '9'])

    # reagent setup
    reagent_1 = tuberack.wells('A1')
    reagent_2 = tuberack.wells('B1')
    samples = reaction_plate.wells()[:sample_number]
    stage_1_samples = reaction_plate.wells()[24:24+sample_number]
    stage_2_samples = reaction_plate.wells()[48:48+sample_number]

    # transfer Reagent 1 to Stage 1 Plate
    pipR.transfer(150, reagent_1, stage_1_samples)

    # transfer Reagent 2 to Stage 2 Plate
    reagent_2_vol = extract_volume * int(extract_reagent2_ratio.split(':')[1])
    if reagent_2_vol >= 30:
        pipette = pipR
    else:
        pipette = pipL
    pipette.transfer(reagent_2_vol, reagent_2, stage_2_samples)

    # transfer samples to Stage 1 Plate
    for source, dest in zip(samples, stage_1_samples):
        pipR.pick_up_tip()
        pipR.transfer(90, source, dest, new_tip='never')
        pipR.blow_out(dest)
        pipR.mix(3, 100, dest)
        pipR.blow_out(dest)
        pipR.drop_tip()

    # incubate for 1 minute
    pipR.delay(minutes=1)

    # transfer extract to Stage 2 Plate
    if extract_volume >= 30:
        pipette = pipR
    else:
        pipette = pipL
    for source, dest in zip(stage_1_samples, stage_2_samples):
        pipette.pick_up_tip()
        pipette.transfer(extract_volume, source, dest, new_tip='never')
        pipette.blow_out(dest)
        if extract_volume > pipette.max_volume:
            mix_volume = pipette.max_volume
        else:
            mix_volume = extract_volume
        pipette.mix(3, mix_volume, dest)
        pipette.blow_out(dest)
        pipette.drop_tip()
