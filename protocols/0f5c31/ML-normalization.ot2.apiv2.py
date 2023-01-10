from opentrons import protocol_api
from opentrons.protocol_api.labware import Well
from opentrons.types import Point
import math

# metadata
metadata = {
    'protocolName': 'Thermal Proteome Profiling (TPP)',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.13'
}


def run(ctx):

    [vol_h_lysate, mount_m300, mount_m20] = get_values(  # noqa: F821
        'vol_h_lysate', 'mount_m300', 'mount_m20')

    # modules
    tc = ctx.load_module('thermocycler')

    # labware
    tc_plate = tc.load_labware('eppendorftwintec_96_wellplate_150ul',
                               'heating plate')
    drug_plate = ctx.load_labware('eppendorftwintec_96_wellplate_150ul',
                                  '4', 'drug plate')
    filter_plate = ctx.load_labware('eppendorftwintec_96_wellplate_150ul',
                                    '5', 'filter plate')
    res12 = ctx.load_labware('nest_12_reservoir_15ml', '1',
                             'H lysate reservoir (column 1)')
    tiprack200 = [
        ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
        for slot in ['2', '3']]
    tiprack20 = [
        ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
        for slot in ['6']]

    # pipettes
    m300 = ctx.load_instrument('p300_multi_gen2', mount_m300,
                               tip_racks=tiprack200)
    m20 = ctx.load_instrument('p20_multi_gen2', mount_m20, tip_racks=tiprack20)

    # reagents and variables
    h_lysate = res12.rows()[0][0]
    l_lysate = res12.rows()[0][1]

    vol_l_lysate = 68.64
    reps_mix = 5
    vol_mix = vol_l_lysate*0.8
    vol_filter = 5.15
    block_temperatures = [i/2 for i in range(37*2, 68*2, int(2.5*2))]
    hold_time_minutes = 3.0
    tc.open_lid()

    def pick_up(pip):
        try:
            pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause(f'\n\n\n\nReplace \
{pip.tip_racks[0].wells()[0].max_volume}ul tipracks \
(slot \',\'.join{[rack.parent for rack in pip.tip_racks]}) before resuming.')
            pip.reset_tipracks()
            pip.pick_up_tip()

    def wick(pip, well, side=1):
        pip.move_to(well.bottom().move(Point(x=side*well.diameter/2*0.8, z=3)))

    def slow_withdraw(pip, well):
        ctx.max_speeds['A'] = 25
        ctx.max_speeds['Z'] = 25
        pip.move_to(well.top())
        del ctx.max_speeds['A']
        del ctx.max_speeds['Z']

    def custom_distribute(pip,
                          vol: float, source: Well,
                          destinations: list,
                          pre_airgap_vol: float = 0,
                          destination_height: float = 0.5,
                          wick_after: bool = True,
                          pick_up_tip: bool = True,
                          drop_tip: bool = True) -> None:

        vol_available_asp = pip.max_volume
        if pick_up_tip and not pip.has_tip:
            pick_up(pip)
        if vol < vol_available_asp:
            num_wells_per_asp = int(vol_available_asp // vol)
            num_asp = math.ceil(len(destinations)/num_wells_per_asp)
            dest_sets = [
                destinations[i*num_wells_per_asp:(i+1)*num_wells_per_asp]
                if i < num_asp - 1
                else destinations[i*num_wells_per_asp:]
                for i in range(num_asp)]
            for dest_set in dest_sets:
                if pre_airgap_vol > 0:
                    pip.aspirate(pre_airgap_vol, source.top())
                pip.aspirate(vol*len(dest_set), source)
                slow_withdraw(pip, source)
                for d in dest_set:
                    pip.dispense(vol, d.bottom(0.5))
                    if wick_after:
                        wick(pip, d)
        else:  # if volume > what can be accommodated by one aspiration
            num_transfers = math.ceil(vol/vol_available_asp)
            vol_per_transfer = round(vol/num_transfers, 2)
            for d in destinations:
                for _ in range(num_transfers):
                    pip.aspirate(vol_per_transfer, source)
                    slow_withdraw(pip, source)
                    for d in dest_set:
                        pip.dispense(vol_per_transfer, d.bottom(0.5))
                        if wick_after:
                            wick(pip, d)
        if drop_tip:
            pip.drop_tip()

    custom_distribute(m20, vol_h_lysate, h_lysate, filter_plate.rows()[0])

    ctx.pause('\n\n\n\nRemove filter plate (slot 5) and spin the H lysis \
into wells filter plate.\n\n\n\n')

    for i, (drug_well, heating_well) in enumerate(
            zip(drug_plate.rows()[0], tc_plate.rows()[0])):
        pick_up(m300)
        m300.aspirate(vol_l_lysate, l_lysate)
        slow_withdraw(m300, l_lysate)
        m300.dispense(vol_l_lysate, drug_well)
        m300.mix(reps_mix, vol_mix, drug_well)
        m300.aspirate(vol_l_lysate, drug_well.bottom(0.2))
        m300.dispense(vol_l_lysate, heating_well)
        slow_withdraw(m300, heating_well)
        m300.drop_tip()

        tc.close_lid()
        for temp in block_temperatures:
            tc.set_block_temperature(
                temp, hold_time_minutes=hold_time_minutes)
        tc.deactivate_block()
        tc.open_lid()

        custom_distribute(m20, vol_filter, heating_well,
                          filter_plate.rows()[0], destination_height=0.5,
                          wick_after=True, pick_up_tip=True, drop_tip=True)
        if i < len(drug_plate.rows()[0]) - 1:
            ctx.pause('\n\n\n\nCentrifuge filter plate. Insert a new filter \
plate on slot 5.\n\n\n\n')
        else:
            ctx.comment('\n\n\n\nCentrifuge filter plate. Protocol complete.')
