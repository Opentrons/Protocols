metadata = {
    'protocolName': 'Custom Normalization & Transfer',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    [norm_data, p300_mount, p20_mount, final_conc,
        water_vol, water_res_vol] = get_values(  # noqa: F821
        "norm_data", "p300_mount", "p20_mount", "final_conc", "water_vol",
        "water_res_vol")

    # Load Labware
    tipracks_20ul = [ctx.load_labware('opentrons_96_tiprack_20ul',
                                      slot) for slot in range(1, 3)]
    tipracks_300ul = [ctx.load_labware('opentrons_96_tiprack_300ul',
                                       slot) for slot in range(3, 5)]
    sample_plate = ctx.load_labware('micronic_96_rack_300ul_tubes', 5)
    pcr_plate = ctx.load_labware('abgene_96_wellplate_200ul', 6)
    # water = ctx.load_labware(
    #         'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', 8)['A1']
    water = ctx.load_labware('thermofishernunc_96_wellplate_2000ul', 8,
                             'Water Reservoir')

    # Load Pipettes
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=tipracks_300ul)
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount,
                              tip_racks=tipracks_20ul)

    data = [[val.strip() for val in line.split(',')]
            for line in norm_data.splitlines()
            if line.split(',')[0].strip()][1:]

    dna_wells = []
    failed_wells = []

    def normalize(i_vol, i_conc, final_conc):

        final_vol = (i_vol*i_conc)/final_conc
        diluent_vol = final_vol - i_vol
        return round(diluent_vol, 1)

    water_volumes = dict.fromkeys(water.wells(), 0)

    def water_tracker(vol):
        '''water_tracker() will track how much water
        was used up per well. If the volume of
        a given well is greater than water_res_vol
        it will remove it from the dictionary and iterate
        to the next well which will act as the reservoir.'''
        well = next(iter(water_volumes))
        if water_volumes[well] > water_res_vol:
            del water_volumes[well]
            well = next(iter(water_volumes))
        water_volumes[well] = water_volumes[well] + vol
        ctx.comment(f'{int(water_volumes[well])} uL of water used from {well}')
        return well

    # Part 1
    for line in data:
        # well, vol = line[0], float(line[5])
        well, i_vol, i_conc = line[0], float(line[2]), float(line[1])
        vol = normalize(i_vol, i_conc, final_conc)
        if vol < 0:
            failed_wells.append(well)
            continue
        pip = p20 if vol < 20 else p300
        pip.transfer(vol, water_tracker(vol), sample_plate[well],
                     new_tip='always',
                     mix_after=(3, 15))
        dna_wells.append(well)
    ctx.comment('Normalization Step is Complete!')

    # Part 2
    ctx.comment('''Adding nuclease-free water to corresponding sample wells on
                the PCR plate.''')
    p300.pick_up_tip()
    for well in dna_wells:
        p300.transfer(water_vol, water_tracker(water_vol), pcr_plate[well],
                      new_tip='never')
    p300.drop_tip()

    ctx.comment('Transferring samples to PCR plate!')
    for well in dna_wells:
        p20.transfer(5, sample_plate[well], pcr_plate[well], new_tip='always',
                     mix_after=(3, 15))

    ctx.comment(f'''The following samples have failed:
                 {", ".join(failed_wells)}''')
    ctx.pause(f'Failed Samples: {", ".join(failed_wells)}')
    ctx.home()
