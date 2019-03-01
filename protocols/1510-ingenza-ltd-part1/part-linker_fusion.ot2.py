from opentrons import labware, instruments, modules
from otcustomizers import FileInput

metadata = {
    'protocolName': 'DNA Assembly',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

transfer_csv_example = """
Source Slot ,Source Well,Volume,Dest Slot,Dest Well,Mix After
5,A1,11,9,A1,
3,D4,4.5,9,A1,
1,B3,4.5,6,A1,Yes
5,A2,6.5,9,A2,
5,D4,4.5,9,A2,
4,A6,4.5,9,A2,
3,A2,4.5,9,A2,Yes
5,A1,11,9,A3,
2,D4,4.5,9,A3,
1,C4,4.5,9,A3,Yes
"""

rack_name = "beckman-coulter-24-tuberack"
if rack_name not in labware.list():
    labware.create(
        rack_name,
        grid=(6, 4),
        spacing=(19, 19),
        diameter=8.38,
        depth=42.9)

# labware setup
reagent_list = {slot: labware.load(rack_name, slot)
                for slot in ['1', '2', '3', '4', '5']}

tipracks_10 = [labware.load('tiprack-10ul', slot)
               for slot in ['10', '11']]
tipracks_50 = [labware.load('opentrons-tiprack-300ul', slot)
               for slot in ['7', '8']]

# instruments setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=tipracks_10)
p50 = instruments.P50_Single(
    mount='right',
    tip_racks=tipracks_50)


def get_transfer_info(csv_string, reagent_list):
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    sources = []
    volumes = []
    dests = []
    mixes = []
    temp_decks = []
    plates = {}
    for line in info_list[1:]:
        if line[0] not in reagent_list.keys():
            raise Exception('Source container in slot ' + line[0] +
                            ' does not exist.')
        else:
            source = reagent_list[line[0]].wells(line[1])

        volume = float(line[2])

        if line[3] not in plates.keys():
            temp_decks.append(modules.load('tempdeck', line[3]))
            plates[line[3]] = labware.load(
                'opentrons-aluminum-block-96-PCR-plate', line[3], share=True)

        if not line[5].lower().strip() == 'yes':
            mixes.append("")
        else:
                mixes.append(True)

        dest = plates[line[3]].wells(line[4])
        sources.append(source)
        volumes.append(volume)
        dests.append(dest)

    return temp_decks, sources, volumes, dests, mixes


def run_custom_protocol(transfer_csv: FileInput=transfer_csv_example):

    temp_decks, sources, volumes, dests, mixes = get_transfer_info(
        transfer_csv, reagent_list)

    [temp_deck.set_temperature(5)for temp_deck in temp_decks]
    [temp_deck.wait_for_temp() for temp_deck in temp_decks]

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
