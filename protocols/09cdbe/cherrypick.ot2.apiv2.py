# metadata
metadata = {
    'protocolName': 'Consolidation from .csv',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.0'
}


def run(ctx):

    plate_type, p20_mount, transfer_csv = get_values(  # noqa: F821
        'plate_type', 'p20_mount', 'transfer_csv')
#     plate_type, p20_mount, transfer_csv = [
#         'biorad_96_wellplate_200ul_pcr', 'right', 'Plate Position,Well ID,\
# Volume,,\n1,A1,3.0,,\n1,B1,4.0,,\n1,C1,5.0,,\n1,D1,3.0,,']

    # load labware
    source_plates = {
        str(i+1): ctx.load_labware(plate_type, slot, 'plate ' + str(i+1))
        for i, slot in enumerate(['2', '5', '8', '11', '6'])
    }
    destination_tube = ctx.load_labware(
        'vwr_15_tuberack_5000ul', '9', 'destination tube').wells()[0]
    tipracks = [
        ctx.load_labware('opentrons_96_tiprack_20ul', slot, '20µl tiprack')
        for slot in ['1', '4', '7', '10', '3']
    ]

    # load pipette
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=tipracks)

    # parse .csv
    transfer_info = [
        [val.strip() for val in line.split(",")]
        for line in transfer_csv.splitlines()[1:] if line
    ]

    # perform transfers
    for line in transfer_info:
        slot, well, volume = line[:3]
        source = source_plates[slot].wells_by_name()[well.upper()]
        vol = float(volume)
        air_vol = (20-vol)/2
        p20.pick_up_tip()
        p20.aspirate(air_vol, source.top())
        p20.aspirate(vol, source)
        p20.aspirate(air_vol, source.top(-1))
        p20.touch_tip(source)
        p20.dispense(20, destination_tube)
        p20.blow_out(destination_tube.bottom(2))
        p20.drop_tip()
