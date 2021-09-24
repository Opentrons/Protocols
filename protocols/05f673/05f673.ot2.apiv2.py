from opentrons import protocol_api

metadata = {
    'protocolName': 'Cell Normalization',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.10'
}


def run(protocol: protocol_api.ProtocolContext):
    [p1000mnt, transfer_csv] = get_values(  # noqa: F821
        'p1000mnt', 'transfer_csv')

    # load labware
    reservoir = protocol.load_labware('agilent_1_reservoir_290ml', '4')
    buffer = reservoir['A1']

    source = [protocol.load_labware('corning_24_wellplate_3.4ml_flat', slot)
              for slot in ['1', '2', '3', '5']]
    outputs = [protocol.load_labware('corning_24_wellplate_3.4ml_flat', slot)
               for slot in ['6', '8', '9', '11']]

    tipracks1000 = [protocol.load_labware('opentrons_96_tiprack_1000ul', '7')]

    # load pipette
    p1000 = protocol.load_instrument(
        'p1000_single_gen2', p1000mnt, tip_racks=tipracks1000)

    def tip_pick_up(pip):
        try:
            pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            protocol.set_rail_lights(False)
            protocol.pause("Replace the tips")
            pip.reset_tipracks()
            protocol.set_rail_lights(True)
            pip.pick_up_tip()

    # process csv
    csv_data = [
        l.split(',') for l in transfer_csv.strip().splitlines() if l][1:]

    # transfer buffer
    protocol.set_rail_lights(True)
    tip_pick_up(p1000)
    for line in csv_data:
        destPlate = int(line[2]) - 1
        destWell = line[3]
        volBuff = int(line[4])

        p1000.aspirate(volBuff, buffer)
        p1000.dispense(volBuff, outputs[destPlate][destWell])
    p1000.drop_tip()

    # transfer samples
    for line in csv_data:
        srcPlate = int(line[0]) - 1
        srcWell = line[1]
        destPlate = int(line[2]) - 1
        destWell = line[3]
        volSamp = int(line[5])

        tip_pick_up(p1000)
        p1000.mix(3, volSamp, source[srcPlate][srcWell])
        p1000.aspirate(volSamp, source[srcPlate][srcWell])
        p1000.dispense(volSamp, outputs[destPlate][destWell])
        p1000.drop_tip()

    protocol.set_rail_lights(False)
