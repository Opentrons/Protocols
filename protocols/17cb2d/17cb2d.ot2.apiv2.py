from opentrons import types

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
    mm1 = [res['A1']]*5+[res['A2']]*4
    mm2 = [res['A11']]*5+[res['A12']]*4
    num_plates += 1
    plates = [
        protocol.load_labware(p384, s) for s in range(1, num_plates)]

    # max_vol = 15 if pip_name == 'p20_multi_gen2' else 180

    # distribute mastermix 1
    protocol.comment('Distributing master mix 1...')
    pip.pick_up_tip()
    for plate, mm in zip(plates, mm1):
        wells = plate.rows()[0]
        disp_vol = 12
        for well in wells:
            pip.aspirate(10, mm)
            protocol.max_speeds['X'] = 25
            pip.move_to(mm.top().move(types.Point(x=3.5, y=0, z=-4)))
            pip.move_to(mm.top().move(types.Point(x=-3.5, y=0, z=-2)))
            protocol.max_speeds['X'] = None
            pip.dispense(disp_vol, well)
            pip.blow_out(well)
            pip.aspirate(2, well.top())
    pip.drop_tip()

    # distribute mastermix 2
    protocol.comment('Distributing master mix 2...')
    pip.pick_up_tip()
    for plate, mm in zip(plates, mm2):
        wells = plate.rows()[1]
        disp_vol = 12
        for well in wells:
            pip.aspirate(10, mm)
            protocol.max_speeds['X'] = 25
            pip.move_to(mm.top().move(types.Point(x=3.5, y=0, z=-4)))
            pip.move_to(mm.top().move(types.Point(x=-3.5, y=0, z=-2)))
            protocol.max_speeds['X'] = None
            pip.dispense(disp_vol, well)
            pip.blow_out(well)
            pip.aspirate(2, well.top())
    pip.drop_tip()
