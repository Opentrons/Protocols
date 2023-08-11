import math
from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': '#6 Aliquot 100 µL in Microcentrifuge Tubes',
    'description': '''This protocol aliquots 100 µL from one \
scintiallation vial into 1.5 mL snap cap microcentrifuge tubes.''',
    'author': 'Parrish Payne <parrish.payne@opentrons.com>'
    }

# def get_values(*names):
#     import json
#     _all_values = json.loads("""{ "num_aliq":55,
#                                   "p1000_mount":"right"}""")
#     return [_all_values[n] for n in names]

# Aliquot: aliquot 100ul from 1 vial of calibrator or QC into microcentrifuge tubes.


def run(ctx):

    # [num_aliquots, p1000_mount] = get_values(  # noqa: F821
    #     "num_aliquots", "p1000_mount")

    num_aliquots = 55
    p1000_mount = 'right'

    # labware

    tips = ctx.load_labware('opentrons_96_filtertiprack_1000ul', 4)
    source_scint_vial_rack = ctx.load_labware('chemglass_11x20mL', 5)
    aliquot_tuberack = [ctx.load_labware(
        'opentrons_24_tuberack_nest_1.5ml_snapcap', slot) for slot in [3, 6, 9]]

    # pipettes

    p1000 = ctx.load_instrument(
        'p1000_single_gen2', p1000_mount, tip_racks=[tips])

    # variables

    vol_aliquot = 100
    disposal_volume = 100
    source_vial = source_scint_vial_rack.wells_by_name()['A1']

    # by column
    all_wells_col = []
    for rack in aliquot_tuberack:
        for well in rack.wells():
            all_wells_col.append(well)
    

    max_dests_per_asp = (p1000.tip_racks[0].wells()[0].max_volume - disposal_volume) // vol_aliquot
    all_destinations = all_wells_col[:num_aliquots]
    num_asp = math.ceil(len(all_destinations)/max_dests_per_asp)
    destination_sets = [
        all_destinations[i*max_dests_per_asp:(i+1)*max_dests_per_asp]
        if i < num_asp - 1
        else all_destinations[i*max_dests_per_asp:]
        for i in range(num_asp)]
    # print(destination_sets)
    p1000.pick_up_tip()
    p1000.aspirate(disposal_volume, source_vial)
    for d_set in destination_sets:
        # print(d_set)
        p1000.aspirate(vol_aliquot*len(d_set), source_vial)
        for d in d_set:
            p1000.dispense(vol_aliquot, d)
    p1000.dispense(p1000.current_volume, source_vial)
    p1000.drop_tip()