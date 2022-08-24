import math
from opentrons.types import Point

metadata = {
    'title': 'NGS Library Prep - Protocol 1',
    'author': 'Nick Diehl <ndiehl@opentrons.com',
    'apiLevel': '2.11'
}


def run(ctx):

    [num_samples_1, num_samples_2, pipette_p20, pipette_p300, mount_p20,
     mount_p300] = get_values(  # noqa: F821
        'num_samples_1', 'num_samples_2', 'pipette_p20', 'pipette_p300',
        'mount_p20', 'mount_p300')

    num_samples = num_samples_1*num_samples_2
    time_mag_incubation = 2.0
    z_offset = 3.0
    x_offset_ratio = 0.7
    height_engage = 7.0

    # labware
    plate = ctx.load_labware('kingfisher_96_deepwell_plate_2ml', '1',
                             'wellplate')
    reservoir = ctx.load_labware('agilent_3_reservoir_95ml', '2',
                                 'reservoir')
    magdeck = ctx.load_module('magnetic module gen2', '3')
    mag_plate = magdeck.load_labware('kingfisher_96_deepwell_plate_2ml')
    tipracks20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', '4')]
    tipracks200 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '5')]
    tuberack = ctx.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '9',
        '1.5ml tuberack')
    shake_plate = ctx.load_labware('kingfisher_96_deepwell_plate_2ml', '10',
                                   'Bioshake plate')
    beads_sample_1 = tuberack.wells()[:num_samples_2]

    # pipettes
    p20 = ctx.load_instrument(pipette_p20, mount_p20, tip_racks=tipracks20)
    p300 = ctx.load_instrument(pipette_p300, mount_p300, tip_racks=tipracks200)

    # reagents
    buffer1 = reservoir.wells()[0]
    buffer2 = reservoir.wells()[1]
    waste = reservoir.wells()[2].top()

    mm_tube = tuberack.wells()[0]
    water = tuberack.wells()[1]
    buffer3 = tuberack.wells()[2]
    buffer4 = tuberack.wells()[3]
    primer1 = tuberack.wells()[4]
    primer4 = tuberack.wells()[5]

    def pick_up(pip=p20, channels=p20.channels):
        def look():
            # iterate and look for required number of consecutive tips
            for rack in pip.tip_racks:
                for col in rack.columns():
                    counter = 0
                    for well in col[::-1]:
                        if well.has_tip:
                            counter += 1
                        else:
                            counter = 0
                        if counter == channels:
                            pip.pick_up_tip(well)
                            return True
            return False

        eval_pickup = look()
        if eval_pickup:
            return
        else:
            # refill rack if no tips available
            ctx.pause(f'Refill {pip} tipracks before resuming.')
            pip.reset_tipracks()
            look()

    index_ref_list = [well for row in mag_plate.rows() for well in row]

    def wash(wells, reagent, vol_initial, vol_wash, wash_reps):

        def bead_mix(vol, reps, well, side):
            bead_loc = well.bottom().move(Point(
                x=side*well.diameter/2*x_offset_ratio, z=z_offset))
            for _ in range(reps):
                p300.aspirate(vol, well.bottom(1))
                p300.dispense(vol, bead_loc)

        # remove initial volume
        magdeck.engage(height_engage)
        ctx.delay(minutes=time_mag_incubation, msg=f'Beads separating for \
{time_mag_incubation} minutes.')
        for well in wells:
            if not p300.has_tip:
                pick_up(p300, 1)
            p300.transfer(vol_initial, well.bottom(1), waste, new_tip='never',
                          rate=0.5)
            p300.drop_tip()

        for _ in range(wash_reps):
            magdeck.disengage()
            for well in wells:
                side = -1 if index_ref_list.index(well) % 2 == 0 else 1
                pick_up(p300, 1)
                p300.transfer(vol_wash, reagent, well.top(-1), new_tip='never')
                p300.dispense(vol_wash, well.bottom(1))
                bead_mix(vol_wash*0.8, 10, well, side)
                p300.drop_tip()

            magdeck.engage(height_engage)
            ctx.delay(minutes=time_mag_incubation, msg=f'Beads separating for \
{time_mag_incubation} minutes.')

        for well in wells:
            pick_up(p300, 1)
            p300.transfer(vol_wash, well.bottom(1), waste, new_tip='never',
                          rate=0.5)
            p300.drop_tip()

        magdeck.disengage()

    """ prep of beads for incubation 1 """

    beads_vol = num_samples*3*20
    wash_well_1 = mag_plate.wells()[0]
    pick_up(p300, 1)
    p300.transfer(beads_vol, beads_sample_1, wash_well_1, new_tip='never')
    wash([wash_well_1], buffer1, beads_vol, 500, 2)

    pick_up(p300, 1)
    p300.transfer(beads_vol, buffer1, wash_well_1, new_tip='never',
                  mix_after=(10, 200))
    p300.drop_tip()

    buffer3_vol = num_samples*3*5
    pick_up(p300, 1)
    p300.transfer(buffer3_vol, buffer3, wash_well_1, new_tip='never')

    ctx.pause('Shake for 30 minutes at RT')

    wash([wash_well_1], buffer1, 90, 500, 2)

    pick_up(p300, 1)
    p300.transfer(910, buffer2, wash_well_1, new_tip='never',
                  mix_after=(10, buffer3_vol*0.8))
    p300.distribute(50, wash_well_1,
                    [well for row in plate.rows()[2:5] for well in row],
                    new_tip='never')
    p300.drop_tip()

    """ prep of beads for incubation 2 """

    beads_vol = 150
    wash_well_2 = mag_plate.wells()[1]
    pick_up(p300, 1)
    p300.transfer(beads_vol, beads_sample_1, wash_well_2, new_tip='never')
    wash([wash_well_2], buffer1, beads_vol, 500, 2)

    pick_up(p300, 1)
    p300.transfer(beads_vol, buffer1, wash_well_2, new_tip='never',
                  mix_after=(10, beads_vol*0.8))
    split_dests = mag_plate.rows()[1][:num_samples_2]
    p300.distribute(50, wash_well_2, split_dests, new_tip='never')
    p300.drop_tip()

    ctx.pause('Add samples type 2 to row B of magnetic plate. Shake for 30 \
minutes at 4C and 500RPM.')

    wash(split_dests, buffer1, 50, 500, 1)

    for s in split_dests:
        pick_up(p300, 1)
        p300.transfer(100, buffer1, s, new_tip='never',
                      mix_after=(10, 100*0.8))
        p300.drop_tip()

    for s in split_dests:
        pick_up(p20, 1)
        p20.transfer(10, buffer3, s, new_tip='never',
                     mix_after=(10, 20))
        p20.drop_tip()

    ctx.pause('Shake for 10 at 4C and 500RPM.')

    wash(split_dests, buffer1, 110, 500, 2)

    pick_up(p300, 1)
    p300.transfer(610, buffer2, wash_well_2, new_tip='never',
                  mix_after=(10, 200))
    p300.distribute(50, wash_well_1,
                    [well for row in shake_plate.rows()[2:5] for well in row],
                    new_tip='never')
    p300.drop_tip()

    # plate prep for incubation 1+2 (MM)
    num_samples_mm_creation = num_samples*3+3+1  # accounts for overage

    # add all constant reagents to each mix tube
    vol_water_mm = 16.7*num_samples_mm_creation
    vol_buffer3_mm = 5*num_samples_mm_creation
    vol_buffer4_mm = 2.5*num_samples_mm_creation
    vol_primer1_mm = 0.4*num_samples_mm_creation
    vol_primer4_mm = 0.4*num_samples_mm_creation

    for reagent, vol in zip(
            [water, buffer3, buffer4, primer1, primer4],
            [vol_water_mm, vol_buffer3_mm, vol_buffer4_mm, vol_primer1_mm,
             vol_primer4_mm]):
        pip = p300 if vol > 20 else p20
        tip_capacity = pip.tip_racks[0].wells()[0].max_volume
        num_transfers = math.ceil(vol/tip_capacity)
        vol_per_transfer = vol/num_transfers
        pick_up(pip, 1)
        for _ in range(num_transfers):
            pip.aspirate(vol_per_transfer, reagent)
            pip.dispense(vol_per_transfer, mm_tube.bottom(5))
        pip.drop_tip()
