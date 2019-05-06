from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'NEBNext Direct Genotyping Solution Panels Part 4',
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

# labware Setup
mag_module = modules.load('magdeck', '1')
mag_plate = labware.load(pcr_plate_type, '1', share=True)
tuberack = labware.load('opentrons-tuberack-2ml-screwcap', '2')
pcr_strips = labware.load('PCR-strip-tall', '3')
temp_module = modules.load('tempdeck', '4')
temp_plate = labware.load(
    'opentrons-aluminum-block-96-PCR-plate', '4', share=True)
trough = labware.load('trough-12row', '5')
tiprack_300 = labware.load('opentrons-tiprack-300ul', '11')
tiprack_10 = labware.load('tiprack-10ul', '9')

# reagent Setup
post_pcr_beads = tuberack.wells('A1')
resuspension_buffer = tuberack.wells('B1')
ethanol = trough.wells('A1')


# instruments setup
m10 = instruments.P10_Multi(
    mount='left',
    tip_racks=[tiprack_10])
p300 = instruments.P300_Single(
    mount='right',
    tip_racks=[tiprack_300])


def run_custom_protocol(engage_height: float=18):

    def remove_supernatant(volume, wellseries):
        for well in wellseries:
            p300.transfer(volume, well, p300.trash_container.top())

    mag_dests = mag_plate.wells('A1', length=4)

    temp_module.set_temperature(37)

    # add Post-PCR Sample Purification Beads
    for dest in mag_dests:
        p300.pick_up_tip()
        p300.transfer(85, post_pcr_beads, dest, new_tip='never')
        p300.mix(10, 60, dest)
        p300.blow_out(dest)
        p300.drop_tip()

    p300.delay(minutes=5)
    robot._driver.run_flag.wait()
    mag_module.engage(height=engage_height)
    p300.delay(minutes=2)

    remove_supernatant(200, mag_dests)

    # wash beads twice with 80% ethanol
    for _ in range(2):
        p300.pick_up_tip()
        p300.transfer(
            200, ethanol, [dest.top() for well in mag_dests], air_gap=True,
            new_tip='never')
        p300.delay(seconds=30)
        for dest in mag_dests:
            if not p300.tip_attached:
                p300.pick_up_tip()
            p300.transfer(
                220, dest, p300.trash_container.top(), air_gap=True,
                new_tip='never')
            p300.drop_tip()

    temp_module.wait_for_temp()

    robot.pause("Transfer the plate from the Magnetic Module to the \
Temperature Module for 5 minutes to dry the beads. Replace the plate back on \
the Magnetic Module before resuming.")

    # resuspend beads in either nuclease-free water or 1X TE
    p300.set_flow_rate(aspirate=30, dispense=30)
    for dest in mag_dests:
        p300.pick_up_tip()
        p300.transfer(30, resuspension_buffer, dest, new_tip='never')
        p300.mix(3, 30, dest)
        p300.drop_tip()

    # transfer the eluted library to a fresh tube
    m10.transfer(28, mag_plate.cols('1'), pcr_strips.cols('1'))
