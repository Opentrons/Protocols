metadata = {
    'protocolName': 'HPLC Dilution',
    'author': 'Nick Diehl <ndiehl@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.12'
}


def run(ctx):

    num_samples = get_values(  # noqa: F821
        'num_samples')

    tuberacks_50 = [
        ctx.load_labware('opentrons_6_tuberack_falcon_50ml_conical', slot)
        for slot in ['1', '4', '7', '2', '5', '8']]
    tuberacks_hplc = [
        ctx.load_labware(
            'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', slot)
        for slot in ['3', '6', '9']]
    tiprack = [ctx.load_labware('opentrons_96_tiprack_1000ul', '10')]
    p1000l, p1000r = [
        ctx.load_instrument('p1000_single_gen2', mount, tip_racks=tiprack)
        for mount in ['left', 'right']]

    samples = [
        well for rack in tuberacks_50 for well in rack.wells()][:num_samples]
