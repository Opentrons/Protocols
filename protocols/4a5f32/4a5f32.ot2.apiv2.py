metadata = {
    'protocolName': 'Nucleic Acid Purification with Magnetic Beads',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.10'
}

def get_values(*names):
    import json
    _all_values = json.loads("""{"m300_mount":"left"}""")
    return [_all_values[n] for n in names]


def run(ctx):

    [m300_mount] = get_values(  # noqa: F821
        "m300_mount")

    # Load Labware
    waste = ctx.load_labware('starlab10ml24wellplate_24_wellplate_10000ul', 1,
                             'Waste Reservoir')
    tips300 = [ctx.load_labware('opentrons_96_tiprack_300ul',
                                slot) for slot in [2, 7, 8]]
    elution_plate = ctx.load_labware('4titude_96_wellplate_200ul', 3,
                                     'Elution Plate')
    mag_mod = ctx.load_module('magnetic module gen2', 4)
    mag_plate = mag_mod.load_labware('4titude_96_wellplate_200ul')
    reagents = ctx.load_labware('starlab_12_reservoir_22000ul', 5,
                                'Reagent Reservoir')

    # Load Pipette
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=tips300)

    # Tip Mapping
    reserved_tips = tips300[0].rows()[0]
    available_tips = [tips300[i].rows()[0] for i in range(1, 3)]
    available_tips = [tip for tips in available_tips for tip in tips]

    print(available_tips)

    # Implement Multiwell Volume Tracking