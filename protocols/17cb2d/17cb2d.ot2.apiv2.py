metadata = {
    'protocolName': 'Plate Filling Master Mix in AB 384 Well Plate',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.5'
}


def run(protocol):
    [p20mnt, num_plates] = get_values(  # noqa: F821
    'p20mnt', 'num_plates')

    # load labware and pipettes
    tips = protocol.load_labware('opentrons_96_tiprack_20ul', '10')
    pip = protocol.load_instrument('p20_single_gen2', p20mnt, tip_racks=[tips])
    res = protocol.load_labware('usascientific_12_reservoir_22ml', '11')
    mm1 = res['A1']
    mm2 = res['A2']
    num_plates += 1
    plates = [
        protocol.load_labware(
            'appliedbiosystemsmicroampoptical384' +
            'wellreactionplatewithbarcode_384_wellplate_30ul',
            s) for s in range(1, num_plates)]

    # distribute mastermix 1
    protocol.comment('Distributing master mix 1...')
    pip.pick_up_tip()
    for plate in plates:
        wells = [w for col in plate.rows()[::2] for w in col]
        mm_vol = 0
        for well in wells:
            if mm_vol < 1:
                pip.aspirate(15, mm1)
                mm_vol = 15
            pip.dispense(7.5, well)
            mm_vol -= 7.5
    pip.drop_tip()

    # distribute mastermix 2
    protocol.comment('Distributing master mix 2...')
    pip.pick_up_tip()
    for plate in plates:
        wells = [w for col in plate.rows()[1::2] for w in col]
        mm_vol = 0
        for well in wells:
            if mm_vol < 1:
                pip.aspirate(15, mm2)
                mm_vol = 15
            pip.dispense(7.5, well)
            mm_vol -= 7.5
    pip.drop_tip()
