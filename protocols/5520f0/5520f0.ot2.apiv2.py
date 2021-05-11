metadata = {
    'protocolName': 'Staining Cell-Based Assay Plates',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    [m300_mount, cols] = get_values(  # noqa: F821
        "m300_mount", "cols")

    # Load Labware
    plate = ctx.load_labware('perkinelmer_384_wellplate_145ul', 1)
    pbs_reservoir = ctx.load_labware('nest_12_reservoir_15ml', 2)
    reagent_reservoir = ctx.load_labware('nest_12_reservoir_15ml', 3)
    pbs_waste_reservoir = ctx.load_labware('nest_12_reservoir_15ml', 4)
    tipracks = [ctx.load_labware('opentrons_96_tiprack_300ul',
                                 slot) for slot in range(5, 9)]

    # Load Pipette
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=tipracks)

    # Single Well Reagents
    primary_antibody = reagent_reservoir.rows()[0][4]
    secondary_antibody = reagent_reservoir.rows()[0][5]

    # Destination Wells
    dest_wells = [plate.rows()[i][col] for col in range(cols) for i in
                  range(2)][:cols*2]

    # Volume Tracking
    class VolTracker:
        def __init__(self, labware, well_vol, pip_type='single',
                     mode='reagent', start=0, end=12):
            self.labware_wells = dict.fromkeys(labware.wells()[start:end], 0)
            self.well_vol = well_vol
            self.pip_type = pip_type
            self.mode = mode
            self.start = start
            self.end = end

        def tracker(self, vol):
            '''tracker() will track how much liquid
            was used up per well. If the volume of
            a given well is greater than self.well_vol
            it will remove it from the dictionary and iterate
            to the next well which will act as the reservoir.'''
            well = next(iter(self.labware_wells))
            if self.labware_wells[well] >= self.well_vol:
                del self.labware_wells[well]
                well = next(iter(self.labware_wells))
            if self.pip_type == 'multi':
                self.labware_wells[well] = self.labware_wells[well] + vol*8
            elif self.pip_type == 'single':
                self.labware_wells[well] = self.labware_wells[well] + vol
            if self.mode == 'waste':
                ctx.comment(f'''{well}: {int(self.labware_wells[well])} uL of
                            total waste''')
            else:
                ctx.comment(f'''{int(self.labware_wells[well])} uL of liquid
                            used from {well}''')
            return well

    # Volume Trackers for Multi-well Reagents
    pbsWasteTrack = VolTracker(pbs_waste_reservoir, 15000, 'multi', 'waste')
    reagentWasteTrack = VolTracker(reagent_reservoir, 15000, 'multi', 'waste',
                                   6, 12)
    pbsTrack = VolTracker(pbs_reservoir, 15000, 'multi')
    pfaTrack = VolTracker(reagent_reservoir, 10000, 'multi', start=0, end=2)
    permTrack = VolTracker(reagent_reservoir, 10000, 'multi', start=2, end=4)

    # Protocol Steps

    # Add/Remove PBS
    def add_remove_pbs(wells, vol):
        m300.pick_up_tip()
        for well in wells:
            m300.aspirate(vol, pbsTrack.tracker(vol))
            m300.dispense(vol, well)
            m300.aspirate(vol, well)
            m300.dispense(vol, pbsWasteTrack.tracker(vol))
        m300.drop_tip()

    # Remove Media (1)
    m300.pick_up_tip()
    for well in dest_wells:
        m300.transfer(45, well, pbsWasteTrack.tracker(45), new_tip='never')
    m300.drop_tip()
    # Add/Remove PBS (2-3)
    add_remove_pbs(dest_wells, 50)
    # Add/Remove PBS (4-5)
    add_remove_pbs(dest_wells, 50)

    # Add/Remove 4% PFA (6-8)
    m300.pick_up_tip()
    for well in dest_wells:
        m300.transfer(50, pfaTrack.tracker(50), well, new_tip='never')
    m300.drop_tip()
    ctx.delay(minutes=20, msg='Pausing for 20 minutes...')
    m300.pick_up_tip()
    for well in dest_wells:
        m300.transfer(50, well, reagentWasteTrack.tracker(50), new_tip='never')
    m300.drop_tip()

    # Add/Remove Perm Buffer (9-11)
    m300.pick_up_tip()
    for well in dest_wells:
        m300.transfer(50, permTrack.tracker(50), well, new_tip='never')
    m300.drop_tip()
    ctx.delay(minutes=15, msg='Pausing for 15 minutes...')
    m300.pick_up_tip()
    for well in dest_wells:
        m300.transfer(50, well, reagentWasteTrack.tracker(50), new_tip='never')
    m300.drop_tip()

    # Add/Remove PBS (12-13)
    add_remove_pbs(dest_wells, 50)
    # Add/Remove PBS (14-15)
    add_remove_pbs(dest_wells, 50)

    # Add/Remove Primary Antibody Solution (16-18)
    m300.pick_up_tip()
    for well in dest_wells:
        m300.transfer(25, primary_antibody, well, new_tip='never')
    m300.drop_tip()
    ctx.delay(minutes=60, msg='Pausing for 60 minutes...')
    m300.pick_up_tip()
    for well in dest_wells:
        m300.transfer(25, well, reagentWasteTrack.tracker(25), new_tip='never')
    m300.drop_tip()

    # Add/Remove PBS (19-20)
    add_remove_pbs(dest_wells, 50)
    # Add/Remove PBS (21-22)
    add_remove_pbs(dest_wells, 50)

    # Add/Remove Secondary Antibody Solution (23-25)
    m300.pick_up_tip()
    for well in dest_wells:
        m300.transfer(25, secondary_antibody, well, new_tip='never')
    m300.drop_tip()
    ctx.delay(minutes=30, msg='Pausing for 30 minutes...')
    m300.pick_up_tip()
    for well in dest_wells:
        m300.transfer(25, well, reagentWasteTrack.tracker(25), new_tip='never')
    m300.drop_tip()

    # Add/Remove PBS (26-27)
    add_remove_pbs(dest_wells, 50)
    # Add/Remove PBS (28-29)
    add_remove_pbs(dest_wells, 50)

    # Add PBS (30)
    m300.pick_up_tip()
    for well in dest_wells:
        m300.aspirate(50, pbsTrack.tracker(50))
        m300.dispense(50, well)
    m300.drop_tip()
