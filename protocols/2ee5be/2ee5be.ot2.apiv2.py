from opentrons import protocol_api

def get_values(*names):
    import json
    _all_values = json.loads("""{"samples":"384","p300_mount":"left","p20_mount":"right"}""")
    return [_all_values[n] for n in names]

metadata = {
    'protocolName': 'PCR/qPCR Prep',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.8'
}


def run(ctx):

    [samples, p300_mount, p20_mount] = get_values(  # noqa: F821
        "samples", "p300_mount", "p20_mount")

    samples = int(samples)

    # Load Labware
    deep_well = [ctx.load_labware('kingfisher_96_deepwell_plate_2ml', slot, f'Sample Plate {slot}') for slot in range(1,5)]
    pcr_plate = ctx.load_labware('microampoptical_384_wellplate_30ul', 5, 'PCR Plate')
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', 6)
    tiprack300 = ctx.load_labware('opentrons_96_tiprack_300ul', 7)
    tiprack200 = [ctx.load_labware('opentrons_96_tiprack_20ul', slot) for slot in range(8,12)]

    water = reservoir['A1']
    multiplex = reservoir['A2']
    dye = reservoir['A3']
    mm = reservoir['A5']

    # Load Pipette
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount, tip_racks=[tiprack300])
    m20 = ctx.load_instrument('p20_multi_gen2', p20_mount, tip_racks=tiprack200)

    # Create PCR Mix
    reactions = round((samples*0.095)+samples)
    p300.transfer(4*reactions, water, mm)
    p300.transfer(5*reactions, multiplex, mm)
    p300.transfer(1*reactions, dye, mm)
    p300.pick_up_tip()
    p300.mix(5, 300, mm)
    p300.drop_tip()

    sample_wells = [well for i in range(4) for well in deep_well[i].rows()[0]]
    all_dest_wells = [pcr_plate.rows()[0][::2], pcr_plate.rows()[0][1::2], pcr_plate.rows()[1][0::2], pcr_plate.rows()[1][1::2]]
    dest_wells = [well for i in range(4) for well in all_dest_wells[i]]

    # Get columns depending on sample number
    columns = samples // 8

    def pick_up(pip):
        try:
            pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            pip.home()
            ctx.pause('Replace ' + str(pip.max_volume) + 'µl tipracks before resuming.')
            pip.reset_tipracks()
            pip.pick_up_tip()

    # Transfer MM to PCR Plate
    pick_up(m20)
    m20.transfer(10, mm, dest_wells[:columns], new_tip='never')
    m20.drop_tip()

    # Transfer Samples to PCR Plate
    for samples, dest in zip(sample_wells[:columns], dest_wells[:columns]):
        pick_up(m20)
        m20.transfer(10, samples, dest, new_tip='never')
        m20.drop_tip()
