metadata = {
    'protocolName': 'Vitrolife Plate Prep',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.10'
}


def run(ctx):

    # Load Labware

    dish = ctx.load_labware('vitrolife_culture_dish', 1)
    tipracks_200ul = ctx.load_labware('opentrons_96_filtertiprack_200ul', 2)
    tipracks_1000ul = ctx.load_labware('opentrons_96_filtertiprack_1000ul', 3)
    tuberack = ctx.load_labware('opentrons_6_tuberack_falcon_50ml_conical', 4)

    # Load Pipettes

    p300 = ctx.load_instrument('p300_single_gen2', 'left',
                               tip_racks=[tipracks_200ul])
    p1000 = ctx.load_instrument('p1000_single_gen2', 'right',
                                tip_racks=[tipracks_1000ul])

    # Helper Functions
    def change_flow_rates(pip, asp_speed, disp_speed):
        pip.flow_rate.aspirate = asp_speed
        pip.flow_rate.dispense = disp_speed

    def reset_flow_rates(pip):
        if pip.name == 'p300_single_gen2':
            pip.flow_rate.aspirate = 92.86
            pip.flow_rate.dispense = 92.86
        else:
            pip.flow_rate.aspirate = 274.7
            pip.flow_rate.dispense = 274.7

    # Reagents

    media = tuberack['A1']
    oil_1 = tuberack['B1']

    # Sample Wells

    wells = []
    for i, row in enumerate(dish.rows()):
        if i % 2 == 0:
            for well in row:
                wells.append(well)
        else:
            for well in row[::-1]:
                wells.append(well)

    oil_loc = dish['D1']

    # Protocol Steps

    # Step 1
    p300.distribute(20, media, wells, new_tip='once')
    # Step 2
    p1000.pick_up_tip()
    for i in range(5):
        reset_flow_rates(p1000)
        if i == 0:
            change_flow_rates(p1000, 200, 200)
        p1000.aspirate(1000, oil_1)
        p1000.dispense(1000, oil_loc)
        ctx.delay(seconds=2)
        p1000.blow_out()
    p1000.drop_tip()
