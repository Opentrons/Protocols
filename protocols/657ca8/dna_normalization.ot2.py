from opentrons import labware, instruments
from otcustomizers import StringSelection, FileInput
import math

metadata = {
    'protocolName': 'DNA Normalization from .csv',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
rack_2ml_name = 'fisherbrand_96_tuberack_2ml_screwcap'
if rack_2ml_name not in labware.list():
    labware.create(
        rack_2ml_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8.5,
        depth=42,
        volume=2000
    )

rack_500ul_name = 'thermoscientific_96_tuberack_0.5ml_screwcap'
if rack_500ul_name not in labware.list():
    labware.create(
        rack_500ul_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7.4,
        depth=29.1,
        volume=500
    )

# create custom labware
dest_rack = labware.load(rack_500ul_name, '1', '0.5ml destination rack')
tipracks300 = [
    labware.load('opentrons_96_tiprack_300ul', slot, '300ul tiprack')
    for slot in ['3', '6']
]
src_rack = labware.load(rack_2ml_name, '4', '2ml source rack')
te_buff = labware.load(
    'opentrons_15_tuberack_nest_15ml_conical',
    '5',
    'TE buffer rack').wells()[0]

example_csv = """PtID,Sample Type,Tube,ng/ul,Plate,Well,DNA (uL),water (uL)
10013393,dna,A01,125.88,Regen60K-001,A01,50,75
10012852,dna,A02,152.083,Regen60K-001,A02,41,84
10013300,dna,A03,136.822,Regen60K-001,A03,46,79
10013324,dna,A04,151.436,Regen60K-001,A04,41,84
10012592,dna,A05,156.14,Regen60K-001,A05,40,85
10012378,dna,A06,100.801,Regen60K-001,A06,62,63
10012541,dna,A07,114.195,Regen60K-001,A07,55,70
10012189,dna,A08,118.836,Regen60K-001,A08,53,72
"""


def run_custom_protocol(
        p300_single_mount: StringSelection('right', 'left') = 'right',
        input_csv_file: FileInput = example_csv
):
    # pipette
    p300 = instruments.P300_Single(
        mount=p300_single_mount, tip_racks=tipracks300)

    def parse_well(well_name):
        return well_name[0].upper() + str(int(well_name[1:]))

    h = te_buff.properties['depth'] - 40
    max_d = 5
    r = te_buff.properties['diameter']/2

    def h_track(vol):
        nonlocal h
        dh = vol/(math.pi*(r**2))*1.1  # account for theoretical volume loss
        if h - dh <= max_d:
            h = max_d
        else:
            h -= dh
        return h

    # parse .csv
    trans_data = [
        [val.strip() for val in line.split(',')]
        for line in input_csv_file.splitlines()[1:] if line
    ]
    s_names = [parse_well(t[2]) for t in trans_data]
    d_names = [parse_well(t[5]) for t in trans_data]
    vols_dna = [float(t[6]) for t in trans_data]
    vols_buffer = [float(t[7]) for t in trans_data]

    # transfer DNA
    for v, s, d in zip(vols_dna, s_names, d_names):
        p300.pick_up_tip()
        p300.transfer(
            v,
            src_rack.wells(s),
            dest_rack.wells(d).bottom(3),
            air_gap=30,
            new_tip='never'
        )
        p300.blow_out(dest_rack.wells(d).top(-2))
        p300.drop_tip()

    # transfer TE buffer
    for v, d in zip(vols_buffer, d_names):
        p300.pick_up_tip()
        h_track(v)
        p300.transfer(
            v,
            te_buff.bottom(h),
            dest_rack.wells(d).bottom(3),
            air_gap=30,
            new_tip='never'
        )
        p300.blow_out(dest_rack.wells(d).top(-2))
        p300.drop_tip()
