from opentrons import labware, instruments
import math


def run_custom_protocol(
        number_of_aliquots: int=25,
        aspirate_speed: float=25,
        dispense_speed: float=50,
        volume: float=40):

    if number_of_aliquots > 239:
        raise Exception("Number of samples cannot exceed 239.")

    if number_of_aliquots < 24:
        tuberack_num = 1
    else:
        tuberack_num = math.ceil(number_of_aliquots - 23 / 24)

    # labware setup
    tuberacks = [labware.load('opentrons-tuberack-2ml-eppendorf', str(slot))
                 for slot in range(1, 11)][:tuberack_num]

    tiprack = labware.load('tiprack-200ul', '11')

    # instrument setup
    p50 = instruments.P50_Single(
        mount='left',
        tip_racks=[tiprack])

    wells = [well for tuberack in tuberacks for well in tuberack.wells()]

    p50.set_flow_rate(aspirate=aspirate_speed, dispense=dispense_speed)

    p50.pick_up_tip()
    for dest in wells[1:number_of_aliquots+1]:
        p50.transfer(volume, wells[0], dest, new_tip='never')
    p50.drop_tip()
