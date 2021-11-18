import itertools
from opentrons.types import Point

metadata = {
    'protocolName': 'SuperScript III: qRT-PCR Prep with CSV File',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def get_values(*names):
    import json
    _all_values = json.loads("""{ "num_col":12,
                                    "incubation_time":3,
                                  "m300_mount":"left",
                                  "p300_mount":"right"}""")
    return [_all_values[n] for n in names]


def run(ctx):

    [num_col, incubation_time,
        m300_mount, p300_mount] = get_values(  # noqa: F821
        "num_col", "incubation_time",
            "m300_mount", "p300_mount")

    num_col = int(num_col)

    # load labware
    mag_mod = ctx.load_module('magnetic module gen2', '3')
    mag_plate = mag_mod.load_labware('storplate_96_wellplate_500ul')
    sample_racks = [ctx.load_labware(
                    'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap',
                    slot, label='tuberack') for slot in ['4', '1', '5', '2']]
    reagent_res = ctx.load_labware('nest_12_reservoir_15ml', '6')
    waste_res = ctx.load_labware('nest_1_reservoir_195ml', '11')
    tipracks = [ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
                for slot in ['7', '8', '9', '10']]

    # load instrument
    m300 = ctx.load_instrument('p300_multi_gen2',
                               m300_mount,
                               tip_racks=tipracks)
    p300 = ctx.load_instrument('p300_single_gen2',
                               p300_mount,
                               tip_racks=tipracks)

    tips = [tip for rack in tipracks[:3] for tip in rack.wells()]
    tips_return = [tip for tip in tipracks[3].wells()]
    tipcount = 0
    tipcount_return = 0

    def pick_up(pip):
        nonlocal tipcount
        pip.pick_up_tip(tips[tipcount])
        if pip.type == "single":
            tipcount += 1
        elif pip.type == "multi":
            tipcount += 8

    def pick_up_return(pip):
        nonlocal tipcount_return
        pip.pick_up_tip(tips_return[tipcount_return])
        if pip.type == "single":
            tipcount_return += 1
        elif pip.type == "multi":
            tipcount_return += 8

    # reagent
    reagent_A = reagent_res.wells()[0]
    reagent_B = reagent_res.wells()[1]
    reagent_C = reagent_res.wells()[2]
    waste = waste_res.wells()[0]

    # functions
    def remove_supernat(vol, loc, index):
        side = -1 if index % 2 == 0 else 1
        aspirate_loc = loc.bottom(z=1).move(
                        Point(x=(loc.diameter/2-2)*side))
        m300.transfer(vol, aspirate_loc, waste, new_tip='never')

    # protocol
    tube_map_double_nest = [
                  [sample_racks[j].columns()[i]+sample_racks[j+1].columns()[i]
                   for i in range(len(sample_racks[0].columns()))]
                  for j in range(0, 4, 2)
                  ]
    tube_map_nest = list(itertools.chain.from_iterable(tube_map_double_nest))
    full_tube_map = list(itertools.chain.from_iterable(
                         tube_map_nest))[:num_col*8]
    plate_cols = mag_plate.rows()[0][:num_col]

    ctx.comment('\n\nAdding Reagent B to Plate\n')
    pick_up(m300)
    for col in plate_cols:
        m300.aspirate(200, reagent_B)
        m300.dispense(200, col)
    m300.drop_tip()

    ctx.comment('\n\nMoving Sample to Plate\n')
    for tube, well in zip(full_tube_map, mag_plate.wells()):
        pick_up_return(p300)
        p300.aspirate(100, tube)
        p300.dispense(100, well)
        p300.return_tip()
    tipcount_return = 0

    ctx.comment('\n\nMixing Samples and Reagent B\n')
    for col in plate_cols:
        pick_up_return(m300)
        m300.mix(10, 200, col)
        m300.return_tip()
    tipcount_return = 0

    ctx.comment('\n\nEngage Magnet with Incubation Time\n')
    mag_mod.engage(height_from_base=13.6)
    ctx.delay(minutes=incubation_time)

    ctx.comment('\n\nRemoving Supernatant\n')
    for i, col in enumerate(plate_cols):
        pick_up_return(m300)
        remove_supernat(400, col, i)
        m300.return_tip()
    tipcount_return = 0

    ctx.comment('\n\nAdding Reagent A to Plate\n')
    pick_up(m300)
    for col in plate_cols:
        m300.transfer(400, reagent_A, col.top(), new_tip='never')
    m300.drop_tip()

    ctx.comment('\n\nIncubation\n')
    ctx.delay(minutes=incubation_time)

    ctx.comment('\n\nRemoving Supernatant\n')
    for i, col in enumerate(plate_cols):
        pick_up_return(m300)
        remove_supernat(400, col, i)
        m300.return_tip()

    ctx.comment('\n\nIncubation and Disengage Magnet\n')
    ctx.delay(minutes=incubation_time)
    mag_mod.disengage()

    ctx.comment('\n\nAdding Reagent C to Plate\n')
    for col in plate_cols:
        pick_up(m300)
        m300.transfer(100, reagent_C, col.top(),
                      new_tip='never',
                      mix_after=(3, 80))
        m300.drop_tip()

    ctx.comment('\n\nIncubate, Magnet, Incubate\n')
    ctx.delay(minutes=incubation_time)
    mag_mod.engage(height_from_base=13.6)
    ctx.delay(minutes=incubation_time)
    mag_mod.disengage()
