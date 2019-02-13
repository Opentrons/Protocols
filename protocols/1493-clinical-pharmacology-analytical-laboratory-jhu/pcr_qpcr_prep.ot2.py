from opentrons import labware, instruments
from otcustomizers import FileInput

metadata = {
    'protocolName': 'PCR/qPCR Prep',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

plate_name = "microAmp-endura-384-well"
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(24, 16),
        spacing=(4.5, 4.5),
        diameter=3.1,
        depth=9.1)

tiprack_name = 'art-tiprack-100ul'
if tiprack_name not in labware.list():
    labware.create(
        tiprack_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=3.5,
        depth=60)

csv_example = """
3,4,5,3,6,7,4,1,8,9,10,2,10,11,6,6,12,11,4,12,12,6,13,14
9,6,6,6,6,6,15,16,17,18,18,18,19,9,9,9,,,,,,,,
3,4,5,3,6,7,4,1,8,9,10,2,10,11,6,6,12,11,4,12,12,6,13,14
9,6,6,6,6,6,15,16,17,18,18,18,19,9,9,9,,,,,,,,
3,4,5,3,6,7,4,1,8,9,10,2,10,11,6,6,12,11,4,12,12,6,13,14
9,6,6,6,6,6,15,16,17,18,18,18,19,9,9,9,,,,,,,,
20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,3,20,20,20
20,20,3,3,20,20,20,20,20,20,20,20,20,20,20,20,,,,,,,,
20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,3,20,20,20
20,20,3,3,20,20,20,20,20,20,20,20,20,20,20,20,,,,,,,,
20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,3,20,20,20
20,20,3,3,20,20,20,20,20,20,20,20,20,20,20,20,,,,,,,,
21,18,6,22,18,23,0,0,0,4,24,0,0,25,22,7,26,27,5,28,20,22,0,0
29,18,20,22,18,26,0,0,30,22,7,7,0,31,28,18,,,,,,,,
32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32
32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,,,,,,,,
"""

# labware setup
tuberacks = [labware.load('opentrons-tuberack-2ml-screwcap', slot)
             for slot in ['1', '4']]
plate = labware.load(plate_name, '2')
pcr_plate = labware.load('biorad-hardshell-96-PCR', '5')
tipracks_p10 = [labware.load('tiprack-10ul', slot)
                for slot in ['3', '6', '7', '8']]
tipracks_p50 = [labware.load(tiprack_name, slot)
                for slot in ['9', '10', '11']]

# instruments setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=tipracks_p10)
p50 = instruments.P50_Single(
    mount='right',
    tip_racks=tipracks_p50)


def csv_to_dict(csv_string):
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    mastermix_dict = {}
    for row_index, line in enumerate(info_list):
        alpha = chr(row_index + 65)
        for col_index, well in enumerate(line, 1):
            if well and well != '0':
                if int(well) not in mastermix_dict.keys():
                    mastermix_dict[int(well)] = []
                mastermix_dict[int(well)].append(alpha + str(col_index))
    return mastermix_dict


def create_mastermix_dict(layout_info):
    mastermix_loc_1 = [well for well in pcr_plate.wells()]
    mastermix_loc_2 = [well for tuberack in tuberacks for well in tuberack][
        len(layout_info)+1:]

    new_dict = {'dest': [], 'reagent_vol': []}
    for key in sorted(layout_info.keys()):
        rxn_num = len(layout_info[key]) + 2
        if rxn_num * 5 < 200:
            dest = mastermix_loc_1.pop(0)
        else:
            dest = mastermix_loc_2.pop(0)
        vol = rxn_num * 2.5
        new_dict['dest'].append(dest)
        new_dict['reagent_vol'].append(vol)
    return new_dict


def run_custom_protocol(
        layout_csv: FileInput=csv_example,
        mix_times: int=3,
        mix_volume: float=3):

    layout_info = csv_to_dict(layout_csv)

    # reagent setup
    taqman = tuberacks[0].wells('A1')

    # define master mixes
    samples = [well for tuberack in tuberacks for well in tuberack][
        1:len(layout_info)+1]

    mastermix_dict = create_mastermix_dict(layout_info)

    # distribute Taqman
    p50.distribute(
        mastermix_dict['reagent_vol'],
        taqman,
        mastermix_dict['dest'],
        blow_out=taqman
        )

    # transfer samples
    for vol, sample, dest in zip(
            mastermix_dict['reagent_vol'], samples, mastermix_dict['dest']):
        p50.pick_up_tip()
        p50.transfer(vol, sample, dest, new_tip='never')
        mix_vol = 50 if vol > 50 else vol
        p50.mix(3, mix_vol, dest)
        p50.drop_tip()

    # transfer and mix master mixes
    for key, mastermix in zip(
            sorted(layout_info.keys()), mastermix_dict['dest']):
        for dest in layout_info[key]:
            p10.pick_up_tip()
            p10.transfer(5, mastermix, plate.wells(dest), new_tip='never')
            p10.mix(mix_times, mix_volume, plate.wells(dest))
            p10.blow_out(plate.wells(dest).top())
            p10.drop_tip()
