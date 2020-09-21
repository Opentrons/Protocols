metadata = {
    'protocolName': 'Plate Filling Master Mix in AB 384 Well Plate',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.5'
}


def run(protocol):
    [piptype, pipmnt, num_plates, p384] = get_values(  # noqa: F821
    'piptype', 'pipmnt', 'num_plates', 'p384')

    # load labware and pipettes
    pip_name, tip_name = piptype.split()
    tips = protocol.load_labware(tip_name, '10')
    pip = protocol.load_instrument(pip_name, pipmnt, tip_racks=[tips])
    res = protocol.load_labware('nest_12_reservoir_15ml', '11')
    mm1 = res['A1']
    mm2 = res['A12']
    num_plates += 1
    plates = [
        protocol.load_labware(p384, s) for s in range(1, num_plates)]

    # max_vol = 15 if pip_name == 'p20_multi_gen2' else 180

    # distribute mastermix 1
    protocol.comment('Distributing master mix 1...')
    pip.pick_up_tip()
    for plate in plates:
        wells = plate.rows()[0]
        disp_vol = 9.5
        for well in wells:
            pip.aspirate(7.5, mm1)
            pip.dispense(disp_vol, well)
            pip.blow_out(well)
            pip.aspirate(2, well.top())
    pip.drop_tip()

    # distribute mastermix 2
    protocol.comment('Distributing master mix 2...')
    pip.pick_up_tip()
    for plate in plates:
        wells = plate.rows()[1]
        disp_vol = 9.5
        for well in wells:
            pip.aspirate(7.5, mm2)
            pip.dispense(disp_vol, well)
            pip.blow_out(well)
            pip.aspirate(2, well.top())
    pip.drop_tip()
