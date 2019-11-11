from opentrons import labware, instruments
from otcustomizers import StringSelection, FileInput

metadata = {
    'protocolName': 'Cherrypicking',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
pcr_name = 'usascientific_96_wellplate_200ul_pcr'
if pcr_name not in labware.list():
    labware.create(
        pcr_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6,
        depth=11,
        volume=200
    )

tiprack_name = 'tipone_96_tiprack_10ul'
if tiprack_name not in labware.list():
    labware.create(
        tiprack_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=3.27,
        depth=39.20
    )

# load labware
cp_plate = labware.load(pcr_name, '1', 'cherrypick plate')
gblock_plate = labware.load(pcr_name, '2', 'gblock plate')
tuberack = labware.load(
    'opentrons_24_tuberack_generic_2ml_screwcap', '4')
tipracks = [
    labware.load(tiprack_name, str(slot), '10ul tiprack')
    for slot in range(5, 8)
]

# reagents
mm = tuberack.wells('A1')
nfw = tuberack.wells('B1')

ex_gblock_csv = """gBlock,Position on Source Plate,Volume of gblock (uL),\
Target Position 1,Target Position 2,Target Position 3,Target Position 4,Target\
 Position 5,Target Position 6,Target Position 7,Target Position 8,Target \
 Position 9,Target Position 10,Target Position 11,Target Position 12,Target\
  Position 13,Target Position 14,Target Position 15
,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,

"""

ex_water_csv = """Volume of NFW,Location On Target Plate,,,
,,,,
,,,,
,,,,
,,,,
"""


def run_custom_protocol(
        p10_single_mount: StringSelection('right', 'left') = 'right',
        gblock_csv: FileInput = ex_gblock_csv,
        water_csv: FileInput = ex_water_csv
):
    # pipette
    p10 = instruments.P10_Single(mount=p10_single_mount, tip_racks=tipracks)

    # transfer mm
    p10.pick_up_tip()
    for well in cp_plate.wells():
        p10.transfer(5, mm, well.bottom(0.5), new_tip='never')
        p10.blow_out(well.bottom(5))
    p10.drop_tip()

    # transfer gblock
    gblock_data = [
        [val.strip() for val in line.split(',')]
        for line in gblock_csv.splitlines()[1:] if line
    ]
    for block in gblock_data:
        if block[0]:
            g_source = gblock_plate.wells(block[1].upper())
            vol = float(block[2])
            dests = [
                cp_plate.wells(well.upper()) for well in block[3:] if well]
            for d in dests:
                p10.pick_up_tip()
                p10.transfer(vol, g_source, d, new_tip='never')
                p10.blow_out()
                p10.drop_tip()

    # transfer nuclease free water
    water_data = [
        [val.strip() for val in line.split(',')]
        for line in water_csv.splitlines()[1:] if line
    ]
    for line in water_data:
        if line[0]:
            vol = float(line[0])
            dest = cp_plate.wells(line[1].upper())
            p10.pick_up_tip()
            p10.transfer(vol, nfw, dest, new_tip='never')
            p10.blow_out()
            p10.drop_tip()
