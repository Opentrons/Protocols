from opentrons import labware, instruments, robot
from otcustomizers import FileInput

metadata = {
    'protocolName': 'NGS CSV Preparation',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware
plate = labware.load('biorad-hardshell-96-PCR', '1')
tubes = labware.load('opentrons-tuberack-2ml-eppendorf', '2')
tips10 = labware.load('tiprack-10ul', '4')
tips50 = labware.load('opentrons-tiprack-300ul', '5')

# pipettes
p10 = instruments.P10_Single(mount='right', tip_racks=[tips10])
p50 = instruments.P50_Single(mount='left', tip_racks=[tips50])

# reagents
buffer_eb = tubes.wells('A1')

example_csv = """Pool#,Sample Well,Sample ID,Index,index sequence,SpectraMax, \
 Molarity (nM),Target Concentration nM,Dil Factor,Library volume to add to \
 pool uL,Volume uL,EB Volume to add to pool uL,,,
Pool1,A6,PDC0027,A06,AGCCATGC,12.38,3.0,4.13,2.42,10,30.12,,,
Pool1,C10,PFT0141,C10,AGATCGCA,12.23,3.0,4.08,2.45,10,,,,
Pool1,G11,PFT0153,G11,AACAACCA,12.01,3.0,4.00,2.50,10,,,,
Pool1,D8,PFT0126,D08,ACAGCAGA,11.99,3.0,4.00,2.50,10,,,,
Pool2,E12,HCC-1954-BL_NORMAL_repA,E12,ACACAGAA,11.61,3.0,3.87,2.58,10,14.79,,,
Pool2,E3,HAPMAP-CONTROL-POOL-XX_repA,E03,ACCTCCAA,11.45,3.0,3.82,2.62,10,,,,
Pool3,F12,NCI-H1395_TUMOR_repA,F12,GAACAGGC,11.32,3.0,3.77,2.65,10,21.89,,,
Pool3,G12,NCI-1395-BL_NORMAL_repA,G12,AACCGAGA,11.06,3.0,3.69,2.71,10,,,,
Pool3,E1,PDA02848,E01,GCCAAGAC,10.91,3.0,3.64,2.75,10,,,,
"""


def run_custom_protocol(CSV_file: FileInput = example_csv):
    pools = {}
    buffer_vols = {}
    wells = {}

    # parse CSV, ignoring headers on first line and empty lines
    rows = CSV_file.splitlines()[1:]
    info = [line.split(',') for line in rows if line]
    for ind, line in enumerate(info):
        pool = line[0].strip()[4:]
        if pool not in pools:
            pools[pool] = {}
            wells = {}
        well = line[1].strip()
        vol = float(line[8])
        wells[well] = vol
        pools[pool] = wells
        if line[10]:
            buffer_vol = float(line[10].strip())
            # buffer_vols.append(buffer_vol)
            buffer_vols[pool] = buffer_vol

    # sort pools and buffer volumes in case CSV is out of pool-ascending order
    s = sorted(pools)
    sorted_pools = {}
    sorted_buffer_vols = {}
    for key in s:
        sorted_pools[key] = pools[key]
        sorted_buffer_vols[key] = buffer_vols[key]

    # setup tip counters
    tips10_needed = 0
    tips50_needed = 0
    for p in sorted_pools:
        set = sorted_pools[p]
        for well in set:
            if set[well] <= 10:
                tips10_needed += 1
            else:
                tips50_needed += 1
    for p in sorted_buffer_vols:
        vol = sorted_buffer_vols[p]
        if vol <= 10:
            tips10_needed += 1
        else:
            tips50_needed += 1

    tips10_count = 0
    tips50_count = 0
    # perform transfers
    pool_count = 1
    for p_ind in pools:
        wells = pools[p_ind]
        b_vol = buffer_vols[p_ind]
        pool_tube = tubes.wells(pool_count)

        for well in wells:
            vol = wells[well]
            pipette = p50 if vol > 10 else p10
            pipette.pick_up_tip()
            pipette.transfer(
                vol,
                plate.wells(well),
                pool_tube,
                blow_out=True,
                new_tip='never'
            )
            pipette.drop_tip()

        if b_vol > 10:
            pipette = p50
            tips10_count += 1
        else:
            pipette = p10
            tips50_count += 1

        if tips50_count >= 96:
            robot.pause('Please replace 300ul tiprack in slot 5 before '
                        'resuming.')
            tips50_count = 0
            p50.reset()
        if tips10_count >= 96:
            robot.pause('Please replace 10ul tiprack in slot 4 before '
                        'resuming.')
            tips10_count = 0
            p10.reset()

        pipette.pick_up_tip()
        pipette.transfer(
            b_vol,
            buffer_eb,
            pool_tube,
            blow_out=True,
            new_tip='never'
        )
        pipette.touch_tip(pool_tube)
        pipette.drop_tip()

        pool_count += 1
        if pool_count == 24:
            robot.pause('Please replace pool tubes in tuberack wells B1-D6 '
                        'before continuing.')
            pool_count = 1
