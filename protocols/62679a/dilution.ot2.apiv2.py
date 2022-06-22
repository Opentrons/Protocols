metadata = {
    'protocolName': 'Compound Dilution',
    'author': 'Nick <ndiehl@opentrons.com',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.12'
}


def run(ctx):

    file_dilution, lw_dmso, mount_p300, mount_p20 = get_values(  # noqa: F821
     'file_dilution', 'lw_dmso', 'mount_p300', 'mount_p20')

    mix_reps = 5

    compound_management_plate = ctx.load_labware(
        'greinerbioone_96_wellplate_340ul', '1', 'compound management plate')
    tipracks200 = [
        ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
        for slot in ['7', '8']]
    tipracks20 = [
        ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
        for slot in ['9']]
    compound_dilution_plates = {
        str(i+1): ctx.load_labware('perkinelmer_96_wellplate_450ul', slot,
                                   f'compound plate {i+1}')
        for i, slot in enumerate(['4', '5', '6', '3'])}
    dmso = ctx.load_labware(lw_dmso, '10', 'DMSO (column 1)').wells()[0]

    p300 = ctx.load_instrument('p300_single_gen2', mount_p300,
                               tip_racks=tipracks200)
    p20 = ctx.load_instrument('p20_single_gen2', mount_p20,
                              tip_racks=tipracks20)

    # parse
    data = [
        [val.strip().lower() for val in line.split(',')]
        for line in file_dilution.splitlines()[3:]
        if line and line.split(',')[0].strip()]

    def parse_well_name(name):
        return f'{name[0].upper()}{int(name[1:])}'

    def parse_column(name):
        return str(int(name[1:]))

    substance_map = {
        line[3]: compound_management_plate.wells_by_name()[
            parse_well_name(line[1])]
        for line in data
    }

    # transfer stock to compound dilution plates
    for line in data:
        p300.transfer(float(line[12]), substance_map[line[10]],
                      compound_dilution_plates[line[8]].wells_by_name()[
                        parse_well_name(line[9])],
                      mix_before=(mix_reps, 50))

    ctx.pause('Check plate/spin down to ensure there are no air bubbles.')

    # pre-transfer DMSO before dilution
    p300.pick_up_tip()
    for line in data:
        p300.distribute(float(line[13]), dmso,
                        compound_dilution_plates[line[8]].columns_by_name()[
                            parse_column(line[9])][1:],
                        disposal_volume=5, air_gap=10, new_tip='never')
    p300.drop_tip()

    # dilute down each column
    for line in data:
        vol = float(line[14])
        column = compound_dilution_plates[
            line[8]].columns_by_name()[parse_column(line[9])]
        [pip, mix_vol] = [p300, 50] if vol >= 20 else [p20, 20]
        pip.pick_up_tip()
        pip.mix(mix_reps, mix_vol, column[0])
        pip.transfer(vol, column[:6], column[1:7],
                     mix_after=(mix_reps, mix_vol), new_tip='never')
        pip.air_gap(pip.min_volume)
        pip.drop_tip()
