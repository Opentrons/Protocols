metadata = {
    'protocolName': 'FA Workflow',
    'author': 'Nick <ndiehl@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    dil_csv_1, desired_conc, p300_mount, p20_mount = get_values(  # noqa: F821
        'dil_csv_1', 'desired_conc', 'p300_mount', 'p20_mount')

    tempdeck1 = ctx.load_module('temperature module gen2', '1')
    tempdeck1.deactivate()
    dil_plate_final = tempdeck1.load_labware(
        'microampenduraplate_96_aluminumblock_200ul', 'dilution plate 2')
    dil_plate_1 = ctx.load_labware(
        'microampenduraplate_96_aluminumblock_200ul', '2',
        'dilution plate 1')
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', '3',
                                 'reagent reservoir')
    tempdeck2 = ctx.load_module('temperature module gen2', '4')
    tempdeck2.set_temperature(4)
    tuberacks = [
        ctx.load_labware(
            'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', slot,
            f'sample tuberack {i+1}')
        for i, slot in enumerate(['5', '6'])]
    tipracks200 = [
        ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
        for slot in ['7', '10']]
    tipracks20 = [
        ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
        for slot in ['8', '11']]

    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=tipracks200)
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount,
                              tip_racks=tipracks20)

    sample_sources = [
        well for tuberack in tuberacks for well in tuberack.wells()]
    water = reservoir.wells()[0]
    hs_dil = reservoir.wells()[1]
    blank_solution = reservoir.wells()[2]
    rna_ladder = tuberacks[1].wells_by_name()['A6']

    data = [
        [val.strip() for val in line.split(',')]
        for line in dil_csv_1.splitlines()
        if line and line.split(',')[0].strip()][1:]
    num_samples = len(data)

    # dilute 2x to 4µg/ml
    dils_1 = dil_plate_1.wells()[:num_samples]
    dils_2 = dil_plate_1.wells()[48:48+num_samples]  # use half of plate

    # pre-allocate water for dilution to 100µg/ml
    p300.pick_up_tip()
    for dil, line in zip(dils_1, data):
        conc = float(line[2])
        sample_vol = 10/conc
        dil_1_vol = 100 - sample_vol
        p300.transfer(dil_1_vol, water, dil, new_tip='never')

    # pre-allocate water for final desired dilution
    for well in dils_2:
        p300.transfer(100-desired_conc, water, well, new_tip='never')
    p300.drop_tip()

    # perform dilutions
    for sample, dil1, dil2, line in zip(sample_sources, dils_1, dils_2, data):
        conc = float(line[2])
        sample_vol = 10/conc
        p20.pick_up_tip()
        p20.transfer(sample_vol, sample, dil1, mix_after=(5, 20),
                     new_tip='never')
        p20.transfer(desired_conc, dil1, dil2, mix_after=(5, 20),
                     new_tip='never')
        p20.drop_tip()

    # determine transfer scheme depending on number of samples
    if 1 <= num_samples <= 15:
        dests = dil_plate_final.rows_by_name()['A'] + [
            dil_plate_final.wells_by_name()[well]
            for well in ['D1', 'D4', 'D7']]
        triplicates = [col[:3] for col in dil_plate_final.columns()] + [
            dil_plate_final.rows_by_name()['D'][i*3:(i+1)*3] for i in range(3)]
        triplicate_sets = triplicates[:num_samples]
        dils_final = dests[:num_samples]
        final_dest = dil_plate_final.wells_by_name()['D12']
        # final_set = dil_plate_final.rows_by_name()['D'][9:]
        blank_wells = [
            well for well in [
                well for row in dil_plate_final.rows()[:4] for well in row]
            if well not in [
                well for set in [*triplicate_sets, *[[final_dest]]]
                for well in set]]

    elif 15 < num_samples <= 31:
        dests = dil_plate_final.rows()['A'] + dil_plate_final.rows()['D'] + [
            dil_plate_final.wells_by_name()[well]
            for well in ['G1', 'G4', 'G7', 'G10', 'H1', 'H4', 'H7']]
        triplicates = [col[:3] for col in dil_plate_final.columns()] + [
            col[4:6] for col in dil_plate_final.columns()] + [
            dil_plate_final.rows_by_name()['G'][i*3:(i+1)*3]
                for i in range(4)] + [
            dil_plate_final.rows_by_name()['H'][i*3:(i+1)*3] for i in range(3)]
        triplicate_sets = triplicates[:num_samples]
        dils_final = dests[:num_samples]
        final_dest = dil_plate_final.wells_by_name()['H12']
        # final_set = dil_plate_final.rows_by_name()['H'][9:]
        blank_wells = [
            well for well in dil_plate_final.wells()
            if well not in [
                well for set in [*triplicate_sets, *[[final_dest]]]
                for well in set]]
    else:
        raise Exception(f'Invalid number of samples given ({num_samples}). \
Must be 1-31 samples.')

    # pre-add HS diluent
    p300.pick_up_tip()
    for d in dests:
        p300.transfer(135, hs_dil, d, new_tip='never')
    p300.transfer(27, hs_dil, final_dest, new_tip='never')
    p300.drop_tip()

    # transfer sample
    for s, d in zip(dils_2, dils_final):
        p20.transfer(15, s, d)

    # transfer RNA ladder
    p20.transfer(3, rna_ladder, final_dest)

    # mix all samples with diluent
    for d in dils_final:
        p300.pick_up_tip()
        p300.mix(10, 120, d)
        p300.drop_tip()

    # mix RNA ladder with diluent
    p300.pick_up_tip()
    p300.mix(10, 20, final_dest)
    p300.drop_tip()

    # heat samples
    ctx.pause('Seal the plate on the temperature module on slot 4. Resume when \
finished.')
    tempdeck1.set_temperature(70)
    ctx.delay(minutes=2)
    ctx.pause('Move the plate from temperature module on slot 4 to temperature \
module on slot 7.')
    tempdeck1.deactivate()
    ctx.delay(minutes=5)
    tempdeck2.deactivate()
    ctx.pause('Centrifuge the plate on temperature module on slot 7. Replace \
on temperature module on slot 4 when complete.')

    # transfer triplicates
    for set in triplicate_sets:
        p300.transfer(50, set[0], set[1:])

    # transfer water to blank wells
    p300.transfer(50, blank_solution, blank_wells)
