from opentrons import labware, instruments

plate = labware.load('96-flat', '1')
deep_plate = labware.load('96-deep-well', '2')
tipracks = [labware.load('opentrons-tiprack-300ul', slot)
            for slot in ['4', '5']]

p50 = instruments.P50_Single(
    mount='left',
    tip_racks=tipracks)


def run_custom_protocol(
        special_mix_identifiers: str='A, B, 10',
        special_mix_height: float=7,
        dilution_transfer_volume: float=20,
        deep_plate_transfer_volume: float=5):

    # serial dilution
    for row in plate.rows():
        p50.transfer(
            dilution_transfer_volume,
            row.wells('12', to='2'),
            row.wells('11', to='1'),
            air_gap=True,
            mix_after=(5, 20))

    names = [well.get_name() for well in plate.wells()]

    identifies = [item.replace(" ", "").upper()
                  for item in special_mix_identifiers.split(',')]

    for source, dest, name in zip(plate.wells(), deep_plate.wells(), names):
        p50.pick_up_tip()
        p50.transfer(deep_plate_transfer_volume, source, dest, new_tip='never')
        if name[0] in identifies or name[1:] in identifies:
            p50.mix(5, 20, dest.bottom(7))
        else:
            p50.mix(5, 20, dest)
        p50.drop_tip()
