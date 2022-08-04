import csv

metadata = {
    'protocolName': 'Custom Normalization',
    'author': 'Steve Plonk <protocols@opentrons.com>',
    'apiLevel': '2.11'
}


def run(ctx):

    # get parameter values from json above
    [count_racks, uploaded_csv
     ] = get_values(  # noqa: F821
      'count_racks', 'uploaded_csv')

    ctx.set_rail_lights(True)
    ctx.delay(seconds=10)
    if count_racks < 1 or count_racks > 3:
        raise Exception('Invalid number of sample racks (must be 1-3).')

    tfers = [line for line in csv.DictReader(uploaded_csv.splitlines())]

    for tfer in tfers:
        if not 2 <= float(tfer['Sample volume (uL)']) <= 15:
            raise Exception('Invalid sample volume (must be 2-15 uL)')
        if not 150 <= float(tfer['Diluent Volume(ul)']) <= 300:
            raise Exception('Invalid buffer volume (must be 150-300 uL)')

    # tips, p20 single, p300 multi
    tips20 = [ctx.load_labware(
     "opentrons_96_tiprack_20ul", str(slot)) for slot in [10]]
    tips300 = [ctx.load_labware(
     "opentrons_96_tiprack_300ul", str(slot)) for slot in [11]]
    p20s = ctx.load_instrument(
        "p20_single_gen2", 'left', tip_racks=tips20)
    p300m = ctx.load_instrument(
        "p300_multi_gen2", 'right', tip_racks=tips300)

    for slot in ['1', '4', '7'][:count_racks]:
        ctx.load_labware(
         'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', slot,
         'Sample Rack in Slot {}'.format(slot))

    diluentreservoir = ctx.load_labware(
     'nest_1_reservoir_195ml', '5', 'Diluent')

    destplate = ctx.load_labware(
     'genesee25221_96_wellplate_300ul', '6', 'Destination Plate')

    # p300m one tip buffer transfer
    p300m.pick_up_tip(tips300[0]['H1'])
    p300m.transfer(
     [float(tfer['Diluent Volume(ul)']) for tfer in tfers],
     diluentreservoir.wells()[0].bottom(1),
     [destplate.wells_by_name()[
      tfer['Destination well']].bottom(1) for tfer in tfers],
     tip_touch=True, new_tip='never')
    p300m.drop_tip()

    # p20s sample transfer
    p20s.transfer(
     [float(tfer['Sample volume (uL)']) for tfer in tfers],
     [ctx.loaded_labwares[int(tfer['Source slot'])].wells_by_name()[
      tfer['Source well']].bottom(1) for tfer in tfers],
     [destplate.wells_by_name()[
      tfer['Destination well']].bottom(1) for tfer in tfers],
     mix_before=(6, 20), mix_after=(3, 20), new_tip='always')
