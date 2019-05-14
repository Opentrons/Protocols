from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'Nucleic Acid Purification',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
res_name = '4titue-reservoir'
if res_name not in labware.list():
    labware.create(res_name,
                   grid=(1, 1),
                   spacing=(0, 0),
                   depth=39.22,
                   diameter=65,
                   volume=290000)

# labware
deep_plate = labware.load('96-deep-well', '2')
new_plate = labware.load('biorad-hardshell-96-PCR', '3')
trough1 = labware.load('trough-12row', '4')
trough2 = labware.load('trough-12row', '5')
waste = labware.load(res_name, '6')
sample_tip_rack = labware.load('tiprack-200ul', '7')
VHB_tip_rack = labware.load('tiprack-200ul', '8')
SPM_tip_rack = labware.load('tiprack-200ul', '9')
elution_buffer_tip_rack = labware.load('tiprack-200ul', '10')
water_tip_rack = labware.load('tiprack-200ul', '11')

# module
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load('biorad-hardshell-96-PCR', '1', share=True)

# pipette
m300 = instruments.P300_Multi(mount='right')

# reagent setup
VHB = trough1.wells('A1', length=6)
SPM = trough1.wells('A7', length=6)
water = trough2.wells('A1')
elution_buffer = trough2.wells('A2')

# tip setup
sample_tips = [well for well in sample_tip_rack.rows('A')]
VHB_tips = [well for well in VHB_tip_rack.rows('A')]
SPM_tips = [well for well in SPM_tip_rack.rows('A')]
elution_buffer_tips = [well for well in elution_buffer_tip_rack.rows('A')]
water_tips = [well for well in water_tip_rack.rows('A')]


def buffer_transfer(buffer, tips, repeats, samples, num_mixes, disengage):
    for ind in range(repeats):
        for s_tip, b_tip, s in zip(sample_tips, tips, samples):
            m300.pick_up_tip(b_tip)
            m300.transfer(180, buffer[ind], s.top(), new_tip='never')
            m300.return_tip()

            m300.pick_up_tip(s_tip)
            m300.mix(num_mixes, 300, s)
            m300.return_tip()

        # incubate on engaged magnet for selected number of minutes
        magdeck.engage()
        m300.delay(minutes=5)

        for tip, s in zip(sample_tips, samples):
            m300.pick_up_tip(tip)
            m300.transfer(200, s, waste, new_tip='never')
            m300.return_tip()
        if disengage is True:
            robot._driver.run_flag.wait()
            magdeck.disengage()


def run_custom_protocol(number_of_sample_columns: int = 12,
                        minutes_to_incubate_on_magnetic_block: int = 5,
                        number_of_initial_mixes: int = 5,
                        number_of_secondary_mixes: int = 25,
                        elution_volume_ul: float = 100,
                        number_of_first_supernatant_transfers: int = 6,
                        number_of_second_supernatant_transfers: int = 2):
    # setup samples
    deep_samples = deep_plate.rows('A')[0:number_of_sample_columns]
    mag_samples = mag_plate.rows('A')[0:number_of_sample_columns]
    new_samples = new_plate.rows('A')[0:number_of_sample_columns]

    for _ in range(5):
        # mix and transfer samples to magnetic plate
        for tip, source, dest in zip(sample_tips, deep_samples, mag_samples):
            m300.pick_up_tip(tip)
            m300.mix(number_of_initial_mixes, 150, source)
            m300.transfer(180, source, dest.top(), new_tip='never')
            m300.return_tip()

        # incubate on engaged magnet for selected number of minutes
        magdeck.engage()
        m300.delay(minutes=minutes_to_incubate_on_magnetic_block)

        # remove supernatant
        for tip, s in zip(sample_tips, mag_samples):
            m300.pick_up_tip(tip)
            m300.transfer(200, s, waste, new_tip='never')
            m300.return_tip()
        magdeck.disengage()

    # buffer transfers
    buffer_transfer(VHB,
                    VHB_tips,
                    number_of_first_supernatant_transfers,
                    mag_samples,
                    number_of_secondary_mixes,
                    True)
    buffer_transfer(SPM,
                    SPM_tips,
                    number_of_second_supernatant_transfers,
                    mag_samples,
                    number_of_secondary_mixes,
                    True)
    buffer_transfer(SPM,
                    SPM_tips,
                    1,
                    mag_samples,
                    number_of_secondary_mixes,
                    False)

    for s_tip, w_tip, s in zip(sample_tips, water_tips, mag_samples):
        m300.pick_up_tip(w_tip)
        m300.transfer(180, water, s.top(), new_tip='never')
        m300.drop_tip()

        m300.pick_up_tip(s_tip)
        m300.transfer(200, s, waste, new_tip='never')
        m300.return_tip()
    magdeck.disengage()

    for tip, s in zip(elution_buffer_tips, mag_samples):
        m300.pick_up_tip(tip)
        m300.transfer(elution_volume_ul,
                      elution_buffer,
                      s.top(),
                      new_tip='never')
        m300.mix(number_of_secondary_mixes, 300, s)
        m300.return_tip()

    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage()
    m300.delay(minutes=5)
    for tip, source, dest in zip(elution_buffer_tips,
                                 mag_samples,
                                 new_samples):
        m300.pick_up_tip(tip)
        m300.transfer(elution_volume_ul, source, dest, new_tip='never')
        m300.drop_tip()
