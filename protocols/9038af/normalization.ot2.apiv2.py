import math
from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Oxford Nanopore Rapid Barcoding with Normalization ',
    'description': '''This protocol carries out rapid barcoding of \
genomic DNA using the Nanopore Rapid Barcoding Kit 96.''',
    'author': 'parrish.payne@opentrons.com'
}

# Oxford Nanopore Rapid Barcoding Kit (SQK-RBK110.96)
# Automate steps 3-9 of the kit instructions.
# 16-32 samples per run (> 24 samples requires two 4-in-1 tube racks)


def run(ctx):

    [input_csv, target_dna_volume, p20_mount, p300_mount, source_type,
        dest_type] = get_values(  # noqa: F821
        'input_csv', 'target_dna_volume', 'p20_mount', 'p300_mount',
        'source_type', 'dest_type')

    # labware
    tempdeck = ctx.load_module('temperature module gen2', '1')
    destination_plate = tempdeck.load_labware(dest_type, 'normalization plate')
    sample_racks = [
        ctx.load_labware(source_type, slot, 'genomic dna')
        for slot in ['2', '5']]
    tube_rack = ctx.load_labware(
        'opentrons_24_aluminumblock_nest_1.5ml_screwcap', '8')
    water = tube_rack.wells()[0]
    barcodes_plate = ctx.load_labware(
        'opentrons_96_aluminumblock_biorad_wellplate_200ul', '4')
    beads = tube_rack.wells()[1]

    tiprack20 = [
        ctx.load_labware('opentrons_96_tiprack_20ul', slot, '20ul tiprack')
        for slot in ['3']]
    tiprack300 = [
        ctx.load_labware(
            'opentrons_96_filtertiprack_200ul', slot, '200ul tiprack')
        for slot in ['6']]

    # pipettes
    p20 = ctx.load_instrument(
        'p20_single_gen2', p20_mount, tip_racks=tiprack20)
    p300 = ctx.load_instrument(
        'p300_single_gen2', p300_mount, tip_racks=tiprack300)

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

    def slow_withdraw(pip, well, delay_seconds=2.0):
        pip.default_speed /= 16
        if delay_seconds > 0:
            ctx.delay(seconds=delay_seconds)
        pip.move_to(well.top())
        pip.default_speed *= 16

    # parse
    data = [
        [val.strip().upper() for val in line.split(',')]
        for line in input_csv.splitlines()[1:]
        if line and line.split(',')[0]]
    barcodes = barcodes_plate.wells()[:len(data)]

    target_mass = 50    # ng

    all_templates = [
        well
        for rack in sample_racks
        for well in rack.wells()
    ]

    # perform normalization
    for i, line in enumerate(data):
        conc = float(line[0])
        transfer_vol = max(target_dna_volume, target_mass/conc)
        s = all_templates[i]
        d = destination_plate.wells()[i]

        # pre-transfer diluent
        pick_up(p20)
        water_vol = target_dna_volume - transfer_vol
        if water_vol > 0:
            p20.aspirate(water_vol, water)
            slow_withdraw(p20, water)
        p20.aspirate(transfer_vol, s)
        slow_withdraw(p20, s)
        p20.dispense(p20.current_volume, d)
        slow_withdraw(p20, d)
        p20.drop_tip()

    # Add 1 uL of Rapid Barcodes (RB01-96, one for each sample)
    num_mix = 5
    mix_vol = 7
    reactions = destination_plate.wells()[:len(data)]
    for b, r in zip(barcodes, reactions):
        pick_up(p20)
        p20.aspirate(1, b.bottom(1))
        slow_withdraw(p300, b)
        p20.dispense(1, r.bottom(1))
        p20.mix(num_mix, mix_vol, r.bottom(2))
        slow_withdraw(p300, r)
        p20.blow_out(r.top(-2))
        p20.drop_tip()

    # Temperature Control
    tempdeck.set_temperature(celsius=30)
    tempdeck.status  # 'holding at target'
    ctx.delay(minutes=2)             # delay for 2 minutes
    tempdeck.set_temperature(celsius=80)
    tempdeck.status  # 'holding at target'
    ctx.delay(minutes=2)             # delay for 2 minutes
    tempdeck.set_temperature(celsius=4)
    tempdeck.status  # 'holding at target'
    ctx.delay(minutes=2)             # delay for 2 minutes
    tempdeck.deactivate()
    tempdeck.status  # 'idle'

    # Pool all barcoded samples in 1.5 mL tube, note total vol
    pool = tube_rack.wells()[2]
    pick_up(p300)
    pool_vol = target_dna_volume + 1
    tip_ref_vol_300 = p300.tip_racks[0].wells()[0].max_volume
    for r in reactions:
        # move to pool tube if you can't aspirate more
        if p300.current_volume + pool_vol > tip_ref_vol_300:
            p300.dispense(p300.current_volume, pool.bottom(2))
            slow_withdraw(p300, pool)
        p300.aspirate(pool_vol, r.bottom(0.5))
        slow_withdraw(p300, r)
    p300.dispense(p300.current_volume, pool.bottom(2))
    slow_withdraw(p300, pool)
    p300.drop_tip()

    # Resuspend beads, add equal vol to pooled barcoded samples
    bead_transfer_vol = len(data)*10
    bead_mix_reps = 10
    bead_mix_vol = 150
    num_asp = math.ceil(bead_transfer_vol/tip_ref_vol_300)
    vol_per_asp = round(bead_transfer_vol/num_asp, 1)
    pick_up(p300)
    p300.mix(bead_mix_reps, bead_mix_vol, beads)
    for _ in range(num_asp):
        p300.aspirate(vol_per_asp, beads.bottom(2))
        slow_withdraw(p300, beads)
        p300.dispense(vol_per_asp, pool.bottom(2))
        slow_withdraw(p300, pool)

    # Mix for 5 min at room temp
    p300.mix(bead_mix_reps, bead_mix_vol, pool)
    slow_withdraw(p300, pool)
    p300.drop_tip()
