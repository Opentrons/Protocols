from opentrons import protocol_api
from opentrons import types
from opentrons.protocol_api.labware import OutOfTipsError


metadata = {
    'protocolName': 'Normalization from Eppendorf tubes with a \
single-channel pipette',
    'author': 'Andrew Sum',
    'source': 'Breakthrough Genomics',
    'apiLevel': '2.12'
}


def run(ctx: protocol_api.ProtocolContext):
    [p300_mount, p20_mount, res_type] = get_values(  # noqa: F821
        "p300_mount", "p20_mount", "res_type")

    ctx.set_rail_lights(True)

    filepath = '/var/lib/jupyter/notebooks/test.csv'
    my_csv = pd.read_csv(filepath)
    volumes = [int(val) for val in my_csv.Volume._ndarray_values]
    volumes_water = [50 - n for n in volumes]
    num_samples = len(volumes)

    # create labware
    labware_tempmod = "thermofisher_96_well_pcrplate_200_aluminumblock"
    labware_tempmod2 = "opentrons_24_aluminumblock_nest_1.5ml_snapcap"

    temp2 = ctx.load_module('Temperature Module', '1')
    sample_plate = temp2.load_labware(
        labware_tempmod2,
        f'{num_samples} RNA samples in 1.5ml eppendorf tubes')

    temp = ctx.load_module('Temperature Module', '4')
    normalized_plate = temp.load_labware(
        labware_tempmod, 'Thermo PCR plate for normalized samples')

    reservoir = ctx.load_labware(res_type, '2')
    water = reservoir.wells()[5]

    tips300 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '10')]
    tips20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', '11')]

    p300 = ctx.load_instrument('p300_single_gen2', 'right', tip_racks=tips300)
    p20 = ctx.load_instrument('p20_single_gen2', 'left', tip_racks=tips20)

    def pick_up(pip):
        try:
            pip.pick_up_tip()
        except OutOfTipsError:
            ctx.pause("Please refill tip boxes")
            pip.reset_tipracks()
            pip.pick_up_tip()

    ctx.comment("Sample volumes: {}".format(volumes))
    ctx.comment("Water volumes: {}".format(volumes_water))

    pick_up(p20)
    pick_up(p300)

    for i, vol in enumerate(volumes_water):
        if vol != 0:
            if vol > 20:
                pipette = p300
            else:
                pipette = p20
        pipette.aspirate(vol, water.bottom(2))
        pipette.move_to(
         water.top(-2).move(types.Point(x=water.length / 2, y=0, z=0)))
        pipette.move_to(water.top())
        pipette.dispense(vol, normalized_plate.wells()[i])
        pipette.blow_out()

    p20.drop_tip()
    p300.drop_tip()

    for i, vol in enumerate(volumes):
        pipette = p20 if vol <= 20 else p300
        if not pipette.has_tip:
            pick_up(pipette)
        if vol != 0:
            # aspirate smaller volumes at lower position in the tube
            if vol > 26:
                loc = -0.2
            else:
                loc = 0.3

            # bring pipette high to avoid crashing with tube caps ]
            pipette.move_to(sample_plate.wells()[i].top(25))
            pipette.aspirate(vol, sample_plate.wells()[i].bottom(loc),
                             rate=0.8)
            pipette.move_to(sample_plate.wells()[i].top(25))
            pipette.dispense(vol, normalized_plate.wells()[i])
            pipette.blow_out()

        pipette.drop_tip()
