from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'QIAseq Targeted DNA Panel Part 2',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

"""
Cleanup of Target Enrichment
"""

# labware setup
mag_module = modules.load('magdeck', '4')
mag_plate = labware.load('biorad-hardshell-96-PCR', '4', share=True)
plate = labware.load('biorad-hardshell-96-PCR', '1')
trough = labware.load('trough-12row', '5')
tipracks_300 = [labware.load('opentrons-tiprack-300ul', slot)
                for slot in ['7', '8', '9', '10', '11']]
tipracks_50 = [labware.load('opentrons-tiprack-300ul', slot)
               for slot in ['2', '3', '6']]

# instrument setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=tipracks_50)

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks_300)

# reagent setup
water = trough.wells('A1')
beads = trough.wells('A2')
ethanol_1 = trough.wells('A3')
ethanol_2 = trough.wells('A4')


m300_tip_count = 0
p50_tip_count = 0


def update_m300_tip_count(num):
    global m300_tip_count
    m300_tip_count += num
    if m300_tip_count == len(tipracks_300) * 12:
        print('reset p300')
        robot.pause('You have run out of tips for the P300 multi-channel \
pipette, refill the tip racks in slot 7, 8, 9, 10, and 11 before \
resuming.')
        m300.reset_tip_tracking()
        m300_tip_count = 0


def run_custom_protocol(
    number_of_samples: int=96,
    human_mitochondria_panel: StringSelection('True', 'False')='False'
        ):

    cols_num = number_of_samples // 8
    wells_num = number_of_samples % 8

    # make sure mag_module is disengaged
    mag_module.disengage()

    # add water to samples
    water_dest = [col[0].top() for col in mag_plate.cols[:cols_num]]
    m300.distribute(80, water, water_dest, disposal_vol=0)
    update_m300_tip_count(1)
    if wells_num:
        water_dest = [well.top()
                      for well in mag_plate.cols(cols_num)[:wells_num]]
        p50.transfer(80, water, water_dest)

    # add QIAseq Beads to samples
    bead_vol = (70 if human_mitochondria_panel == 'True' else 100)
    bead_dest = [col[0].top() for col in mag_plate.cols[:cols_num]]
    m300.distribute(bead_vol, beads, bead_dest, disposal_vol=0)
    update_m300_tip_count(1)
    if wells_num:
        bead_dest = [well.top()
                     for well in mag_plate.cols(cols_num)[:wells_num]]
        p50.transfer(bead_vol, beads, bead_dest)

    m300.delay(minutes=5)
    mag_module.engage()
    m300.delay(minutes=5)

    multi_dispense_loc = [
        col[0].top()
        for col in mag_plate.cols[:cols_num+(1 if wells_num else 0)]
        ]
    multi_aspirate_loc = [
        col[0]
        for col in mag_plate.cols[:cols_num+(1 if wells_num else 0)]
        ]

    # remove supernatant
    for col in multi_aspirate_loc:
        m300.transfer(200, col.bottom(1), m300.trash_container.top())
        update_m300_tip_count(1)

    # wash beads with ethanol
    for ethanol in [ethanol_1, ethanol_2]:
        m300.distribute(200, ethanol, multi_dispense_loc)
        update_m300_tip_count(1)
        for col in multi_dispense_loc:
            m300.transfer(200, col, m300.trash_container.top())
            update_m300_tip_count(1)

    # remove extra ethanol
    for col in multi_dispense_loc:
        m300.transfer(200, col, m300.trash_container.top())
        update_m300_tip_count(1)

    # air dry beads
    m300.delay(minutes=10)

    mag_module.disengage()

    # elute DNA
    for well in mag_plate.wells('A1', length=number_of_samples):
        p50.pick_up_tip()
        p50.transfer(16, water, well, new_tip='never')
        p50.mix(3, 10, well)
        p50.blow_out(well.top())
        p50.drop_tip()

    mag_module.engage()
    m300.delay(minutes=2)

    # transfer supernatant to clean plate
    sources = mag_plate.wells('A1', length=number_of_samples)
    dests = plate.wells('A1', length=number_of_samples)
    for source, dest in zip(sources, dests):
        p50.pick_up_tip()
        p50.transfer(13.4, source, dest, new_tip='never')
        p50.blow_out(dest.top())
        p50.drop_tip()
