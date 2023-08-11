from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': '#3 Making Quality Control Levels in 20 ml Scintillation Vials',
    'description': '''This protocol creates quality controls from Working Stocks by performing a dilutional series in methanol.''',
    'author': 'parrish.payne@opentrons.com'
    }

# WS1 in A1
# Quality control 8 (QC8)= 3000ul WS1 + 1000 MeOH ul MeOH in A2
# QC7=1500 ul QC8 + 1500 MeOH in A3
# QC6=1200 ul QC8 + 3300 MeOH in A4
# QC5=1500 ul QC6 + 2500 MeOH in B1
# QC4=2000 ul QC5 + 2000 MeOH in B2
# QC3=2000 ul QC4 + 3000 MeOH in B3
# QC2=2000 ul QC3 + 3000 MeOH in C1
# QC1=2000 ul QC2 + 2000 MeOH in C2
# # pure MeOH in C4 used as source vial
# Repeat for WS2, WS3 and WS4


def run(protocol: protocol_api.ProtocolContext):

    tips = [protocol.load_labware('opentrons_96_filtertiprack_1000ul', 1)]
    scint_vial = protocol.load_labware('chemglass_11x20mL', 2)

    p1000 = protocol.load_instrument(
        'p1000_single_gen2', 'right', tip_racks=tips)

    def slow_withdraw(pip, well, z=0, delay_seconds=0):
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
    dilution_sources = [
        [well for row in scint_vial.rows() for well in row][0]] + [
            [well for row in scint_vial.rows() for well in row][1]]*2 + [well for row in scint_vial.rows() for well in row][3:8]
    dilution_destinations = [well for row in scint_vial.rows() for well in row][1:9]
    meoh_destinations = [well for row in scint_vial.rows() for well in row][1:9]
    vols_meoh = [1000, 1500, 3300, 2500, 2000, 3000, 3000, 2000]
    vols_dilution = [3000, 1500, 1200, 1500, 2000, 2000, 2000, 2000]

# pre-addition of meoh
    p1000.pick_up_tip()
    for vol, d in zip(vols_meoh, meoh_destinations):
        p1000.transfer(vol, meoh, d, new_tip='never', air_gap=20)
    p1000.drop_tip()

    for vol, s, d in zip(
            vols_dilution, dilution_sources, dilution_destinations):
        p1000.pick_up_tip()
        p1000.transfer(vol, s, d.top(-5), new_tip='never', air_gap=20)
        p1000.mix(5, 500, d.bottom(5))
        p1000.drop_tip()
