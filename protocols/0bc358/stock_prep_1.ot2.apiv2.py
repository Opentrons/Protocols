from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': '1. Stock Prep 1',
    'description': '''This protocol pools various analytes and dilutes \
them with MeOH.''',
    'author': 'parrish.payne@opentrons.com'
}

# Working stock 1(WS1): take 80ul of each analyte in HPLC vial (48 \
# analytes total), combine in 20ml Scintillation vial.
# Add 160 µL of MeOH to 3840ul pool to make total of 4 ml.
# Working stock 2(WS2): take 80 ul of each analyte in HPLC vial (47 \
# analytes total), combine in 20ml Scintillation vial.
# Add 240 µL of MeOH to 3760ul pool to make total of 4 ml.
# Working stock 3(WS3): take 80 ul of 28 analyte in HPLC vial 28 analytes, \
# 800 ul of 2 analyte (30 analytes total) , combine in 20ml Scintillation vial.
# Add 160 µL of MeOH to 3840ul pool to make total of 4 ml.
# Working stock 4(WS4): take 80 ul of 2 analyte, 400 of 8 analyte (10 \
# analytes total) in HPLC vial, combine in 20ml Scintillation vial.
# Add 640 µL of MeOH to 3360ul pool to make total of 4 ml.
# Quality control working stock (prep exactly the same way as calibrator \
# working stock)


def run(protocol: protocol_api.ProtocolContext):

    tips1 = [
        protocol.load_labware('opentrons_96_filtertiprack_200ul', slot)
        for slot in ['1', '4']]
    tips2 = [
        protocol.load_labware('opentrons_96_filtertiprack_1000ul', slot)
        for slot in ['7']]
    hplc_vial = protocol.load_labware('nest_96_wellplate_200ul_flat', 2)
    scint_vial = protocol.load_labware('chemglass_11x20mL', 3)

    p300 = protocol.load_instrument(
        'p300_single_gen2', 'left', tip_racks=tips1)
    p1000 = protocol.load_instrument(
        'p1000_single_gen2', 'right', tip_racks=tips2)

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

    # locations
    ws1 = scint_vial.wells_by_name()['A1']
    qc1 = scint_vial.wells_by_name()['C1']
    ws2 = scint_vial.wells_by_name()['A2']
    qc2 = scint_vial.wells_by_name()['C2']
    ws3 = scint_vial.wells_by_name()['A3']
    qc3 = scint_vial.wells_by_name()['C3']
    ws4 = scint_vial.wells_by_name()['A4']
    qc4 = scint_vial.wells_by_name()['C4']
    meoh = scint_vial.wells_by_name()['B1']

    vol_airgap_p300 = 20
    vol_airgap_p1000 = 50

    # WS1 and QC1
    vol_analyte_1 = 80
    sources_1 = hplc_vial.wells()[:48]
    destinations = [ws1, qc1]
    for d in destinations:
        for s in sources_1:
            p300.pick_up_tip()
            p300.aspirate(vol_analyte_1, s)
            slow_withdraw(p300, s)
            p300.air_gap(vol_airgap_p300)
            p300.dispense(p300.current_volume, d)
            slow_withdraw(p300, d)
            p300.drop_tip()

    # qs to 4 mL with MeOH
    vol_meoh_1 = 160
    destinations = [ws1, qc1]
    for d in destinations:
        p300.pick_up_tip()
        p300.aspirate(vol_meoh_1, meoh)
        slow_withdraw(p300, meoh)
        p300.air_gap(vol_airgap_p300)
        p300.dispense(p300.current_volume, d)
        slow_withdraw(p300, d)
        p300.drop_tip()

    # WS2 and QC2
    vol_analyte_2 = 80.0
    sources_2 = hplc_vial.wells()[:47]
    destinations_2 = [ws2, qc2]
    for d in destinations_2:
        for s in sources_2:
            p300.pick_up_tip()
            p300.aspirate(vol_analyte_2, s)
            slow_withdraw(p300, s)
            p300.air_gap(vol_airgap_p300)
            p300.dispense(p300.current_volume, d)
            slow_withdraw(p300, d)
            p300.drop_tip()

    # qs to 4 mL with MeOH
    vol_meoh_2 = 240
    destinations_2 = [ws2, qc2]
    for d in destinations_2:
        p300.pick_up_tip()
        p300.aspirate(vol_meoh_2, meoh)
        slow_withdraw(p300, meoh)
        p300.air_gap(vol_airgap_p300)
        p300.dispense(p300.current_volume, d)
        slow_withdraw(p300, d)
        p300.drop_tip()

    # WS3 and QC3
    sources_3a = hplc_vial.wells()[:28]
    vol_analyte_3a = 80.0
    destinations_3 = [ws3, qc3]
    for d in destinations_3:
        for s in sources_3a:
            p300.pick_up_tip()
            p300.aspirate(vol_analyte_3a, s)
            slow_withdraw(p300, s)
            p300.air_gap(vol_airgap_p300)
            p300.dispense(p300.current_volume, d)
            slow_withdraw(p300, d)
            p300.drop_tip()

    vol_analyte_3b = 800.0
    sources_3b = hplc_vial.wells()[28:30]
    for d in destinations_3:
        for s in sources_3b:
            p1000.pick_up_tip()
            p1000.aspirate(vol_analyte_3b, s)
            slow_withdraw(p1000, s)
            p1000.air_gap(vol_airgap_p1000)
            p1000.dispense(p1000.current_volume, d)
            slow_withdraw(p1000, d)
            p1000.drop_tip()

    # qs to 4 mL with MeOH
    vol_meoh_3 = 160
    for d in destinations_3:
        p300.pick_up_tip()
        p300.aspirate(vol_meoh_3, meoh)
        slow_withdraw(p300, meoh)
        p300.air_gap(vol_airgap_p300)
        p300.dispense(p300.current_volume, d)
        slow_withdraw(p300, d)
        p300.drop_tip()

    # WS4 and QC4
    sources_4a = hplc_vial.wells()[:2]
    vol_analyte_4a = 80.0
    destinations_4 = [ws4, qc4]
    for d in destinations_4:
        for s in sources_4a:
            p300.pick_up_tip()
            p300.aspirate(vol_analyte_4a, s)
            slow_withdraw(p300, s)
            p300.air_gap(vol_airgap_p300)
            p300.dispense(p300.current_volume, d)
            slow_withdraw(p300, d)
            p300.drop_tip()

    vol_analyte_4b = 400.0
    sources_4b = hplc_vial.wells()[2:10]
    for d in destinations_4:
        for s in sources_4b:
            p1000.pick_up_tip()
            p1000.aspirate(vol_analyte_4b, s)
            slow_withdraw(p1000, s)
            p1000.air_gap(vol_airgap_p1000)
            p1000.dispense(p1000.current_volume, d)
            slow_withdraw(p1000, d)
            p1000.drop_tip()

    # qs to 4 mL with MeOH
    vol_meoh_4 = 640.0
    for d in destinations_4:
        p1000.pick_up_tip()
        p1000.aspirate(vol_meoh_4, meoh)
        slow_withdraw(p1000, meoh)
        p1000.air_gap(vol_airgap_p1000)
        p1000.dispense(p1000.current_volume, d)
        slow_withdraw(p1000, d)
        p1000.drop_tip()
