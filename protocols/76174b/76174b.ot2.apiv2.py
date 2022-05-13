from opentrons.protocol_api.labware import OutOfTipsError

metadata = {
    'protocolName': '''Perkin Elmer AlphaLISA''',
    'author': 'Steve Plonk <protocols@opentrons.com>',
    'apiLevel': '2.11'
}


def run(ctx):

    # get parameter values from json above
    [count_plates] = get_values(  # noqa: F821
      'count_plates')

    ctx.set_rail_lights(True)

    if not 1 <= count_plates <= 2:
        raise Exception('Count of 384-well plates must be 1 or 2.')

    # helper functions

    # notify user to replenish tips
    def pick_up_or_refill(pip):
        try:
            pip.pick_up_tip()
        except OutOfTipsError:
            ctx.pause(
             """Please Refill the {} Tip Boxes
             and Empty the Tip Waste""".format(pip))
            pip.reset_tipracks()
            pip.pick_up_tip()

    # yield list chunks of length n
    def create_chunks(list_name, n):
        for i in range(0, len(list_name), n):
            yield list_name[i:i+n]

    # tips, p20 multi
    tips20 = [ctx.load_labware(
     "opentrons_96_tiprack_20ul", str(slot)) for slot in [4, 7, 8, 9]]
    p20m = ctx.load_instrument(
        "p20_multi_gen2", 'left', tip_racks=tips20)

    optiplates = [
     ctx.load_labware(
      'perkinelmer_384_wellplate_105ul', str(
       slot), name) for slot, name in zip([1, 2][:count_plates],
                                          ['OptiPlate 1', 'OptiPlate 2']
                                          [:count_plates])]

    serialdilutions = ctx.load_labware(
     'corning_96_wellplate_320ul', '3', 'Sample Serial Dilutions')

    ligandplate = ctx.load_labware(
     'corning_96_wellplate_320ul', '5', 'Ligands')
    ligands = ligandplate.columns()[:count_plates]

    reagents = ctx.load_labware(
     'corning_96_wellplate_320ul', '6', 'Anti-Ligand, Acceptor, Donor')
    [antiligand, acceptor, donor] = [
     chunk for chunk in [*create_chunks(reagents.columns(), count_plates)][:3]]

    for item, location in zip(
     ['receptors', 'samples', 'ligands', 'anti-ligand', 'acceptor', 'donor'],
     [optiplates, serialdilutions, ligands, antiligand, acceptor, donor]):
        ctx.comment("\nPlace {0} in {1}\n".format(item, location))

    ctx.comment("Transferring 8 uL Sample Serial Dilution to OptiPlate 1")
    for chunk_index in [0, 1]:
        for row in optiplates[0].rows()[:2]:

            for source, dest in zip(serialdilutions.rows()[0],
                                    [*create_chunks(row, 12)][chunk_index]):

                pick_up_or_refill(p20m)
                p20m.aspirate(8, source.bottom(1))
                p20m.dispense(8, dest.bottom(1))
                p20m.drop_tip()

    ctx.comment("Transferring 4 uL Ligand to OptiPlates")
    for index, plate in enumerate(optiplates):
        for row in plate.rows()[:2]:
            for well in row:
                pick_up_or_refill(p20m)
                p20m.aspirate(4, ligands[index][0].bottom(1))
                p20m.dispense(4, well.bottom(1))
                p20m.drop_tip()

    ctx.pause("Robot paused. Resume when ready.")

    ctx.comment("Transferring 4 uL anti-Ligand to OptiPlates")
    for index, plate in enumerate(optiplates):
        for row in plate.rows()[:2]:
            for well in row:
                pick_up_or_refill(p20m)
                p20m.aspirate(4, antiligand[index][0].bottom(1))
                p20m.dispense(4, well.bottom(1))
                p20m.drop_tip()

    ctx.comment("Transferring 4 uL acceptor to OptiPlates")
    for index, plate in enumerate(optiplates):
        for row in plate.rows()[:2]:
            for well in row:
                pick_up_or_refill(p20m)
                p20m.aspirate(4, acceptor[index][0].bottom(1))
                p20m.dispense(4, well.bottom(1))
                p20m.drop_tip()

    ctx.pause("Robot paused. Resume when ready.")

    ctx.comment("Transferring 4 uL donor to OptiPlates")
    for index, plate in enumerate(optiplates):
        for row in plate.rows()[:2]:
            for well in row:
                pick_up_or_refill(p20m)
                p20m.aspirate(4, donor[index][0].bottom(1))
                p20m.dispense(4, well.bottom(1))
                p20m.drop_tip()

    ctx.comment(
     '''Process Complete.''')
