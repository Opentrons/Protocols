from opentrons import labware, instruments
from otcustomizers import FileInput, StringSelection

metadata = {
    'protocolName': 'DNA Assembly',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

transfer_csv_example = """
Source Slot ,Source Well,Volume,Dest Slot,Dest Well,Mix After
5,A1,11,9,A2,
8,D4,4.5,9,A1,
8,B3,4.5,9,A1,Yes
5,A2,6.5,9,A2,
8,D4,4.5,9,A2,
8,A9,4.5,9,A2,
8,A2,4.5,9,A2,Yes
5,A1,11,9,A3,
8,E4,4.5,9,A3,
8,C8,4.5,9,A3,Yes
"""

rack_name = "beckman-coulter-24-tuberack-5"
if rack_name not in labware.list():
    labware.create(
        rack_name,
        grid=(6, 4),
        spacing=(19, 19),
        diameter=8.38,
        depth=42.9)

custom_plate_name = 'greiner-sapphire-96-PCR-plate'
if custom_plate_name not in labware.list():
    labware.create(
        custom_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.57,
        depth=20)

# labware setup
reagent_list = {
                '5': labware.load(rack_name, '5'),
                '8': labware.load('biorad-hardshell-96-PCR', '8')
                }

tipracks_10 = [labware.load('tiprack-10ul', slot)
               for slot in ['7', '10', '11']]
tipracks_50 = [labware.load('opentrons-tiprack-300ul', slot)
               for slot in ['4']]

# instruments setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=tipracks_10)
p50 = instruments.P50_Single(
    mount='right',
    tip_racks=tipracks_50)


def get_transfer_info(csv_string, reagent_list, dest_plate):
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    sources = []
    volumes = []
    dests = []
    mixes = []
    plates = {}
    for line in info_list[1:]:
        if line[0] not in reagent_list.keys():
            raise Exception('Source container in slot ' + line[0] +
                            ' does not exist.')
        else:
            source = reagent_list[line[0]].wells(line[1])

        volume = float(line[2])

        if line[3] not in plates.keys():
            plates[line[3]] = labware.load(
                dest_plate, line[3], share=True)

        if not line[5].lower().strip() == 'yes':
            mixes.append("")
        else:
                mixes.append(True)

        dest = plates[line[3]].wells(line[4])
        sources.append(source)
        volumes.append(volume)
        dests.append(dest)

    return sources, volumes, dests, mixes


def run_custom_protocol(
    dest_plate: StringSelection(
        'greiner-sapphire-96-PCR-plate', 'biorad-hardshell-96-PCR', '384-plate'
            )='greiner-sapphire-96-PCR-plate',
    transfer_csv: FileInput=transfer_csv_example
        ):

    sources, volumes, dests, mixes = get_transfer_info(
        transfer_csv, reagent_list, dest_plate)

    for vol, source, dest, mix_after in zip(volumes, sources, dests, mixes):
        if vol > 10:
            pipette = p50
        else:
            pipette = p10
        pipette.pick_up_tip()
        pipette.transfer(vol, source, dest, new_tip='never')
        if mix_after:
            if vol <= pipette.max_volume:
                mix_vol = vol
            else:
                mix_vol = pipette.max_volume
            pipette.mix(3, mix_vol, dest)
        pipette.blow_out(dest.top())
        pipette.drop_tip()
