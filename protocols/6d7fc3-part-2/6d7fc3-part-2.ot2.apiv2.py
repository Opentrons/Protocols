from opentrons import protocol_api

metadata = {
    'protocolName': '''GeneRead QIAact Lung DNA UMI Panel Kit: Adapter Ligation''',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.11'
}

def get_values(*names):
    import json
    _all_values = json.loads("""{"samples":12, "p300_mount":"left", "p20_mount":"right"}""")
    return [_all_values[n] for n in names]

def run(ctx):

    [samples, p300_mount,
        p20_mount] = get_values(  # noqa: F821
        "samples", "p300_mount", "p20_mount")

    if not 1 <= samples <= 12:
        raise Exception('''Invalid number of samples.
                        Sample number must be between 1-12.''')

    # Load Labware
    tipracks_200ul = ctx.load_labware('opentrons_96_filtertiprack_200ul', 9)
    tipracks_20ul = ctx.load_labware('opentrons_96_filtertiprack_20ul', 6)
    tc_mod = ctx.load_module('thermocycler module')
    tc_plate = tc_mod.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
    temp_mod = ctx.load_module('temperature module gen2', 3)
    temp_plate = temp_mod.load_labware(
                    'opentrons_24_aluminumblock_nest_1.5ml_screwcap')

    # Load Pipettes
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=[tipracks_200ul])
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount,
                              tip_racks=[tipracks_20ul])

    # Helper Functions
    def pick_up(pip, loc=None):
        try:
            if loc:
                pip.pick_up_tip(loc)
            else:
                pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            pip.home()
            pip.pause("Please replace the empty tip racks!")
            pip.reset_tipracks()
            pip.pick_up_tip()

    # Wells
    tc_plate_wells = tc_plate.wells()[:samples]
    adapter_wells = temp_plate.wells()[:samples]
    ligation_mm = temp_plate['A6']

    # Protocol Steps

    # Pre-Cool Thermocycler and Temperature Module to 4C
    ctx.comment('Pre-Cooling Thermocycler to 4°C')
    ctx.comment('Pre-Cooling Temperature Module to 4°C')
    temp_mod.start_set_temperature(4)
    tc_mod.set_block_temperature(4)
    tc_mod.open_lid()
    temp_mod.await_temperature(4)
    ctx.pause('''Temperature Module has been cooled to 4°C.
              Please place your samples and reagents on the
              temperature module.''')

    # Mix Ligation MM
    pick_up(p300)
    p300.mix(10, 50, ligation_mm)
    p300.drop_tip()

        
