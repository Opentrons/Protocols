from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': '#6 Aliquot 100 µL in Microcentrifuge Tubes',
    'description': '''This protocol aliquots 100 µL from one \
scintiallation vial into 1.5 mL snap cap microcentrifuge tubes.''',
    'author': 'parrish.payne@opentrons.com'
    }

def get_values(*names):
    import json
    _all_values = json.loads("""{ "num_samp":46,
                                  "p300_mount":"left",
                                  "p1000_mount":"right"}""")
    return [_all_values[n] for n in names]

# Aliquot: Take the complete calibration/Quality control curve stock prepped above, aliquot 100ul each into microcentrifuge tubes.


def run(protocol: protocol_api.ProtocolContext):

    [num_samp, p300_mount] = get_values(  # noqa: F821
        "num_samp", "p300_mount")



    tips = protocol.load_labware('opentrons_96_filtertiprack_200ul', 1)
    source_scint_vial_rack = protocol.load_labware('chemglass_11x20mL', 2)
    aliquot_tuberack = protocol.load_labware(
        'opentrons_24_tuberack_nest_1.5ml_snapcap', 3)
    aliquot_tuberack_2 = protocol.load_labware(
        'clickbio_24_tuberack_1500ul', 6)

    p300 = protocol.load_instrument(
        'p300_single_gen2', p300_mount, tip_racks=[tips])

    def slow_withdraw(pip, well, z=0, delay_seconds=2.0):
        pip.default_speed /= 10
        if delay_seconds > 0:
            protocol.delay(seconds=delay_seconds)
        pip.move_to(well.top(z))
        pip.default_speed *= 10
    
    airgap_vol = 20

    def transfer(vol, source, destination, pip=p300):
        pip.aspirate(vol, source)
        slow_withdraw(pip, source)
        pip.air_gap(airgap_vol)
        pip.dispense(vol+airgap_vol, destination)
        slow_withdraw(pip, destination)

    source_vials = source_scint_vial_rack.wells_by_name()['A1']


    # by column
    all_wells_col = []
    for rack in [aliquot_tuberack, aliquot_tuberack_2]:
        for well in rack.wells():
            all_wells_col.append(well)

    # all_wells_col = [well for rack in [aliquot_tuberack, aliquot_tuberack_2] for well in rack.wells()][:num_samp]
    #
    # by row
    all_wells_row = []
    for rack in [aliquot_tuberack, aliquot_tuberack_2]:
        for row in rack.rows():
            for well in row:
                all_wells_row.append(well)

    # all_wells_row = [well for rack in [aliquot_tuberack, aliquot_tuberack_2] for row in rack.rows() for well in row][:num_samp]

    vol_aliquot = 100

    # Transfer 100 µL of calibrator or QC into 1.5 mL microcentrifuge tube
    p300.pick_up_tip()
    for well in all_wells_col[:num_samp]:
        transfer(vol_aliquot, source_vials, well)
    p300.drop_tip()
