from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection, FileInput

metadata = {
    'protocolName': 'OA/CNV Dilution from CSV',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
elution_name = 'KingFisher-96-well'
if elution_name not in labware.list():
    labware.create(
        elution_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8,
        depth=12,
        volume=1000
    )

dilution_name = 'USAScientific-96-PCR'
if dilution_name not in labware.list():
    labware.create(
        dilution_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.6,
        depth=15.5,
        volume=100
    )

trough_name = 'USAScientific-trough-1channel'
if trough_name not in labware.list():
    labware.create(
        trough_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=30,
        depth=21.5,
        volume=25000
    )

# load labware and modules
oa_dilution_plate = labware.load(dilution_name, '2', 'OA dilution plate')
cnv_dilution_plate = labware.load(dilution_name, '5', 'CNV dilution plate')
trough = labware.load(trough_name, '6', 'water trough')
tips10 = [labware.load('tiprack-10ul', slot) for slot in ['4', '7', '8']]
tips50 = [labware.load('opentrons-tiprack-300ul', slot)
          for slot in ['9', '10', '11']]

# reagents
water = trough.wells('A1')

example_csv = """011519 PGx - OA & CNV dilutions,,,,,,,,,
,,,,OA,,,CNV,,
Well,ID,Concentration,Well,ul DNA,ul H2O,Well,ul DNA,ul H2O,
A1,NTC,6.1,A1,30.0,0.0,A1,16.3,3.7,
A2,EXT_CTRL_2,447.4,A2,3.4,26.6,A2,2.0,18.0,
A3,MD11636,11.8,A3,30.0,0.0,A3,8.5,11.5,
A4,MD11637,9.0,A4,30.0,0.0,A4,11.1,8.9,
A5,MD11638,15.3,A5,30.0,0.0,A5,6.5,13.5,
A6,MD11639,16.9,A6,30.0,0.0,A6,5.9,14.1,
A7,MD11640,58.8,A7,25.5,4.5,A7,2.0,18.0,
A8,MD11641,26.5,A8,30.0,0.0,A8,3.8,16.2,
A9,MD11642,37.6,A9,30.0,0.0,A9,2.7,17.3,
A10,MD11643,15.9,A10,30.0,0.0,A10,6.3,13.7,
A11,MD11644,11.5,A11,30.0,0.0,A11,8.7,11.3,
A12,PHI17444,69.3,A12,21.6,8.4,A12,2.0,18.0,
B1,PHI17445,11.8,B1,30.0,0.0,B1,8.5,11.5,
"""


def run_custom_protocol(
        csv_file: FileInput = example_csv,
        P10_mount: StringSelection('right', 'left') = 'right',
        P50_mount: StringSelection('left', 'right') = 'left',
        magnet_setup_for_OA: StringSelection(
            'Opentrons magnetic module',
            'Thermo Fisher magnetic stand') = 'Opentrons magnetic module',
        dilution_run: StringSelection('OA', 'CNV', 'both') = 'both'
):
    # checks
    if P10_mount == P50_mount:
        raise Exception('Please select different mounts for P10 and P50 \
pipettes.')

    # pipettes
    p10 = instruments.P10_Single(mount=P10_mount, tip_racks=tips10)
    p50 = instruments.P50_Single(mount=P50_mount, tip_racks=tips50)

    # csv parse
    data = [line.split(',') for line in csv_file.splitlines() if line][3:]

    if dilution_run == 'OA' or dilution_run == 'both':

        if magnet_setup_for_OA == 'Opentrons magnetic module':
            magdeck = modules.load('magdeck', '1')
            elution_plate = labware.load(
                elution_name,
                '1',
                'elution plate',
                share=True
            )
            magdeck.engage(height=16)
        else:
            elution_plate = labware.load(
                elution_name,
                '1',
                'elution plate on magnetic stand'
            )

        p10.home()
        p10.delay(minutes=2)
        robot.comment('Incubating on magnet for 2 minutes...')

        # water to OA transfer
        for line in data:
            if line[5]:
                vol = float(line[5])
                if vol != 0:
                    dest = oa_dilution_plate.wells(line[3])
                    pipette = p10 if vol <= 10 else p50
                    if not pipette.tip_attached:
                        pipette.pick_up_tip()
                    pipette.transfer(
                        vol,
                        water,
                        dest,
                        new_tip='never'
                    )
                    pipette.blow_out()
        if p10.tip_attached:
            p10.drop_tip()
        if p50.tip_attached:
            p50.drop_tip()

        # elution to OA DNA transfer
        for line in data:
            if line[4]:
                vol = float(line[4])
                if vol != 0:
                    source = elution_plate.wells(line[0])
                    dest = oa_dilution_plate.wells(line[3])
                    pipette = p10 if vol <= 10 else p50
                    pipette.pick_up_tip()
                    pipette.transfer(
                        vol,
                        source,
                        dest,
                        new_tip='never'
                    )
                    pipette.mix(5, 9, dest)
                    pipette.blow_out()
                    pipette.drop_tip()

        if magnet_setup_for_OA == 'Opentrons magnetic module':
            magdeck.disengage()

    if dilution_run == 'CNV' or dilution_run == 'both':

        # water to CNV transfer
        for line in data:
            if line[8]:
                vol = float(line[8])
                if vol != 0:
                    dest = cnv_dilution_plate.wells(line[6])
                    pipette = p10 if vol <= 10 else p50
                    if not pipette.tip_attached:
                        pipette.pick_up_tip()
                    pipette.transfer(
                        vol,
                        water,
                        dest,
                        new_tip='never'
                    )
                    pipette.blow_out()

        # OA to CNV DNA transfer
        for line in data:
            if line[7]:
                vol = float(line[7])
                if vol != 0:
                    source = oa_dilution_plate.wells(line[3])
                    dest = cnv_dilution_plate.wells(line[6])
                    pipette = p10 if vol <= 10 else p50
                    if not pipette.tip_attached:
                        pipette.pick_up_tip()
                    pipette.transfer(
                        vol,
                        source,
                        dest,
                        new_tip='never'
                    )
                    pipette.mix(5, vol, dest)
                    pipette.blow_out()
                    pipette.drop_tip()
