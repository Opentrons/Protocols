metadata = {
    'protocolName': 'BMDA - Dengue Protocol',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.8'
}


def run(ctx):

    # Load Labware
    reagents = ctx.load_labware('opentrons_24_aluminumblock_generic_2ml_screwcap', 7)
    pcr_plate = ctx.load_labware('opentrons_96_aluminumblock_generic_pcr_strip_200ul', 8)
    tiprack_200ul = ctx.load_labware('opentrons_96_filtertiprack_200ul', 1)
    tiprack_20ul = ctx.load_labware('opentrons_96_filtertiprack_20ul', 2)

    # Load Instruments
    p300 = ctx.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack_200ul])
    p20 = ctx.load_instrument('p20_single_gen2', 'left', tip_racks=[tiprack_20ul])

    # Get Sample Wells
    mm = reagents.wells()[0]
    components = reagents.wells()[12:]
    volumes = [51, 85, 51, 119, 136, 34, 34, 34, 34, 34, 34, 34]

    # Add Components to Master Mix
    p300.transfer(volumes, components, mm, new_tip='always')
    p300.pick_up_tip()
    p300.mix(20)
    p300.drop_tip()

    # Add Master Mix to 32 wells
    p20.transfer(20, mm, pcr_plate.wells()[:32], new_tip='once')
