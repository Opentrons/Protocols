metadata = {
    'protocolName': 'Custom Normalization & Transfer',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    [norm_data, p300_mount, p20_mount, final_conc] = get_values(  # noqa: F821
        "norm_data", "p300_mount", "p20_mount", "final_conc")

    # Load Labware
    tipracks_20ul = [ctx.load_labware('opentrons_96_tiprack_20ul',
                                      slot) for slot in range(1, 3)]
    tipracks_300ul = [ctx.load_labware('opentrons_96_tiprack_300ul',
                                       slot) for slot in range(3, 5)]
    sample_plate = ctx.load_labware('micronic_96_rack_300ul_tubes', 5)
    pcr_plate = ctx.load_labware('abgene_96_wellplate_200ul', 6)
    water = ctx.load_labware(
            'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', 8)['A1']

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

    # Part 1
    for line in data:
        # well, vol = line[0], float(line[5])
        well, i_vol, i_conc = line[0], float(line[2]), float(line[1])
        vol = normalize(i_vol, i_conc, final_conc)
        if vol < 0:
            failed_wells.append(well)
            continue
        pip = p20 if vol < 20 else p300
        pip.transfer(vol, water, sample_plate[well], new_tip='always',
                     mix_after=(3, 15))
        dna_wells.append(well)

    # Part 2
    p300.pick_up_tip()
    for well in dna_wells:
        p300.transfer(32.5, water, pcr_plate[well], new_tip='never')
    p300.drop_tip()

    for well in dna_wells:
        p20.transfer(5, sample_plate[well], pcr_plate[well], new_tip='always',
                     mix_after=(3, 15))

    ctx.comment(f'The following samples have failed:{", ".join(failed_wells)}')
    ctx.pause(f'Failed Samples: {", ".join(failed_wells)}')
