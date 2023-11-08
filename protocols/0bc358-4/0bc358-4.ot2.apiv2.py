import math
from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': '#4 Making Calibrator Curve using 20 mL Scintillation Vial',
    'description': '''This protocol makes Calibrator Curve by adding 275 µL of QC \
made from Working Stock to 4.4 mL of blank urine in a 20 mL Scintillation Vial.''',
    'author': 'Parrish Payne <parrish.payne@opentrons.com>'
    }

# Making Calibrator Curves using 20 ml Scintillation vial:
# For each destination vial C2-C10
# Add 4400ul blank urine
# Add 275 ul of each WS-1, WS-2, WS-3 and WS-4

def run(ctx):

    # labware

    tips = ctx.load_labware('opentrons_96_filtertiprack_1000ul', 4)
    urine = ctx.load_labware('neptunetiprackbase_1_reservoir_300ml', 10).wells()[0]
    source_scint_vial_rack = [ctx.load_labware('analytical_12_tuberack_20000ul', slot)
            for slot in [7, 8, 9]]
    dest_scint_vial_rack = ctx.load_labware('analytical_12_tuberack_20000ul', 11)

    # pipettes

    p1000 = ctx.load_instrument(
        'p1000_single_gen2', 'right', tip_racks=[tips])

    # functions 

    def slow_withdraw(pip, well, z=-3, delay_seconds=0):
        pip.default_speed /= 10
        if delay_seconds > 0:
            ctx.delay(seconds=delay_seconds)
        pip.move_to(well.top(z))
        pip.default_speed *= 10

    def transfer(vol, source, destination, pip=p1000):
        pip.aspirate(vol, source)
        slow_withdraw(pip, source)
        pip.dispense(vol, destination)
        slow_withdraw(pip, destination)
        pip.blow_out(destination)

    source_tubes = [tube for tuberack in source_scint_vial_rack for row in tuberack.rows() for tube in row]
    source_chunks = [source_tubes[i:i+4] for i in range(0, len(source_tubes), 4)]
    dest_vials = [tube for row in dest_scint_vial_rack.rows() for tube in row][:9]

    # variables

    vol_urine = 4400
    vol_airgap = 20
    vol_ws = 275
    asp_rate = 0.02

    # protocol

    ctx.comment('\n----------TRANSFER URINE TO SCINTILLATION VIALS-----------\n\n')

    num_transfers = math.ceil(vol_urine/p1000.max_volume)
    vol_per_transfer = vol_urine/num_transfers
    p1000.pick_up_tip()
    for d in dest_vials:
        for n in range(num_transfers):
            transfer(vol_per_transfer, urine, d)
    p1000.drop_tip()

    # Transfer 275 µL of each Working Stock (WS-1, WS-2, WS-3, WS-4)
    # into 20 mL scintillation vial. Repeat for each Mother Stock C3-C10
    
    ctx.comment('\n---------------TRANSFER WORKING STOCKS----------------\n\n')

    for chunk, d in zip(source_chunks, dest_vials):

        for well in chunk:
            p1000.pick_up_tip()
            p1000.mix(1, vol_ws, well)
            p1000.aspirate(vol_ws, well)
            slow_withdraw(p1000, well)
            p1000.aspirate(vol_airgap, well, rate = asp_rate)
            p1000.dispense(vol_ws+vol_airgap, d)
            p1000.mix(1, vol_ws)
            slow_withdraw(p1000, d)
            p1000.blow_out()
            p1000.drop_tip()
