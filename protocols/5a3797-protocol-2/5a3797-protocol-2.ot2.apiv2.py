metadata = {
    'protocolName': 'Protocol 2 - PCR setup',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.8'
}


def run(ctx):

    [m20_mount] = get_values(  # noqa: F821
        "m20_mount")

    # Load Labware
    tipracks = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
                for slot in range(1, 3)]
    mastermix = ctx.load_labware('nest_12_reservoir_15ml', 7)
    sample_plate = ctx.load_labware('kingfisher_96_deepwell_plate_2ml', 4)
    pcr_plate = ctx.load_labware(
                'thermofishermicroampfast96well0.1_96_wellplate_100ul', 5)

    # Load Pipette
    m20 = ctx.load_instrument('p20_multi_gen2', 'left', tip_racks=tipracks)

    # Aliquot 15uL of Mastermix
    m20.transfer(15, mastermix.wells(), pcr_plate.wells())

    # Aliquot 10 uL of Sample
    m20.transfer(10, sample_plate.wells(), pcr_plate.wells(), new_tip='always')
