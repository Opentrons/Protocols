from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'NEBNext Direct Genotyping Solution Panels Part 3',
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
temp_module = modules.load('tempdeck', '4')
temp_plate = labware.load(
    'opentrons-aluminum-block-96-PCR-plate', '4', share=True)
reagent_plate = labware.load(pcr_plate_type, '5')
tiprack_300 = labware.load('opentrons-tiprack-300ul', '11')
tiprack_10 = labware.load('tiprack-10ul', '9')

# reagent Setup
hyb_wash = tuberack.wells('B1')
bead_wash_buffer_2 = tuberack.wells('D1')
blunt_mastermix = tuberack.wells('A2')
bead_wash_buffer_1 = tuberack.wells('B2')
adaptor_ligation_mastermix = tuberack.wells('C2')

spec_enhancer_enzy_mix = reagent_plate.cols('1')


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

    def transfer_bead_washing_buffer(volume, buffer, wellseries):
        for well in wellseries:
            p300.pick_up_tip()
            p300.transfer(volume, buffer, well, new_tip='never')
            p300.mix(10, volume-30, well)
            p300.blow_out(well)
            p300.drop_tip()

    temp_module.set_temperature(62)

    """1.8. Bead Binding
    """
    mag_dests = mag_plate.wells('A1', length=4)
    mag_module.engage(height=18)
    p300.delay(seconds=15)

    remove_supernatant(200, mag_dests)

    # wash beads with HW twice
    for _ in range(2):
        p300.pick_up_tip()
        p300.transfer(
            150, hyb_wash, [dest.top(-5) for dest in mag_dests],
            new_tip='never')
        for dest in mag_dests:
            if not p300.tip_attached:
                p300.pick_up_tip()
            p300.mix(10, 120, dest)
            p300.blow_out(dest)
            p300.drop_tip()
        temp_module.wait_for_temp()
        robot.pause("Transfer the plate from Magnetic Module to Temperature \
Module for 5 minutes. Then transfer the plate back to the Magnetic Module.")
        robot._driver.run_flag.wait()
        mag_module.engage(height=18)
        p300.delay(seconds=15)
        for dest in mag_dests:
            p300.transfer(200, dest, p300.trash_container.top())
        mag_module.disengage()

    temp_module.set_temperature(37)

    transfer_bead_washing_buffer(150, bead_wash_buffer_2, mag_dests)

    mag_module.engage(height=18)
    p300.delay(seconds=15)

    remove_supernatant(200, mag_dests)

    """1.9. 3' Blunting of DNA
    """
    # transfer Blunting Master Mix
    p300.pick_up_tip()
    p300.mix(5, 300, blunt_mastermix)
    p300.set_flow_rate(aspirate=100, dispense=100)
    p300.distribute(
        100, blunt_mastermix, [dest.top(-3) for dest in mag_dests],
        blow_out=blunt_mastermix, new_tip='never')
    p300.set_flow_rate(aspirate=150, dispense=300)
    for dest in mag_dests:
        if not p300.tip_attached:
            p300.pick_up_tip()
        p300.mix(10, 80, dest)
        p300.blow_out(dest)
        p300.drop_tip()

    temp_module.wait_for_temp()
    robot.pause("Transfer the plate from Magnetic Module to Temperature Module \
for incubation for 10 minutes at 37°C. Transfer the plate back on the \
Magnetic Module right after the incubation.")

    """1.9.6. Post-Reaction Wash
    """
    temp_module.set_temperature(20)
    robot._driver.run_flag.wait()
    mag_module.engage(height=18)
    p300.delay(seconds=15)

    remove_supernatant(150, mag_dests)

    transfer_bead_washing_buffer(150, bead_wash_buffer_1, mag_dests)

    mag_module.engage(height=18)
    p300.delay(seconds=15)

    remove_supernatant(200, mag_dests)

    transfer_bead_washing_buffer(150, bead_wash_buffer_2, mag_dests)

    p300.delay(minutes=5)

    """1.10. 3' Adaptor Ligation
    """

    robot._driver.run_flag.wait()
    mag_module.engage(height=18)
    p300.delay(seconds=15)

    remove_supernatant(200, mag_dests)

    # transfer 3' Adaptor Ligation Mix
    p300.pick_up_tip()
    p300.mix(5, 300, adaptor_ligation_mastermix)
    p300.set_flow_rate(aspirate=100, dispense=100)
    p300.distribute(
        100, adaptor_ligation_mastermix, [dest.top(-3) for dest in mag_dests],
        blow_out=blunt_mastermix, new_tip='never')
    p300.set_flow_rate(aspirate=150, dispense=300)
    for dest in mag_dests:
        if not p300.tip_attached:
            p300.pick_up_tip()
        p300.mix(10, 80, dest)
        p300.blow_out(dest)
        p300.drop_tip()

    temp_module.wait_for_temp()
    robot.pause("Place the plate on the Temperature Module. Resume when \
ready. Refer to Deck Config 2.")

    robot._driver.run_flag.wait()
    p300.delay(minutes=15)

    """1.11. Off-Target Removal
    """
    # transfer Specificity Enhancer Enzyme Mix
    m10.pick_up_tip()
    m10.transfer(
        5, spec_enhancer_enzy_mix, temp_plate.cols('1'), mix_after=(10, 10),
        new_tip='never')
    m10.blow_out(temp_plate.cols('1'))
    m10.drop_tip()

    temp_module.set_temperature(37)
    temp_module.wait_for_temp()
    p300.delay(minutes=15)

    """1.11.5. Post-reaction Wash
    """
    p300.home()
    robot.pause("Transfer the plate back on the Magnetic Module. Refer to \
Deck Config 1.")

    robot._driver.run_flag.wait()
    mag_module.engage(height=18)
    p300.delay(seconds=15)

    remove_supernatant(120, mag_dests)

    transfer_bead_washing_buffer(150, bead_wash_buffer_1, mag_dests)

    mag_module.engage(height=18)
    p300.delay(seconds=15)

    remove_supernatant(200, mag_dests)

    transfer_bead_washing_buffer(150, bead_wash_buffer_2, mag_dests)

    """1.12. Library Amplification
    """
    mag_module.engage(height=18)
    p300.delay(seconds=15)

    remove_supernatant(200, mag_dests)
