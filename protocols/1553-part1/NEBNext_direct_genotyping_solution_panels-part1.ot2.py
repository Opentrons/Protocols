from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'NEBNext Direct Genotyping Solution Panels Part 1',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

pcr_plate_type = 'framestar-96-PCR-skirted'
if pcr_plate_type not in labware.list():
    labware.create(
        pcr_plate_type,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.5,
        depth=15.1)

deep_well_block_type = 'greiner-bioone-96-well-masterblock-1ml'
if deep_well_block_type not in labware.list():
    labware.create(
        deep_well_block_type,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=38.2)

half_block_type = 'greiner-bioone-96-well-masterblock-0.5ml'
if half_block_type not in labware.list():
    labware.create(
        half_block_type,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=23.3)


# labware setup
mag_module = modules.load('magdeck', '1')
mag_block = labware.load(deep_well_block_type, '1', share=True)
trough = labware.load('trough-12row', '2')
temp_module = modules.load('tempdeck', '4')
temp_plate = labware.load(
    'opentrons-aluminum-block-96-PCR-plate', '4', share=True)
reagent_plate = labware.load(half_block_type, '5')
adaptor_plate = labware.load(pcr_plate_type, '7')
tipracks_10 = [labware.load('tiprack-10ul', slot)
               for slot in ['3', '6', '8', '9']]
tipracks_300 = [labware.load('opentrons-tiprack-300ul', slot)
                for slot in ['10', '11']]

# instruments setup
m10 = instruments.P10_Multi(
    mount='left',
    tip_racks=tipracks_10)
p300 = instruments.P300_Single(
    mount='right',
    tip_racks=tipracks_300)

# reagent setup
fragm_mastermix = reagent_plate.cols('1')
ligation_mastermix = reagent_plate.cols('2')
stop_solution = reagent_plate.cols('3')
hybrid_mastermix = reagent_plate.wells('A4')

beads = trough.wells('A1')
ethanol = trough.wells('A2')
nuclease_free_water = trough.wells('A3')
pre_hyb_beads = trough.wells('A4')


