metadata = {
    'protocolName': 'Sample Prep MALDI spotting - Fresh Spiking',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [num_tubes, vol_plasma, vol_analyte,
     p20_mount, p1000_mount] = get_values(  # noqa: F821
        "num_tubes", "vol_plasma", "vol_analyte",
         "p20_mount", "p1000_mount")

    if not 1 <= num_tubes <= 10:
        raise Exception("Enter a number of tubes between 1-10")

    # load labware
    analyte_rack = ctx.load_labware(
                   'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', '1')
    final_rack = ctx.load_labware(
                 'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', '2')
    falcon_rack = ctx.load_labware(
                    'opentrons_15_tuberack_falcon_15ml_conical', '3')
    tiprack1000 = ctx.load_labware('opentrons_96_tiprack_1000ul', '4')
    tiprack20 = ctx.load_labware('opentrons_96_tiprack_20ul', '5')

    # load instrument
    p20 = ctx.load_instrument('p20_single_gen2',
                              p20_mount, tip_racks=[tiprack20])
    p1000 = ctx.load_instrument(
                'p1000_single_gen2', p1000_mount, tip_racks=[tiprack1000])

    # protocol
    plasma = falcon_rack.wells()[0]

    # add analyte
    for source, dest in zip(analyte_rack.wells()[:num_tubes],
                            final_rack.wells()):
        p20.pick_up_tip()
        p20.aspirate(vol_analyte, source)
        p20.dispense(vol_analyte, dest)
        p20.move_to(dest.top())
        p20.blow_out()
        p20.touch_tip()
        p20.drop_tip()

    # add plasma

    for tube in final_rack.wells()[:num_tubes]:
        p1000.pick_up_tip()
        p1000.aspirate(vol_plasma, plasma)
        p1000.dispense(vol_plasma, tube)
        p1000.mix(5, 0.7*(vol_plasma+vol_analyte), tube)
        p1000.move_to(tube.top())
        p1000.blow_out()
        p1000.drop_tip()
