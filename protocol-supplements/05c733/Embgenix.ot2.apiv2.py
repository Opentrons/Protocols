import math
from opentrons.types import Point

metadata = {
    'protocolName': 'Embgenix™ PGT-A Kit: Preparation of Whole Genome \
Amplification',
    'author': 'Nick <ndiehl@opentrons.com',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.12'
}

PERFORM_CELL_LYSIS_PREP = True
PERFORM_WHOLE_GENOME_AMPLIFICATION_PREP = True
PERFORM_DILUTION_OF_WHOLE_GENOME_AMPLIFICATION_PRODUCTS = True
PERFORM_FRAGMENTATION_AND_ADAPTER_LIGATION = True
PERFORM_LIBRARY_AMPLIFICATION_AND_INDEXING = True


def run(ctx):

    num_samples = 16
    vol_sample = 5.0
    m20_mount = 'left'
    m300_mount = 'right'

    # labware
    tuberack = ctx.load_labware(
        'opentrons_24_aluminumblock_nest_1.5ml_snapcap', '4',
        '1.5ml Eppendorf tube aluminum block')
    distribution_plate = ctx.load_labware(
        'eppendorftwin.tec96_96_aluminumblock_200ul', '5',
        'plate for mix distribution')
    udi_plate = ctx.load_labware('axygen_96well_pcr_microplate_200ul', '6',
                                 'UDI plate')
    tempdeck = ctx.load_module('temperature module gen2', '7')
    tempdeck.set_temperature(4)
    sample_plate = tempdeck.load_labware(
        'opentrons_96_aluminumblock_biorad_wellplate_200ul', 'sample plate')
    tipracks20 = [
        ctx.load_labware('opentrons_96_filtertiprack_20ul', '8')]
    tipracks200 = [
        ctx.load_labware('opentrons_96_filtertiprack_200ul', '9')]

    # pipettes
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount,
                              tip_racks=tipracks20)
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=tipracks200)

    m20.flow_rate.aspirate /= 3
    m20.flow_rate.dispense /= 3
    m300.flow_rate.aspirate /= 3
    m300.flow_rate.dispense /= 3

    # reagents
    num_cols = math.ceil(num_samples/8)

    samples_s = sample_plate.wells()[:num_samples]
    samples_m = sample_plate.rows()[0][:num_cols]
    dilution1_samples_s = sample_plate.wells()[num_samples:num_samples*2]
    dilution1_samples_m = sample_plate.rows()[0][num_cols:num_cols*2]
    dilution2_samples_s = sample_plate.wells()[num_samples*2:num_samples*3]
    dilution2_samples_m = sample_plate.rows()[0][num_cols*2:num_cols*3]
    ligation_samples_m = sample_plate.rows()[0][num_cols*3:num_cols*4]
    udi_m = udi_plate.rows()[0][:num_cols]

    mm_ce = tuberack.wells_by_name()['A1']
    mm_wga = tuberack.wells_by_name()['B1']
    wd1 = tuberack.wells_by_name()['C1']
    wd2 = tuberack.wells_by_name()['D1']
    mm_library_prep = tuberack.wells_by_name()['A2']
    mm_library_amp = tuberack.wells_by_name()['B2']
    stem_loop_adapters = tuberack.wells_by_name()['C2']

    def pick_up(pip, num_tips):
        tip_cols = [col for rack in pip.tip_racks for col in rack.columns()]
        for col in tip_cols:
            count = 0
            for tip in col[::-1]:
                if tip.has_tip:
                    count += 1
                if count == num_tips:
                    pip.pick_up_tip(tip)
                    return
        ctx.pause(f'Refill {pip.tip_racks[0].wells()[0].max_volume}uL tiprack \
 before resuming.')
        pip.reset_tipracks()
        pick_up(pip, num_tips)

    def wick(pip, well, side=1):
        pip.move_to(well.bottom().move(Point(x=side*well.diameter/2*0.8, z=3)))

    def slow_withdraw(well, pip=m20):
        ctx.max_speeds['A'] = 25
        ctx.max_speeds['Z'] = 25
        pip.move_to(well.top())
        del ctx.max_speeds['A']
        del ctx.max_speeds['Z']

    def column_distribute(volume, source, distribution_column,
                          final_destinations_s=samples_s,
                          final_destinations_m=samples_m, mix_reps=10,
                          mix_vol=10, new_tip=True, drop_tip=True):
        if num_cols > 1:
            vol_per_row = volume*num_cols*1.1  # overage
            pip = m300 if vol_per_row > 20 else m20
            pick_up(pip, 1)
            wells_per_asp = math.floor(
                pip.tip_racks[0].wells()[0].max_volume//vol_per_row)
            num_aspirations = math.ceil(8/wells_per_asp)
            distribution_chunks = [
                distribution_column[i*wells_per_asp:(i+1)*wells_per_asp]
                if i < num_aspirations - 1
                else distribution_column[i*wells_per_asp:]
                for i in range(num_aspirations)
            ]
            for chunk in distribution_chunks:
                pip.aspirate(vol_per_row*len(chunk), source)
                for well in chunk:
                    pip.dispense(vol_per_row, well.bottom(1))
                    wick(pip, well)
            pip.drop_tip()

            # reassign pipette based on transfer volume per sample
            pip = m300 if volume > 20 else m20
            if not new_tip:
                pick_up(pip, 8)
            for i, s in enumerate(final_destinations_m):
                if not pip.has_tip:
                    pick_up(pip, 8)
                pip.transfer(volume, distribution_column[0].bottom(-2),
                             s.bottom(1), new_tip='never')
                if mix_reps > 0:
                    pip.mix(mix_reps, mix_vol, s.bottom(1))
                # wick(pip, s)
                slow_withdraw(s, pip)
                if new_tip:
                    if i < len(final_destinations_m) or drop_tip:
                        pip.drop_tip()
            if pip.has_tip and drop_tip:
                pip.drop_tip()
        else:
            pip = m300 if volume > 20 else m20
            if not new_tip:
                pick_up(pip, 1)
            for i, s in enumerate(final_destinations_s):
                if not pip.has_tip:
                    pick_up(pip, 1)
                pip.transfer(volume, source, s.bottom(-2), new_tip='never')
                pip.mix(mix_reps, mix_vol, s.bottom(1))
                # wick(pip, s)
                slow_withdraw(s, pip)
                if new_tip:
                    if i < len(final_destinations_s) - 1 or drop_tip:
                        pip.drop_tip()
            if pip.has_tip and drop_tip:
                pip.drop_tip()

    """
    V. Preparation of Whole Genome Amplification
    """

    """ V:A — Cell Lysis/gDNA Extraction"""
    if PERFORM_CELL_LYSIS_PREP:
        vol_total_reaction = 30.0
        vol_mm_ce = vol_total_reaction - vol_sample
        column_distribute(vol_mm_ce, mm_ce, distribution_plate.columns()[0],
                          mix_reps=0)

        ctx.pause('Proceed with steps V:A:4-7 and replace sample plate on \
temperature module before resuming.')

    """ V:B — Whole Genome Amplification"""
    if PERFORM_WHOLE_GENOME_AMPLIFICATION_PREP:
        vol_mm_wga = 45.0
        column_distribute(vol_mm_wga, mm_wga, distribution_plate.columns()[1],
                          mix_vol=75*0.6)

        ctx.pause('Proceed with steps V:B:4-5 and replace sample plate on \
temperature module before resuming.')

    """ V:C — Dilution of Whole Genome Amplified Products"""
    if PERFORM_DILUTION_OF_WHOLE_GENOME_AMPLIFICATION_PRODUCTS:
        vol_wd1 = 76.0
        vol_wga_product = 4.0
        # pre-transfer dilution buffer
        column_distribute(vol_wd1, wd1, distribution_plate.columns()[2],
                          final_destinations_m=dilution1_samples_m,
                          final_destinations_s=dilution1_samples_s, mix_reps=0,
                          new_tip=False)

        # transfer sample to dilution and mix
        for s, d in zip(samples_m, dilution1_samples_m):
            pick_up(m20, 8)
            m20.transfer(vol_wga_product, s, d, mix_after=(10, 20),
                         new_tip='never')
            wick(m20, d)
            m20.drop_tip()

        vol_wd2 = 55.0
        vol_wga_product = 5.0
        # pre-transfer dilution buffer
        column_distribute(vol_wd2, wd2, distribution_plate.columns()[3],
                          final_destinations_m=dilution2_samples_m,
                          final_destinations_s=dilution2_samples_s, mix_reps=0,
                          new_tip=False)

        # transfer sample to dilution and mix
        for s, d in zip(dilution1_samples_m, dilution2_samples_m):
            pick_up(m20, 8)
            m20.transfer(vol_wga_product, s, d, mix_after=(10, 20),
                         new_tip='never')
            wick(m20, d)
            m20.drop_tip()

    """
    VI. Library Preparation
    """

    """ VI:A — Fragmentation and Adapter Ligation"""
    if PERFORM_FRAGMENTATION_AND_ADAPTER_LIGATION:
        vol_stem_loop_adapters = 4.0
        vol_wd2_product = 8.0

        column_distribute(vol_stem_loop_adapters,
                          stem_loop_adapters,
                          distribution_plate.columns()[4],
                          final_destinations_m=ligation_samples_m,
                          mix_reps=0,
                          new_tip=False,
                          drop_tip=False)

        for s, d in zip(dilution2_samples_m, ligation_samples_m):
            if not m20.has_tip:
                pick_up(m20, 8)
            wick(m20, d)
            m20.transfer(vol_wd2_product, s, d, mix_after=(10, 20),
                         new_tip='never')
            wick(m20, d)
            m20.drop_tip()

        # library prep mm
        vol_mm_library_prep = 10.5
        column_distribute(vol_mm_library_prep, mm_library_prep,
                          distribution_plate.columns()[5],
                          final_destinations_m=ligation_samples_m, mix_reps=10,
                          new_tip=True)

        ctx.pause('Proceed with steps VI:A:7-8 and replace sample plate on \
temperature module before resuming.')

    """ VIB — Library Amplification and Indexing with UDI """
    if PERFORM_LIBRARY_AMPLIFICATION_AND_INDEXING:
        # library prep mm
        vol_mm_library_amp = 25.5
        column_distribute(vol_mm_library_amp, mm_library_amp,
                          distribution_plate.columns()[6],
                          final_destinations_m=ligation_samples_m, mix_reps=1,
                          new_tip=True)

        # transfer UDI primers
        vol_udi = 2.0
        for s, d in zip(udi_m, ligation_samples_m):
            pick_up(m20, 8)
            m20.aspirate(vol_udi, s)
            m20.move_to(s.top(5))
            ctx.delay(seconds=10)
            m20.dispense(vol_udi, d)
            m20.mix(10, 20, d)
            wick(m20, d)
            m20.drop_tip()

        ctx.comment('Proceed with steps VI:B:5-7. Protocol complete.')
