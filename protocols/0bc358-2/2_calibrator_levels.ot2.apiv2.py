from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': '#2 Making Calibrator levels in 20 ml Scintillation vials',
    'description': '''This protocol creates calibrators from Working Stocks by performing a dilutional series in methanol.''',
    'author': 'Parrish Payne <parrish.payne@opentrons.com>'
    }

# Calibrator 10 (C10)=WS1 in A1
# C9=2000ul from C10+2000ul MeOH, mix in A2
# C8=2000ul from C9+2000ul MeOH, mix in A3
# C7=2000ul from C8+2000ul MeOH, mix in A4
# C6=2000ul from C7+2000ul MeOH, mix in B1
# C5=2000ul from C6+2000ul MeOH, mix in B2
# C4=2000ul from C5+2000ul MeOH, mix in B3
# C3=2000ul from C4+2000ul MeOH, mix in C1
# C2=2000ul from C3+2000ul MeOH, mix in C2
# C0=2000ul pure MeOH in C3
# pure MeOH used as source vial in C4
# Repeat for WS2, WS3 and WS4


def run(protocol: protocol_api.ProtocolContext):

    tips = [protocol.load_labware('opentrons_96_filtertiprack_1000ul', 1)]
    scint_vial = protocol.load_labware('chemglass_11x20mL', 2)

    p1000 = protocol.load_instrument(
        'p1000_single_gen2', 'right', tip_racks=tips)

    def slow_withdraw(pip, well, z=0, delay_seconds=2.0):
        pip.default_speed /= 10
        if delay_seconds > 0:
            protocol.delay(seconds=delay_seconds)
        pip.move_to(well.top(z))
        pip.default_speed *= 10

    def transfer(pip, vol, source, destination):
        pip.aspirate(vol, source)
        slow_withdraw(pip, source)
        pip.dispense(vol, destination)
        slow_withdraw(pip, destination)

    meoh = scint_vial.wells_by_name()['C4']
    dilution_sources = [well for row in scint_vial.rows() for well in row][:8]
    dilution_destinations = [well for row in scint_vial.rows() for well in row][1:9]
    meoh_destinations = [well for row in scint_vial.rows() for well in row][1:10]
    vol_meoh = 2000

    # pre-addition of meoh
    p1000.pick_up_tip()
    for d in meoh_destinations:
        p1000.transfer(vol_meoh, meoh, d, new_tip='never', air_gap=20)
    p1000.drop_tip()

    dil_transfer_vol = 2000
    for s, d in zip(dilution_sources, dilution_destinations):
        p1000.pick_up_tip()
        p1000.transfer(dil_transfer_vol, s, d.top(-5), new_tip='never', air_gap=20)
        p1000.mix(5, 500, d.bottom(5))
        p1000.drop_tip()
