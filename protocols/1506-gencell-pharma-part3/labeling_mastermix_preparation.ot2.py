from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Labeling Master Mix Preparation',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


def run_custom_protocol(
        sample_num: StringSelection('4', '8', '12', '16')='4'
        ):

    sample_num = int(sample_num)

    # labware setup
    screwcap_rack = labware.load('opentrons-tuberack-2ml-screwcap', '4')
    eppendorf_rack = labware.load('opentrons-tuberack-2ml-eppendorf', '5')
    plate = labware.load('PCR-strip-tall', '2')
    tiprack_10 = labware.load('tiprack-10ul', '8')
    tipracks_300 = [labware.load('opentrons-tiprack-300ul', slot)
                    for slot in ['3', '6', '9']]

    # instruments setup
    p10 = instruments.P10_Single(
        mount='left',
        tip_racks=[tiprack_10])

    p50 = instruments.P50_Single(
        mount='right',
        tip_racks=tipracks_300)

    # reagent setup
    water = screwcap_rack.wells('D1')
    RE_buffer = screwcap_rack.wells('D2')
    dntps = screwcap_rack.wells('D3')
    cy3 = screwcap_rack.wells('D4')
    cy5 = screwcap_rack.wells('D5')
    exo = screwcap_rack.wells('D6')

    mixcy3 = eppendorf_rack.wells('A1')
    mixcy5 = eppendorf_rack.wells('A3')

    samples = [well for well in plate.wells(0, length=sample_num)]
    controls = [well for well in plate.wells(sample_num, length=sample_num)]

    # Transfer reagents to mastermix
    cys = [cy3, cy5]
    volume_dict = {
        4: {water: 9, RE_buffer: 45, dntps: 22.5, 'cys': 13.5, exo: 4.5},
        8: {water: 17, RE_buffer: 85, dntps: 42.5, 'cys': 25.5, exo: 8.5},
        12: {water: 25, RE_buffer: 125, dntps: 62.5, 'cys': 37.5, exo: 12.5},
        16: {water: 33, RE_buffer: 165, dntps: 82.5, 'cys': 49.5, exo: 16.5}
    }

    for index, mastermix in enumerate([mixcy3, mixcy5]):
        for reagent, volume in volume_dict[sample_num].items():
            if volume > 10:
                pipette = p50
            else:
                pipette = p10
            pipette.pick_up_tip()
            if reagent == 'cys':
                reagent = cys[index]
                pipette.mix(5, volume, reagent)
            elif reagent == exo:
                pipette.mix(5, volume, reagent)
            pipette.transfer(
                volume, reagent, mastermix, blow_out=True, new_tip='always')

    # Distribute mastermixes in samples and controls
    for source, dests in zip([mixcy3, mixcy5], [samples, controls]):
        p50.pick_up_tip()
        p50.mix(5, 50, source)
        p50.blow_out(source)
        for dest in dests:
            if not p50.tip_attached:
                p50.pick_up_tip()
            p50.transfer(21, source, dest, new_tip='never')
            p50.mix(5, 30, dest)
            p50.blow_out(dest)
            p50.drop_tip()
