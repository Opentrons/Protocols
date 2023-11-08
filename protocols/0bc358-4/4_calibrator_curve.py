import math
from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': '#4 Making Calibrator Curve using 20 mL Scintillation Vial',
    'description': '''This protocol pools various analytes and dilutes \
them with MeOH.''',
    'author': 'parrish.payne@opentrons.com'
    }

# Making Calibrator Curves using 20 ml Scintillation vial:
# Take 275 ul of C0-C10 made from WS1, add 4400ul blank urine, mix, to make a complete calibration curve
# Take 275 ul of C0-C10 made from WS2, add 4400ul blank urine, mix, to make a complete calibration curve
# Take 275 ul of C0-C10 made from WS3, add 4400ul blank urine, mix, to make a complete calibration curve
# Take 275 ul of C0-C10 made from WS4, add 4400ul blank urine, mix, to make a complete calibration curve
# Aliquot: Take the complete calibration/Quality control curve stock prepped above, aliquot 100ul each into microcentrifuge tubes.

def run(protocol: protocol_api.ProtocolContext):

    tips = protocol.load_labware('opentrons_96_filtertiprack_1000ul', 1)
    urine = protocol.load_labware('nest_1_reservoir_195ml', 5).wells()[0]
    aliquot_tuberack = protocol.load_labware(
        'opentrons_24_tuberack_nest_1.5ml_snapcap', 2)
    source_scint_vial_rack = protocol.load_labware('chemglass_11x20mL', 3)
    dest_scint_vial_rack = protocol.load_labware('chemglass_11x20mL', 6)

    p1000 = protocol.load_instrument(
        'p1000_single_gen2', 'right', tip_racks=[tips])

    def slow_withdraw(pip, well, z=0, delay_seconds=2.0):
        pip.default_speed /= 10
        if delay_seconds > 0:
            protocol.delay(seconds=delay_seconds)
        pip.move_to(well.top(z))
        pip.default_speed *= 10

    def transfer(vol, source, destination, pip=p1000):
        pip.aspirate(vol, source)
        slow_withdraw(pip, source)
        pip.dispense(vol, destination)
        slow_withdraw(pip, destination)

    def mix_high_low(reps, vol, well, pip=p1000, z_low=5.0, z_high=20):
        for _ in range(reps):
            pip.aspirate(vol, well.bottom(z_low))
            pip.dispense(vol, well.bottom(z_high))

    source_vials = source_scint_vial_rack.wells()[:10]
    dest_vials = dest_scint_vial_rack.wells()[:10]
    aliquots = aliquot_tuberack.wells()[:10]
    vol_vial = 275
    vol_urine = 4400

    # Pre-transfer urine to each destination vial
    num_transfers = math.ceil(vol_urine/p1000.max_volume)
    vol_per_transfer = vol_urine/num_transfers
    p1000.pick_up_tip()
    for d in dest_vials:
        for n in range(num_transfers):
            transfer(vol_per_transfer, urine, d)
    p1000.drop_tip()

    # Transfer 275 µL of each C0-C10 into 20 mL scintillation vial
    for s, d in zip(source_vials, dest_vials):
        p1000.pick_up_tip()
        transfer(vol_vial, s, d)
        mix_high_low(10, 750, d)
        p1000.drop_tip()
