metadata = {
    'protocolName': 'PCR Prep',
    'author': 'Nick Diehl <ndiehl@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):
    """Protocol."""
    [rna_plate_type, sample_vol, mm_vol, m20_mount] = get_values(  # noqa: F821
        'rna_plate_type', 'sample_vol', 'mm_vol', 'm20_mount')

    # load labware
    rna_source_plates = [
        ctx.load_labware(rna_plate_type, slot, f'RNA source plate {i+1}')
        for i, slot in enumerate(['2', '3', '5', '6'])]
    tempdeck = ctx.load_module('temperature module gen2', '4')
    tempdeck.set_temperature(4)
    mm_strips = tempdeck.load_labware(
        'opentrons_96_aluminumblock_generic_pcr_strip_200ul',
        'mastermix strips (1-3)').rows()[0][:3]
    dest_plate = ctx.load_labware('custom_384_wellplate_100ul', '1',
                                  'destination plate')
    tipracks = [
        ctx.load_labware('opentrons_96_tiprack_20ul', slot)
        for slot in ['7', '8', '9', '10', '11']]

    # load instrument
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount, tip_racks=tipracks)
    pick_up_current = 0.6
    ctx._implementation._hw_manager.hardware._attached_instruments[
        m20._implementation.get_mount()].update_config_item(
            'pick_up_current', pick_up_current)

    samples_sources_sets = [plate.rows()[0] for plate in rna_source_plates]
    destination_sets = [
        dest_plate.rows()[i][j*12:(j+1)*12]
        for i in range(2) for j in range(2)]
    mm_destinations = [
        well for row in dest_plate.rows()[:2] for well in row]

    # pre-add mastermix
    cols_per_mm_strip = int(len(mm_destinations)/len(mm_strips))
    m20.pick_up_tip()
    for i, d in enumerate(mm_destinations):
        m20.transfer(mm_vol, mm_strips[i//cols_per_mm_strip], d.bottom(1),
                     new_tip='never')
    m20.drop_tip()

    # add samples
    for i, (s_set, d_set) in enumerate(
            zip(samples_sources_sets, destination_sets)):
        ctx.pause(f'Ensure plate {i+1} is on deck before resuming.')
        for s, d in zip(s_set, d_set):
            m20.pick_up_tip()
            m20.aspirate(sample_vol, s.bottom(1))
            m20.aspirate(2, d.bottom(2))
            m20.dispense(m20.current_volume, d.bottom(2))
            m20.drop_tip()
