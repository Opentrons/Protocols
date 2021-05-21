from opentrons import protocol_api, types
import math

metadata = {
    'protocolName': 'Ligation Sequencing Kit: DNA Repair and End-Prep',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.10'
}


def run(ctx):

    [samples, m300_mount, mag_engage_height] = get_values(  # noqa: F821
        "samples", "m300_mount", "mag_engage_height")

    cols = math.ceil(samples/8)

    # Load Labware
    tc_mod = ctx.load_module('Thermocycler Module')
    tc_plate = tc_mod.load_labware('biorad_96_wellplate_200ul_pcr')
    mag_mod = ctx.load_module('magnetic module', '1')
    mag_plate = mag_mod.load_labware(
        'thermofisher_96_midi_storage_plate_800ul')
    midi_plate_2 = ctx.load_labware('thermofisher_96_midi_storage_plate_800ul',
                                    2)
    reservoir1 = ctx.load_labware('nest_12_reservoir_15ml', 4)
    reservoir2 = ctx.load_labware('nest_1_reservoir_195ml', 5)
    tipracks = [ctx.load_labware('opentrons_96_tiprack_300ul', slot) for
                slot in [3, 6, 9]]
    trash = ctx.loaded_labwares[12]['A1']

    # Load Pipettes
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=tipracks)

    # Reagents
    dna_repair_buff = reservoir1['A1']
    dna_repair_mix = reservoir1['A2']
    rxn_buffer = reservoir1['A3']
    enzyme_mix = reservoir1['A4']
    nfa = reservoir1['A5']
    endprep_mm = reservoir1['A8']
    ampure_beads = reservoir1['A12']
    ethanol = reservoir2['A1']

    # Sample Wells
    tc_plate_wells = tc_plate.rows()[0][:cols]
    mag_plate_wells = mag_plate.rows()[0][:cols]
    midi_plate_2_wells = midi_plate_2.rows()[0][:cols]

    # Helper Functions
    def pick_up(pip):
        """Function that can be used instead of .pick_up_tip() that will pause
        robot when robot runs out of tips, prompting user to replace tips
        before resuming"""
        try:
            pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            pip.home()
            ctx.pause("Replace the tips")
            pip.reset_tipracks()
            pip.pick_up_tip()

    def remove_supernatant(vol, src, dest, side):
        m300.flow_rate.aspirate = 20
        m300.aspirate(10, src.top())
        while vol > 300:
            m300.aspirate(
                300, src.bottom().move(types.Point(x=side, y=0, z=0.5)))
            m300.dispense(300, dest)
            m300.aspirate(10, dest)
            vol -= 300
        m300.aspirate(vol, src.bottom().move(types.Point(x=side, y=0, z=0.5)))
        m300.dispense(vol, dest)
        m300.dispense(10, dest)
        m300.flow_rate.aspirate = 50

    sides = [-1, 1] * 6
    sides = sides[:cols]

    def magnet(delay_mins):
        mag_mod.engage(height_from_base=mag_engage_height)
        ctx.delay(minutes=delay_mins, msg='Allowing beads to settle.')

    # PROTOCOL STEPS

    # Create End Prep Master Mix
    m300.transfer(27*samples, nfa, endprep_mm)
    m300.transfer(3.5*samples, dna_repair_buff, endprep_mm)
    m300.transfer(2*samples, dna_repair_mix, endprep_mm)
    m300.transfer(3.5*samples, rxn_buffer, endprep_mm)
    m300.transfer(3*samples, enzyme_mix, endprep_mm, mix_after=(5, 300))

    # Transfer End Prep Mix to Samples on PCR Plate (1)
    m300.transfer(39, endprep_mm, tc_plate_wells, new_tip='always',
                  mix_after=(3, 30))

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

    # Add AMPure XP Beads to Mag Mod (6-7)
    for well in mag_plate_wells:
        pick_up(m300)
        m300.transfer(60, ampure_beads, well, new_tip='never',
                      mix_after=(3, 60))
        m300.drop_tip()

    # Pause for Hula Mixer/Spin Down (8-9)
    ctx.pause('''Incubate on Hula Mixer for 5 minutes and spin down the samples.
                 Then place back on the magnet and click resume.''')

    # Engage Magnet and Delay for 5 Minutes (10)
    magnet(5)
    # Remove Supernatant (11)
    for well, side in zip(mag_plate_wells, sides):
        pick_up(m300)
        remove_supernatant(100, well, trash, side)
        m300.drop_tip()

    # (12-14)
    for _ in range(2):
        # Wash Beads with Ethanol (12)
        for well in mag_plate_wells:
            m300.transfer(200, ethanol, well.top(-3), mix_after=(3, 200))

        # Remove Supernatant (11)
        for well, side in zip(mag_plate_wells, sides):
            pick_up(m300)
            remove_supernatant(100, well, trash, side)
            m300.drop_tip()

    # Pause and Remove Samples for Spin Down (15)
    mag_mod.disengage()
    ctx.pause('''Spin down and place samples back on the maget.
              Then click resume.''')
    magnet(1)

    # Remove Residual Ethanol (16)
    for well, side in zip(mag_plate_wells, sides):
        pick_up(m300)
        remove_supernatant(100, well, trash, side)
        m300.drop_tip()

    # Add 61 uL of Nuclease-free Water (17)
    mag_mod.disengage()
    for well in mag_plate_wells:
        m300.transfer(61, nfa, well.top(-3), mix_after=(3, 60))
    ctx.delay(minutes=2, msg='Incubating at Room Temperature for 2 minutes...')

    # Engage Magnet (18)
    magnet(5)

    # Transfer Eluate into MIDI plate for part 2 (19)
    for well, dest, side in zip(mag_plate_wells, midi_plate_2_wells, sides):
        pick_up(m300)
        remove_supernatant(100, well, dest, side)
        m300.drop_tip()
