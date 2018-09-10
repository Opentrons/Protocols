from opentrons import labware, instruments
from otcustomizers import FileInput

plate = labware.load('96-deep-well', '1')
tuberack = labware.load('tube-rack-15_50ml', '2')

tiprack = labware.load('tiprack-200ul', '3')
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack])

example_csv = """
Well;Lot;Volume to dispense (�l)
A01;18FT-1296;5
A02;18FT-1297;5
A03;18FT-1298;7
A04;18FT-1299;5
A05;18FT-1300;5
A06;18FT-1301;4
A07;18FT-1302;5
A08;18FT-1303;6
A09;18FT-1304;7
A10;18FT-1305;5
A11;18FT-1306;5
A12;18FT-1307;3
B01;18FT-1308;4
B02;18FT-1309;3
B03;18FT-1310;3
B04;18FT-1311;5
B05;18FT-1312;4
B06;18FT-1313;2
B07;18FT-1314;5
B08;18FT-1315;5
B09;18FT-1316;4
B10;18FT-1317;5
B11;18FT-1318;3
B12;18FT-1319;3
C01;18FT-1320;3
C02;18FT-1321;4
C03;18FT-1322;4
C04;18FT-1323;2
C05;18FT-1324;3
C06;18FT-1325;2
C07;18FT-1326;5
C08;18FT-1327;3
C09;18FT-1328;2
C10;18FT-1329;2
C11;18FT-1330;3
C12;18FT-1331;2
D01;18FT-1332;4
D02;18FT-1333;3
D03;18FT-1334;3
D04;18FT-1335;4
D05;18FT-1336;3
D06;18FT-1337;4
D07;18FT-1338;3
D08;18FT-1339;3
D09;18FT-1340;3
D10;18FT-1341;3
D11;18FT-1342;3
D12;18FT-1343;2
E01;18FT-1344;6
E02;18FT-1345;2
E03;18FT-1346;3
E04;18FT-1347;2
E05;18FT-1348;2
E06;18FT-1349;3
E07;18FT-1350;2
E08;18FT-1351;2
E09;18FT-1352;3
E10;18FT-1353;2
E11;18FT-1354;3
E12;18FT-1355;2
F01;18FT-1356;11
F02;18FT-1357;3
F03;18FT-1358;3
F04;18FT-1359;3
F05;18FT-1360;4
F06;18FT-1361;2
F07;18FT-1362;3
F08;18FT-1363;3
F09;18FT-1364;3
F10;18FT-1365;3
F11;18FT-1366;2
F12;18FT-1367;3
G01;18FT-1368;2
G02;18FT-1369;2
G03;18FT-1370;1
G04;18FT-1371;4
G05;18FT-1372;3
G06;18FT-1373;2
G07;18FT-1374;3
G08;18FT-1375;3
G09;18FT-1376;3
G10;18FT-1377;2
G11;18FT-1378;2
G12;18FT-1379;3
H01;18FT-1380;6
H02;18FT-1381;4
H03;18FT-1382;3
H04;18FT-1383;3
H05;18FT-1384;3
H06;18FT-1385;2
H07;18FT-1386;3
H08;18FT-1387;3
H09;18FT-1388;4
H10;18FT-1389;2
H11;18FT-1390;3
H12;18FT-1391;2

"""


def csv_to_dict(csv_string):
    csv_list = [line.split(';') for line in csv_string.splitlines() if line]
    headers = [cell.split(' ')[0].lower() for cell in csv_list[0]]
    new_dict = {header: [] for header in headers}
    for line in csv_list[1:]:
        for cell, header in zip(line, headers):
            if header == 'well':
                if cell[1] == '0':
                    cell = cell.replace('0', '')
            if header == 'volume':
                cell = float(cell)
            new_dict[header].append(cell)
    return new_dict


def run_custom_protocol(
    volume_csv: FileInput=example_csv
        ):

    info_dict = csv_to_dict(volume_csv)

    total_vol = sum(info_dict['volume'])

    if total_vol > 15000:
        dest = tuberack.wells('A3')
    else:
        dest = tuberack.wells('A1')

    for source, vol in zip(info_dict['well'], info_dict['volume']):
        p50.transfer(vol, plate.wells(source), dest, mix_before=(5, vol))
