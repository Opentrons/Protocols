from opentrons import labware, instruments, robot
from otcustomizers import FileInput

metadata = {
    'protocolName': 'MS Fraction Transfer Method',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

masterblock_name = 'greiner-bio-one-96-well-masterblock-0.5ml'
if masterblock_name not in labware.list():
    labware.create(
        masterblock_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=23.3
        )

autosampler_plate_name = 'agilent_autosampler_plate_2ml'
if autosampler_plate_name not in labware.list():
    labware.create(
        autosampler_plate_name,
        grid=(9, 6),
        spacing=(13, 13),
        diameter=11,
        depth=30
        )

scintillation_plate_name = 'scintillation_flat_bottom_vial_plate_20ml'
if scintillation_plate_name not in labware.list():
    labware.create(
        scintillation_plate_name,
        grid=(4, 2),
        spacing=(30, 38),
        diameter=16,
        depth=55
        )

tiprack_name = 'tipone-tiprack-300ul-filter'
if tiprack_name not in labware.list():
    labware.create(
        tiprack_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=3.5,
        depth=60
        )

# labware setup
fraction_block = labware.load(masterblock_name, '1')
autosampler_plate = labware.load(autosampler_plate_name, '2')
scintillation_plate = labware.load(scintillation_plate_name, '3')
scintillation_plate_2 = labware.load(scintillation_plate_name, '6')
trough = labware.load('trough-12row', '4')
tipracks = [labware.load(tiprack_name, slot)
            for slot in ['5', '7', '8', '9', '10', '11']]

# instrument setup
p300 = instruments.P300_Single(
    mount='left',
    tip_racks=tipracks)

# reagent setup
water = fraction_block.wells('A1')

hplc_csv_example = """
sourcePosition,sourceWell,volume,destPosition,destWell
1,C4,35,2,A1
1,C5,35,2,A2
1,C6,35,2,A3
1,C7,35,2,A4
1,C8,35,2,A5
"""

scintillation_csv_example = """
sourcePosition,sourceWell,volume,destPosition,destWell
1,D6,1000,3,A1
1,D7,2000,3,A2
1,D8,20000,3,A4
1,E9,9500,3,A3
"""

scint_volumes = {well.get_name(): [0, 0]
                 for well in scintillation_plate.wells()}


def transfer_to_scint_vials(volume, source, dest):
    global scint_volumes
    well_name = dest.get_name()
    dests = [dest, scintillation_plate_2.wells(well_name)]
    for index, value in enumerate(scint_volumes[well_name]):
        if value == 10000:
            continue
        else:
            if value + volume <= 10000:
                p300.transfer(volume, source, dests[index])
                scint_volumes[well_name][index] = value + volume
                break
            elif value + volume > 10000:
                vol_1 = 10000 - value
                volume -= vol_1
                p300.transfer(vol_1, source, dests[index])
                scint_volumes[well_name][index] = 10000


def csv_to_lists(csv_string):
    vol, source, dest = [], [], []
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    for line in info_list[1:]:
        source_plate = robot.deck.children_by_name[line[0]][0]
        source_well = line[1]
        volume = float(line[2])
        dest_plate = robot.deck.children_by_name[line[3]][0]
        dest_well = line[4]
        source.append(source_plate.wells(source_well))
        vol.append(volume)
        dest.append(dest_plate.wells(dest_well))
    return vol, source, dest


def run_custom_protocol(
        hplc_csv: FileInput=hplc_csv_example,
        scintillation_csv: FileInput=scintillation_csv_example):
    """
    Transfer from Fraction Plate to HPCL Vials
    """
    hplc_vol, hplc_source, hplc_dest = csv_to_lists(hplc_csv)

    for vol, source, dest in zip(hplc_vol, hplc_source, hplc_dest):
        p300.transfer(vol, source, dest)

    """
    Transfer from Fraction Plate to openVials
    """
    scint_vol, scint_source, scint_dest = csv_to_lists(
        scintillation_csv)

    for vol, source, dest in zip(scint_vol, scint_source, scint_dest):
        transfer_to_scint_vials(vol, source, dest)

    """
    Wash Plate With Water
    """
    for source in scint_source:
        p300.transfer(1000, water, source, new_tip='always')

    """
    Transfer Water to openVials
    """
    for source, dest in zip(scint_source, scint_dest):
        transfer_to_scint_vials(1000, source, dest)
