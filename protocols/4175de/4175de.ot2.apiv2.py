from opentrons import protocol_api
import math

metadata = {
    'protocolName': 'Cherrypicking PCR/qPCR prep',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.7'
}

def run(protocol):
    
    [transfer_csv, total_samples, p20_mount, pcr_labware] = get_values(  # noqa: F821
    "transfer_csv", "total_samples", "p20_mount", "pcr_labware")

    # Load Tip Racks
    tiprack1 = protocol.load_labware('opentrons_96_filtertiprack_20ul', 1) 
    tiprack2 = protocol.load_labware('opentrons_96_filtertiprack_20ul', 4)
    tiprack3 = protocol.load_labware('opentrons_96_filtertiprack_20ul', 7)

    # Load Module
    temp_mod = protocol.load_module('temperature module gen2', 3)
    pcr_plate = temp_mod.load_labware(pcr_labware)
    mastermix = protocol.load_labware('opentrons_24_tuberack_generic_2ml_screwcap', 2)

    # Load labware via CSV
    transfer_info = [[val.strip().lower() for val in line.split(',')]
                     for line in transfer_csv.splitlines()
                     if line.split(',')[0].strip()][1:]
    for line in transfer_info:
        s_lw, s_slot, d_lw, d_slot = line[:2] + line[4:6]
        for slot, lw in zip([s_slot, d_slot], [s_lw, d_lw]):
            if not int(slot) in protocol.loaded_labwares:
                protocol.load_labware(lw.lower(), slot)

    # Load Pipette
    pipette_type = 'p20_single_gen2'
    pipette = protocol.load_instrument(pipette_type, p20_mount, tip_racks=[tiprack1, tiprack2, tiprack3])

    # Activate temperature module and set temperature to 4 Celsius
    # Pauses protocol until desired temperature is reached
    protocol.comment("Setting temperature to 4C on the Temperature Module")
    temp_mod.set_temperature(4)

    # Transfer Master Mix to Variable # of wells on PCR Plate sequentially
    protocol.comment("Transferring master mix to the PCR plate on the Temperature Deck")
    mastermix_wells = []
    for i in range(math.ceil(int(total_samples)/12)):
        for well in pcr_plate.rows()[i]:
            mastermix_wells.append(well)
    for well in range(int(total_samples)):
        pipette.transfer(11.5, mastermix.wells_by_name()['A6'], mastermix_wells[well], new_tip='once')

    def parse_well(well):
        letter = well[0]
        number = well[1:]
        return letter.upper() + str(int(number))

    # Transfer DNA from source wells to PCR Plate
    for line in transfer_info:
        _, s_slot, s_well, h, _, d_slot, d_well, vol = line[:8]
        source = protocol.loaded_labwares[int(s_slot)].wells_by_name()[parse_well(s_well)].bottom(float(h))
        dest = protocol.loaded_labwares[int(d_slot)].wells_by_name()[parse_well(d_well)]
        pipette.transfer(float(vol), source, dest, new_tip='always')