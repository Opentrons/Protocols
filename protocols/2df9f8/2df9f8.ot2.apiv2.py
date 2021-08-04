"""Protocol."""
metadata = {
    'protocolName': 'Plate Filling Heat Inactivated Covid Samples for PCR',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.7'
}


def run(ctx):
    """Protocol."""
    [num_samp, plate, m20_mount] = get_values(  # noqa: F821
        'num_samp', 'plate', 'm20_mount')

    if not 1 <= num_samp <= 94:
        raise Exception("Enter a number of samples between 1-94")

    # load labware
    plate = ctx.load_labware(plate, '4')
    tiprack = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
               for slot in ['5', '6']]
    tuberacks = [ctx.load_labware(
        'samples_24_tuberack_1500ul', slot)
        for slot in ['7', '8', '10', '11']]
    reagent_rack = ctx.load_labware(
        'mastermix_24_tuberack_2000ul', 1)

    # load instrument
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount, tip_racks=tiprack)

    # multi as single channel
    num_chan_per_pickup = 1  # (only pickup tips on front-most channel)
    tips_ordered = [
        tip for rack in tiprack
        for row in rack.rows()[
            len(rack.rows())-num_chan_per_pickup::-1*num_chan_per_pickup]
        for tip in row]

    tip_count = 0

    def pick_up():
        nonlocal tip_count
        m20.pick_up_tip(tips_ordered[tip_count])
        tip_count += 1

    # protocol
    sample_tubes = [tube for rack in tuberacks
                    for row in rack.rows()
                    for tube in row][:num_samp]
    negative_ctrl = reagent_rack.rows()[0][0]
    positive_ctrl = reagent_rack.rows()[0][1]
    ctrls = [negative_ctrl, positive_ctrl]
    mastermix = reagent_rack.rows()[0][5]

    plate_wells = [well for row in plate.rows() for well in row]

    # distribute controls, mastermix
    airgap = 5
    for s, d in zip(ctrls, plate.rows()[0]):
        pick_up()
        m20.aspirate(5, s)
        m20.air_gap(airgap)
        m20.dispense(5+airgap, d)
        m20.blow_out()
        m20.drop_tip()

    pick_up()
    for d in plate_wells[:num_samp+2]:
        m20.aspirate(15, mastermix)
        m20.dispense(15, d.top())
        m20.blow_out()
    m20.drop_tip()

    # distribute sample
    for s, d in zip(sample_tubes, plate_wells[2:]):
        pick_up()
        m20.aspirate(5, s)
        m20.air_gap(airgap)
        m20.dispense(5+airgap, d)
        m20.mix(5, 17, d)
        m20.blow_out()
        m20.drop_tip()
