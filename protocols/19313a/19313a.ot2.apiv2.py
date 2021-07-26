import os
import csv
from opentrons.types import Point

metadata = {
    'protocolName': 'RNA Extraction with Magnetic Life',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.10'
}


def get_values(*names):
    import json
    _all_values = json.loads("""{"num_samp": 2,
    "reset_tipracks": true, "mix_reps1": 5, "mix_reps2": 5,
    "mix_reps_wash1": 5, "mix_reps_wash2": 5, "mix_reps_elution1": 5,
    "mix_reps_elution2": 5, "settling_1": 5, "settling_2": 5, "settling_3": 5,
    "settling_wash": 5, "settling_drying": 5, "settling_elution1": 5,
    "settling_elution2": 5, "wash1_vol": 150, "wash2_vol": 150,
    "elution_vol": 150, "asp_height":1, "length_from_side":2,
    "lysis_vol": 100, "move_vol": 100, "binding_buffer_vol": 100,
    "final_vol": 100,
    "heating_module_temp": 65, "mag_height_1": 4.5,
    "waste_water_mode": true, "p300_mount":"left"}""")
    return [_all_values[n] for n in names]


def run(ctx):

    [num_samp, reset_tipracks, mix_reps1, mix_reps2, mix_reps_wash1,
     mix_reps_wash2, mix_reps_elution1, mix_reps_elution2, settling_1,
     settling_2, settling_3, settling_wash, settling_drying, settling_elution1,
     settling_elution2, wash1_vol, wash2_vol, elution_vol, lysis_vol, move_vol,
     binding_buffer_vol, final_vol, heating_module_temp, mag_height_1,
     waste_water_mode, asp_height, length_from_side,
     p300_mount] = get_values(  # noqa: F821
        "num_samp", "reset_tipracks", "mix_reps1", "mix_reps2",
        "mix_reps_wash1", "mix_reps_wash2", "mix_reps_elution1",
        "mix_reps_elution2", "settling_1", "settling_2", "settling_3",
        "settling_wash", "settling_drying", "settling_elution1",
        "settling_elution2", "wash1_vol", "wash2_vol", "elution_vol",
        "lysis_vol", "move_vol", "binding_buffer_vol", "final_vol",
        "heating_module_temp", "mag_height_1", "waste_water_mode",
        "asp_height", "length_from_side", "p300_mount")

    # if not 0 <= num_samp <= 4:
    #     raise Exception('Please enter a sample number between 1-4')

    # load labware
    mag_mod = ctx.load_module('magnetic module gen2', '7')
    mag_plate = mag_mod.load_labware(
        'nest_96_wellplate_2ml_deep', label='Mag Plate')
    reagent_tuberack = ctx.load_labware(
                'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', '4',
                label='Reagent Tuberack')
    waste_tuberack = ctx.load_labware(
                'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', '5',
                label='Waste Tuberack')
    tiprack300 = [ctx.load_labware('opentrons_96_tiprack_300ul', slot)
                  for slot in ['8', '9']]
    temp_mod = ctx.load_module('temperature module gen2', '10')
    temp_rack = temp_mod.load_labware(
        'opentrons_24_aluminumblock_nest_1.5ml_snapcap',
        label='Temperature tuberack')
    tiprack200 = ctx.load_labware('opentrons_96_filtertiprack_200ul', '11')

    # load instrument
    p300 = ctx.load_instrument('p300_single_gen2',
                               p300_mount,
                               tip_racks=tiprack300)

    # Tip tracking between runs
    if not ctx.is_simulating():
        file_path = '/data/csv/tiptracking.csv'
        file_dir = os.path.dirname(file_path)
        # check for file directory
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        # check for file; if not there, create initial tip count tracking
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as outfile:
                outfile.write("0, 0\n")

    tip_count_list = []
    if ctx.is_simulating():
        tip_count_list = [0, 0]
    elif reset_tipracks:
        tip_count_list = [0, 0]
    else:
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            tip_count_list = next(csv_reader)

    num_one = int(tip_count_list[0])
    num_two = int(tip_count_list[1])
    tips_300 = [tip for tiprack in tiprack300 for tip in tiprack.wells()]

    p300.starting_tip = tips_300[num_one]

    def pick_up300():
        try:
            p300.pick_up_tip()
        except ctx.labware.OutOfTipsError:
            ctx.pause("Replace all 300ul non-filter tip racks")
            p300.reset_tipracks()
            p300.pick_up_tip()

    filter_tip_count = num_two

    def pick_up_filter():
        nonlocal filter_tip_count
        try:
            p300.pick_up_tip(tiprack200.wells()[filter_tip_count])
            filter_tip_count += 1
        except filter_tip_count == 96:
            ctx.pause("Replace all 300ul non-filter tip racks")
            filter_tip_count = 0
            p300.pick_up_tip(tiprack200.wells()[filter_tip_count])

    # load reagents
    elution_buffer = reagent_tuberack.wells_by_name()['C2']
    binding_buffer = reagent_tuberack.wells_by_name()['A3']
    rps_wash_buffer = reagent_tuberack.wells_by_name()['A4']
    wash_buffer = reagent_tuberack.wells_by_name()['B3']
    samples = mag_plate.rows()[0][:12:3][:num_samp]
    samples_second_well = mag_plate.rows()[0][1:12:3][:num_samp]
    samples_third_well = mag_plate.rows()[0][2:12:3][:num_samp]
    waste = waste_tuberack.wells()[0]

    def remove_supernatant(vol, index, loc):
        side = -1 if index % 2 == 0 else 1
        aspirate_loc = loc.bottom(z=asp_height).move(
                Point(x=(loc.length/2-length_from_side)*side))
        p300.aspirate(vol, aspirate_loc)
        p300.dispense(vol, waste)
        p300.blow_out()

    # initialize temp mod and magnetic mod
    temp_mod.set_temperature(heating_module_temp)
    mag_mod.engage(height_from_base=mag_height_1)
    ctx.pause('''
                Temperature module at desired temperature,
                and magnetic module is enageged.
               Select "Resume" on the Opentrons app to begin the protocol.
               ''')

    if waste_water_mode:
        mag_mod.disengage()
        for sample in samples:
            pick_up_filter()
            p300.mix(mix_reps1, 80, sample)
            p300.touch_tip()
            p300.drop_tip()
        ctx.delay(minutes=settling_1)
        ctx.comment('\n\n\n')

        # binding
        for sample in samples:
            pick_up_filter()
            p300.aspirate(binding_buffer_vol, binding_buffer)
            p300.dispense(binding_buffer_vol, sample)
            p300.mix(mix_reps2, 180, sample)
            p300.touch_tip()
            p300.drop_tip()
        ctx.comment('\n\n\n')

        if not mag_mod.status == 'enaged':
            mag_mod.engage(height_from_base=mag_height_1)
        ctx.delay(minutes=settling_2)

        # remove 200ul of supernatant
        for i, sample in enumerate(samples):
            pick_up_filter()
            remove_supernatant(200, i, sample)
            p300.drop_tip()
    ctx.comment('\n\n\n')

    # remove storage buffer
    ctx.delay(minutes=settling_3)
    for sample in samples:
        pick_up300()
        for _ in range(5):
            p300.aspirate(300, sample)
            p300.dispense(300, waste.top(z=-3))
            p300.blow_out()
        p300.drop_tip()
    mag_mod.disengage()
    ctx.comment('\n\n\n')

    # RPS wash
    for i, sample in enumerate(samples):
        pick_up300()
        p300.aspirate(wash1_vol, rps_wash_buffer)
        p300.dispense(wash1_vol, sample)
        p300.mix(mix_reps_wash1)
        mag_mod.engage(height_from_base=mag_height_1)
        ctx.delay(minutes=settling_wash)
        remove_supernatant(300, i, sample)
        p300.blow_out()
        p300.drop_tip()
        mag_mod.disengage()
    ctx.comment('\n\n\n')

    # two washes
    ctx.comment('Two washes')
    for wash in range(2):
        for i, sample in enumerate(samples):
            pick_up300()
            p300.aspirate(wash2_vol, wash_buffer)
            p300.dispense(wash2_vol, sample)
            p300.mix(mix_reps_wash1, 300, sample)
            mag_mod.engage(height_from_base=mag_height_1)
            ctx.delay(minutes=settling_wash)
            remove_supernatant(300, i, sample)
            p300.drop_tip()
            mag_mod.disengage()
            ctx.comment('\n')
    ctx.comment('\n\n\n')

    # drying
    ctx.delay(minutes=settling_2)
    for i, sample in enumerate(samples):
        pick_up300()
        p300.aspirate(300, sample)
        p300.dispense(300, waste)
        p300.drop_tip()
    ctx.comment('\n\n\n')

    # elution
    for sample, samp_well2, samp_well3, dest in zip(samples,
                                                    samples_second_well,
                                                    samples_third_well,
                                                    temp_rack.rows()[0]):
        pick_up300()
        p300.aspirate(elution_vol, elution_buffer)
        p300.dispense(elution_vol, sample)
        p300.mix(mix_reps_elution1, 50, sample)
        p300.aspirate(move_vol, sample)
        p300.dispense(move_vol, dest)
        for _ in range(3):
            ctx.delay(minutes=settling_elution1)
            p300.mix(mix_reps_elution2, 200, dest)
        p300.aspirate(move_vol, dest)
        p300.dispense(move_vol, samp_well2)
        p300.blow_out()
        p300.drop_tip()
        mag_mod.engage(height_from_base=mag_height_1)
        ctx.delay(minutes=settling_elution2)
        pick_up_filter()
        p300.aspirate(final_vol, samp_well2)
        p300.dispense(final_vol, samp_well3)
        p300.drop_tip()
        mag_mod.disengage()
    ctx.comment('\n\n\n')

    # write updated tipcount to CSV
    new_tip_count = str(num_one)+", "+str(num_two)+"\n"
    if not ctx.is_simulating():
        with open(file_path, 'w') as outfile:
            outfile.write(new_tip_count)
