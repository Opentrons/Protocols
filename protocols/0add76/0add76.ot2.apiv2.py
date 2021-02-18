import csv

metadata = {
    'protocolName': 'Version Update - Adding BTM to DBS',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.7'
}


def run(ctx):

    # load Labware
    reservoir = ctx.load_labware('nest_1_reservoir_195ml', '6')  # changecustom
    pcr_plate = ctx.load_labware('vwrpcr_96_wellplate_200ul', '8')
    tiprack_300 = ctx.load_labware('vwr_96_tiprack_300ul', '9')
    dna_stock = ctx.load_labware('vwr_square_96_microplate_2000ul', '10')
    tiprack_10 = ctx.load_labware('vwr_96_tiprack_10ul', '11')

    # load instruments
    p20 = ctx.load_instrument('p20_single_gen2', 'left',
                              tip_racks=[tiprack_10])

    p300 = ctx.load_instrument('p300_single_gen2', 'right',
                               tip_racks=[tiprack_300])

    # csv file --> dictionary with well as key
    
    dict_plate = {}
    with open('/Users/ramifarawi/Desktop/PROJECTS/CSV/DNA_PROTOCOL.csv', 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader)
        for row in reader:
            dict_plate[row[3]] = [float(row[1]), float(row[2])]

    for well in dict_plate:
        vol_dna = dict_plate[well][0]
        p20.transfer(vol_dna, dna_stock[well], pcr_plate[well], new_tip='always')

    for well in dict_plate:
        vol_water = dict_plate[well][1]
        p300.transfer(vol_water, reservoir['A1'], pcr_plate[well], new_tip='always')
