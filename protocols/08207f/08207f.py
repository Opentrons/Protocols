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

Library Norm 1 Well, Internal ID, External ID, nM, Norm Amount (nM), Volume Required (µl), Sample Volume (µl), Dilutent Volume (µl)


csv_data = csv_raw.splitlines()[1:] # Discard the blank first line.
csv_reader = csv.DictReader(csv_data) 
for csv_row in csv_reader:
    source_well = csv_row['source_well']
    # destination_well = csv_row['destination_well']
    sample_volume = float(csv_row['sample_volume'])
    diluent_volume = float(csv_row['diluent_volume'])
 