def run_custom_protocol(engage_height: float=14.94):

    def remove_supernatant(volume, wellseries):
        for well in wellseries:
            p300.transfer(volume, well, p300.trash_container.top())

    """1.2. Fragmentation and End Prep
    """
    temp_plate_dest = temp_plate.cols()
    temp_module.set_temperature(4)
    temp_module.wait_for_temp()

    # transfer fragmentation master mix
    for col in temp_plate_dest:
        m10.pick_up_tip()
        m10.transfer(3, fragm_mastermix, col, new_tip='never')
        m10.mix(10, 5, col)
        m10.blow_out(col)
        m10.drop_tip()

    robot.pause("Run the plate in a thermocycler. Spin down the plate and \
place the plate back to slot 4 before resuming the protocol.")

    """1.3. 5' Ligation with Sample Indexing
    """
    # transfer indexed 5' adaptor
    adaptors = adaptor_plate.cols()
    for source, dest in zip(adaptors, temp_plate_dest):
        m10.transfer(5, source, dest)

    # transfer ligatoin master mix
    for col in temp_plate_dest:
        m10.pick_up_tip()
        m10.transfer(
            10, ligation_mastermix, col, mix_after=(10, 10), new_tip='never')
        m10.blow_out(col)
        m10.drop_tip()

    robot.pause("Incubate the plate in the thermocycler for 15 minutes at \
20°C. Remove the Adpator Plate from slot 7 and replace with a new clean PCR \
plate or PCR strip tubes for PCR. Put the plate from the thermocycler back \
on the temperature module before resuming. Refer to Config 2 to make sure \
the deck setup is correct.")

    # transfer stop solution
    for col in temp_plate_dest:
        m10.pick_up_tip()
        m10.transfer(
            2.5, stop_solution, col, mix_after=(10, 10), new_tip='never')
        m10.blow_out(col)
        m10.drop_tip()

    """1.4. Sample Pooling and Bead Cleanup
    """
    pool_sources = [temp_plate.cols(index*3, length=3) for index in range(4)]
    pools = mag_block.wells('A1', length=4)

    # pool samples
    for sources, tube in zip(pool_sources, pools):
        for col in sources:
            p300.transfer(24, col, tube, new_tip='always')

    # add beads
    for pool in pools:
        p300.pick_up_tip()
        p300.transfer(
            461, beads, pool.top(), mix_before=(3, 10), new_tip='never')
        p300.mix(10, 50, pool)
        p300.blow_out(pool)
        p300.drop_tip()

    p300.delay(minutes=5)
    robot._driver.run_flag.wait()
    mag_module.engage(height=engage_height)
    p300.delay(minutes=5)

    remove_supernatant(1200, pools)

    # wash pools twice with 80% ethanol
    for _ in range(2):
        p300.pick_up_tip()
        p300.transfer(
            270, ethanol, [pool.top() for pool in pools], air_gap=30,
            new_tip='never')
        for pool in pools:
            if not p300.tip_attached:
                p300.pick_up_tip()
            p300.transfer(
                300, pool, p300.trash_container.top(), new_tip='never')
            p300.drop_tip()

    # air dry beads for 5 minutes
    robot.comment("Air dry beads for 5 minutes. Protocol will resume \
    automatically.")
    p300.delay(minutes=5)

    robot._driver.run_flag.wait()
    mag_module.disengage()

    # resuspend beads with sterile water
    for pool in pools:
        p300.pick_up_tip()
        p300.transfer(
            202, nuclease_free_water, pool, mix_after=(3, 150),
            new_tip='never')
        p300.blow_out(pool)
        p300.drop_tip()

    p300.delay(minutes=2)
    robot._driver.run_flag.wait()
    mag_module.engage(height=engage_height)
    p300.delay(minutes=2)

    # transfer to new tube
    dests = mag_block.wells('A2', length=4)
    for source, dest in zip(pools, dests):
        p300.transfer(200, source, dest)

    mag_module.disengage()

    """1.5. Pre-hybridization Bead Cleanup
    """
    # transfer Pre-Hyb Sample Purification Beads
    pools = mag_block.wells('A2', length=4)
    for pool in pools:
        p300.pick_up_tip()
        p300.mix(3, 300, pre_hyb_beads)
        p300.transfer(360, pre_hyb_beads, pool, new_tip='never')
        p300.mix(10, 300, pool)
        p300.blow_out(pool)
        p300.drop_tip()

    p300.delay(minutes=5)
    robot._driver.run_flag.wait()
    mag_module.engage(height=engage_height)
    p300.delay(minutes=5)

    # remove supernatant
    for pool in pools:
        p300.transfer(400, pool, p300.trash_container.top())

    # wash pools twice with 80% ethanol
    for _ in range(2):
        p300.pick_up_tip()
        p300.transfer(
            270, ethanol, [pool.top() for pool in pools], air_gap=30,
            new_tip='never')
        for pool in pools:
            if not p300.tip_attached:
                p300.pick_up_tip()
            p300.transfer(
                300, pool, p300.trash_container.top(), new_tip='never')
            p300.drop_tip()

    # air dry beads for 5 minutes
    robot.comment("Air dry beads for 5 minutes. Protocol will resume \
automatically.")
    p300.delay(minutes=5)

    robot._driver.run_flag.wait()
    mag_module.disengage()

    # resuspend beads with sterile water
    for pool in pools:
        p300.pick_up_tip()
        p300.transfer(
            62, nuclease_free_water, pool, mix_after=(3, 40), new_tip='never')
        p300.blow_out(pool)
        p300.drop_tip()

    p300.delay(minutes=2)
    robot._driver.run_flag.wait()
    mag_module.engage(height=engage_height)
    p300.delay(minutes=2)

    # transfer to new tube
    dests = adaptor_plate.wells('A1', length=4)
    for source, dest in zip(pools, dests):
        p300.transfer(60, source, dest)

    mag_module.disengage()

    """1.6. Bait Hybridization
    """
    # transfer hybridization master mix
    pools = adaptor_plate.wells('A1', length=4)
    for pool in pools:
        p300.pick_up_tip()
        p300.set_flow_rate(aspirate=60, dispense=60)
        p300.transfer(60, hybrid_mastermix, pool, new_tip='never')
        p300.set_flow_rate(aspirate=150, dispense=300)
        p300.mix(10, 100, pool)
        p300.blow_out(pool)
        p300.drop_tip()

    robot.comment("This is the end of this part of the protocol. Seal the \
plate in slot 7 before placing in a thermocycler for Biat Hybridization.")
