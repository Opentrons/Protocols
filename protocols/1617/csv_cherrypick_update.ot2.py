from opentrons import labware, instruments, robot
from otcustomizers import StringSelection, FileInput

metadata = {
    'protocolName': 'CSV Cherrypicking',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

example_csv = """source deck,Source well,volume,Destination deck,Destination \
well,mixing volume,mixing cycle
4,A1,20,1,A12,20, 1
5,D7,40,1,D12,40, 2
6,C3,70,2,G8,10, 3
"""
labware_def = """{"ordering":[["A1","B1","C1","D1","E1","F1","G1","H1",\
"I1","J1","K1","L1"\
,"M1","N1","O1","P1"],["A2","B2","C2","D2","E2","F2","G2","H2","I2","J2",\
"K2","L2","M2","N2","O2","P2"],["A3","B3","C3","D3","E3","F3","G3","H3","\
I3","J3","K3","L3","M3","N3","O3","P3"],["A4","B4","C4","D4","E4","F4","G\
4","H4","I4","J4","K4","L4","M4","N4","O4","P4"],["A5","B5","C5","D5","E5\
","F5","G5","H5","I5","J5","K5","L5","M5","N5","O5","P5"],["A6","B6","C6"\
,"D6","E6","F6","G6","H6","I6","J6","K6","L6","M6","N6","O6","P6"],["A7",\
"B7","C7","D7","E7","F7","G7","H7","I7","J7","K7","L7","M7","N7","O7","P7\
"],["A8","B8","C8","D8","E8","F8","G8","H8","I8","J8","K8","L8","M8","N8"\
,"O8","P8"],["A9","B9","C9","D9","E9","F9","G9","H9","I9","J9","K9","L9",\
"M9","N9","O9","P9"],["A10","B10","C10","D10","E10","F10","G10","H10","I1\
0","J10","K10","L10","M10","N10","O10","P10"],["A11","B11","C11","D11","E\
11","F11","G11","H11","I11","J11","K11","L11","M11","N11","O11","P11"],["\
A12","B12","C12","D12","E12","F12","G12","H12","I12","J12","K12","L12","M\
12","N12","O12","P12"],["A13","B13","C13","D13","E13","F13","G13","H13","\
I13","J13","K13","L13","M13","N13","O13","P13"],["A14","B14","C14","D14",\
"E14","F14","G14","H14","I14","J14","K14","L14","M14","N14","O14","P14"],\
["A15","B15","C15","D15","E15","F15","G15","H15","I15","J15","K15","L15",\
"M15","N15","O15","P15"],["A16","B16","C16","D16","E16","F16","G16","H16"\
,"I16","J16","K16","L16","M16","N16","O16","P16"],["A17","B17","C17","D17\
","E17","F17","G17","H17","I17","J17","K17","L17","M17","N17","O17","P17"\
],["A18","B18","C18","D18","E18","F18","G18","H18","I18","J18","K18","L18\
","M18","N18","O18","P18"],["A19","B19","C19","D19","E19","F19","G19","H1\
9","I19","J19","K19","L19","M19","N19","O19","P19"],["A20","B20","C20","D\
20","E20","F20","G20","H20","I20","J20","K20","L20","M20","N20","O20","P2\
0"],["A21","B21","C21","D21","E21","F21","G21","H21","I21","J21","K21","L\
21","M21","N21","O21","P21"],["A22","B22","C22","D22","E22","F22","G22","\
H22","I22","J22","K22","L22","M22","N22","O22","P22"],["A23","B23","C23",\
"D23","E23","F23","G23","H23","I23","J23","K23","L23","M23","N23","O23","\
P23"],["A24","B24","C24","D24","E24","F24","G24","H24","I24","J24","K24",\
"L24","M24","N24","O24","P24"]],"brand":{"brand":"Echo qualified 384-well\
(384PP)","brandId":["LABCYTE/P-05525"]},"metadata":{"displayName":"Echo Q\
ualified 384-well(384PP) 384 Well Plate 65 µL","displayCategory":"wellPla\
te","displayVolumeUnits":"µL","tags":[]},"dimensions":{"xDimension":127.6\
,"yDimension":85.4,"zDimension":14.4},"wells":{"A1":{"depth":10.9,"totalL\
iquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"\
x":12.2,"y":76.3,"z":3.5},"B1":{"depth":10.9,"totalLiquidVolume":65,"shap\
e":"rectangular","xDimension":3.8,"yDimension":3.8,"x":12.2,"y":71.8,"z":\
3.5},"C1":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDi\
mension":3.8,"yDimension":3.8,"x":12.2,"y":67.3,"z":3.5},"D1":{"depth":10\
.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimens\
ion":3.8,"x":12.2,"y":62.8,"z":3.5},"E1":{"depth":10.9,"totalLiquidVolume\
":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":12.2,"y"\
:58.3,"z":3.5},"F1":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectang\
ular","xDimension":3.8,"yDimension":3.8,"x":12.2,"y":53.8,"z":3.5},"G1":{\
"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.\
8,"yDimension":3.8,"x":12.2,"y":49.3,"z":3.5},"H1":{"depth":10.9,"totalLi\
quidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x\
":12.2,"y":44.8,"z":3.5},"I1":{"depth":10.9,"totalLiquidVolume":65,"shape\
":"rectangular","xDimension":3.8,"yDimension":3.8,"x":12.2,"y":40.3,"z":3\
.5},"J1":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDim\
ension":3.8,"yDimension":3.8,"x":12.2,"y":35.8,"z":3.5},"K1":{"depth":10.\
9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimensi\
on":3.8,"x":12.2,"y":31.3,"z":3.5},"L1":{"depth":10.9,"totalLiquidVolume"\
:65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":12.2,"y":\
26.8,"z":3.5},"M1":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangu\
lar","xDimension":3.8,"yDimension":3.8,"x":12.2,"y":22.3,"z":3.5},"N1":{"\
depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8\
,"yDimension":3.8,"x":12.2,"y":17.8,"z":3.5},"O1":{"depth":10.9,"totalLiq\
uidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x"\
:12.2,"y":13.3,"z":3.5},"P1":{"depth":10.9,"totalLiquidVolume":65,"shape"\
:"rectangular","xDimension":3.8,"yDimension":3.8,"x":12.2,"y":8.8,"z":3.5\
},"A2":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimen\
sion":3.8,"yDimension":3.8,"x":16.7,"y":76.3,"z":3.5},"B2":{"depth":10.9,\
"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension\
":3.8,"x":16.7,"y":71.8,"z":3.5},"C2":{"depth":10.9,"totalLiquidVolume":6\
5,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":16.7,"y":67\
.3,"z":3.5},"D2":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangula\
r","xDimension":3.8,"yDimension":3.8,"x":16.7,"y":62.8,"z":3.5},"E2":{"de\
pth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"\
yDimension":3.8,"x":16.7,"y":58.3,"z":3.5},"F2":{"depth":10.9,"totalLiqui\
dVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":1\
6.7,"y":53.8,"z":3.5},"G2":{"depth":10.9,"totalLiquidVolume":65,"shape":"\
rectangular","xDimension":3.8,"yDimension":3.8,"x":16.7,"y":49.3,"z":3.5}\
,"H2":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimens\
ion":3.8,"yDimension":3.8,"x":16.7,"y":44.8,"z":3.5},"I2":{"depth":10.9,"\
totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension"\
:3.8,"x":16.7,"y":40.3,"z":3.5},"J2":{"depth":10.9,"totalLiquidVolume":65\
,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":16.7,"y":35.\
8,"z":3.5},"K2":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular\
","xDimension":3.8,"yDimension":3.8,"x":16.7,"y":31.3,"z":3.5},"L2":{"dep\
th":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"y\
Dimension":3.8,"x":16.7,"y":26.8,"z":3.5},"M2":{"depth":10.9,"totalLiquid\
Volume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":16\
.7,"y":22.3,"z":3.5},"N2":{"depth":10.9,"totalLiquidVolume":65,"shape":"r\
ectangular","xDimension":3.8,"yDimension":3.8,"x":16.7,"y":17.8,"z":3.5},\
"O2":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimensi\
on":3.8,"yDimension":3.8,"x":16.7,"y":13.3,"z":3.5},"P2":{"depth":10.9,"t\
otalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":\
3.8,"x":16.7,"y":8.8,"z":3.5},"A3":{"depth":10.9,"totalLiquidVolume":65,"\
shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":21.2,"y":76.3,\
"z":3.5},"B3":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular",\
"xDimension":3.8,"yDimension":3.8,"x":21.2,"y":71.8,"z":3.5},"C3":{"depth\
":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDi\
mension":3.8,"x":21.2,"y":67.3,"z":3.5},"D3":{"depth":10.9,"totalLiquidVo\
lume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":21.2\
,"y":62.8,"z":3.5},"E3":{"depth":10.9,"totalLiquidVolume":65,"shape":"rec\
tangular","xDimension":3.8,"yDimension":3.8,"x":21.2,"y":58.3,"z":3.5},"F\
3":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension\
":3.8,"yDimension":3.8,"x":21.2,"y":53.8,"z":3.5},"G3":{"depth":10.9,"tot\
alLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.\
8,"x":21.2,"y":49.3,"z":3.5},"H3":{"depth":10.9,"totalLiquidVolume":65,"s\
hape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":21.2,"y":44.8,"\
z":3.5},"I3":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","\
xDimension":3.8,"yDimension":3.8,"x":21.2,"y":40.3,"z":3.5},"J3":{"depth"\
:10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDim\
ension":3.8,"x":21.2,"y":35.8,"z":3.5},"K3":{"depth":10.9,"totalLiquidVol\
ume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":21.2,\
"y":31.3,"z":3.5},"L3":{"depth":10.9,"totalLiquidVolume":65,"shape":"rect\
angular","xDimension":3.8,"yDimension":3.8,"x":21.2,"y":26.8,"z":3.5},"M3\
":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension"\
:3.8,"yDimension":3.8,"x":21.2,"y":22.3,"z":3.5},"N3":{"depth":10.9,"tota\
lLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8\
,"x":21.2,"y":17.8,"z":3.5},"O3":{"depth":10.9,"totalLiquidVolume":65,"sh\
ape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":21.2,"y":13.3,"z\
":3.5},"P3":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","x\
Dimension":3.8,"yDimension":3.8,"x":21.2,"y":8.8,"z":3.5},"A4":{"depth":1\
0.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimen\
sion":3.8,"x":25.7,"y":76.3,"z":3.5},"B4":{"depth":10.9,"totalLiquidVolum\
e":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":25.7,"y\
":71.8,"z":3.5},"C4":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectan\
gular","xDimension":3.8,"yDimension":3.8,"x":25.7,"y":67.3,"z":3.5},"D4":\
{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3\
.8,"yDimension":3.8,"x":25.7,"y":62.8,"z":3.5},"E4":{"depth":10.9,"totalL\
iquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"\
x":25.7,"y":58.3,"z":3.5},"F4":{"depth":10.9,"totalLiquidVolume":65,"shap\
e":"rectangular","xDimension":3.8,"yDimension":3.8,"x":25.7,"y":53.8,"z":\
3.5},"G4":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDi\
mension":3.8,"yDimension":3.8,"x":25.7,"y":49.3,"z":3.5},"H4":{"depth":10\
.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimens\
ion":3.8,"x":25.7,"y":44.8,"z":3.5},"I4":{"depth":10.9,"totalLiquidVolume\
":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":25.7,"y"\
:40.3,"z":3.5},"J4":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectang\
ular","xDimension":3.8,"yDimension":3.8,"x":25.7,"y":35.8,"z":3.5},"K4":{\
"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.\
8,"yDimension":3.8,"x":25.7,"y":31.3,"z":3.5},"L4":{"depth":10.9,"totalLi\
quidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x\
":25.7,"y":26.8,"z":3.5},"M4":{"depth":10.9,"totalLiquidVolume":65,"shape\
":"rectangular","xDimension":3.8,"yDimension":3.8,"x":25.7,"y":22.3,"z":3\
.5},"N4":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDim\
ension":3.8,"yDimension":3.8,"x":25.7,"y":17.8,"z":3.5},"O4":{"depth":10.\
9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimensi\
on":3.8,"x":25.7,"y":13.3,"z":3.5},"P4":{"depth":10.9,"totalLiquidVolume"\
:65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":25.7,"y":\
8.8,"z":3.5},"A5":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangul\
ar","xDimension":3.8,"yDimension":3.8,"x":30.2,"y":76.3,"z":3.5},"B5":{"d\
epth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,\
"yDimension":3.8,"x":30.2,"y":71.8,"z":3.5},"C5":{"depth":10.9,"totalLiqu\
idVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":\
30.2,"y":67.3,"z":3.5},"D5":{"depth":10.9,"totalLiquidVolume":65,"shape":\
"rectangular","xDimension":3.8,"yDimension":3.8,"x":30.2,"y":62.8,"z":3.5\
},"E5":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimen\
sion":3.8,"yDimension":3.8,"x":30.2,"y":58.3,"z":3.5},"F5":{"depth":10.9,\
"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension\
":3.8,"x":30.2,"y":53.8,"z":3.5},"G5":{"depth":10.9,"totalLiquidVolume":6\
5,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":30.2,"y":49\
.3,"z":3.5},"H5":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangula\
r","xDimension":3.8,"yDimension":3.8,"x":30.2,"y":44.8,"z":3.5},"I5":{"de\
pth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"\
yDimension":3.8,"x":30.2,"y":40.3,"z":3.5},"J5":{"depth":10.9,"totalLiqui\
dVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":3\
0.2,"y":35.8,"z":3.5},"K5":{"depth":10.9,"totalLiquidVolume":65,"shape":"\
rectangular","xDimension":3.8,"yDimension":3.8,"x":30.2,"y":31.3,"z":3.5}\
,"L5":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimens\
ion":3.8,"yDimension":3.8,"x":30.2,"y":26.8,"z":3.5},"M5":{"depth":10.9,"\
totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension"\
:3.8,"x":30.2,"y":22.3,"z":3.5},"N5":{"depth":10.9,"totalLiquidVolume":65\
,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":30.2,"y":17.\
8,"z":3.5},"O5":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular\
","xDimension":3.8,"yDimension":3.8,"x":30.2,"y":13.3,"z":3.5},"P5":{"dep\
th":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"y\
Dimension":3.8,"x":30.2,"y":8.8,"z":3.5},"A6":{"depth":10.9,"totalLiquidV\
olume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":34.\
7,"y":76.3,"z":3.5},"B6":{"depth":10.9,"totalLiquidVolume":65,"shape":"re\
ctangular","xDimension":3.8,"yDimension":3.8,"x":34.7,"y":71.8,"z":3.5},"\
C6":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimensio\
n":3.8,"yDimension":3.8,"x":34.7,"y":67.3,"z":3.5},"D6":{"depth":10.9,"to\
talLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3\
.8,"x":34.7,"y":62.8,"z":3.5},"E6":{"depth":10.9,"totalLiquidVolume":65,"\
shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":34.7,"y":58.3,\
"z":3.5},"F6":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular",\
"xDimension":3.8,"yDimension":3.8,"x":34.7,"y":53.8,"z":3.5},"G6":{"depth\
":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDi\
mension":3.8,"x":34.7,"y":49.3,"z":3.5},"H6":{"depth":10.9,"totalLiquidVo\
lume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":34.7\
,"y":44.8,"z":3.5},"I6":{"depth":10.9,"totalLiquidVolume":65,"shape":"rec\
tangular","xDimension":3.8,"yDimension":3.8,"x":34.7,"y":40.3,"z":3.5},"J\
6":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension\
":3.8,"yDimension":3.8,"x":34.7,"y":35.8,"z":3.5},"K6":{"depth":10.9,"tot\
alLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.\
8,"x":34.7,"y":31.3,"z":3.5},"L6":{"depth":10.9,"totalLiquidVolume":65,"s\
hape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":34.7,"y":26.8,"\
z":3.5},"M6":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","\
xDimension":3.8,"yDimension":3.8,"x":34.7,"y":22.3,"z":3.5},"N6":{"depth"\
:10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDim\
ension":3.8,"x":34.7,"y":17.8,"z":3.5},"O6":{"depth":10.9,"totalLiquidVol\
ume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":34.7,\
"y":13.3,"z":3.5},"P6":{"depth":10.9,"totalLiquidVolume":65,"shape":"rect\
angular","xDimension":3.8,"yDimension":3.8,"x":34.7,"y":8.8,"z":3.5},"A7"\
:{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":\
3.8,"yDimension":3.8,"x":39.2,"y":76.3,"z":3.5},"B7":{"depth":10.9,"total\
LiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,\
"x":39.2,"y":71.8,"z":3.5},"C7":{"depth":10.9,"totalLiquidVolume":65,"sha\
pe":"rectangular","xDimension":3.8,"yDimension":3.8,"x":39.2,"y":67.3,"z"\
:3.5},"D7":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xD\
imension":3.8,"yDimension":3.8,"x":39.2,"y":62.8,"z":3.5},"E7":{"depth":1\
0.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimen\
sion":3.8,"x":39.2,"y":58.3,"z":3.5},"F7":{"depth":10.9,"totalLiquidVolum\
e":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":39.2,"y\
":53.8,"z":3.5},"G7":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectan\
gular","xDimension":3.8,"yDimension":3.8,"x":39.2,"y":49.3,"z":3.5},"H7":\
{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3\
.8,"yDimension":3.8,"x":39.2,"y":44.8,"z":3.5},"I7":{"depth":10.9,"totalL\
iquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"\
x":39.2,"y":40.3,"z":3.5},"J7":{"depth":10.9,"totalLiquidVolume":65,"shap\
e":"rectangular","xDimension":3.8,"yDimension":3.8,"x":39.2,"y":35.8,"z":\
3.5},"K7":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDi\
mension":3.8,"yDimension":3.8,"x":39.2,"y":31.3,"z":3.5},"L7":{"depth":10\
.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimens\
ion":3.8,"x":39.2,"y":26.8,"z":3.5},"M7":{"depth":10.9,"totalLiquidVolume\
":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":39.2,"y"\
:22.3,"z":3.5},"N7":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectang\
ular","xDimension":3.8,"yDimension":3.8,"x":39.2,"y":17.8,"z":3.5},"O7":{\
"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.\
8,"yDimension":3.8,"x":39.2,"y":13.3,"z":3.5},"P7":{"depth":10.9,"totalLi\
quidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x\
":39.2,"y":8.8,"z":3.5},"A8":{"depth":10.9,"totalLiquidVolume":65,"shape"\
:"rectangular","xDimension":3.8,"yDimension":3.8,"x":43.7,"y":76.3,"z":3.\
5},"B8":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDime\
nsion":3.8,"yDimension":3.8,"x":43.7,"y":71.8,"z":3.5},"C8":{"depth":10.9\
,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimensio\
n":3.8,"x":43.7,"y":67.3,"z":3.5},"D8":{"depth":10.9,"totalLiquidVolume":\
65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":43.7,"y":6\
2.8,"z":3.5},"E8":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangul\
ar","xDimension":3.8,"yDimension":3.8,"x":43.7,"y":58.3,"z":3.5},"F8":{"d\
epth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,\
"yDimension":3.8,"x":43.7,"y":53.8,"z":3.5},"G8":{"depth":10.9,"totalLiqu\
idVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":\
43.7,"y":49.3,"z":3.5},"H8":{"depth":10.9,"totalLiquidVolume":65,"shape":\
"rectangular","xDimension":3.8,"yDimension":3.8,"x":43.7,"y":44.8,"z":3.5\
},"I8":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimen\
sion":3.8,"yDimension":3.8,"x":43.7,"y":40.3,"z":3.5},"J8":{"depth":10.9,\
"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension\
":3.8,"x":43.7,"y":35.8,"z":3.5},"K8":{"depth":10.9,"totalLiquidVolume":6\
5,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":43.7,"y":31\
.3,"z":3.5},"L8":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangula\
r","xDimension":3.8,"yDimension":3.8,"x":43.7,"y":26.8,"z":3.5},"M8":{"de\
pth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"\
yDimension":3.8,"x":43.7,"y":22.3,"z":3.5},"N8":{"depth":10.9,"totalLiqui\
dVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":4\
3.7,"y":17.8,"z":3.5},"O8":{"depth":10.9,"totalLiquidVolume":65,"shape":"\
rectangular","xDimension":3.8,"yDimension":3.8,"x":43.7,"y":13.3,"z":3.5}\
,"P8":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimens\
ion":3.8,"yDimension":3.8,"x":43.7,"y":8.8,"z":3.5},"A9":{"depth":10.9,"t\
otalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":\
3.8,"x":48.2,"y":76.3,"z":3.5},"B9":{"depth":10.9,"totalLiquidVolume":65,\
"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":48.2,"y":71.8\
,"z":3.5},"C9":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular"\
,"xDimension":3.8,"yDimension":3.8,"x":48.2,"y":67.3,"z":3.5},"D9":{"dept\
h":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yD\
imension":3.8,"x":48.2,"y":62.8,"z":3.5},"E9":{"depth":10.9,"totalLiquidV\
olume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":48.\
2,"y":58.3,"z":3.5},"F9":{"depth":10.9,"totalLiquidVolume":65,"shape":"re\
ctangular","xDimension":3.8,"yDimension":3.8,"x":48.2,"y":53.8,"z":3.5},"\
G9":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimensio\
n":3.8,"yDimension":3.8,"x":48.2,"y":49.3,"z":3.5},"H9":{"depth":10.9,"to\
talLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3\
.8,"x":48.2,"y":44.8,"z":3.5},"I9":{"depth":10.9,"totalLiquidVolume":65,"\
shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":48.2,"y":40.3,\
"z":3.5},"J9":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular",\
"xDimension":3.8,"yDimension":3.8,"x":48.2,"y":35.8,"z":3.5},"K9":{"depth\
":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDi\
mension":3.8,"x":48.2,"y":31.3,"z":3.5},"L9":{"depth":10.9,"totalLiquidVo\
lume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":48.2\
,"y":26.8,"z":3.5},"M9":{"depth":10.9,"totalLiquidVolume":65,"shape":"rec\
tangular","xDimension":3.8,"yDimension":3.8,"x":48.2,"y":22.3,"z":3.5},"N\
9":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension\
":3.8,"yDimension":3.8,"x":48.2,"y":17.8,"z":3.5},"O9":{"depth":10.9,"tot\
alLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.\
8,"x":48.2,"y":13.3,"z":3.5},"P9":{"depth":10.9,"totalLiquidVolume":65,"s\
hape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":48.2,"y":8.8,"z\
":3.5},"A10":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","\
xDimension":3.8,"yDimension":3.8,"x":52.7,"y":76.3,"z":3.5},"B10":{"depth\
":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDi\
mension":3.8,"x":52.7,"y":71.8,"z":3.5},"C10":{"depth":10.9,"totalLiquidV\
olume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":52.\
7,"y":67.3,"z":3.5},"D10":{"depth":10.9,"totalLiquidVolume":65,"shape":"r\
ectangular","xDimension":3.8,"yDimension":3.8,"x":52.7,"y":62.8,"z":3.5},\
"E10":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimens\
ion":3.8,"yDimension":3.8,"x":52.7,"y":58.3,"z":3.5},"F10":{"depth":10.9,\
"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension\
":3.8,"x":52.7,"y":53.8,"z":3.5},"G10":{"depth":10.9,"totalLiquidVolume":\
65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":52.7,"y":4\
9.3,"z":3.5},"H10":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangu\
lar","xDimension":3.8,"yDimension":3.8,"x":52.7,"y":44.8,"z":3.5},"I10":{\
"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.\
8,"yDimension":3.8,"x":52.7,"y":40.3,"z":3.5},"J10":{"depth":10.9,"totalL\
iquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"\
x":52.7,"y":35.8,"z":3.5},"K10":{"depth":10.9,"totalLiquidVolume":65,"sha\
pe":"rectangular","xDimension":3.8,"yDimension":3.8,"x":52.7,"y":31.3,"z"\
:3.5},"L10":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","x\
Dimension":3.8,"yDimension":3.8,"x":52.7,"y":26.8,"z":3.5},"M10":{"depth"\
:10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDim\
ension":3.8,"x":52.7,"y":22.3,"z":3.5},"N10":{"depth":10.9,"totalLiquidVo\
lume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":52.7\
,"y":17.8,"z":3.5},"O10":{"depth":10.9,"totalLiquidVolume":65,"shape":"re\
ctangular","xDimension":3.8,"yDimension":3.8,"x":52.7,"y":13.3,"z":3.5},"\
P10":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimensi\
on":3.8,"yDimension":3.8,"x":52.7,"y":8.8,"z":3.5},"A11":{"depth":10.9,"t\
otalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":\
3.8,"x":57.2,"y":76.3,"z":3.5},"B11":{"depth":10.9,"totalLiquidVolume":65\
,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":57.2,"y":71.\
8,"z":3.5},"C11":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangula\
r","xDimension":3.8,"yDimension":3.8,"x":57.2,"y":67.3,"z":3.5},"D11":{"d\
epth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,\
"yDimension":3.8,"x":57.2,"y":62.8,"z":3.5},"E11":{"depth":10.9,"totalLiq\
uidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x"\
:57.2,"y":58.3,"z":3.5},"F11":{"depth":10.9,"totalLiquidVolume":65,"shape\
":"rectangular","xDimension":3.8,"yDimension":3.8,"x":57.2,"y":53.8,"z":3\
.5},"G11":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDi\
mension":3.8,"yDimension":3.8,"x":57.2,"y":49.3,"z":3.5},"H11":{"depth":1\
0.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimen\
sion":3.8,"x":57.2,"y":44.8,"z":3.5},"I11":{"depth":10.9,"totalLiquidVolu\
me":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":57.2,"\
y":40.3,"z":3.5},"J11":{"depth":10.9,"totalLiquidVolume":65,"shape":"rect\
angular","xDimension":3.8,"yDimension":3.8,"x":57.2,"y":35.8,"z":3.5},"K1\
1":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension\
":3.8,"yDimension":3.8,"x":57.2,"y":31.3,"z":3.5},"L11":{"depth":10.9,"to\
talLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3\
.8,"x":57.2,"y":26.8,"z":3.5},"M11":{"depth":10.9,"totalLiquidVolume":65,\
"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":57.2,"y":22.3\
,"z":3.5},"N11":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular\
","xDimension":3.8,"yDimension":3.8,"x":57.2,"y":17.8,"z":3.5},"O11":{"de\
pth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"\
yDimension":3.8,"x":57.2,"y":13.3,"z":3.5},"P11":{"depth":10.9,"totalLiqu\
idVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":\
57.2,"y":8.8,"z":3.5},"A12":{"depth":10.9,"totalLiquidVolume":65,"shape":\
"rectangular","xDimension":3.8,"yDimension":3.8,"x":61.7,"y":76.3,"z":3.5\
},"B12":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDime\
nsion":3.8,"yDimension":3.8,"x":61.7,"y":71.8,"z":3.5},"C12":{"depth":10.\
9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimensi\
on":3.8,"x":61.7,"y":67.3,"z":3.5},"D12":{"depth":10.9,"totalLiquidVolume\
":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":61.7,"y"\
:62.8,"z":3.5},"E12":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectan\
gular","xDimension":3.8,"yDimension":3.8,"x":61.7,"y":58.3,"z":3.5},"F12"\
:{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":\
3.8,"yDimension":3.8,"x":61.7,"y":53.8,"z":3.5},"G12":{"depth":10.9,"tota\
lLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8\
,"x":61.7,"y":49.3,"z":3.5},"H12":{"depth":10.9,"totalLiquidVolume":65,"s\
hape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":61.7,"y":44.8,"\
z":3.5},"I12":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular",\
"xDimension":3.8,"yDimension":3.8,"x":61.7,"y":40.3,"z":3.5},"J12":{"dept\
h":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yD\
imension":3.8,"x":61.7,"y":35.8,"z":3.5},"K12":{"depth":10.9,"totalLiquid\
Volume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":61\
.7,"y":31.3,"z":3.5},"L12":{"depth":10.9,"totalLiquidVolume":65,"shape":"\
rectangular","xDimension":3.8,"yDimension":3.8,"x":61.7,"y":26.8,"z":3.5}\
,"M12":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimen\
sion":3.8,"yDimension":3.8,"x":61.7,"y":22.3,"z":3.5},"N12":{"depth":10.9\
,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimensio\
n":3.8,"x":61.7,"y":17.8,"z":3.5},"O12":{"depth":10.9,"totalLiquidVolume"\
:65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":61.7,"y":\
13.3,"z":3.5},"P12":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectang\
ular","xDimension":3.8,"yDimension":3.8,"x":61.7,"y":8.8,"z":3.5},"A13":{\
"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.\
8,"yDimension":3.8,"x":66.2,"y":76.3,"z":3.5},"B13":{"depth":10.9,"totalL\
iquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"\
x":66.2,"y":71.8,"z":3.5},"C13":{"depth":10.9,"totalLiquidVolume":65,"sha\
pe":"rectangular","xDimension":3.8,"yDimension":3.8,"x":66.2,"y":67.3,"z"\
:3.5},"D13":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","x\
Dimension":3.8,"yDimension":3.8,"x":66.2,"y":62.8,"z":3.5},"E13":{"depth"\
:10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDim\
ension":3.8,"x":66.2,"y":58.3,"z":3.5},"F13":{"depth":10.9,"totalLiquidVo\
lume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":66.2\
,"y":53.8,"z":3.5},"G13":{"depth":10.9,"totalLiquidVolume":65,"shape":"re\
ctangular","xDimension":3.8,"yDimension":3.8,"x":66.2,"y":49.3,"z":3.5},"\
H13":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimensi\
on":3.8,"yDimension":3.8,"x":66.2,"y":44.8,"z":3.5},"I13":{"depth":10.9,"\
totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension"\
:3.8,"x":66.2,"y":40.3,"z":3.5},"J13":{"depth":10.9,"totalLiquidVolume":6\
5,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":66.2,"y":35\
.8,"z":3.5},"K13":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangul\
ar","xDimension":3.8,"yDimension":3.8,"x":66.2,"y":31.3,"z":3.5},"L13":{"\
depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8\
,"yDimension":3.8,"x":66.2,"y":26.8,"z":3.5},"M13":{"depth":10.9,"totalLi\
quidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x\
":66.2,"y":22.3,"z":3.5},"N13":{"depth":10.9,"totalLiquidVolume":65,"shap\
e":"rectangular","xDimension":3.8,"yDimension":3.8,"x":66.2,"y":17.8,"z":\
3.5},"O13":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xD\
imension":3.8,"yDimension":3.8,"x":66.2,"y":13.3,"z":3.5},"P13":{"depth":\
10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDime\
nsion":3.8,"x":66.2,"y":8.8,"z":3.5},"A14":{"depth":10.9,"totalLiquidVolu\
me":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":70.7,"\
y":76.3,"z":3.5},"B14":{"depth":10.9,"totalLiquidVolume":65,"shape":"rect\
angular","xDimension":3.8,"yDimension":3.8,"x":70.7,"y":71.8,"z":3.5},"C1\
4":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension\
":3.8,"yDimension":3.8,"x":70.7,"y":67.3,"z":3.5},"D14":{"depth":10.9,"to\
talLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3\
.8,"x":70.7,"y":62.8,"z":3.5},"E14":{"depth":10.9,"totalLiquidVolume":65,\
"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":70.7,"y":58.3\
,"z":3.5},"F14":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular\
","xDimension":3.8,"yDimension":3.8,"x":70.7,"y":53.8,"z":3.5},"G14":{"de\
pth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"\
yDimension":3.8,"x":70.7,"y":49.3,"z":3.5},"H14":{"depth":10.9,"totalLiqu\
idVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":\
70.7,"y":44.8,"z":3.5},"I14":{"depth":10.9,"totalLiquidVolume":65,"shape"\
:"rectangular","xDimension":3.8,"yDimension":3.8,"x":70.7,"y":40.3,"z":3.\
5},"J14":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDim\
ension":3.8,"yDimension":3.8,"x":70.7,"y":35.8,"z":3.5},"K14":{"depth":10\
.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimens\
ion":3.8,"x":70.7,"y":31.3,"z":3.5},"L14":{"depth":10.9,"totalLiquidVolum\
e":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":70.7,"y\
":26.8,"z":3.5},"M14":{"depth":10.9,"totalLiquidVolume":65,"shape":"recta\
ngular","xDimension":3.8,"yDimension":3.8,"x":70.7,"y":22.3,"z":3.5},"N14\
":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension"\
:3.8,"yDimension":3.8,"x":70.7,"y":17.8,"z":3.5},"O14":{"depth":10.9,"tot\
alLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.\
8,"x":70.7,"y":13.3,"z":3.5},"P14":{"depth":10.9,"totalLiquidVolume":65,"\
shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":70.7,"y":8.8,"\
z":3.5},"A15":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular",\
"xDimension":3.8,"yDimension":3.8,"x":75.2,"y":76.3,"z":3.5},"B15":{"dept\
h":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yD\
imension":3.8,"x":75.2,"y":71.8,"z":3.5},"C15":{"depth":10.9,"totalLiquid\
Volume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":75\
.2,"y":67.3,"z":3.5},"D15":{"depth":10.9,"totalLiquidVolume":65,"shape":"\
rectangular","xDimension":3.8,"yDimension":3.8,"x":75.2,"y":62.8,"z":3.5}\
,"E15":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimen\
sion":3.8,"yDimension":3.8,"x":75.2,"y":58.3,"z":3.5},"F15":{"depth":10.9\
,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimensio\
n":3.8,"x":75.2,"y":53.8,"z":3.5},"G15":{"depth":10.9,"totalLiquidVolume"\
:65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":75.2,"y":\
49.3,"z":3.5},"H15":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectang\
ular","xDimension":3.8,"yDimension":3.8,"x":75.2,"y":44.8,"z":3.5},"I15":\
{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3\
.8,"yDimension":3.8,"x":75.2,"y":40.3,"z":3.5},"J15":{"depth":10.9,"total\
LiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,\
"x":75.2,"y":35.8,"z":3.5},"K15":{"depth":10.9,"totalLiquidVolume":65,"sh\
ape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":75.2,"y":31.3,"z\
":3.5},"L15":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","\
xDimension":3.8,"yDimension":3.8,"x":75.2,"y":26.8,"z":3.5},"M15":{"depth\
":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDi\
mension":3.8,"x":75.2,"y":22.3,"z":3.5},"N15":{"depth":10.9,"totalLiquidV\
olume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":75.\
2,"y":17.8,"z":3.5},"O15":{"depth":10.9,"totalLiquidVolume":65,"shape":"r\
ectangular","xDimension":3.8,"yDimension":3.8,"x":75.2,"y":13.3,"z":3.5},\
"P15":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimens\
ion":3.8,"yDimension":3.8,"x":75.2,"y":8.8,"z":3.5},"A16":{"depth":10.9,"\
totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension"\
:3.8,"x":79.7,"y":76.3,"z":3.5},"B16":{"depth":10.9,"totalLiquidVolume":6\
5,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":79.7,"y":71\
.8,"z":3.5},"C16":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangul\
ar","xDimension":3.8,"yDimension":3.8,"x":79.7,"y":67.3,"z":3.5},"D16":{"\
depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8\
,"yDimension":3.8,"x":79.7,"y":62.8,"z":3.5},"E16":{"depth":10.9,"totalLi\
quidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x\
":79.7,"y":58.3,"z":3.5},"F16":{"depth":10.9,"totalLiquidVolume":65,"shap\
e":"rectangular","xDimension":3.8,"yDimension":3.8,"x":79.7,"y":53.8,"z":\
3.5},"G16":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xD\
imension":3.8,"yDimension":3.8,"x":79.7,"y":49.3,"z":3.5},"H16":{"depth":\
10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDime\
nsion":3.8,"x":79.7,"y":44.8,"z":3.5},"I16":{"depth":10.9,"totalLiquidVol\
ume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":79.7,\
"y":40.3,"z":3.5},"J16":{"depth":10.9,"totalLiquidVolume":65,"shape":"rec\
tangular","xDimension":3.8,"yDimension":3.8,"x":79.7,"y":35.8,"z":3.5},"K\
16":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimensio\
n":3.8,"yDimension":3.8,"x":79.7,"y":31.3,"z":3.5},"L16":{"depth":10.9,"t\
otalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":\
3.8,"x":79.7,"y":26.8,"z":3.5},"M16":{"depth":10.9,"totalLiquidVolume":65\
,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":79.7,"y":22.\
3,"z":3.5},"N16":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangula\
r","xDimension":3.8,"yDimension":3.8,"x":79.7,"y":17.8,"z":3.5},"O16":{"d\
epth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,\
"yDimension":3.8,"x":79.7,"y":13.3,"z":3.5},"P16":{"depth":10.9,"totalLiq\
uidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x"\
:79.7,"y":8.8,"z":3.5},"A17":{"depth":10.9,"totalLiquidVolume":65,"shape"\
:"rectangular","xDimension":3.8,"yDimension":3.8,"x":84.2,"y":76.3,"z":3.\
5},"B17":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDim\
ension":3.8,"yDimension":3.8,"x":84.2,"y":71.8,"z":3.5},"C17":{"depth":10\
.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimens\
ion":3.8,"x":84.2,"y":67.3,"z":3.5},"D17":{"depth":10.9,"totalLiquidVolum\
e":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":84.2,"y\
":62.8,"z":3.5},"E17":{"depth":10.9,"totalLiquidVolume":65,"shape":"recta\
ngular","xDimension":3.8,"yDimension":3.8,"x":84.2,"y":58.3,"z":3.5},"F17\
":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension"\
:3.8,"yDimension":3.8,"x":84.2,"y":53.8,"z":3.5},"G17":{"depth":10.9,"tot\
alLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.\
8,"x":84.2,"y":49.3,"z":3.5},"H17":{"depth":10.9,"totalLiquidVolume":65,"\
shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":84.2,"y":44.8,\
"z":3.5},"I17":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular"\
,"xDimension":3.8,"yDimension":3.8,"x":84.2,"y":40.3,"z":3.5},"J17":{"dep\
th":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"y\
Dimension":3.8,"x":84.2,"y":35.8,"z":3.5},"K17":{"depth":10.9,"totalLiqui\
dVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":8\
4.2,"y":31.3,"z":3.5},"L17":{"depth":10.9,"totalLiquidVolume":65,"shape":\
"rectangular","xDimension":3.8,"yDimension":3.8,"x":84.2,"y":26.8,"z":3.5\
},"M17":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDime\
nsion":3.8,"yDimension":3.8,"x":84.2,"y":22.3,"z":3.5},"N17":{"depth":10.\
9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimensi\
on":3.8,"x":84.2,"y":17.8,"z":3.5},"O17":{"depth":10.9,"totalLiquidVolume\
":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":84.2,"y"\
:13.3,"z":3.5},"P17":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectan\
gular","xDimension":3.8,"yDimension":3.8,"x":84.2,"y":8.8,"z":3.5},"A18":\
{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3\
.8,"yDimension":3.8,"x":88.7,"y":76.3,"z":3.5},"B18":{"depth":10.9,"total\
LiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,\
"x":88.7,"y":71.8,"z":3.5},"C18":{"depth":10.9,"totalLiquidVolume":65,"sh\
ape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":88.7,"y":67.3,"z\
":3.5},"D18":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","\
xDimension":3.8,"yDimension":3.8,"x":88.7,"y":62.8,"z":3.5},"E18":{"depth\
":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDi\
mension":3.8,"x":88.7,"y":58.3,"z":3.5},"F18":{"depth":10.9,"totalLiquidV\
olume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":88.\
7,"y":53.8,"z":3.5},"G18":{"depth":10.9,"totalLiquidVolume":65,"shape":"r\
ectangular","xDimension":3.8,"yDimension":3.8,"x":88.7,"y":49.3,"z":3.5},\
"H18":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimens\
ion":3.8,"yDimension":3.8,"x":88.7,"y":44.8,"z":3.5},"I18":{"depth":10.9,\
"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension\
":3.8,"x":88.7,"y":40.3,"z":3.5},"J18":{"depth":10.9,"totalLiquidVolume":\
65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":88.7,"y":3\
5.8,"z":3.5},"K18":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangu\
lar","xDimension":3.8,"yDimension":3.8,"x":88.7,"y":31.3,"z":3.5},"L18":{\
"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.\
8,"yDimension":3.8,"x":88.7,"y":26.8,"z":3.5},"M18":{"depth":10.9,"totalL\
iquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"\
x":88.7,"y":22.3,"z":3.5},"N18":{"depth":10.9,"totalLiquidVolume":65,"sha\
pe":"rectangular","xDimension":3.8,"yDimension":3.8,"x":88.7,"y":17.8,"z"\
:3.5},"O18":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","x\
Dimension":3.8,"yDimension":3.8,"x":88.7,"y":13.3,"z":3.5},"P18":{"depth"\
:10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDim\
ension":3.8,"x":88.7,"y":8.8,"z":3.5},"A19":{"depth":10.9,"totalLiquidVol\
ume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":93.2,\
"y":76.3,"z":3.5},"B19":{"depth":10.9,"totalLiquidVolume":65,"shape":"rec\
tangular","xDimension":3.8,"yDimension":3.8,"x":93.2,"y":71.8,"z":3.5},"C\
19":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimensio\
n":3.8,"yDimension":3.8,"x":93.2,"y":67.3,"z":3.5},"D19":{"depth":10.9,"t\
otalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":\
3.8,"x":93.2,"y":62.8,"z":3.5},"E19":{"depth":10.9,"totalLiquidVolume":65\
,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":93.2,"y":58.\
3,"z":3.5},"F19":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangula\
r","xDimension":3.8,"yDimension":3.8,"x":93.2,"y":53.8,"z":3.5},"G19":{"d\
epth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,\
"yDimension":3.8,"x":93.2,"y":49.3,"z":3.5},"H19":{"depth":10.9,"totalLiq\
uidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x"\
:93.2,"y":44.8,"z":3.5},"I19":{"depth":10.9,"totalLiquidVolume":65,"shape\
":"rectangular","xDimension":3.8,"yDimension":3.8,"x":93.2,"y":40.3,"z":3\
.5},"J19":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDi\
mension":3.8,"yDimension":3.8,"x":93.2,"y":35.8,"z":3.5},"K19":{"depth":1\
0.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimen\
sion":3.8,"x":93.2,"y":31.3,"z":3.5},"L19":{"depth":10.9,"totalLiquidVolu\
me":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":93.2,"\
y":26.8,"z":3.5},"M19":{"depth":10.9,"totalLiquidVolume":65,"shape":"rect\
angular","xDimension":3.8,"yDimension":3.8,"x":93.2,"y":22.3,"z":3.5},"N1\
9":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension\
":3.8,"yDimension":3.8,"x":93.2,"y":17.8,"z":3.5},"O19":{"depth":10.9,"to\
talLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3\
.8,"x":93.2,"y":13.3,"z":3.5},"P19":{"depth":10.9,"totalLiquidVolume":65,\
"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":93.2,"y":8.8,\
"z":3.5},"A20":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular"\
,"xDimension":3.8,"yDimension":3.8,"x":97.7,"y":76.3,"z":3.5},"B20":{"dep\
th":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"y\
Dimension":3.8,"x":97.7,"y":71.8,"z":3.5},"C20":{"depth":10.9,"totalLiqui\
dVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":9\
7.7,"y":67.3,"z":3.5},"D20":{"depth":10.9,"totalLiquidVolume":65,"shape":\
"rectangular","xDimension":3.8,"yDimension":3.8,"x":97.7,"y":62.8,"z":3.5\
},"E20":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDime\
nsion":3.8,"yDimension":3.8,"x":97.7,"y":58.3,"z":3.5},"F20":{"depth":10.\
9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimensi\
on":3.8,"x":97.7,"y":53.8,"z":3.5},"G20":{"depth":10.9,"totalLiquidVolume\
":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":97.7,"y"\
:49.3,"z":3.5},"H20":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectan\
gular","xDimension":3.8,"yDimension":3.8,"x":97.7,"y":44.8,"z":3.5},"I20"\
:{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":\
3.8,"yDimension":3.8,"x":97.7,"y":40.3,"z":3.5},"J20":{"depth":10.9,"tota\
lLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8\
,"x":97.7,"y":35.8,"z":3.5},"K20":{"depth":10.9,"totalLiquidVolume":65,"s\
hape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":97.7,"y":31.3,"\
z":3.5},"L20":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular",\
"xDimension":3.8,"yDimension":3.8,"x":97.7,"y":26.8,"z":3.5},"M20":{"dept\
h":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yD\
imension":3.8,"x":97.7,"y":22.3,"z":3.5},"N20":{"depth":10.9,"totalLiquid\
Volume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":97\
.7,"y":17.8,"z":3.5},"O20":{"depth":10.9,"totalLiquidVolume":65,"shape":"\
rectangular","xDimension":3.8,"yDimension":3.8,"x":97.7,"y":13.3,"z":3.5}\
,"P20":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimen\
sion":3.8,"yDimension":3.8,"x":97.7,"y":8.8,"z":3.5},"A21":{"depth":10.9,\
"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension\
":3.8,"x":102.2,"y":76.3,"z":3.5},"B21":{"depth":10.9,"totalLiquidVolume"\
:65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":102.2,"y"\
:71.8,"z":3.5},"C21":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectan\
gular","xDimension":3.8,"yDimension":3.8,"x":102.2,"y":67.3,"z":3.5},"D21\
":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension"\
:3.8,"yDimension":3.8,"x":102.2,"y":62.8,"z":3.5},"E21":{"depth":10.9,"to\
talLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3\
.8,"x":102.2,"y":58.3,"z":3.5},"F21":{"depth":10.9,"totalLiquidVolume":65\
,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":102.2,"y":53\
.8,"z":3.5},"G21":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangul\
ar","xDimension":3.8,"yDimension":3.8,"x":102.2,"y":49.3,"z":3.5},"H21":{\
"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.\
8,"yDimension":3.8,"x":102.2,"y":44.8,"z":3.5},"I21":{"depth":10.9,"total\
LiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,\
"x":102.2,"y":40.3,"z":3.5},"J21":{"depth":10.9,"totalLiquidVolume":65,"s\
hape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":102.2,"y":35.8,\
"z":3.5},"K21":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular"\
,"xDimension":3.8,"yDimension":3.8,"x":102.2,"y":31.3,"z":3.5},"L21":{"de\
pth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"\
yDimension":3.8,"x":102.2,"y":26.8,"z":3.5},"M21":{"depth":10.9,"totalLiq\
uidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x"\
:102.2,"y":22.3,"z":3.5},"N21":{"depth":10.9,"totalLiquidVolume":65,"shap\
e":"rectangular","xDimension":3.8,"yDimension":3.8,"x":102.2,"y":17.8,"z"\
:3.5},"O21":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","x\
Dimension":3.8,"yDimension":3.8,"x":102.2,"y":13.3,"z":3.5},"P21":{"depth\
":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDi\
mension":3.8,"x":102.2,"y":8.8,"z":3.5},"A22":{"depth":10.9,"totalLiquidV\
olume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":106\
.7,"y":76.3,"z":3.5},"B22":{"depth":10.9,"totalLiquidVolume":65,"shape":"\
rectangular","xDimension":3.8,"yDimension":3.8,"x":106.7,"y":71.8,"z":3.5\
},"C22":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDime\
nsion":3.8,"yDimension":3.8,"x":106.7,"y":67.3,"z":3.5},"D22":{"depth":10\
.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimens\
ion":3.8,"x":106.7,"y":62.8,"z":3.5},"E22":{"depth":10.9,"totalLiquidVolu\
me":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":106.7,\
"y":58.3,"z":3.5},"F22":{"depth":10.9,"totalLiquidVolume":65,"shape":"rec\
tangular","xDimension":3.8,"yDimension":3.8,"x":106.7,"y":53.8,"z":3.5},"\
G22":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimensi\
on":3.8,"yDimension":3.8,"x":106.7,"y":49.3,"z":3.5},"H22":{"depth":10.9,\
"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension\
":3.8,"x":106.7,"y":44.8,"z":3.5},"I22":{"depth":10.9,"totalLiquidVolume"\
:65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":106.7,"y"\
:40.3,"z":3.5},"J22":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectan\
gular","xDimension":3.8,"yDimension":3.8,"x":106.7,"y":35.8,"z":3.5},"K22\
":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension"\
:3.8,"yDimension":3.8,"x":106.7,"y":31.3,"z":3.5},"L22":{"depth":10.9,"to\
talLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3\
.8,"x":106.7,"y":26.8,"z":3.5},"M22":{"depth":10.9,"totalLiquidVolume":65\
,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":106.7,"y":22\
.3,"z":3.5},"N22":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangul\
ar","xDimension":3.8,"yDimension":3.8,"x":106.7,"y":17.8,"z":3.5},"O22":{\
"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.\
8,"yDimension":3.8,"x":106.7,"y":13.3,"z":3.5},"P22":{"depth":10.9,"total\
LiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,\
"x":106.7,"y":8.8,"z":3.5},"A23":{"depth":10.9,"totalLiquidVolume":65,"sh\
ape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":111.2,"y":76.3,"\
z":3.5},"B23":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular",\
"xDimension":3.8,"yDimension":3.8,"x":111.2,"y":71.8,"z":3.5},"C23":{"dep\
th":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"y\
Dimension":3.8,"x":111.2,"y":67.3,"z":3.5},"D23":{"depth":10.9,"totalLiqu\
idVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":\
111.2,"y":62.8,"z":3.5},"E23":{"depth":10.9,"totalLiquidVolume":65,"shape\
":"rectangular","xDimension":3.8,"yDimension":3.8,"x":111.2,"y":58.3,"z":\
3.5},"F23":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xD\
imension":3.8,"yDimension":3.8,"x":111.2,"y":53.8,"z":3.5},"G23":{"depth"\
:10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDim\
ension":3.8,"x":111.2,"y":49.3,"z":3.5},"H23":{"depth":10.9,"totalLiquidV\
olume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":111\
.2,"y":44.8,"z":3.5},"I23":{"depth":10.9,"totalLiquidVolume":65,"shape":"\
rectangular","xDimension":3.8,"yDimension":3.8,"x":111.2,"y":40.3,"z":3.5\
},"J23":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDime\
nsion":3.8,"yDimension":3.8,"x":111.2,"y":35.8,"z":3.5},"K23":{"depth":10\
.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimens\
ion":3.8,"x":111.2,"y":31.3,"z":3.5},"L23":{"depth":10.9,"totalLiquidVolu\
me":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":111.2,\
"y":26.8,"z":3.5},"M23":{"depth":10.9,"totalLiquidVolume":65,"shape":"rec\
tangular","xDimension":3.8,"yDimension":3.8,"x":111.2,"y":22.3,"z":3.5},"\
N23":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimensi\
on":3.8,"yDimension":3.8,"x":111.2,"y":17.8,"z":3.5},"O23":{"depth":10.9,\
"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension\
":3.8,"x":111.2,"y":13.3,"z":3.5},"P23":{"depth":10.9,"totalLiquidVolume"\
:65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":111.2,"y"\
:8.8,"z":3.5},"A24":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectang\
ular","xDimension":3.8,"yDimension":3.8,"x":115.7,"y":76.3,"z":3.5},"B24"\
:{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":\
3.8,"yDimension":3.8,"x":115.7,"y":71.8,"z":3.5},"C24":{"depth":10.9,"tot\
alLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.\
8,"x":115.7,"y":67.3,"z":3.5},"D24":{"depth":10.9,"totalLiquidVolume":65,\
"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":115.7,"y":62.\
8,"z":3.5},"E24":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangula\
r","xDimension":3.8,"yDimension":3.8,"x":115.7,"y":58.3,"z":3.5},"F24":{"\
depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8\
,"yDimension":3.8,"x":115.7,"y":53.8,"z":3.5},"G24":{"depth":10.9,"totalL\
iquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"\
x":115.7,"y":49.3,"z":3.5},"H24":{"depth":10.9,"totalLiquidVolume":65,"sh\
ape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":115.7,"y":44.8,"\
z":3.5},"I24":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular",\
"xDimension":3.8,"yDimension":3.8,"x":115.7,"y":40.3,"z":3.5},"J24":{"dep\
th":10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"y\
Dimension":3.8,"x":115.7,"y":35.8,"z":3.5},"K24":{"depth":10.9,"totalLiqu\
idVolume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":\
115.7,"y":31.3,"z":3.5},"L24":{"depth":10.9,"totalLiquidVolume":65,"shape\
":"rectangular","xDimension":3.8,"yDimension":3.8,"x":115.7,"y":26.8,"z":\
3.5},"M24":{"depth":10.9,"totalLiquidVolume":65,"shape":"rectangular","xD\
imension":3.8,"yDimension":3.8,"x":115.7,"y":22.3,"z":3.5},"N24":{"depth"\
:10.9,"totalLiquidVolume":65,"shape":"rectangular","xDimension":3.8,"yDim\
ension":3.8,"x":115.7,"y":17.8,"z":3.5},"O24":{"depth":10.9,"totalLiquidV\
olume":65,"shape":"rectangular","xDimension":3.8,"yDimension":3.8,"x":115\
.7,"y":13.3,"z":3.5},"P24":{"depth":10.9,"totalLiquidVolume":65,"shape":"\
rectangular","xDimension":3.8,"yDimension":3.8,"x":115.7,"y":8.8,"z":3.5}\
},"groups":[{"metadata":{"displayName":"Echo Qualified 384-well(384PP) 38\
4 Well Plate 65 µL","displayCategory":"wellPlate","wellBottomShape":"flat\
"},"brand":{"brand":"Echo qualified 384-well(384PP)","brandId":["LABCYTE/\
P-05525"]},"wells":["A1","B1","C1","D1","E1","F1","G1","H1","I1","J1","K1\
","L1","M1","N1","O1","P1","A2","B2","C2","D2","E2","F2","G2","H2","I2","\
J2","K2","L2","M2","N2","O2","P2","A3","B3","C3","D3","E3","F3","G3","H3"\
,"I3","J3","K3","L3","M3","N3","O3","P3","A4","B4","C4","D4","E4","F4","G\
4","H4","I4","J4","K4","L4","M4","N4","O4","P4","A5","B5","C5","D5","E5",\
"F5","G5","H5","I5","J5","K5","L5","M5","N5","O5","P5","A6","B6","C6","D6\
","E6","F6","G6","H6","I6","J6","K6","L6","M6","N6","O6","P6","A7","B7","\
C7","D7","E7","F7","G7","H7","I7","J7","K7","L7","M7","N7","O7","P7","A8"\
,"B8","C8","D8","E8","F8","G8","H8","I8","J8","K8","L8","M8","N8","O8","P\
8","A9","B9","C9","D9","E9","F9","G9","H9","I9","J9","K9","L9","M9","N9",\
"O9","P9","A10","B10","C10","D10","E10","F10","G10","H10","I10","J10","K1\
0","L10","M10","N10","O10","P10","A11","B11","C11","D11","E11","F11","G11\
","H11","I11","J11","K11","L11","M11","N11","O11","P11","A12","B12","C12",\
"D12","E12","F12","G12","H12","I12","J12","K12","L12","M12","N12","O12",\
"P12","A13","B13","C13","D13","E13","F13","G13","H13","I13","J13","K13",\
"L13","M13","N13","O13","P13","A14","B14","C14","D14","E14","F14","G14","H\
14","I14","J14","K14","L14","M14","N14","O14","P14","A15","B15","C15","D1\
5","E15","F15","G15","H15","I15","J15","K15","L15","M15","N15","O15","P15\
","A16","B16","C16","D16","E16","F16","G16","H16","I16","J16","K16","L16"\
,"M16","N16","O16","P16","A17","B17","C17","D17","E17","F17","G17","H17",\
"I17","J17","K17","L17","M17","N17","O17","P17","A18","B18","C18","D18","\
E18","F18","G18","H18","I18","J18","K18","L18","M18","N18","O18","P18","A\
19","B19","C19","D19","E19","F19","G19","H19","I19","J19","K19","L19","M1\
9","N19","O19","P19","A20","B20","C20","D20","E20","F20","G20","H20","I20\
","J20","K20","L20","M20","N20","O20","P20","A21","B21","C21","D21","E21"\
,"F21","G21","H21","I21","J21","K21","L21","M21","N21","O21","P21","A22",\
"B22","C22","D22","E22","F22","G22","H22","I22","J22","K22","L22","M22","\
N22","O22","P22","A23","B23","C23","D23","E23","F23","G23","H23","I23","J\
23","K23","L23","M23","N23","O23","P23","A24","B24","C24","D24","E24","F2\
4","G24","H24","I24","J24","K24","L24","M24","N24","O24","P24"]}],"parame\
ters":{"format":"irregular","quirks":[],"isTiprack":false,"isMagneticModu\
leCompatible":false,"loadName":"echoqualified384well384pp_384_wellplate_6\
5ul"},"namespace":"custom_beta","version":1,"schemaVersion":2,"cornerOffs\
etFromSlot":{"x":0,"y":0,"z":0}}"""


def run_custom_protocol(
        transfer_cherrypick_CSV: FileInput = example_csv,
        source_plate_type: StringSelection(
            'Bio-Rad Hardshell 96-well plate',
            'Opentrons 4x6 tube rack',
            'Corning 384-well plate',
            'Echo 384-well plate') = 'Bio-Rad Hardshell 96-well plate',
        destination_plate_type: StringSelection(
            'Bio-Rad Hardshell 96-well plate',
            'Opentrons 4x6 tube rack') = 'Bio-Rad Hardshell 96-well plate',
        pipette_selection: StringSelection('P10 and P300', 'P10 and P50',
                                           'P50 and P300') = 'P10 and P300',
        pipette_tip_type: StringSelection('Opentrons', 'TipOne') = 'Opentrons',
        p10_aspirate_speed_in_ul_per_s_if_applicable: float = 5,
        p10_dispense_speed_in_ul_per_s_if_applicable: float = 10
):

    if source_plate_type == 'Bio-Rad Hardshell 96-well plate':
        source_name = 'biorad_96_wellplate_200ul_pcr'
    elif source_plate_type == 'Opentrons 4x6 tube rack':
        source_name = 'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap'
    elif source_plate_type == 'Corning 384-well plate':
        source_name = 'corning_384_wellplate_112ul_flat'

    if destination_plate_type == 'Bio-Rad Hardshell 96-well plate':
        dest_name = 'biorad_96_wellplate_200ul_pcr'
    else:
        dest_name = 'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap'

    # pop top 6 lines of CSV that do not contain transfer info
    transfer_info = [
        line.split(',')
        for line in transfer_cherrypick_CSV.splitlines() if line
    ]
    transfer_info.pop(0)
    source_plate_slots = []
    source_wells = []
    target_plate_slots = []
    target_wells = []
    volumes = []
    mix_vols = []
    mix_cycles = []

    # parse for transfer information
    for line in transfer_info:
        source_plate_slots.append(line[0].strip())
        source_wells.append(line[1].strip())
        volumes.append(float(line[2].strip()))
        target_plate_slots.append(line[3].strip())
        target_wells.append(line[4].strip())
        mix_vols.append(float(line[5].strip()))
        mix_cycles.append(int(line[6].strip()))

    unique_source_slots = {}
    source_plate_inds = 0
    for slot in source_plate_slots:
        if slot not in unique_source_slots:
            unique_source_slots.update({slot: source_plate_inds})
            source_plate_inds += 1

    unique_target_slots = {}
    target_plate_inds = 0
    for slot in target_plate_slots:
        if slot not in unique_target_slots:
            unique_target_slots.update({slot: target_plate_inds})
            target_plate_inds += 1

    # load proper labware
    if source_plate_type == 'Echo 384-well plate':
        import json
        source_plates = [robot.add_container_by_definition(
            json.loads(labware_def),
            key
                ) for key in unique_source_slots]
    else:
        source_plates = [labware.load(source_name, key, 'source ' + key)
                         for key in unique_source_slots]

    destination_plates = [labware.load(dest_name, key, 'destination ' + key)
                          for key in unique_target_slots]

    # constants for row check
    row_names = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    num_s_rows = len(source_plates[0].get_grid()['1'])
    s_rows = row_names[:num_s_rows][:num_s_rows]
    num_s_cols = len(source_plates[0].get_grid())
    num_t_rows = len(destination_plates[0].get_grid()['1'])
    t_rows = row_names[:num_t_rows][:num_t_rows]
    num_t_cols = len(destination_plates[0].get_grid())

    def well_check(s, t):
        s_row = s[0]
        s_col = int(s[1:])
        t_row = t[0]
        t_col = int(t[1:])
        # checks
        if s_row not in s_rows:
            raise Exception('Invalid source well row [' + s + ']')
        if s_col > num_s_cols:
            raise Exception('Invalid source well column [' + s + ']')
        if t_row not in t_rows:
            raise Exception('Invalid target well row [' + t + ']')
        if t_col > num_t_cols:
            raise Exception('Invalid target well column [' + t + ']')

    # pipette and tiprack setup depending on pipette selection
    if pipette_selection.split(' ')[0] == 'P10':
        if pipette_tip_type == 'Opentrons':
            tips10 = [
                labware.load('opentrons_96_tiprack_10ul', slot)
                for slot in ['10', '11']
            ]
            tips300 = [
                labware.load('opentrons_96_tiprack_300ul', slot)
                for slot in ['7', '8', '9']
            ]
        else:
            tiprack300_name = 'tipone_96_tiprack_300ul'
            if tiprack300_name not in labware.list():
                labware.create(
                    tiprack300_name,
                    grid=(12, 8),
                    spacing=(9, 9),
                    diameter=5.23,
                    depth=59.30
                )

            tiprack10_name = 'tipone_96_tiprack_10ul'
            if tiprack10_name not in labware.list():
                labware.create(
                    tiprack10_name,
                    grid=(12, 8),
                    spacing=(9, 9),
                    diameter=6,
                    depth=34
                )
            tips10 = [
                labware.load('tipone_96_tiprack_10ul', slot)
                for slot in ['10', '11']
            ]
            tips300 = [
                labware.load('tipone_96_tiprack_300ul', slot)
                for slot in ['7', '8', '9']
            ]
        tips10_max = 96*2
        tips300_max = 96*3
        all_tips_10 = [well for rack in tips10 for well in rack.wells()]
        p10 = instruments.P10_Single(mount='right')
        p10.set_flow_rate(
            aspirate=p10_aspirate_speed_in_ul_per_s_if_applicable,
            dispense=p10_dispense_speed_in_ul_per_s_if_applicable
        )
        if pipette_selection.split(' ')[2] == 'P50':
            p50 = instruments.P50_Single(mount='left')
        else:
            p300 = instruments.P300_Single(mount='left')
        tip10_count = 0
    else:
        if pipette_tip_type == 'TipOne':
            tiprack300_name = 'tipone_96_tiprack_300ul'
            if tiprack300_name not in labware.list():
                labware.create(
                    tiprack300_name,
                    grid=(12, 8),
                    spacing=(9, 9),
                    diameter=5.23,
                    depth=59.30
                )
            tips300 = [labware.load('tipone_96_tiprack_300ul', slot)
                       for slot in ['7', '8', '9', '10', '11']]
        else:
            tips300 = [labware.load('opentrons_96_tiprack_300ul', slot)
                       for slot in ['7', '8', '9', '10', '11']]
        tips300_max = 96*5
        p50 = instruments.P50_Single(mount='right')
        p300 = instruments.P300_Single(mount='left')
    all_tips_300 = [well for rack in tips300 for well in rack.wells()]
    tip300_count = 0

    # perform transfers
    for s_slot, s_well, t_slot, t_well, vol, mix_vol, mix_n in zip(
            source_plate_slots,
            source_wells,
            target_plate_slots,
            target_wells,
            volumes,
            mix_vols,
            mix_cycles):

        if pipette_selection.split(' ')[0] == 'P10':
            if tip10_count == tips10_max:
                robot.pause('Replace tipracks before resuming.')
                p10.reset()
                tip10_count = 0
        if tip300_count == tips300_max:
            robot.pause('Replace tipracks before resuming.')
            p50.reset()
            p300.reset()
            tip300_count = 0

        if vol > 0:
            s_plate_ind = unique_source_slots[s_slot]
            s_plate = source_plates[s_plate_ind]
            t_plate_ind = unique_target_slots[t_slot]
            t_plate = destination_plates[t_plate_ind]

            well_check(s_well, t_well)
            source = s_plate.wells(s_well)
            target = t_plate.wells(t_well)

            if pipette_selection == 'P10 and P50':
                if vol <= 10:
                    pipette = p10
                    pipette.pick_up_tip(all_tips_10[tip10_count])
                    tip10_count += 1
                else:
                    pipette = p50
                    pipette.pick_up_tip(all_tips_300[tip300_count])
                    tip300_count += 1
            elif pipette_selection == 'P10 and P300':
                if vol <= 30:
                    pipette = p10
                    pipette.pick_up_tip(all_tips_10[tip10_count])
                    tip10_count += 1
                else:
                    pipette = p300
                    pipette.pick_up_tip(all_tips_300[tip300_count])
                    tip300_count += 1
            else:
                if vol <= 50:
                    pipette = p50
                else:
                    pipette = p300
                tip300_count += 1
                pipette.pick_up_tip(all_tips_300[tip300_count])

            pipette.transfer(
                vol,
                source,
                target,
                blow_out=True,
                new_tip='never'
                )
            if mix_vol > pipette.max_volume:
                mix_vol = pipette.max_volume
            pipette.mix(mix_n, mix_vol)
            pipette.blow_out(target.top())
            pipette.drop_tip()
