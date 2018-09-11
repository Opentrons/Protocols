from opentrons import labware, instruments
from otcustomizers import FileInput

# labware setup
plate = labware.load('96-flat', '1')
tuberack = labware.load('tube-rack-2ml', '2')

# reagent setup
sg_mastermix = tuberack.wells('A1')
fwd_1 = tuberack.wells('B1')
rvs_1 = tuberack.wells('C1')
h2o = tuberack.wells('D1')
pt1 = tuberack.wells('A2')
pt2 = tuberack.wells('B2')
pt3 = tuberack.wells('C2')
pt4 = tuberack.wells('D2')
ctl1 = tuberack.wells('A3')
ctl2 = tuberack.wells('B3')
ctl3 = tuberack.wells('C3')
ctl4 = tuberack.wells('D3')
taqMan_mastermix = tuberack.wells('A4')
hk_gene_probe = tuberack.wells('B4')
fwd_2 = tuberack.wells('C4')
rvs_2 = tuberack.wells('D4')
pta = tuberack.wells('A5')
ptb = tuberack.wells('B5')
ptc = tuberack.wells('C5')
ptd = tuberack.wells('D5')
hk = tuberack.wells('A6')
goi1 = tuberack.wells('B6')
goi2 = tuberack.wells('C6')

# pipette setup
tiprack_10 = labware.load('tiprack-10ul', '4')
tiprack_50 = labware.load('tiprack-200ul', '5')

p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack_10])

p50 = instruments.P50_Single(
    mount='right',
    tip_racks=[tiprack_50])


csv_example = """
CTL 1; GOI1,CTL 1; GOI1,CTL 1; GOI1,CTL 1; HK,CTL 1; HK,CTL 1; HK,,,,,,
CTL 2; GOI1,CTL 2; GOI1,CTL 2; GOI1,CTL 2; HK,CTL 2; HK,CTL 2; HK,,,,,,
CTL 3; GOI1,CTL 3; GOI1,CTL 3; GOI1,CTL 3; HK,CTL 3; HK,CTL 3; HK,,,,,,
CTL 4; GOI1,CTL 4; GOI1,CTL 4; GOI1,CTL 4; HK,CTL 4; HK,CTL 4; HK,,,,,,
PT 1; GOI1,PT 1; GOI1,PT 1; GOI1,PT 1; HK,PT 1; HK,PT 1; HK,,,,,,
,,,,,,,,,,,
,,,,,,,,,,,
,,GOI1,,,HK,,,,,,
"""


def create_layout_dict(layout_csv):
    """
    Transform the csv into a dictionary with headers:
    'ctl1', 'ctl2', 'ctl3', 'ctl4', 'pt1', 'pt2', 'pt3', 'pt4', 'pta', 'ptb',
    'ptc', 'ptd', 'h2o', 'hk', 'goi1', 'goi2'
    """
    # create a list of rows
    layout_list = [line for line in layout_csv.splitlines() if line]

    layout_dict = {}
    layout_dict['h2o'] = []

    # go through each well, for each reagents involved, append well location to
    # the reagent list in the dictionary
    for line, row in zip(layout_list, plate.rows()):
        for reagents, cell in zip(line.split(','), row.wells()):
            for reagent in reagents.split(';'):
                if reagent:
                    # remove space between the string and make string lowercase
                    reagent = reagent.replace(" ", "").lower()
                    # create a new key in the dictionary if the reagent is new
                    if reagent not in layout_dict.keys():
                        layout_dict[reagent] = []
                    layout_dict[reagent].append(cell)
                    # if there is only one reagent in the cell (mastermix),
                    # add water to that cell
                    if len(reagents.split(';')) == 1:
                        layout_dict['h2o'].append(cell)
    return layout_dict


def run_custom_protocol(
    ngoi: int=43,
    n1: int=22,
    n2: int=22,
    layout_csv: FileInput=csv_example
        ):

    ngoi = ngoi * 1.15
    n1 = n1 * 1.15
    n2 = n2 * 1.15

    # set up housekeeping master mix
    p50.transfer(round(ngoi*7.5), taqMan_mastermix, hk)
    p10.transfer(round(ngoi*0.3, 1), hk_gene_probe, hk)
    p50.transfer(round(ngoi*5.75), h2o, hk, mix_after=(2, 50))

    # set up goi1 master mix
    p50.transfer(round(n1*7.5), sg_mastermix, goi1)
    p10.transfer(round(n1*0.3, 1), fwd_1, goi1)
    p10.transfer(round(n1*0.3, 1), rvs_1, goi1)
    p50.transfer(round(n1*5.9), h2o, goi1)

    # set up goi2 master mix
    p50.transfer(round(n2*7.5), sg_mastermix, goi2)
    p10.transfer(round(n2*0.3, 1), fwd_2, goi2)
    p10.transfer(round(n2*0.3, 1), rvs_2, goi2)
    p50.transfer(round(n2*5.9), h2o, goi2)

    mastermix = {'hk': hk, 'goi1': goi1, 'goi2': goi2}

    sample = {'ctl1': ctl1, 'ctl2': ctl2, 'ctl3': ctl3, 'ctl4': ctl4,
              'pt1': pt1, 'pt2': pt2, 'pt3': pt3, 'pt4': pt4, 'pta': pta,
              'ptb': ptb, 'ptc': ptc, 'ptd': ptd, 'h2o': h2o}

    layout_dict = create_layout_dict(layout_csv)

    # first distribute master mixes
    for key in mastermix:
        if key in layout_dict:
            p50.distribute(14, mastermix[key], layout_dict[key])

    # then transfer samples
    for key in sample:
        if key in layout_dict:
            p10.transfer(
                1,
                sample[key],
                [cell.bottom(1) for cell in layout_dict[key]],
                mix_after=(3, 10),
                new_tip='always')
