from opentrons import labware, instruments, modules

reservoir_name = 'trough-2row'
if reservoir_name not in labware.list():
    labware.create(
        reservoir_name,
        grid=(2, 1),
        spacing=(54, 0),
        diameter=53,
        depth=39.2,
        volume=14400)

# labware setup
deep_well = labware.load('96-deep-well', '1')
reagent = labware.load(reservoir_name, '2')
temp_module = modules.load('tempdeck', '6')
temp_pcr = labware.load(
    'opentrons-aluminum-block-PCR-strips-200ul', '6', share=True)
microplate_1 = labware.load('96-flat', '4')
microplate_2 = labware.load('96-flat', '5')
tiprack_50 = [labware.load('opentrons-tiprack-300ul', slot)
              for slot in ['7', '8']]
tiprack_300 = labware.load('opentrons-tiprack-300ul', '9')


# reagent setup
reagent_1 = reagent.wells('A1')
reagent_2 = reagent.wells('A2')

# instrument setup
m50 = instruments.P50_Multi(
    mount='left',
    tip_racks=tiprack_50)

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack_300])

# set temperature to 4°C
temp_module.set_temperature(4)

# dispense reagent 1 across plate 1
m300.distribute(50, reagent_1, microplate_1.cols())

# dispense reagent 2 across plate 2
m300.distribute(45, reagent_2, microplate_2.cols())

# transfer deep plate to plate 1
m50.transfer(
    25,
    deep_well.cols(),
    microplate_1.cols(),
    mix_after=(5, 50), new_tip='always')

# make sure the temperature is at 4°C before transferring to PCR strips
temp_module.wait_for_temp()

# transfer plate 1 to plate 2, then to PCR strips on temperature module
for plate_1_loc, plate_2_loc, pcr_loc in zip(
        microplate_1.cols(), microplate_2.cols(), temp_pcr.cols()):
    m50.pick_up_tip()
    m50.transfer(5, plate_1_loc, plate_2_loc,
                 mix_after=(5, 30), new_tip='never')
    m50.transfer(30, plate_2_loc, pcr_loc, new_tip='never')
    m50.drop_tip()
