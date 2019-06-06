from opentrons import labware, instruments, modules
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Cell3 Target: Cell Free DNA Target Enrichment Part 2',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


def run_custom_protocol(
        number_of_samples: StringSelection('16', '48', '96')='96'):

    number_of_samples = int(number_of_samples)

    # labware setup
    plate = labware.load('biorad-hardshell-96-PCR', '1')
    temp_module = modules.load('tempdeck', '7')
    temp_plate = labware.load(
        'opentrons-aluminum-block-96-PCR-plate', '7', share=True)
    tuberack = labware.load('opentrons-aluminum-block-2ml-screwcap', '8')
    tipracks_300 = [labware.load('opentrons-tiprack-300ul', slot)
                    for slot in ['6', '9']]
    tipracks_50 = [labware.load('opentrons-tiprack-300ul', slot)
                   for slot in ['10', '11']]

    # instrument setup
    m50 = instruments.P50_Multi(
        mount='left',
        tip_racks=tipracks_50)
    p300 = instruments.P300_Single(
        mount='right',
        tip_racks=tipracks_300)

    # reagent setup
    nuclease_free_water = tuberack.wells('A1')
    ligation_buffer = tuberack.wells('B1')
    dna_ligase_enzyme = tuberack.wells('C1')
    mastermix = tuberack.wells('D6')

    temp_module.set_temperature(4)
    temp_module.wait_for_temp()

    # define sample locations
    samples = temp_plate.wells('A1', length=number_of_samples)
    col_num = int(number_of_samples / 8)
    sample_cols = temp_plate.cols('1', length=col_num)

    # transfer adapters to reactions
    adapter_cols = plate.cols('1', length=col_num)
    for adapter, sample in zip(adapter_cols, sample_cols):
        m50.pick_up_tip()
        m50.transfer(5, adapter, sample, new_tip='never')
        m50.mix(3, 40, sample)
        m50.blow_out(sample[0].top())
        m50.drop_tip()

    # determine ligation master mix component volumes
    buffer_vol = (20 * number_of_samples) * 1.05
    enzyme_vol = (10 * number_of_samples) * 1.05
    water_vol = (15 * number_of_samples) * 1.05
    volumes = [buffer_vol, enzyme_vol, water_vol]
    components = [ligation_buffer, dna_ligase_enzyme, nuclease_free_water]

    # prepare ligation master mix
    for vol, component in zip(volumes, components):
        p300.pick_up_tip()
        p300.transfer(vol, component, mastermix, new_tip='never')
        mix_vol = p300.max_volume if vol > p300.max_volume else vol
        p300.mix(10, mix_vol, mastermix)
        p300.blow_out(mastermix.top())
        p300.drop_tip()

    # transfer ligation master mix to each reaction
    for sample in samples:
        p300.pick_up_tip()
        p300.transfer(45, mastermix, sample, new_tip='never')
        p300.mix(10, 50, sample)
        p300.blow_out(sample.top())
        p300.drop_tip()
