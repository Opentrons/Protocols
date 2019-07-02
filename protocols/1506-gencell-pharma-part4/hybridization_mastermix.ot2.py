from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Hybridization Master Mix',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


def run_custom_protocol(
        sample_num: StringSelection('4', '8', '12', '16')='4'
        ):

    sample_num = int(sample_num)

    # labware setup
    eppendorf_rack = labware.load('opentrons-tuberack-2ml-eppendorf', '5')
    samples_plate = labware.load('PCR-strip-tall', '1')

    tiprack_50 = labware.load('opentrons-tiprack-300ul', '6')
    tiprack_300 = labware.load('opentrons-tiprack-300ul', '3')

    # pipette setup
    p300 = instruments.P300_Single(
        mount='left',
        tip_racks=[tiprack_300])

    p50 = instruments.P50_Single(
        mount='right',
        tip_racks=[tiprack_50])

    # reagent setup
    cot = eppendorf_rack.wells('A1')
    blockagent = eppendorf_rack.wells('A2')
    hyb_buf = eppendorf_rack.wells('A3')

    mix_dest = eppendorf_rack.wells('D1')

    samples = [well for well in samples_plate.wells('A1', length=sample_num)]

    volume_dict = {
        4: {cot: 25, blockagent: 55, hyb_buf: 275},
        8: {cot: 45, blockagent: 99, hyb_buf: 495},
        12: {cot: 65, blockagent: 143, hyb_buf: 715},
        16: {cot: 90, blockagent: 198, hyb_buf: 990}
    }

    # create master mix
    for reagent, volume in volume_dict[sample_num].items():
        if volume > 50:
            pipette = p300
        else:
            pipette = p50
        pipette.pick_up_tip()
        if reagent == hyb_buf:
            pipette.mix(5, pipette.max_volume, reagent)
            pipette.blow_out(reagent)
        pipette.transfer(
            volume, reagent, mix_dest.top(), blow_out=True, new_tip='always')

    # transfer and mix master mix in samples
    p300.pick_up_tip()
    p300.mix(5, 300, mix_dest)
    p300.blow_out(mix_dest)
    for sample in samples:
        if not p300.tip_attached:
            p300.pick_up_tip()
        p300.transfer(71, mix_dest, sample, new_tip='never')
        p300.mix(5, 50, sample)
        p300.blow_out(sample)
        p300.drop_tip()
