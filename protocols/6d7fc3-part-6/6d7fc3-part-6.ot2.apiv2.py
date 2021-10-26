from opentrons import protocol_api

metadata = {
    'protocolName': '''GeneRead QIAact Lung DNA UMI Panel Kit:
                       Universal PCR Amplification''',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [samples, p300_mount,
        p20_mount] = get_values(  # noqa: F821
        "samples", "p300_mount", "p20_mount")

    if not 1 <= samples <= 12:
        raise Exception('''Invalid number of samples.
                        Sample number must be between 1-12.''')

    # Load Labware
    tipracks_200ul = ctx.load_labware('opentrons_96_filtertiprack_200ul', 9)
    tipracks_20ul = ctx.load_labware('opentrons_96_filtertiprack_20ul', 6)
    tc_mod = ctx.load_module('thermocycler module')
    tc_plate = tc_mod.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
    temp_mod = ctx.load_module('temperature module gen2', 3)
    temp_plate = temp_mod.load_labware(
                    'opentrons_24_aluminumblock_nest_2ml_snapcap')
    pcr_tubes = ctx.load_labware(
                    'opentrons_96_aluminumblock_generic_pcr_strip_200ul',
                    2)

    # Load Pipettes
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=[tipracks_200ul])
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount,
                              tip_racks=[tipracks_20ul])

    # Helper Functions
    def pick_up(pip, loc=None):
        try:
            if loc:
                pip.pick_up_tip(loc)
            else:
                pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            pip.home()
            pip.pause("Please replace the empty tip racks!")
            pip.reset_tipracks()
            pip.pick_up_tip()

    # Wells
    mm = temp_plate['A1']
    upcr_buffer = temp_plate['B1']
    pcr_primer_A = temp_plate['C1']
    pcr_primer_B = temp_plate['D1']
    dna_poly = temp_plate['A2']
    pcr_tube_wells = pcr_tubes.wells()[:samples]
    tc_plate_wells = tc_plate.wells()[:samples]

    # Protocol Steps

    # Pre-Cool Thermocycler and Temperature Module to 4C
    ctx.comment('Pre-Cooling Temperature Module to 4°C')
    temp_mod.set_temperature(4)
    ctx.pause('''Temperature Module has been cooled to 4°C.
              Please place your samples and reagents on the
              temperature module.''')

    # Prepare Universal Master Mix
    upcr_buffer_vol = 4*samples+2
    pcr_primer_A_vol = 0.8*samples+0.4
    pcr_primer_B_vol = 0.8*samples+0.4
    dna_poly_vol = 1*samples+0.5
    mix_vol = (upcr_buffer_vol + pcr_primer_A_vol + pcr_primer_B_vol
               + dna_poly_vol)

    pip = p300 if upcr_buffer_vol > 20 else p20
    pick_up(pip)
    pip.aspirate(upcr_buffer_vol, upcr_buffer)
    pip.dispense(upcr_buffer_vol, mm)
    pip.drop_tip()

    pip = p300 if pcr_primer_A_vol > 20 else p20
    pick_up(pip)
    pip.aspirate(pcr_primer_A_vol, pcr_primer_A)
    pip.dispense(pcr_primer_A_vol, mm)
    pip.drop_tip()

    pip = p300 if pcr_primer_B_vol > 20 else p20
    pick_up(pip)
    pip.aspirate(pcr_primer_B_vol, pcr_primer_B)
    pip.dispense(pcr_primer_B_vol, mm)
    pip.drop_tip()

    pip = p300 if dna_poly_vol > 20 else p20
    pick_up(pip)
    pip.aspirate(dna_poly_vol, dna_poly)
    pip.dispense(dna_poly_vol, mm)
    pip.drop_tip()

    pip = p300 if mix_vol > 20 else p20
    pick_up(pip)
    pip.mix(10, mix_vol, mm)
    pip.drop_tip()

    # Add Master Mix to PCR Tubes with enriched DNA
    for well in pcr_tube_wells:
        pick_up(p20)
        p20.aspirate(6.6, mm)
        p20.dispense(6.6, well)
        p20.mix(7, 10)
        p20.drop_tip()

    # Centrifuge
    ctx.pause('Centrifuge the enriched DNA briefly and return them to slot 2.')

    # Transfer Samples to PCR Plate
    for src, dest in zip(pcr_tube_wells, tc_plate_wells):
        pick_up(p300)
        p300.aspirate(20, src)
        p300.dispense(20, dest)
        p300.drop_tip()

    tc_mod.close_lid()
    tc_mod.set_lid_temperature(103)

    profile = [
        {'temperature': 98, 'hold_time_seconds': 15},
        {'temperature': 60, 'hold_time_minutes': 2}
    ]

    tc_mod.set_block_temperature(95, hold_time_minutes=13, block_max_volume=20)
    tc_mod.set_block_temperature(98, hold_time_minutes=2, block_max_volume=20)
    tc_mod.execute_profile(steps=profile, repetitions=21, block_max_volume=20)
    tc_mod.set_block_temperature(72, hold_time_minutes=5, block_max_volume=20)
    tc_mod.set_block_temperature(4, hold_time_minutes=5, block_max_volume=20)
    tc_mod.set_block_temperature(4)
    tc_mod.open_lid()
    tc_mod.deactivate_lid()

    ctx.comment('Protocol Complete!')
