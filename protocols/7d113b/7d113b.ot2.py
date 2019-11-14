from opentrons import instruments, labware, robot
from otcustomizers import FileInput, StringSelection

metadata = {
    'protocolName': 'DNA Normalization with CSV',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# Create labware
dna_plate = labware.load('biorad_96_wellplate_200ul_pcr', '1', 'Sample Plate')
final_plate = labware.load('biorad_96_wellplate_200ul_pcr', '2', 'Final Plate')
tr = labware.load(
    'opentrons_15_tuberack_falcon_15ml_conical', '3', 'Tube Rack')
t50 = [labware.load('opentrons_96_tiprack_300ul', '4', '50uL Tips')]
t10 = [labware.load('opentrons_96_tiprack_10ul', '5', '10uL Tips')]

water = tr.wells('A1')

example_csv = """
A1, 100
A2, 90
H12, 1
B1, 10
C2, 12.5

"""


def run_custom_protocol(
    v_csv: FileInput = example_csv,
    p50_mount: StringSelection('left', 'right') = 'left',
    p10_mount: StringSelection('right', 'left') = 'right',
    final_concentration: float = 10,
    final_volume: int = 150
):

    # Create pipettes
    p10 = instruments.P10_Single(mount=p10_mount, tip_racks=t10)
    p50 = instruments.P50_Single(mount=p50_mount, tip_racks=t50)

    pip_ht = 60

    def water_transfer(dest, vol):
        nonlocal pip_ht

        pip = p10 if vol < 10 else p50
        if not pip.tip_attached:
            pip.pick_up_tip()
        pip.transfer(
            vol, water.bottom(pip_ht), final_plate.wells(dest), new_tip='never'
            )

        delta_h = 1.1*(vol/174.37)  # pi*r**2 + 10%
        delta_h = round(delta_h, 2)
        if pip_ht - delta_h > 4:
            pip_ht -= delta_h
        else:
            pip_ht = 4

    def dna_transfer(loc, vol):
        pip = p10 if vol < 10 else p50

        if not pip.tip_attached:
            pip.pick_up_tip()
        pip.transfer(
            vol, dna_plate.wells(loc), final_plate.wells(loc), new_tip='never'
            )
        pip.blow_out(final_plate.wells(loc).top())
        pip.drop_tip()

    src = []  # well destinations (from CSV)
    v1 = []  # volume of DNA to be transferred (determined mathematically)
    water_vol = []  # volume of water to be transferred

    vol_const = final_volume * final_concentration

    for x, y in [row.split(',') for row in v_csv.strip().splitlines() if row]:
        conc1 = float(y)
        vol1 = round(vol_const/conc1, 1)
        if vol1 > final_volume:
            vol1 = final_volume
        ww = final_volume - vol1
        src.append(x)
        v1.append(vol1)
        water_vol.append(ww)

    robot.comment('Adding correct amount of water to corresponding wells.')
    # transfer water
    for dest, vol in zip(src, water_vol):
        if vol > 0:
            water_transfer(dest, vol)

    robot.comment('Adding correct amount of DNA to corresponding wells')
    # transfer dna
    for dest, vol in zip(src, v1):
        dna_transfer(dest, vol)

    robot.comment('Protocol now complete.')
