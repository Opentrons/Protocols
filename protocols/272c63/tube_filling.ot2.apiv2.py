from opentrons.types import Point

# metadata
metadata = {
    'protocolName': 'Tube Filling',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.4'
}


def run(ctx):

    num_samples, p1000_mount, input_csv = [
        24, 'left',
        'distance down tube to aspirate (in mm),aspiration speed (in ul/s),\
        dispense speed (in ul/s)\n20,100,100\n20,100,100\n']

    tiprack1000 = [ctx.load_labware('opentrons_96_tiprack_1000ul', '1')]
    sample_racks = [
        ctx.load_labware('custom_6_tuberack_100ml', slot, 'Samples ' + name)
        for slot, name in zip(['5', '2', '6', '3'],
                              ['1, 2, 5, 6, 9, 10', '3, 4, 7, 8, 11, 12',
                               '13, 14, 17, 18, 21, 22',
                               '15, 16, 19, 20, 23, 24'])]
    lw_racks = [
        ctx.load_labware('custom_15_tuberack_6000ul', slot, name)
        for slot, name in zip(['10', '11'], ['LW 1-15', 'LW 16-24 (6 spare)'])]
    icp_racks = [
        ctx.load_labware('custom_15_tuberack_6000ul', slot, name)
        for slot, name in zip(['7', '8'],
                              ['ICP 1-15', 'ICP 16-24 (6 spare)'])]
    ir_rack = ctx.load_labware('custom_24_testtuberack_2ml', '4',
                               'IR tubes (1-24)')

    # pipette
    p1000 = ctx.load_instrument('p1000_single_gen2', p1000_mount,
                                tip_racks=tiprack1000)

    # parse .csv file
    csv_data = [
        [val.strip() for val in line.split(',')]
        for line in input_csv.splitlines()[1:]
        if line]
    depths, asp_rates, dispense_rates = [
        [float(line[ind]) for line in csv_data]
        for ind in range(3)]
    samples_odered = [
        well
        for i in range(2)
        for j in range(3)
        for rack in sample_racks[i*2:i*2+2]
        for well in rack.columns()[j]][:num_samples]
    lw_ordered = [
        well
        for rack in lw_racks
        for col in rack.columns()
        for well in col[::-1]][:num_samples]
    icp_ordered = [
        well
        for rack in icp_racks
        for col in rack.columns()
        for well in col[::-1]][:num_samples]
    ir_ordered = ir_rack.wells()[:num_samples]

    # transfers
    for asp_rate, dispense_rate, depth, s, icp, lw, ir in zip(
            asp_rates, dispense_rates, depths, samples_odered, icp_ordered,
            lw_ordered, ir_ordered):
        p1000.flow_rate.aspirate = asp_rate
        p1000.flow_rate.dispense = dispense_rate
        p1000.pick_up_tip()
        p1000.aspirate(1000, s.top(-1*depth))
        p1000.dispense(500, icp.top(-2))
        p1000.dispense(500, lw.top(-2))
        p1000.aspirate(1000, s.top(-1*depth))
        p1000.dispense(500, ir.top(-2))
        p1000.drop_tip()
