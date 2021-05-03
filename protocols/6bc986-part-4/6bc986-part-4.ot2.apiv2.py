import math
from opentrons import types

metadata = {
    'protocolName': '3. Master Mix only-edit',
    'author': 'Steve Plonk <protocols@opentrons.com>',
    'apiLevel': '2.9'
}


def run(ctx):

    # get parameter values from json above
    [clearance_aspirate, clearance_dispense, sample_count
     ] = get_values(  # noqa: F821
      'clearance_aspirate', 'clearance_dispense', 'sample_count')

    num_cols = math.ceil(sample_count / 8)
    tip_max = 50

    # p50 multi, p20 multi and tips
    tips20 = [ctx.load_labware("opentrons_96_tiprack_20ul", '1')]
    tips300 = [ctx.load_labware("opentrons_96_tiprack_300ul", '4')]
    p20m = ctx.load_instrument(
        "p20_multi_gen2", 'right', tip_racks=tips20)
    p50m = ctx.load_instrument(
        "p50_multi", 'left', tip_racks=tips300)

    # thermo 96 well plate on slot 6
    dna_template = ctx.load_labware("thermo_96_wellplate_200ul", '6')
    p20m.transfer(0, dna_template.wells_by_name()[
     'A1'], dna_template.wells_by_name()['A1'], trash=False)

    # usa plate on slot 3
    usa_plate = ctx.load_labware("usa_96_wellplate_200ul", '3')

    # aspir8 reservoir in slot 2 with ghost movement to reservoir
    reservoir = ctx.load_labware("aspir8_1_reservoir_taped", '2')

    # to distribute and blow out with control over location within the well
    def create_chunks(list_name, n):
        for i in range(0, len(list_name), n):
            yield list_name[i:i+n]

    def repeat_dispense(dist_vol, source, dest, max_asp=tip_max, disposal=0):
        for chunk in create_chunks(dest.columns()[
         :num_cols], math.floor((max_asp - disposal) / dist_vol)):
            if disposal > 0:
                p50m.aspirate(disposal, source)
            p50m.aspirate(dist_vol*len(chunk), source)
            for column in chunk:
                p50m.dispense(dist_vol, column[0].bottom(clearance_dispense))
            p50m.blow_out(source.move(types.Point(x=0, y=0, z=0)))

    # 20 ul master mix to two columns, blow out to bottom of reservoir, repeat
    p50m.pick_up_tip()
    repeat_dispense(20, reservoir.wells_by_name()[
     'A1'].bottom(clearance_aspirate), usa_plate, disposal=5)
    p50m.drop_tip()
