from opentrons import labware, instruments, modules

temp_module = modules.load('tempdeck', '4')
plate = labware.load('96-flat', '4', share=True)

dilution_plate = labware.load('96-flat', '2')
microplate = labware.load('96-flat', '3')

tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '1')
pcr_strips = labware.load('PCR-strip-tall', '5')
trough = labware.load('trough-12row', '6')

# reagent setup
dilution_buffer = trough.wells('A1')
TE_buffer = trough.wells('A2')
dnase_1 = tuberack.wells('A1')
proK_mix = tuberack.wells('B1')
master_mix = tuberack.wells('C1')
standards_ctrl = pcr_strips.cols('1')


tiprack10 = labware.load('tiprack-10ul', '7')
tiprack300 = labware.load('tiprack-200ul', '8')

# pipette setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack10])

p300 = instruments.P300_Single(
    mount='right',
    tip_racks=[tiprack300])


def run_custom_protocol(
        sample_num: int=16):

    samples = tuberack.wells('A2', length=sample_num)

    # dilute samples in PCR Dilution Buffer
    dilution_loc = dilution_plate.wells('A1', length=sample_num)
    p300.transfer(198, dilution_buffer, dilution_loc)
    p10.transfer(2, samples, dilution_loc, new_tip='always')

    # add DNAse I solution and diluted samples to plate
    plate_loc = plate.wells('A1', length=sample_num)
    p300.distribute(40, dnase_1, plate_loc, disposal_vol=0)
    p10.transfer(10, samples, plate_loc, new_tip='always')

    temp_module.set_temperate(37)
    temp_module.wait_for_temp()
    p10.delay(minutes=60)
    temp_module.deactivate()

    # add and mix in proteinase K
    for loc in plate_loc:
        p300.transfer(50, proK_mix, loc, mix_after=(3, 50))

    temp_module.set_temperate(37)
    temp_module.wait_for_temp()
    p10.delay(minutes=60)
    temp_module.set_temperate(95)
    temp_module.wait_for_temp()
    p10.delay(minutes=10)
    temp_module.set_temperate(4)
    temp_module.wait_for_temp()

    dilution_loc = microplate.wells('A4', length=sample_num)
    p300.transfer(245, TE_buffer, dilution_loc, new_tip='never')
    p10.transfer(5, plate_loc, dilution_loc, new_tip='always')

    total_locs = 24 + sample_num * 3
    p10.transfer(7.5, master_mix, microplate.wells('A1', total_locs))

    standards_ctrl_loc = [row.wells('1', to='3') for row in microplate.rows()]
    for source, dest in zip(standards_ctrl, standards_ctrl_loc):
        p10.distribute(2.5, source, dest, disposal_vol=1)

    sample_loc = []
    for index in range(4, 12, 3):
        for row in microplate.rows():
            sample_loc.append(row.wells(str(index), length=3))
    sample_loc = sample_loc[:sample_num]

    for sample, dest in zip(samples, sample_loc):
        p10.distribute(2.5, sample, dest, disposal_vol=1)
