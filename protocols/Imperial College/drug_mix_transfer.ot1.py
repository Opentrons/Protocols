from opentrons import containers, instruments
from otcustomizers import FileInput

target_plate = containers.load('24-well-plate', 'C3')
mix_plate = containers.load('24-well-plate', 'B3')
comp_plate_1 = containers.load('96-deep-well', 'A2')
comp_plate_2 = containers.load('96-deep-well', 'B2')
comp_plate_3 = containers.load('96-deep-well', 'C2')

trash = containers.load('trash-box', 'E3')
tip_rack_1 = containers.load('tiprack-10ul', 'E2')
tip_rack_2 = containers.load('tiprack-10ul', 'E1')
tip_rack_3 = containers.load('tiprack-10ul', 'D2')
tip_rack_4 = containers.load('tiprack-10ul', 'D1')

tip_racks = [tip_rack_1, tip_rack_2, tip_rack_3, tip_rack_4]

p10 = instruments.Pipette(
    name='p10',
    trash_container=trash,
    tip_racks=tip_racks,
    max_volume=10,
    axis='a')


def csv_to_list(csv_string):
    data = [
        line.split(',')
        for line in csv_string.split('\n') if line.strip()
        if line
    ]
    return [cell for row in data for cell in row]


def get_csv_content(csv_string):
    content = {}

    csv_list = csv_to_list(csv_string)
    headers = csv_list[0:27]

    for i in range(1, int(len(csv_list)/27)):
        for j in range(0, len(headers)):
            if headers[j] in content:
                pass
            else:
                content[headers[j]] = []
            content[headers[j]].append(csv_list[i*27+j])

    new_dict = {}
    for i in range(3, 27):
        for j in range(0, len(content[headers[i]])):
            if content['Plate'][j] == '1':
                content['Plate'][j] = comp_plate_1
            elif content['Plate'][j] == '2':
                content['Plate'][j] = comp_plate_2
            elif content['Plate'][j] == '3':
                content['Plate'][j] = comp_plate_3

        new_dict[headers[i]] = (list(zip(content[headers[i]], content['Plate'],
                                content['Well'])))
        del_list = []
        for k in range(0, len(new_dict[headers[i]])):
            if not new_dict[headers[i]][k][0]:
                del_list.append(k)
        for m in del_list:
            del new_dict[headers[i]][m]

    return headers, new_dict


volumes_csv = """
Compound,Plate,Well,A1,B1,C1,D1,A2,B2,C2,D2,A3,B3,C3,D3,A4,B4,C4,D4,A5,B5,C5,D5,A6,B6,C6,D6
comp_1,1,A1,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4
comp_2,1,B1,,2,,4,,6,,8,,10,,2,,4,,6,,8,,10,,2,,4
comp_3,1,C1,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4
"""


def run_custom_protocol(volumes_csv: FileInput=volumes_csv):

    headers, transfer_dict = get_csv_content(volumes_csv)

    for i in headers[3:]:
        trasnfer_vol = 0
        for j in transfer_dict[i][:-1]:
            p10.transfer(int(j[0]), j[1][2], mix_plate[i])
            trasnfer_vol += int(j[0])
        else:
            p10.transfer(int(j[0]), j[1][2], mix_plate[i],
                         mix_after=(2, int(j[0])))
            trasnfer_vol += int(j[0])
            p10.transfer(trasnfer_vol, mix_plate[i], target_plate[i])
