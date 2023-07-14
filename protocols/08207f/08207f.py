08207f
from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Liquid Transfer Using .csv File',
    'description': '''This protocol transfers liquid from  \
genomic DNA using the Nanopore Rapid Barcoding Kit 96.''',
    'author': 'parrish.payne@opentrons.com'
}

# Slot 1 Opentrons 96 Filter Tip Rack 20 µL
# Slot 2 Opentrons 96 Filter Tip Rack 200 µL
# Slot 3 Eppendorf twin.tec® PCR Plates-96 well plate (0030129512) with DNA samples mounted on Temperature Deck with Aluminum Block (Gen2)
# Slot 5 Opentrons 10 Tube Rack with Falson 4x50, 6x15 ml Conicl with dilution buffer/water in 50 ml tube 
# Slot 6 empty plate for diluted samples (end-point-plate); Eppendorf twin.tec® PCR Plates-96 well plate (0030129512) 
# Slot 8 Opentrons 96 Filter Tip Rack 20 µL
# Slot 9  Opentrons 96 Filter Tip Rack 200 µL

# Step 1: Transfer X uL (from .csv file) of buffer from tube rack A3 to X number of wells in 96 well plate (same tips), slot6 (the number of samples will be specified in .csv file); use p300/or p20 single channel.
# Step 2: Use single channel p20 to add X uL of sample (data in the .csv file) from A1 (slot3) to A1 well in end-point-plate (slot6) (well A1 to well A1, well B1 to well B1 …). Use 10ul air gap and blow out, new tip each time.
# Step 3: Repeat steps 2 across plate

def run(ctx):

    [input_csv, p20_mount, p300_mount] = get_values(  # noqa: F821
        'input_csv', 'p20_mount', 'p300_mount')

    # labware
    tiprack20 = [
        ctx.load_labware('opentrons_96_filtertiprack_20ul', slot, '20ul tiprack')
        for slot in ['1', '8']]
    tiprack300 = [
        ctx.load_labware(
            'opentrons_96_filtertiprack_200ul', slot, '200ul tiprack')
        for slot in ['2', '9']]
    tempdeck = ctx.load_module('temperature module gen2', '3')
    dna_plate = tempdeck.load_labware('Eppendorf twin.tec® PCR Plates-96 well')
    tube_rack = ctx.load_labware(
        'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', '5')
    dest_plate = ctx.load_labware('Eppendorf twin.tec® PCR Plates-96 well plate', '6', 'end-point-plate')    

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

 ####### PP to edit below




    barcodes = barcodes_plate.wells()[:len(data)]
    
    all_templates = [
        well
        for rack in sample_racks
        for well in rack.wells()
    ]

    # perform normalization
    for i, line in enumerate(data):
        conc = float(line[0])
        transfer_vol = min(target_dna_volume, target_mass/conc)
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
        slow_withdraw(p20, b)
        p20.dispense(1, r.bottom(1))
        p20.mix(num_mix, mix_vol, r.bottom(2))
        slow_withdraw(p20, r)
        p20.blow_out(r.top(-2))
        p20.drop_tip()

    # Temperature Control to be performed on external thermocycler
    ctx.pause('Seal plate (slot 4). Incubate at 30°C for 2 minutes, then at 80°C for 2 minutes. \
        Briefly put the plate on ice to cool.')

    # Pool all barcoded samples in 1.5 mL tube, note total vol
    pool = tube_rack.wells()[2]
    pick_up(p20)
    pool_vol = target_dna_volume + 1
    tip_ref_vol_20 = p20.tip_racks[0].wells()[0].max_volume
    for r in reactions:
        # move to pool tube if you can't aspirate more
        if p20.current_volume + pool_vol > tip_ref_vol_20:
            p20.dispense(p20.current_volume, pool.bottom(2))
            slow_withdraw(p20, pool)
        p20.aspirate(pool_vol, r.bottom(0.5))
        slow_withdraw(p20, r)
    p20.dispense(p20.current_volume, pool.bottom(2))
    slow_withdraw(p20, pool)
    p20.drop_tip()

    # Resuspend beads, add equal vol to pooled barcoded samples
    bead_transfer_vol = len(data)*(target_dna_volume+1)
    bead_mix_reps = 10
    bead_mix_vol = bead_transfer_vol*0.9
    tip_ref_vol_1000 = 1000
    num_asp = math.ceil(bead_transfer_vol/tip_ref_vol_1000)
    vol_per_asp = round(bead_transfer_vol/num_asp, 1)
    pick_up(p1000)
    p1000.mix(bead_mix_reps, bead_mix_vol, beads)
    for _ in range(num_asp):
        p1000.aspirate(vol_per_asp, beads.bottom(2))
        slow_withdraw(p1000, beads)
        p1000.dispense(vol_per_asp, pool.bottom(2))
        slow_withdraw(p1000, pool)

    # Mix for 5 min at room temp
    num_mix = 10
    pool_mix_vol = min(bead_transfer_vol*1.5, 900)
    for _ in range(num_mix):
        p1000.aspirate(pool_mix_vol, pool.bottom(5))
        p1000.dispense(pool_mix_vol, pool.bottom(15))
        ctx.delay(seconds=30)
    slow_withdraw(p1000, pool)
    p1000.drop_tip()