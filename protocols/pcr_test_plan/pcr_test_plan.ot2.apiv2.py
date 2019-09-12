DNA_VOLUME = 1
PRIMER_VOLUME = 2
MASTER_MIX_VOLUME = 20


def run(protocol_context):
    # labware setup
    total_volume = DNA_VOLUME + 2*PRIMER_VOLUME + MASTER_MIX_VOLUME
    if total_volume != 25:
        raise Exception("Total reaction volume must be 25 uL.")

    tipracks_10ul = [protocol_context.load_labware(
        'opentrons_96_tiprack_10ul', slot) for slot in [1, 2]]
    tiprack_300ul = protocol_context.load_labware(
        'opentrons_96_tiprack_300ul', 3)

    rt_reagents = protocol_context.load_labware(
        'opentrons_24_tuberack_nest_1.5ml_snapcap', 6)

    thermocycler = protocol_context.load_module('thermocycler')
    reaction_plate = thermocycler.load_labware(
        'nest_96_wellplate_100ul_pcr_full_skirt')

    # open thermocycler lid and keep block temperature at 4°C
    thermocycler.open_lid()
    thermocycler.set_block_temperature(4)

    # instrument setup
    p10 = protocol_context.load_instrument('p10_single', 'left',
                                           tip_racks=tipracks_10ul)
    p50 = protocol_context.load_instrument('p50_single', 'right',
                                           tip_racks=[tiprack_300ul])

    # reagent setup
    master_mix = rt_reagents.wells()[0]
    primer_1 = rt_reagents.wells()[4]
    primer_2 = rt_reagents.wells()[5]

    # transfer master mix
    volume_in_tube = master_mix.max_volume
    for well in reaction_plate.wells():
        p50.pick_up_tip()
        if volume_in_tube < MASTER_MIX_VOLUME:
            master_mix = master_mix
        p50.aspirate(MASTER_MIX_VOLUME, master_mix)
        p50.dispense(MASTER_MIX_VOLUME, well)
        p50.blow_out(well.top())
        p50.drop_tip()

    # transfer primer 1
    for well in reaction_plate.wells():
        p10.pick_up_tip()
        p10.aspirate(PRIMER_VOLUME, primer_1)
        p10.dispense(PRIMER_VOLUME, well)
        p10.blow_out(well.bottom(3))
        p10.drop_tip()

    # transfer primer 2
    for well in reaction_plate.wells():
        p10.pick_up_tip()
        p10.aspirate(PRIMER_VOLUME, primer_2)
        p10.dispense(PRIMER_VOLUME, well)
        p10.blow_out(well.bottom(3))
        p10.drop_tip()
