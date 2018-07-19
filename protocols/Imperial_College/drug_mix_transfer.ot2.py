from opentrons import labware, instruments
from otcustomizers import FileInput

target_plate = labware.load('24-well-plate', 1)
mix_plate = labware.load('24-well-plate', 2)
comp_plate_1 = labware.load('96-deep-well', 3)
comp_plate_2 = labware.load('96-deep-well', 4)
comp_plate_3 = labware.load('96-deep-well', 5)

tip_rack_1 = labware.load('tiprack-10ul', 6)
tip_rack_2 = labware.load('tiprack-10ul', 7)
tip_rack_3 = labware.load('tiprack-10ul', 8)
tip_rack_4 = labware.load('tiprack-10ul', 9)

tip_racks = [tip_rack_1, tip_rack_2, tip_rack_3, tip_rack_4]

p10 = instruments.P10_Single(
    mount='left',
    tip_racks=tip_racks)


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

    for column_num in range(1, int(len(csv_list) / 27)):
        for header_num in range(0, len(headers)):
            if headers[header_num] in content:
                pass
            else:
                content[headers[header_num]] = []
            content[headers[header_num]].append(
                csv_list[column_num * 27 + header_num])

    new_dict = {}
    for well_num in range(3, 27):
        for compound in range(0, len(content[headers[well_num]])):
            if content['Plate'][compound] == '1':
                content['Plate'][compound] = comp_plate_1
            elif content['Plate'][compound] == '2':
                content['Plate'][compound] = comp_plate_2
            elif content['Plate'][compound] == '3':
                content['Plate'][compound] = comp_plate_3

        new_dict[headers[well_num]] = (list(zip(
            content[headers[well_num]], content['Plate'], content['Well'])))

        del_list = []
        for empty_volume in range(0, len(new_dict[headers[well_num]])):
            if not new_dict[headers[well_num]][empty_volume][0]:
                del_list.append(empty_volume)
        for empty_compound in del_list:
            del new_dict[headers[well_num]][empty_compound]

    return headers, new_dict


example_volumes_csv = """
Compound,Plate,Well,A1,B1,C1,D1,A2,B2,C2,D2,A3,B3,C3,D3,A4,B4,C4,D4,A5,B5,C5,D5,A6,B6,C6,D6
comp_1,1,A1,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4
comp_2,1,B1,,2,,4,,6,,8,,10,,2,,4,,6,,8,,10,,2,,4
comp_3,1,C1,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4
"""


def run_custom_protocol(volumes_csv: FileInput=example_volumes_csv):

    headers, transfer_dict = get_csv_content(volumes_csv)
    print(headers)
    print(transfer_dict)

    for well in headers[3:]:
        trasnfer_vol = 0
        count = 1
        for each_compound in transfer_dict[well]:
            volume = int(each_compound[0])
            source = each_compound[1][each_compound[2]]
            p10.transfer(volume, source, mix_plate[well])
            trasnfer_vol += volume
            if count == len(transfer_dict[well]):
                p10.transfer(trasnfer_vol, mix_plate[well], target_plate[well])
            count += 1
