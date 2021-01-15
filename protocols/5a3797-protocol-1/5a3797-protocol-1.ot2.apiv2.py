metadata = {
    'protocolName': 'Protocol 1 - Washing Aliquot',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.8'
}


def run(ctx):

    [m300_mount] = get_values(  # noqa: F821
        "m300_mount")

    # Load Labware
    tipracks = ctx.load_labware('opentrons_96_filtertiprack_200ul', 1)
    wash_1 = ctx.load_labware('nest_12_reservoir_15ml', 7)
    wash_2 = ctx.load_labware('nest_12_reservoir_15ml', 8)
    elution = ctx.load_labware('nest_12_reservoir_15ml', 9)
    dw_plate_wash_1 = ctx.load_labware('kingfisher_96_deepwell_plate_2ml', 4)
    dw_plate_wash_2 = ctx.load_labware('kingfisher_96_deepwell_plate_2ml', 5)
    dw_plate_elution = ctx.load_labware('kingfisher_96_deepwell_plate_2ml', 6)

    # Load Pipette
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=[tipracks])

    # Aliquot 500uL of Wash 1
    m300.transfer(500, wash_1.wells(), dw_plate_wash_1.wells())

    # Aliquot 1000uL of Wash 2
    m300.transfer(1000, wash_2.wells(), dw_plate_wash_2.wells())

    # Aliquot 50uL of Elution
    m300.transfer(50, elution.wells(), dw_plate_elution.wells())
