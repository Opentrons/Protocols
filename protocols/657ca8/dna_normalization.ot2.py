from opentrons import labware, instruments
from otcustomizers import StringSelection, FileInput
import math

metadata = {
    'protocolName': 'DNA Normalization from .csv',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
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
src_racks = {
    str(i+1): labware.load(
        'opentrons_24_tuberack_generic_2ml_screwcap',
        slot,
        '2ml source rack ' + str(i+1)
    )
    for i, slot in enumerate(['1', '2', '4', '5'])
}
dest_rack = labware.load(rack_500ul_name, '3', '0.5ml destination rack')
te_buff = labware.load(
    'opentrons_15_tuberack_nest_15ml_conical',
    '6',
    'TE buffer rack').wells()[0]
tipracks300 = [
    labware.load('opentrons_96_tiprack_300ul', slot, '300ul tiprack')
    for slot in ['8', '9']
]

example_csv = """PtID,Source rack (1-4),Source well,Destination well,DNA (ul), \
water (ul)
10013393,1,A01,A01,50,75
10012852,2,A02,A02,41,84
10013300,1,A03,A03,46,79
10013324,1,A04,A04,41,84
10012592,1,A05,A05,40,85
10012378,1,A06,A06,62,63
10012541,1,B1,A07,55,70
10012189,1,B2,A08,53,72
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
    s_slots = [t[1] for t in trans_data]
    s_names = [parse_well(t[2]) for t in trans_data]
    d_names = [parse_well(t[3]) for t in trans_data]
    vols_dna = [float(t[4]) for t in trans_data]
    vols_buffer = [float(t[5]) for t in trans_data]

    # transfer DNA
    for sl, v, s, d in zip(s_slots, vols_dna, s_names, d_names):
        p300.pick_up_tip()
        src_rack = src_racks[sl]
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
