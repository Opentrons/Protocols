metadata = {
    'protocolName': 'Sample Transfer to 96 Well-Plate',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def get_values(*names):
    import json
    _all_values = json.loads("""{"num_samp":4, "p1000_mount":"left", "delay": 5}""")
    return [_all_values[n] for n in names]

def run(ctx):

    [num_samp, delay, p1000_mount] = get_values(  # noqa: F821
             "num_samp", "delay", "p1000_mount")

    if not 1 <= num_samp <= 96:
        raise Exception("Enter a sample number between 1-96")

    # load labware
    tuberack_96 = [ctx.load_labware('6x4_0.6inch_t6', slot, label='Tuberack')
                   for slot in ['1', '4', '7', '10']]
    plate = ctx.load_labware('microamp_96_wellplate_100ul', '2')
    tiprack = ctx.load_labware('opentrons_96_tiprack_1000ul', '5')

    # load instrument
    p1000 = ctx.load_instrument('p1000_single_gen2',
                                p1000_mount, tip_racks=[tiprack])

    tubes = [tube for tuberack in tuberack_96 for tube in tuberack.wells()]

    # protocol
    for samp, dest in zip(tubes, plate.wells()):
        p1000.pick_up_tip()
        p1000.aspirate(200, samp)
        ctx.delay(seconds=delay)
        p1000.dispense(200, dest)
        p1000.drop_tip()
