# flake8: noqa

metadata = {
    'protocolName': 'DYNABEADS FOR IP - 96 well: Part 1/2',
    'author': 'Boren Lin <boren.lin@opentrons.com>',
    'source': '',
    'apiLevel': '2.11'
}

########################

NUM_SAMPLES = 96
wash_volume = 200
wash_times = 3

total_cols = int(NUM_SAMPLES//8)
r1 = int(NUM_SAMPLES%8)
if r1 != 0: total_cols = total_cols + 1

#########################

def run(ctx):

    # load labware
    reagent_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '4', 'reagents')
    reagent_tube = ctx.load_labware('opentrons_15_tuberack_nest_15ml_conical', '5', 'reagents - stock')
    tiprack = ctx.load_labware('opentrons_96_tiprack_300ul', '7')

    # load pipette
    pip_single = ctx.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack])

    # liquids
    beads = reagent_plate.columns()[0]
    ab = reagent_plate.columns()[1]
    beads_stock = reagent_tube.rows()[0][0]
    ab_stock = reagent_tube.rows()[0][1]


    # protocol

    ctx.comment('\n\n\n~~~~~~~~MIXING AND TRANSFER BEADS ~~~~~~~~\n')
    pip_single.pick_up_tip()
    for i in range(total_cols):
        h = 5 + i * 3
        pip_single.mix(5, 250, beads_stock.bottom(z=h), rate = 5)
    for i in range(8):
         pip_single.transfer(total_cols*50,
                        beads_stock,
                        beads[i],
                        blow_out=True,
                        blowout_location='destination well',
                        new_tip='never',
                        mix_before=(5, 100),
                        )
    pip_single.drop_tip()
    ctx.comment('\n\n\n~~~~~~~~TRANSFER AB ~~~~~~~~\n')
    pip_single.pick_up_tip()
    for i in range(8):
         pip_single.transfer(total_cols*50,
                        ab_stock,
                        ab[i],
                        blow_out=True,
                        blowout_location='destination well',
                        new_tip='never',
                        )
    pip_single.drop_tip()
