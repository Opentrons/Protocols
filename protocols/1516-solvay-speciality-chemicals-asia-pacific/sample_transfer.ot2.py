from opentrons import labware, instruments
# from otcustomizers import FileInput
import math

metadata = {
    'protocolName': 'Solution Transfer',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

vial_rack_name = '24-custom-vial-rack'
if vial_rack_name not in labware.list():
    labware.create(
        vial_rack_name,
        grid=(6, 4),
        spacing=(20, 20),
        diameter=10,
        depth=21
        )

volume_csv_example = """
Produit1,Produit2,Produit3,Produit4,Produit5,Produit6,Produit7,Produit8,Produit9,Produit10,Produit11,Produit12
0,109,275,26,201,116,122,110,280,97,22,258
39,129,248,58,30,123,195,247,1,203,62,60
19,148,53,272,0,153,173,270,25,245,28,83
58,169,193,250,27,212,3,55,232,235,82,43
223,93,177,115,288,252,130,102,256,16,233,113
141,299,90,252,50,156,125,55,110,65,150,237
49,74,223,12,228,112,182,202,253,208,294,134
181,240,182,2,266,82,200,157,248,65,139,139
214,1,244,120,253,129,221,181,217,166,168,172
213,245,196,27,122,160,144,248,245,44,239,108
"""

# labware setup
mother_racks = [labware.load('opentrons-tuberack-50ml', slot)
                for slot in ['2', '5', '8']]
sample_racks = [labware.load(vial_rack_name, slot)
                for slot in ['3', '6', '9']]
tipracks_300 = [labware.load('opentrons-tiprack-300ul', slot)
                for slot in ['10', '11']]
tipracks_1000 = [labware.load('tiprack-1000ul', slot)
                 for slot in ['1', '4', '7']]

# instruments setup
p300 = instruments.P300_Single(
    mount='left',
    tip_racks=tipracks_300)
p1000 = instruments.P1000_Single(
    mount='right',
    tip_racks=tipracks_1000)


# def run_custom_protocol(volume_csv: FileInput=volume_csv_example):
def run_custom_protocol():
    volume_csv = volume_csv_example

    def get_volume_lists(csv_string):
        info_list = [cell for line in volume_csv.splitlines() if line
                     for cell in [line.split(',')]]
        volume_lists = [[] for _ in range(len(info_list[0]))]
        for line in info_list[1:]:
            for index, cell in enumerate(line):
                volume_lists[index].append(float(cell))
        return volume_lists

    def get_source_list(volume_lists):
        source_dict = {index: [] for index in range(len(volume_lists))}
        source_tubes = [well for rack in mother_racks for well in rack]
        tube_count = 0
        for index, volumes in enumerate(volume_lists):
            total_vol = sum(volumes)
            tube_num = math.ceil(total_vol / 50000)
            source_dict[index] = source_tubes[tube_count:tube_count+tube_num]
            tube_count += tube_num
        return source_dict

    vials = [well for rack in sample_racks for well in rack.wells()]
    volume_lists = get_volume_lists(volume_csv)
    sources = get_source_list(volume_lists)

    for source_index, volumes in enumerate(volume_lists):
        if len(sources[source_index]) < 2:
            source = sources[source_index]
        else:
            source = sources[source_index][0]
        source_volume_tracker = 50000
        dests = vials[:len(volumes)]
        for vol, dest in zip(volumes, dests):
            if vol == 0:
                pass
            else:
                if vol > 300:
                    pipette = p1000
                else:
                    pipette = p300
                if not pipette.tip_attached:
                    pipette.pick_up_tip()
                if vol > source_volume_tracker:
                    source = next(source)
                    source_volume_tracker = 50000
                pipette.transfer(vol, source, dest.top(-10), new_tip='never')
                pipette.blow_out(dest.top(-10))
                source_volume_tracker -= vol
        if p1000.tip_attached:
            p1000.drop_tip()
        if p300.tip_attached:
            p300.drop_tip()

run_custom_protocol()
