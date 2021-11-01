metadata = {
    'protocolName': 'Normalization',
    'author': 'Nick <ndiehl@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    dil_csv_1, dil_csv_2, p300_mount, p20_mount = get_values(  # noqa: F821
        'dil_csv_1', 'dil_csv_2', 'p300_mount', 'p20_mount')

    tuberacks = [
        ctx.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', slot,
            f'sample tuberack {i+1}')
        for i, slot in enumerate(['4', '5'])]
    dil_plate_1 = ctx.load_labware(
        'microampenduraplate_96_aluminumblock_200ul', '1',
        'dilution plate 1')
    dil_plate_2 = ctx.load_labware(
        'microampenduraplate_96_aluminumblock_200ul', '2',
        'dilution plate 2')
    final_plate = ctx.load_labware(
        'microampenduraplate_96_aluminumblock_200ul', '3', 'final plate')

    p300 = ctx.load_instrument('p300_single_gen2', p300_mount, tip_racks=[])
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=[])

    sample_sources = [
        well for tuberack in tuberacks for well in tuberack.wells()]
    dils_1 = dil_plate_1.wells()
    dils_2 = dil_plate_2.wells()

    def dilute(csv, sources, dests):
