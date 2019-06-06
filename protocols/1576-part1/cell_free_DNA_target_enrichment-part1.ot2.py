from opentrons import labware, instruments, modules
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Cell3 Target: Cell Free DNA Target Enrichment Part 1',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


def run_custom_protocol(
        kit_version: StringSelection(
            'A: cell free DNA and fragmented DNA samples',
            'B: intact genomic DNA samples'
            )='A: cell free DNA and fragmented DNA samples',
        number_of_samples: StringSelection('16', '48', '96')='96',
        DNA_volume: float=35,
        DNA_input: StringSelection('>= 50 ng', '< 50 ng')='>=50 ng'):

    number_of_samples = int(number_of_samples)

    # labware setup
    temp_module = modules.load('tempdeck', '7')
    temp_plate = labware.load(
        'opentrons-aluminum-block-96-PCR-plate', '7', share=True)
    tuberack = labware.load('opentrons-aluminum-block-2ml-screwcap', '8')
    tiprack_300 = labware.load('opentrons-tiprack-300ul', '9')
    tipracks_50 = [labware.load('opentrons-tiprack-300ul', slot)
                   for slot in ['10', '11']]

    # instrument setup
    p50 = instruments.P50_Single(
        mount='left',
        tip_racks=tipracks_50)
    p300 = instruments.P300_Single(
        mount='right',
        tip_racks=[tiprack_300])

    # reagent setup
    nuclease_free_water = tuberack.wells('A1')
    end_repair_buffer = tuberack.wells('B1')
    end_repair_enzyme_mix = tuberack.wells('C1')
    frag_buffer = tuberack.wells('A2')
    frag_enhancer = tuberack.wells('A3')
    frag_enzyme_mix = tuberack.wells('A4')
    mastermix = tuberack.wells('D6')

    temp_module.set_temperature(4)
    temp_module.wait_for_temp()

    # define sample locations
    samples = temp_plate.wells('A1', length=number_of_samples)

    # determine master mix components and volumes based on kit used
    if 'A: ' in kit_version:
        buffer_vol = (5 * number_of_samples) * 1.05
        water_vol = ((35 - DNA_volume) * number_of_samples) * 1.05
        volumes = [buffer_vol, water_vol]
        components = [end_repair_buffer, nuclease_free_water]
    else:
        buffer_vol = (5 * number_of_samples) * 1.05
        enhancer_vol = ((2.5 if DNA_input == '< 50 ng' else 0) *
                        number_of_samples) * 1.05
        water_vol = ((35 - enhancer_vol - DNA_volume) * number_of_samples
                     ) * 1.05
        volumes = [buffer_vol, enhancer_vol, water_vol]
        components = [frag_buffer, frag_enhancer, nuclease_free_water]

    # prepare reaction mix
    for vol, component in zip(volumes, components):
        if vol > 50:
            pipette = p300
        else:
            pipette = p50
        if vol > 0:
            pipette.pick_up_tip()
            pipette.transfer(vol, component, mastermix, new_tip='never')
            mix_vol = pipette.max_volume if vol > pipette.max_volume else vol
            pipette.mix(5, mix_vol, mastermix)
            pipette.drop_tip()

    # distribute and mix mastermix into each sample
    mastermix_vol = 40 - DNA_volume
    for sample in samples:
        p50.pick_up_tip()
        p50.transfer(mastermix_vol, mastermix, sample, new_tip='never')
        p50.mix(10, 30, sample)
        p50.blow_out(sample.top())
        p50.drop_tip()

    # determine the enzyme to use based on kit used
    if 'A: ' in kit_version:
        enzyme_mix = end_repair_enzyme_mix
    else:
        enzyme_mix = frag_enzyme_mix

    # transfer Enzyme Mix to each sample
    for sample in samples:
        p50.pick_up_tip()
        p50.transfer(10, enzyme_mix, sample, new_tip='never')
        p50.mix(10, 30, sample)
        p50.blow_out(sample.top())
        p50.drop_tip()
