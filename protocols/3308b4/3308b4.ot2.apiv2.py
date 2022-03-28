"""PROTOCOL."""
metadata = {
    'protocolName': 'PCR/qPCR Prep',
    'author': 'Opentrons',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def run(ctx):

    [mount_side
     ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "mount_side")

    # define all custom variables above here with descriptions:

    # number of samples

    # "True" for park tips, "False" for discard tips

    # load labware
    spr_well = ctx.load_labware('nest_1_reservoir_195ml', '4')
    vhb_well = ctx.load_labware('nest_1_reservoir_195ml', '5')
    water_well = ctx.load_labware('nest_1_reservoir_195ml', '6')
    spr_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '7')
    vhb_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '8')
    water_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '9')
    '''

    Add your labware here with:

    labware_name = ctx.load_labware('{loadname}', '{slot number}')

    If loading labware on a module, you can load with:

    labware_name = module_name.load_labware('{loadname}')
    where module_name is defined above.

    '''

    # load tipracks
    tiprack = [
        ctx.load_labware('opentrons_96_tiprack_300ul', '1')
        ]
    '''

    Add your tipracks here as a list:

    For a single tip rack:

    tiprack_name = [ctx.load_labware('{loadname}', '{slot number}')]

    For multiple tip racks of the same type:

    tiprack_name = [ctx.load_labware('{loadname}', 'slot')
                     for slot in ['1', '2', '3']]

    If two different tipracks are on the deck, use convention:
    tiprack[number of microliters]
    e.g. tiprack10, tiprack20, tiprack200, tiprack300, tiprack1000

    '''

    # load instrument
    m300 = ctx.load_instrument(
        'p300_multi_gen2', mount=mount_side, tip_racks=tiprack)

    # reagents
    spr = spr_well.wells()[0]
    vhb = vhb_well.wells()[0]
    water = water_well.wells()[0]

    # lists
    volume_list = [350, 350, 50]
    source_list = [spr, vhb, water]
    dest_list = [spr_plate.rows()[0], vhb_plate.rows()[0],
                 water_plate.rows()[0]]

    # protocol
    for volume, source, dest in zip(volume_list, source_list, dest_list):
        m300.pick_up_tip()
        m300.transfer(volume,
                      source,
                      dest,
                      new_tip='never'
                      )
        m300.drop_tip()
