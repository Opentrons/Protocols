"""OPENTRONS."""
import math

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
     num_samp, m20_mount
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "num_samp", "m20_mount")

    # define all custom variables above here with descriptions:
    if m20_mount == 'right':
        m300_mount = 'left'
    else:
        m300_mount = 'right'
    num_cols = math.ceil(num_samp/8)
    num_etoh_wells = math.ceil((0.4*num_samp)/15)
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

    etoh_total = reagent_resv.rows()[:num_etoh_wells]
    # trash_total = [liquid_trash_1, liquid_trash_2, liquid_trash_3,
    #                liquid_trash_4]
    # Volume and Height Tracking

    class VolHeightTracker:
        def __init__(self, labware, well_vol, start=0, end=12,
                     min_height=1, comp_coeff=0.9, msg='Reset Labware'):
            try:
                self.labware_wells = dict.fromkeys(
                    labware.wells()[start:end], 0)
            except Exception:
                self.labware_wells = dict.fromkeys(
                    labware, 0)
            self.labware_wells_backup = self.labware_wells.copy()
            self.well_vol = well_vol
            self.start = start
            self.end = end
            self.min_height = min_height
            self.comp_coeff = comp_coeff
            self.width = labware.wells()[0].xDimension
            self.length = labware.wells()[0].yDimension
            self.area = self.width*self.length
            self.msg = msg

        def tracker(self, vol):
            '''tracker() will track how much liquid
            was used up per well. If the volume of
            a given well is greater than self.well_vol
            it will remove it from the dictionary and iterate
            to the next well which will act as the reservoir.'''
            well = next(iter(self.labware_wells))
            if self.labware_wells[well] + vol >= self.well_vol:
                del self.labware_wells[well]
                if len(self.labware_wells) < 1:
                    ctx.pause(self.msg)
                    self.labware_wells = self.labware_wells_backup.copy()
                well = next(iter(self.labware_wells))
            dh = (self.well_vol - self.labware_wells[well]) / self.area \
                * self.comp_coeff
            height = self.min_height if dh < 1 else round(dh, 2)
            self.labware_wells[well] = self.labware_wells[well] + vol
            ctx.comment(f'''{int(self.labware_wells[well])} uL of liquid
                        used from {well}''')
            ctx.comment(f'Current Liquid Height of {well}: {height}mm')
            return well.bottom(height)

        def trash_tracker(self, vol):
            '''WIP trash_tracker() will track how much liquid
            was added per well. If the volume of
            a given well is greater than cutoff_vol
            it will remove it from the dictionary and iterate
            to the next well which will act as the new trash.'''
            cutoff_vol = self.well_vol*0.75
            well = next(iter(self.labware_wells))
            if self.labware_wells[well] + vol >= cutoff_vol:
                del self.labware_wells[well]
                if len(self.labware_wells) < 1:
                    ctx.pause(self.msg)
                    self.labware_wells = self.labware_wells_backup.copy()
                well = next(iter(self.labware_wells))
            dh = (self.well_vol - self.labware_wells[well]) / self.area \
                * self.comp_coeff
            height = self.min_height if dh < 1 else round(dh, 2)
            self.labware_wells[well] = self.labware_wells[well] + vol
            ctx.comment(f'''{int(self.labware_wells[well])} uL of liquid
                        used from {well}''')
            ctx.comment(f'Current Liquid Height of {well}: {height}mm')
            return well.bottom(height)

    etohTrack = VolHeightTracker(etoh_total, well_vol=etoh_res_vol, start=0,
                                 end=96)
    etoh_volumes = dict.fromkeys(reagent_resv.wells()[:4], 0)

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

    # PROTOCOL
    etoh_wash_vol = 200
    for dest in sample_plate_dest:
        m300.transfer(etoh_wash_vol, etohTrack.tracker(etoh_wash_vol*8), dest,
                      new_tip='never')
