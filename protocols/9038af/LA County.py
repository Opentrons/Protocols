def get_values(*names):
    import json
    _all_values = json.loads("""{"input_csv":"source plate well,destination plate well,volume sample (µl),volume diluent (µl)\\nA1, A1,5,100\\nB1,B1,,101\\nC1,C1,,102\\nD1,D1,,103","p20_type":"p20_multi_gen2","p20_mount":"right","p300_type":"p300_single_gen2","p300_mount":"left","source_type":"eppendorf_96_well_on_block","using_tempdeck":true,"dest_type":"opentrons_96_aluminumblock_biorad_wellplate_200ul","reservoir_type":"opentrons_15_tuberack_5000ul"}""")
    return [_all_values[n] for n in names]
    
from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Rapid Barcoding with Normalization ',
    'description': '''This protocol carries out rapid barcoding of \
genomic DNA using the Nanopore Rapid Barcoding Kit 96.''',
    'author': 'parrish.payne@opentrons.com'
}

# Oxford Nanopore Rapid Barcoding Kit (SQK-RBK110.96)
# Automate steps 3-9 of the kit instructions.
# 16-32 samples per run (> 24 samples requires two 4-in-1 tube racks)

def run(ctx):

    [input_csv, p20_mount, p300_mount, source_type, 
        dest_type] = get_values(  # noqa: F821
        'input_csv', 'p20_mount', 'p300_mount',
        'source_type', 'dest_type')

    # labware

    
    tempdeck = ctx.load_module('temperature module gen2', '3')
    destination_plate = tempdeck.load_labware(dest_type, 'normalization plate')
    sample_rack = ctx.load_labware(source_type, '3', 'genomic dna')
    
    tube_rack = ctx.load_labware(
        'opentrons_24_aluminumblock_nest_1.5ml_screwcap', '5')
    water = tube_rack.wells()[0]
    barcodes_plate = ctx.load_labware('opentrons_96_aluminumblock_biorad_wellplate_200ul', '6')
    beads = tube_rack.wells()[1]

    tiprack20 = [
        ctx.load_labware('opentrons_96_tiprack_20ul', slot, '20ul tiprack')
        for slot in ['1']
    ]
    tiprack300 = [
        ctx.load_labware('opentrons_96_filtertiprack_200ul', slot, '200ul tiprack')
        for slot in ['4']
    ]

    # pipettes
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=tiprack20)
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount, tip_racks=tiprack300)

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

    # parse
    data = [
        [val.strip().upper() for val in line.split(',')]
        for line in input_csv.splitlines()[1:]
        if line and line.split(',')[0]]
    barcodes = barcodes_plate.wells()[:len(data)]

    target_mass = 50    # ng
    target_vol = 9      # uL

    # perform normalization
    for i, line in enumerate(data):
        conc = float(line[0])
        transfer_vol = target_mass/conc
        s = sample_rack.wells()[i]
        d = destination_plate.wells()[i]

        # pre-transfer diluent
        pick_up(p20)
        water_vol = target_vol - transfer_vol
        pip.apsirate(water_vol, water)
        pip.aspirate(transfer_vol, s)
        pip.dispense(p20.current_volume, d)
        pip.drop_tip()
    
    # Add 1 uL of Rapid Barcodes (RB01-96, one for each sample)
    num_mix = 5
    mix_vol = 7
    reactions = destination_plate.wells()[:len(data)]
    for b, r in zip(barcodes, reactions)
        pick_up(p20)
        p20.apirate(1, b.bottom(1), r, new_tip='always')
        p20.dispense (1, r.bottom(1))
        p20.mix(num_mix, mix_vol, r.bottom(2))
        p20.blow_out(r.top(-2))
        p20.drop_tip()

    # Temperature Control
    temp_mod.set_temperature(celsius=30)
    temp_mod.status  # 'holding at target'
    ctx.delay(minutes=2)             # delay for 2 minutes
    temp_mod.set_temperature(celsius=80)
    temp_mod.status  # 'holding at target'
    ctx.delay(minutes=2)             # delay for 2 minutes
    temp_mod.set_temperature(celsius=4)
    temp_mod.status  # 'holding at target'
    ctx.delay(minutes=2)             # delay for 2 minutes
    temp_mod.deactivate()
    temp_mod.status  # 'idle'

    # Pool all barcoded samplpes in 1.5 mL tube, note total vol
    pool = tube_rack.wells()[2]
    for r in reactions
        pick_up(p300)
        pip.apirate(12, b.bottom(1), new_tip='always')
     
        pip.blow_out(d.top(-2))
        pip.drop_tip()

    # Resuspend beads, add equal vol to pooled barcoded samples
    bead_transfer_vol = len(data)*10
    bead_mix_vol = 150
    pick_up(p300)
    pip.mix(10, bead_mix_vol, beads)
    pip.aspirate(bead_transfer_vol, beads)
    pip.dispense(bead_transfer_vol, pool)
 
    # Mix for 5 min at room temp
    num_mix = 10
    mix_vol = 150
    pip.mix(10, mix_vol, beads)
    pip.drop_tip()