"""OPENTRONS."""
import math
from opentrons import types

metadata = {
    'protocolName': 'rhAmpSeq Library Prep Part 1 - PCR 1',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def run(ctx):
    """PROTOCOL."""
    [
     num_samples, m20_mount
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "num_samples", "m20_mount")

    # define all custom variables above here with descriptions:
    if m20_mount == 'right':
        m300_mount = 'left'
    else:
        m300_mount = 'right'
    num_cols = math.ceil(num_samples/8)
    num_etoh_wells = math.ceil((0.4*num_samples)/15)
    m20_speed_mod = 4
    airgap_library = 5
    etoh_res_vol = 15000
    # load modules
    mag_module = ctx.load_module('magnetic module gen2', '1')

    # load labware
    sample_plate = mag_module.load_labware('nest_96_wellplate'
                                           '_100ul_pcr_full_skirt')
    reagent_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',
                                     '2')
    reagent_resv = ctx.load_labware('nest_12_reservoir_15ml', '3')
    # load tipracks
    tiprack20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul',
                                  str(slot))
                 for slot in [4, 5]]
    tiprack300 = [ctx.load_labware('opentrons_96_filtertiprack_200ul',
                                   str(slot))
                  for slot in [6, 7, 8, 9, 10, 11]]
    # load instrument
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount, tip_racks=tiprack20)
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=tiprack300)
    # reagents
    sample_plate_dest = sample_plate.rows()[0][:num_cols]
    library_mix = reagent_plate.rows()[0][0]
    pcr_forward = reagent_plate.rows()[0][1]
    pcr_reverse = reagent_plate.rows()[0][2]
    beads_1 = reagent_plate.rows()[0][3]
    beads_2 = reagent_plate.rows()[0][4]
    idte = reagent_plate.rows()[0][5]
    # well volume tracking is better solution for this
    etoh_1 = reagent_resv.wells()[0]
    etoh_2 = reagent_resv.wells()[1]
    etoh_3 = reagent_resv.wells()[2]
    etoh_4 = reagent_resv.wells()[3]
    liquid_trash_1 = reagent_resv.wells()[8]
    liquid_trash_2 = reagent_resv.wells()[9]
    liquid_trash_3 = reagent_resv.wells()[10]
    liquid_trash_4 = reagent_resv.wells()[11]

    etoh_total = [etoh_1, etoh_2, etoh_3, etoh_4]
    trash_total = [liquid_trash_1, liquid_trash_2, liquid_trash_3,
                   liquid_trash_4]
    # Volume and Height Tracking
    # class VolHeightTracker:
    #     def __init__(self, labware, well_vol, start=0, end=12,
    #                  min_height=1, comp_coeff=0.9, msg='Reset Labware'):
    #         try:
    #             self.labware_wells = dict.fromkeys(
    #                 labware.wells()[start:end], 0)
    #         except Exception:
    #             self.labware_wells = dict.fromkeys(
    #                 labware, 0)
    #         self.labware_wells_backup = self.labware_wells.copy()
    #         self.well_vol = well_vol
    #         self.start = start
    #         self.end = end
    #         self.min_height = min_height
    #         self.comp_coeff = comp_coeff
    #         self.width = labware.wells()[0].xDimension
    #         self.length = labware.wells()[0].yDimension
    #         self.area = self.width*self.length
    #         self.msg = msg
    #
    #     def tracker(self, vol):
    #         '''tracker() will track how much liquid
    #         was used up per well. If the volume of
    #         a given well is greater than self.well_vol
    #         it will remove it from the dictionary and iterate
    #         to the next well which will act as the reservoir.'''
    #         well = next(iter(self.labware_wells))
    #         if self.labware_wells[well] + vol >= self.well_vol:
    #             del self.labware_wells[well]
    #             if len(self.labware_wells) < 1:
    #                 ctx.pause(self.msg)
    #                 self.labware_wells = self.labware_wells_backup.copy()
    #             well = next(iter(self.labware_wells))
    #         dh = (self.well_vol - self.labware_wells[well]) / self.area \
    #             * self.comp_coeff
    #         height = self.min_height if dh < 1 else round(dh, 2)
    #         self.labware_wells[well] = self.labware_wells[well] + vol
    #         ctx.comment(f'''{int(self.labware_wells[well])} uL of liquid
    #                     used from {well}''')
    #         ctx.comment(f'Current Liquid Height of {well}: {height}mm')
    #         return well.bottom(height)
    #
    #     def trash_tracker(self, vol):
    #         '''WIP trash_tracker() will track how much liquid
    #         was added per well. If the volume of
    #         a given well is greater than self.well_vol
    #         it will remove it from the dictionary and iterate
    #         to the next well which will act as the new trash.'''
    #         cutoff_vol = self.well_vol*0.75
    #         well = next(iter(self.labware_wells))
    #         if self.labware_wells[well] + vol >= cutoff_vol:
    #             del self.labware_wells[well]
    #             if len(self.labware_wells) < 1:
    #                 ctx.pause(self.msg)
    #                 self.labware_wells = self.labware_wells_backup.copy()
    #             well = next(iter(self.labware_wells))
    #         dh = (self.well_vol - self.labware_wells[well]) / self.area \
    #             * self.comp_coeff
    #         height = self.min_height if dh < 1 else round(dh, 2)
    #         self.labware_wells[well] = self.labware_wells[well] + vol
    #         ctx.comment(f'''{int(self.labware_wells[well])} uL of liquid
    #                     used from {well}''')
    #         ctx.comment(f'Current Liquid Height of {well}: {height}mm')
    #         return well.bottom(height)

    # etohTrack = VolHeightTracker(etoh_total, well_vol=etoh_res_vol, start=0,
    #                              end=96)
    etoh_volumes = dict.fromkeys(reagent_resv.wells()[:4], 0)
    supernatant_headspeed_modulator = 5

    def liquid_tracker(vol):
        '''liquid_tracker() will track how much liquid
        was used up per well. If the volume of
        a given well is greater than 'liquid'_res_vol
        it will remove it from the dictionary and iterate
        to the next well which will act as the reservoir.'''
        well = next(iter(etoh_volumes))
        if etoh_volumes[well] > etoh_res_vol:
            del etoh_volumes[well]
            well = next(iter(etoh_volumes))
        etoh_volumes[well] = etoh_volumes[well] + vol
        ctx.comment(f'{int(etoh_volumes[well])} uL of water used from {well}')
        return well

    def bead_mixing(well, pip, mvol, reps=8):

            """
            'bead_mixing' will mix liquid that contains beads. This will be done by
            aspirating from the bottom of the well and dispensing from the top as to
            mix the beads with the other liquids as much as possible. Aspiration and
            dispensing will also be reversed for a short to to ensure maximal mixing.
            param well: The current well that the mixing will occur in.
            param pip: The pipet that is currently attached/ being used.
            param mvol: The volume that is transferred before the mixing steps.
            param reps: The number of mix repetitions that should occur. Note~
            During each mix rep, there are 2 cycles of aspirating from bottom,
            dispensing at the top and 2 cycles of aspirating from middle,
            dispensing at the bottom
            """
            center = well.top().move(types.Point(x=0, y=0, z=5))
            aspbot = well.bottom(1)
            asptop = well.bottom(10)
            disbot = well.bottom(3)
            distop = well.top()

            vol = mvol * .9

            pip.move_to(center)
            for _ in range(reps):
                pip.aspirate(vol, aspbot)
                pip.dispense(vol, distop)
                pip.aspirate(vol, asptop)
                pip.dispense(vol, disbot)
    # PROTOCOL
    etoh_wash_vol = 200
    for dest in sample_plate_dest:
        m300.flow_rate.aspirate /= 4
        m300.flow_rate.dispense /= 4
        m300.pick_up_tip()
        m300.aspirate(30, beads_1)
        m300.dispense(30, dest)
        m300.flow_rate.aspirate *= 2
        m300.flow_rate.dispense *= 2
        bead_mixing(dest, m300, 30, reps=10)
        m300.flow_rate.aspirate *= 2
        m300.flow_rate.dispense *= 2
        m300.drop_tip()

    ctx.delay(minutes=10)
    mag_module.engage()
    ctx.delay(minutes=5)

    ctx.comment('''discarding supernatant''')
    ctx.max_speeds['Z'] = 50
    ctx.max_speeds['A'] = 50
    num_times = 1
    mag_module.engage()
    ctx.delay(minutes=3)
    for source in sample_plate_dest:
        side = 1 if num_times % 2 == 0 else -1
        m300.pick_up_tip()
        m300.flow_rate.aspirate /= 5
        m300.move_to(source.top())
        ctx.max_speeds['Z'] /= supernatant_headspeed_modulator
        ctx.max_speeds['A'] /= supernatant_headspeed_modulator
        m300.aspirate(
            50, source.bottom().move(types.Point(x=side,
                                                 y=0, z=0.5)))
        m300.move_to(source.top())
        m300.flow_rate.aspirate *= 5
        ctx.max_speeds['Z'] *= supernatant_headspeed_modulator
        ctx.max_speeds['A'] *= supernatant_headspeed_modulator
        m300.dispense(50, liquid_trash_1)
        m300.drop_tip()
        num_times += 1
        print(side)

        # etoh wash needs the multi-source well function to work!
    ctx.comment("Ethanol Wash")
    for _ in range(2):
        for dest in sample_plate_dest:
            m300.pick_up_tip()
            m300.aspirate(200, etoh_1)
            m300.dispense(200, dest)
            m300.drop_tip()
        ctx.delay(minutes=1)
        for source in sample_plate_dest:
            side = 1 if num_times % 2 == 0 else -1
            m300.pick_up_tip()
            m300.flow_rate.aspirate /= 5
            m300.move_to(source.top())
            ctx.max_speeds['Z'] /= supernatant_headspeed_modulator
            ctx.max_speeds['A'] /= supernatant_headspeed_modulator
            m300.aspirate(
                50, source.bottom().move(types.Point(x=side,
                                                     y=0, z=0.5)))
            m300.move_to(source.top())
            m300.flow_rate.aspirate *= 5
            ctx.max_speeds['Z'] *= supernatant_headspeed_modulator
            ctx.max_speeds['A'] *= supernatant_headspeed_modulator
            m300.dispense(50, liquid_trash_1)
            m300.drop_tip()
            num_times += 1
            print(side)

    ctx.delay(minutes=3)
    mag_module.disengage()
    ctx.comment('Adding IDTE')
    for dest in sample_plate_dest:
        m20.pick_up_tip()
        m20.aspirate(15, idte)
        m20.dispense(15, idte)
        m20.drop_tip()

    ctx.pause("Please vortex and centrifuge sample plate, return to slot 1")

    ctx.delay(minutes=3)
