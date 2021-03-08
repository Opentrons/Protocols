import math
from opentrons.types import Point

metadata = {
    'protocolName': 'Slide Array Spotting',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    [num_plates, num_samples, num_slides, array_pattern, blot_dwell_time,
     slow_speed, sample_height, sample_dwell_time, slide_dwell_time,
     m300_mount] = get_values(  # noqa: F821
        'num_plates', 'num_samples', 'num_slides', 'array_pattern',
        'blot_dwell_time', 'slow_speed', 'sample_height', 'sample_dwell_time',
        'slide_dwell_time', 'm300_mount')

    # space for parameters
    num_plates = num_plates
    num_samples = num_samples
    num_slides = num_slides
    array_pattern = array_pattern
    blot_dwell_time = blot_dwell_time
    slow_speed = slow_speed
    sample_height = sample_height
    sample_dwell_time = sample_dwell_time
    slide_dwell_time = slide_dwell_time
    m300_mount = m300_mount

    sample_plates = [
        ctx.load_labware('eppendorf_96_wellplate_350ul', slot,
                         'sample plate ' + str(i+1))
        for i, slot in enumerate(['1', '3'][:num_plates])]
    slides = ctx.load_labware(
        'gracebiolabsflexwell_768_other_192x10ul_192x10ul_192x10ul_192x10ul',
        '2', 'slides')
    pin_wash_res = ctx.load_labware('axygen_4_reservoir_73000ul', '7',
                                    'pin wash reservoir')
    blot_res = ctx.load_labware('axygen_4_reservoir_73000ul', '8',
                                'blot reservoir')
    tiprack300 = [ctx.load_labware('opentrons_96_tiprack_300ul', '10')]
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=tiprack300)

    # setup samples
    num_cols = math.ceil(num_samples/8)
    if array_pattern == 1:
        slide_sets = [
            [well for set in [slides.rows()[row][i*8:i*8+8]
             for i in range(num_slides)] for well in set]
            for row in range(num_plates)]
    elif array_pattern == 2:
        slide_sets = [
            [well for i in range(num_slides)
             for col in slides.columns()[i*8+3*p:i*8+3+3*p]
             for well in col[:2]]
            for p in range(num_plates)]
    else:
        slide_sets = [
            [well for s in range(num_slides)
             for row in slides.rows()[p:4:2]
             for well in row[s*8+(p % 2):s*8+8:2]]
            for p in range(num_plates)]

    sample_sets = [plate.rows()[0][:num_cols] for plate in sample_plates]

    # wash and blot

    def wash_blot():
        for wash, blot in zip(pin_wash_res.wells(), blot_res.wells()):
            movement_locs = [
                wash.center().move(Point(x=side*5)) for side in [-1, 1]]
            m300.move_to(wash.center())
            for _ in range(5):
                for m in movement_locs:
                    m300.move_to(m)
            m300.move_to(wash.center())

            ctx.max_speeds['A'] = slow_speed
            ctx.max_speeds['Z'] = slow_speed
            m300.move_to(blot.top())
            m300.move_to(blot.bottom())
            ctx.delay(seconds=blot_dwell_time)

            del ctx.max_speeds['A']
            del ctx.max_speeds['Z']

    m300.pick_up_tip()
    wash_blot()

    for sample_set, slide_set in zip(sample_sets, slide_sets):
        for sample, slide_spot in zip(sample_set, slide_set):
            ctx.max_speeds['A'] = slow_speed
            ctx.max_speeds['Z'] = slow_speed
            m300.move_to(sample.bottom(sample_height))
            ctx.delay(seconds=sample_dwell_time)
            m300.move_to(slide_spot.bottom(0.1))
            ctx.delay(seconds=slide_dwell_time)
            del ctx.max_speeds['A']
            del ctx.max_speeds['Z']
            wash_blot()

    m300.return_tip()
