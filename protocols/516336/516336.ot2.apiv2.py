metadata = {
    'protocolName': 'DNA Repair and End-Prep',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.10'
}

def get_values(*names):
    import json
    _all_values = json.loads("""{"samples":96,"m300_mount":"left"}""")
    return [_all_values[n] for n in names]

def run(ctx):

    [samples, m300_mount] = get_values(  # noqa: F821
        "samples", "m300_mount")

    # Load Labware
    tc_mod = ctx.load_module('Thermocycler Module')
    tc_plate = tc_mod.load_labware('biorad_96_wellplate_200ul_pcr')

    mag_mod = ctx.load_module('magnetic module', '1')
    mag_plate = mag_mod.load_labware('thermofisher_96_midi_storage_plate_800ul')
    midi_plate_2 = ctx.load_labware('thermofisher_96_midi_storage_plate_800ul', 2)

    reservoir1 = ctx.load_labware('nest_12_reservoir_15ml', 4)
    reservoir2 = ctx.load_labware('nest_1_reservoir_195ml', 5)

    tipracks = [ctx.load_labware('opentrons_96_tiprack_300ul', slot) for slot in [3, 6, 9]]

    # Load Pipettes
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount, tip_racks=tipracks)

    # Reagents
    dna_repair_buff = reservoir1['A1']
    dna_repair_mix = reservoir1['A2']
    rxn_buffer = reservoir1['A3']
    enzyme_mix = reservoir1['A4']
    nfa = reservoir1['A5']
    endprep_mm = reservoir1['A8']

    # Sample Wells
    tc_plate_wells = tc_plate.rows()[0]
    mag_plate_wells = mag_plate.rows()[0]

    # Helper Functions
    

    # PROTOCOL STEPS

    # Create End Prep Master Mix
    m300.transfer(27*samples, nfa, endprep_mm)
    m300.transfer(3.5*samples, dna_repair_buff, endprep_mm)
    m300.transfer(2*samples, dna_repair_mix, endprep_mm)
    m300.transfer(3.5*samples, rxn_buffer, endprep_mm)
    m300.transfer(3*samples, enzyme_mix, endprep_mm, mix_after=(5,300))

    # Transfer End Prep Mix to Samples on PCR Plate (1)
    m300.transfer(39, endprep_mm, tc_plate_wells, new_tip='always', mix_after=(3, 30))

    # Pause for Spin Down (2)
    ctx.pause('Spin down the plate and resume.')

    # Incubate on Thermocycler (3)
    tc_mod.close_lid()
    profile = [{'temperature': 20, 'hold_time_minutes': 5},
               {'temperature': 65, 'hold_time_minutes': 5}]
    tc_mod.execute_profile(steps=profile, repetitions=1, block_max_volume=60)
    tc_mod.open_lid()

    # Resuspend AMPure Beads (4)
    m300.pick_up_tip()
    m300.mix(5, 300, endprep_mm.bottom(z=3))
    m300.drop_tip()

    # Transfer Samples from TC to Mag Mod (5)
    for src, dest in zip(tc_plate_wells, mag_plate_wells):
        m300.pick_up_tip()
        m300.transfer(60, src, dest, new_tip='never')
        m300.drop_tip()
    
    # Add AMPure XP Beads to Mag Mod
