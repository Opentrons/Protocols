from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'NGS Library Prep',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


def run_custom_protocol(
        number_of_columns: int=12,
        p10_tiprack_type: StringSelection(
            'opentrons_96_tiprack_10ul',
            'fisherbrand-filter-tiprack-10ul',
            'phenix-filter-tiprack-10ul')='phenix-filter-tiprack-10ul',
        p50_tiprack_type: StringSelection(
            'opentrons_96_tiprack_300ul',
            'fisherbrand-filter-tiprack-200ul',
            'phenix-filter-tiprack-300ul')='phenix-filter-tiprack-300ul'):

    for tiprack_type in [p10_tiprack_type, p50_tiprack_type]:
        if tiprack_type not in labware.list():
            labware.create(
                tiprack_type,
                grid=(12, 8),
                spacing=(9, 9),
                diameter=5,
                depth=60)

    # labware setup
    plate = labware.load('biorad-hardshell-96-PCR', '1')
    mag_module = modules.load('magdeck', '4')
    mag_plate = labware.load('biorad-hardshell-96-PCR', '4', share=True)
    reagent_tubes = labware.load('96-PCR-tall', '5')
    deep_plate = labware.load('96-deep-well', '7')
    trough = labware.load('trough-12row', '8')

    tipracks_10 = [labware.load(p10_tiprack_type, slot)
                   for slot in ['10', '11']]
    tipracks_50 = [labware.load(p50_tiprack_type, slot)
                   for slot in ['2', '3', '6', '9']]

    # instruments setup
    m10 = instruments.P10_Multi(
        mount='right',
        tip_racks=tipracks_10)
    m50 = instruments.P50_Multi(
        mount='left',
        tip_racks=tipracks_50)

    # tip counters
    m50_tip_count = 0
    m10_tip_count = 0

    # reagent setup
    rxn_buffer_mm = reagent_tubes.cols('1')
    mastermix = reagent_tubes.cols('2')
    y_yoke_adapter = reagent_tubes.cols('3')
    q5_mastermix = reagent_tubes.cols('4')
    speedbeads = deep_plate.cols('1')
    ethanol = trough.wells('A1')
    tle = trough.wells('A2')

    def update_m50_tip_count(num):
        """This counts the number of tips used for the P50Multi and pauses the
        protocol and prompts user to refill tip racks when neccessary.
        """
        nonlocal m50_tip_count
        if m50_tip_count == len(tipracks_50) * 12:
            robot.pause("Your 300 uL tips have run out. Replenish tip racks \
    before resuming.")
            m50.reset_tip_tracking()
            m50_tip_count = 0
        m50_tip_count += num

    def update_m10_tip_count(num):
        """This counts the number of tips used for the P10Single and pauses the
        protocol and prompts user to refill tip racks when neccessary.
        """
        nonlocal m10_tip_count
        if m10_tip_count == len(tipracks_10) * 12:
            robot.pause("Your 10 uL tips have run out. Replenish tip racks \
    before resuming.")
            m10.reset_tip_tracking()
            m10_tip_count = 0
        m10_tip_count += num

    # define sample columns
    sample_cols = plate.rows('A').wells('1', length=number_of_columns)

    # transfer Rxn Buffer Master Mix to samples
    update_m10_tip_count(1)
    for well in sample_cols:
        m10.pick_up_tip()
        m10.aspirate(4.5, rxn_buffer_mm)
        m10.dispense(4.5, well)
        m10.blow_out(well.top())
        m10.drop_tip()

    robot.pause("Quickly vortex and spin down. Place on Thermocycler (37C for \
12 minutes, 65C for 30 minutes, hold at 4C. While on Thermocycler create \
master mix for Ligation. Place the plate back to slot 1 before resuming the \
protocol.")

    # transfer and mix master mix to samples
    for well in sample_cols:
        update_m50_tip_count(1)
        m50.transfer(15.5, mastermix, well, mix_after=(3, 10))

    # add Y yoke adapter to samples
    for well in sample_cols:
        update_m10_tip_count(1)
        m10.pick_up_tip()
        m10.transfer(1.3, y_yoke_adapter, well, new_tip='never')
        m10.mix(3, 5)
        m10.blow_out()
        m10.drop_tip()

    robot.pause("Spin to remove liquid from sides. Incubate at 20C for 15 \
minutes on thermocycler. Place the plate on the Magnetic Module before \
resuming the protocol. Place a clean plate in slot 1.")

    # update sample columns as plate is now on magnetic module
    sample_cols = mag_plate.rows('A').wells('1', length=number_of_columns)

    # transfer beads to samples
    for well in sample_cols:
        update_m50_tip_count(1)
        m50.pick_up_tip()
        m50.mix(3, 50, speedbeads)
        m50.transfer(32.3, speedbeads, well, new_tip='never')
        m50.mix(5, 30)
        m50.blow_out(well)
        m50.drop_tip()

    m50.delay(minutes=5)
    mag_module.engage()
    m50.delay(minutes=2)

    for col_index, well in enumerate(sample_cols, 1):
        # remove supernatant
        update_m50_tip_count(1)
        m50.transfer(100, well, m10.trash_container.top())
        # wash beads twice
        for _ in range(2):
            update_m50_tip_count(1)
            m50.pick_up_tip()
            m50.transfer(100, ethanol, well, new_tip='never')
            m50.delay(seconds=1)
            m50.transfer(120, well, m50.trash_container.top(), new_tip='never')
            m50.drop_tip()
        # mix in TLE
        mag_module.disengage()
        update_m50_tip_count(1)
        m50.transfer(17.5, tle, well, mix_after=(3, 10))
        mag_module.engage()
        m50.delay(minutes=2)
    # define columns in output plate
    output_cols = plate.rows('A').wells('1', length=number_of_columns)

    # distribute Q5 master mix
    update_m50_tip_count(1)
    m50.distribute(
            12.5,
            q5_mastermix,
            [col for col in output_cols],
            disposal_vol=0)

    # transfer samples to new plate
    for source, dest in zip(sample_cols, output_cols):
        update_m10_tip_count(1)
        m10.transfer(10, source, dest, blow_out=True)

    mag_module.disengage()
