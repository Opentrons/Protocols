import math


def get_values(*names):
    import json
    _all_values = json.loads("""{"m20_mount":"left",samples":384, "pcr_mix_vol":7.5, "sample_vol":5, "asp_height":1, "disp_height":1}""")
    return [_all_values[n] for n in names]


metadata = {
    'protocolName': 'Sample Plate Filling 96 Wells to 384 Well Plate',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    [m20_mount, samples, pcr_mix_vol, sample_vol, asp_height,
        disp_height] = get_values(  # noqa: F821
        "m20_mount", "samples", "pcr_mix_vol", "sample_vol",
        "asp_height", "disp_height")

    # Load Labware
    tipracks_20ul = [ctx.load_labware('opentrons_96_filtertiprack_20ul',
                                      slot) for slot in range(7, 12)]
    pcr_mix = ctx.load_labware('nest_12_reservoir_15ml', 6,
                               'PCR Mix Reservoir')['A1']
    pcr_plate = ctx.load_labware(
        'appliedbiosystems_microamp_optical_384_wellplate_30ul', 3,
        '384 Well PCR Plate')
    elution_plates = [ctx.load_labware('molgen_96_well_elution_plate',
                                       slot) for slot in [1, 2, 4, 5]]

    # Load Pipettes
    m20 = ctx.load_instrument('p20_multi_gen2', 'left',
                              tip_racks=tipracks_20ul)

    # Get columns
    columns = math.ceil(samples / 8)

    # Get sample and dest wells in correct order
    sample_wells = [well for i in range(4) for well in
                    elution_plates[i].rows()[0]][:columns]
    pcr_dests = [a for b in zip(pcr_plate.rows()[0],
                 pcr_plate.rows()[1]) for a in b][:columns]

    # Add RT-PCR Mix
    m20.pick_up_tip()
    for dest in pcr_dests:
        m20.transfer(pcr_mix_vol, pcr_mix, dest.bottom(disp_height),
                     new_tip='never')
    m20.drop_tip()

    # Add RNA Samples
    for source, dest in zip(sample_wells, pcr_dests):
        m20.transfer(sample_vol, source.bottom(asp_height),
                     dest.bottom(disp_height), new_tip='always',
                     mix_after=(5, 5))
