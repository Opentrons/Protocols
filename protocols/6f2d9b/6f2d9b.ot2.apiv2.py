from opentrons import protocol_api

metadata = {
    'protocolName': 'COVID-19 Sample Prep',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.9'
}

def get_values(*names):
    import json
    _all_values = json.loads("""{"p1000_mount":"left", "p20_mount":"right"}""")
    return [_all_values[n] for n in names]

def run(ctx):

    [p1000_mount, p20_mount] = get_values(  # noqa: F821
        "p1000_mount", "p20_mount")

    def pick_up(pip):
        """Function that can be used instead of .pick_up_tip() that will pause
        robot when robot runs out of tips, prompting user to replace tips
        before resuming"""
        try:
            pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            pip.home()
            ctx.pause("Please replace the empty tip rack.")
            pip.reset_tipracks()
            pip.pick_up_tip()

    # Load Labware
    dwp = ctx.load_labware('nest_96_wellplate_2ml_deep', 3) # Replace with real deep well plate during optimization
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', 6) # Replace with correct reservoir(s) during optimization
    tiprack_1000ul = ctx.load_labware('opentrons_96_filtertiprack_1000ul', 1)
    tiprack_20ul = ctx.load_labware('opentrons_96_filtertiprack_20ul', 2)

    # Load Pipettes
    p1000 = ctx.load_instrument('p1000_single_gen2', p1000_mount, tip_racks=[tiprack_1000ul])
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=[tiprack_20ul])

    # Reagents
    magbead = reservoir['A1']
    ms2 = reservoir['A2']
    proteinase = reservoir['A3']

    # Get sample wells, skip G12 and H12 for controls
    sample_wells = dwp.wells()[:-2]

    # Transfer Mag Bead Mix
    p1000.transfer(275, magbead, sample_wells)

    # Transfer MS2
    p20.transfer(5, ms2, sample_wells, new_tip='always')

    # Transfer Proteinase K
    for sample in sample_wells:
        pick_up(p20)
        p20.aspirate(5, proteinase)
        p20.dispense(5, sample)
        p20.drop_tip()

    # Remove Reservoir and Add Tube Racks
    ctx.pause('Please remove the reservoir on Slot 6, and add all the patient sample tube racks.')
    del ctx.deck['6']
    tuberacks = [ctx.load_labware('12x_multi_tuberack', slot) for slot in range(4, 12)]
    tube_wells = [well for rack in tuberacks for well in rack.wells()][:94]

    # Transfer 200 uL of Patient Samples to each well
    for source, dest in zip(tube_wells, sample_wells):
        pick_up(p1000)
        p1000.aspirate(200, source)
        p1000.dispense(200, dest)
        p1000.drop_tip()
