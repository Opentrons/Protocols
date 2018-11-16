from opentrons import labware, instruments, modules, robot

trough_name = 'trough-2row'
if trough_name not in labware.list():
    labware.create(
        trough_name,
        grid=(2, 1),
        spacing=(54, 0),
        diameter=53,
        depth=42)

# labware setup
elisa_plate = labware.load('96-flat', '2', 'ELISA plate')
dilution_plate = labware.load('96-deep-well', '3', 'Dilution Plate')
temp_deck = modules.load('tempdeck', '4')
sample_plate = labware.load('96-flat', '4', 'Sample Plate', share=True)

trough = labware.load('trough-12row', '5')
trough_2 = labware.load(trough_name, '7')

tiprack50 = labware.load('opentrons-tiprack-300ul', '1')
tiprack300s = [labware.load('opentrons-tiprack-300ul', slot)
               for slot in ['6', '8', '9', '10', '11']]

for well in trough_2.wells():
    well.properties['width'] = 53
    well.properties['length'] = 71

# reagent setup
cAMP_standard = trough.wells('A1')
lysis_buffer = trough.wells('A2')
diluted_cAMP = trough.wells('A3')
antibody = trough.wells('A4')
substrate_solution = trough.wells('A5')
wash_buffer = trough_2.wells('A1')
liquid_trash = trough_2.wells('A2')

# pipette setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack50])
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tiprack300s)

multi_tip_count = 0


def update_multi_tip_count(num):
    global multi_tip_count
    multi_tip_count += num
    if multi_tip_count == 12 * len(tiprack300s):
        robot.pause("Your P300 tips have run out. Resume the protocol when the \
        tips are replenished. Slot 6, 8, 9, 10, and 11.")
        m300.reset_tip_tracking()
        m300.start_at_tip(tiprack300s[0].cols(0))
        multi_tip_count = 0


def run_custom_protocol(
        sample_start_col: str='1',
        number_of_sample_cols: int=2,
        standards_start_col: str='1'):

    # define sample plate locations
    samples = [col for col in sample_plate.cols(
        sample_start_col, length=number_of_sample_cols)]

    standard_dest = [
        col for col in elisa_plate.cols(standards_start_col, length=2)]

    dest_col_str = str(int(standards_start_col)+2)
    sample_dest = [
        col for col in elisa_plate.cols(
            dest_col_str, length=number_of_sample_cols)]

    # incubate sample plate at 37°C for 30 minutes
    temp_deck.set_temperature(37)
    temp_deck.wait_for_temp()
    m300.delay(minutes=30)

    # slow pipette flow rate down by half for viscous lysis buffer
    m300.set_flow_rate(aspirate=75, dispense=150)
    p50.set_flow_rate(aspirate=20, dispense=25)

    # inactivate the reaction
    for sample in samples:
        m300.pick_up_tip()
        m300.transfer(52, lysis_buffer, sample,
                      mix_after=(2, 40), new_tip='never')
        m300.blow_out(sample)
        m300.drop_tip()
        update_multi_tip_count(1)

    # incubate plate at 37°C for 10 minutes
    m300.delay(minutes=10)

    # create serial dilutions
    m300.transfer(270, lysis_buffer, dilution_plate.cols('1'))
    update_multi_tip_count(1)
    p50.transfer(30, lysis_buffer, dilution_plate.wells('H1'))
    p50.transfer(30, cAMP_standard, dilution_plate.wells('A1'),
                 mix_after=(10, 50))
    p50.transfer(
        30,
        dilution_plate.wells('A1', length=6),
        dilution_plate.wells('B1', length=6),
        mix_after=(10, 50))

    # set pipette flow rate back to default
    m300.set_flow_rate(aspirate=150, dispense=300)
    p50.set_flow_rate(aspirate=25, dispense=50)

    # transfer standards to ELISA plate
    m300.pick_up_tip()
    for col in standard_dest:
        m300.transfer(
            60, dilution_plate.cols('1'), col[0].top(), new_tip='never')
    m300.drop_tip()
    update_multi_tip_count(1)

    # transfer samples to ELISA plate
    for source, dest in zip(samples, sample_dest):
        m300.transfer(60, source, dest)
        update_multi_tip_count(1)

    plate_loc = standard_dest + sample_dest

    # transfer dilution cAMP-AP to plate
    for col in plate_loc:
        m300.transfer(30, diluted_cAMP, col, mix_after=(2, 30))
        update_multi_tip_count(1)

    # transfer antibody to plate and mix
    for col in plate_loc:
        m300.transfer(60, antibody, col, mix_after=(2, 30))
        update_multi_tip_count(1)

    m300.delay(minutes=60)

    # remove solution from wells
    for col in plate_loc:
        m300.transfer(150, col, liquid_trash)
        update_multi_tip_count(1)

    # wash 6x with wash buffer
    m300.pick_up_tip()
    start_tip = m300.current_tip()
    for cycle in range(6):
        if not m300.tip_attached:
            m300.start_at_tip(start_tip)
            m300.pick_up_tip()
        m300.distribute(
            200, wash_buffer, [col[0] for col in plate_loc], trash=False)
        m300.transfer(200, plate_loc, liquid_trash, trash=False)
    update_multi_tip_count(2)

    # add substrate/enhancer solution to plate
    m300.pick_up_tip()
    for col in plate_loc:
        m300.transfer(100, substrate_solution, col[0].top(), new_tip='never')
    m300.drop_tip()
    update_multi_tip_count(1)
