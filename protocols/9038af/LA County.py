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

    [input_csv, p20_type, p20_mount, p300_type, p300_mount, source_type,
     using_tempdeck, dest_type, reservoir_type] = get_values(  # noqa: F821
        'input_csv', 'p20_type', 'p20_mount', 'p300_type', 'p300_mount',
        'source_type', 'using_tempdeck', 'dest_type', 'reservoir_type')

    # labware

    if using_tempdeck:
        tempdeck = ctx.load_module('temperature module gen2', '3')
        tempdeck.set_temperature(4)
        source_plate = tempdeck.load_labware(source_type, 'source plate')

    else:
        source_plate = ctx.load_labware(source_type, 2, 'source plate')

    destination_plate = ctx.load_labware(dest_type, '3', 'destination plate')
    
    water = ctx.load_labware(
        'opentrons_24_aluminumblock_nest_1.5ml_screwcap', '5',
        (position A1)').wells()[0].bottom(1)

    barcodes = ctx.load_labware(
        'opentrons_24_aluminumblock_nest_1.5ml_screwcap', '5',
        (position B1)').wells()[0].bottom(1)

    beads = ctx.load_labware(
        'opentrons_24_aluminumblock_nest_1.5ml_screwcap', '5',
        (position C1)').wells()[0].bottom(1)

    tiprack20 = [
        ctx.load_labware('opentrons_96_tiprack_20ul', slot, '20ul tiprack')
        for slot in ['1']
    ]
    tiprack300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot, '300ul tiprack')
        for slot in ['4']
    ]

    # pipettes
    p20 = ctx.load_instrument(p20_type, p20_mount, tip_racks=tiprack20)
    p300 = ctx.load_instrument(p300_type, p300_mount, tip_racks=tiprack300)

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

    # perform normalization
    for line in data:
        s, d, vol_s, vol_w = line[:4]

        if not vol_w:
            vol_w = 0
        else:
            vol_w = float(vol_w)

        d = destination_plate.wells_by_name()[d]

        # pre-transfer diluent
        pip = p300 if vol_w > 20 else p20
        if not pip.has_tip:
            pick_up(pip)

        pip.transfer(vol_w, water, d.bottom(2), new_tip='never')
        pip.blow_out(d.top(-2))

    for pip in [p20, p300]:
        if pip.has_tip:
            pip.drop_tip()

    # perform normalization
    for line in data:
        s, d, vol_s, vol_w = line[:4]
        if not vol_s:
            vol_s = 0
        else:
            vol_s = float(vol_s)

        s = source_plate.wells_by_name()[s]
        d = destination_plate.wells_by_name()[d]

        # transfer sample
        pip = p300 if vol_s > 20 else p20
        if vol_s != 0:
            pick_up(pip)
            pip.transfer(vol_s, s.bottom(3), d, new_tip='never')
            pip.blow_out(d.top(-2))
            pip.drop_tip()

        # Add 1 uL of Rapid Barcodes (RB01-96, one for each sample)
        pip = p20
            pick_up(pip)
                pip.transfer(barcodes, s.bottom(3), d, new_tip='always')
                pip.mix(5, 7, d.bottom(2))
                pip.blow_out(d.top(-2))
                pip.drop_tip()

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

        # Resuspend beads, add equal vol to pooled barcoded

        # Mix for 5 min at room temp