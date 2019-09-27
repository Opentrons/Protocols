from opentrons import labware, instruments, robot
from otcustomizers import FileInput
import itertools

metadata = {
    'protocolName': 'DNA Concentration Normalization',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware setup
tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '2')
samples = [labware.load('opentrons-tuberack-2ml-eppendorf', slot)
           for slot in ['3', '4', '5', '6']]
pcr_plate = labware.load('PCR-strip-tall', '1')

tipracks_10 = labware.load('tiprack-10ul', '7')
tiprack_300 = labware.load('opentrons-tiprack-300ul', '9')

# instruments setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tipracks_10])
p50 = instruments.P50_Single(
    mount='right',
    tip_racks=[tiprack_300])

# reagent setup
buffer = tuberack.wells('A1')

csv_example = """
Well,Vol. of DNA  (μL),Vol. of diluent  (μL)
A1,18,8.0
B1,6.4,8.6
C1,9.2,5.8
D1,6.0,9.0
E1,14.7,0.3
F1,7.8,7.2
"""

p10_tip_count = 0
p50_tip_count = 0


def update_p10_tip_count(num):
    global p10_tip_count
    p10_tip_count += num
    if p10_tip_count > 96:
        robot.pause('The P10 tips have run out. Replenish tip rack before \
resuming protocol.')
        p10.reset_tip_tracking()
        p10_tip_count = 0


def update_p50_tip_count(num):
    global p50_tip_count
    p50_tip_count += num
    if p50_tip_count > 96:
        robot.pause('The P50 tips have run out. Replenish tip rack before \
resuming protocol.')
        p50.reset_tip_tracking()
        p50_tip_count = 0


def run_custom_protocol(
        volume_csv: FileInput=csv_example,
        max_reaction_volume: float=15,
        starting_well: str='A1',
        ending_well: str='H12'):

    def csv_to_list(csv_string):
        dests, dna_vol, diluent_vol = [], [], []
        info_list = [cell for line in csv_string.splitlines() if line
                     for cell in [line.split(',')]]
        for line in info_list[1:]:
            dest_well = line[0]
            vol_dna = float(line[1])
            if float(line[1]) > max_reaction_volume:
                vol_dna = max_reaction_volume
            vol_dil = float(line[2])
            if float(line[2]) < 1:
                vol_dil = 0
            dests.append(pcr_plate.wells(dest_well))
            dna_vol.append(vol_dna)
            diluent_vol.append(vol_dil)

        return dests, dna_vol, diluent_vol

    dests,  dna_vols, diluent_vols = csv_to_list(volume_csv)
    tube_wells = [well for rack in samples for well in tuberack.wells()]

    # distribute buffer
    for vol, dest in zip(diluent_vols, dests):
        if vol >= 5:
            pipette = p50
        elif vol > 0 and vol < 5:
            pipette = p10
        else:
            continue
        if not pipette.tip_attached:
            pipette.pick_up_tip()
            pipette.aspirate(buffer)
        if vol > pipette.current_volume:
            pipette.aspirate(buffer)
        pipette.dispense(vol, dest)
    if p50.tip_attached:
        p50.drop_tip()
        update_p50_tip_count(1)
    if p10.tip_attached:
        p10.drop_tip()
        update_p10_tip_count(1)

    # transfer and mix samples
    pcr_wells = [well for well in pcr_plate.wells()]
    tube_wells = [well for rack in tuberack for well in tuberack.wells()]
    master_list = zip(dna_vols, pcr_wells, tube_wells)
    starting_well_index = pcr_plate.get_index_from_name(starting_well)
    ending_well_index = pcr_plate.get_index_from_name(ending_well)
    for vol, dest, source in list(
            itertools.islice(
                master_list, starting_well_index, ending_well_index+1)):
        if vol > 10:
            pipette = p50
            update_p50_tip_count(1)
        else:
            pipette = p10
            update_p10_tip_count(1)
        pipette.pick_up_tip()
        pipette.transfer(vol, source, dest, new_tip='never')
        pipette.mix(3, pipette.max_volume / 2, dest)
        pipette.drop_tip()
