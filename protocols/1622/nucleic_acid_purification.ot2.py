from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'Nucleic Acid Purfication',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
deepwell_name = 'Abgene-deepwell-96'
if deepwell_name not in labware.list():
    labware.create(
        deepwell_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8.4,
        depth=39.36,
        volume=2200
    )

elution_name = 'Eppendorf-96-flat'
if elution_name not in labware.list():
    labware.create(
        elution_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=11.3,
        volume=200
    )

# load modules and labware
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load(deepwell_name, '1', share=True)
trough1 = labware.load('trough-12row', '2', 'reagent trough 1')
trough2 = labware.load('trough-12row', '3', 'reagent trough 2')
tempdeck = modules.load('tempdeck', '4')
tempdeck.set_temperature(65)
tempdeck.wait_for_temp()
elution_plate = labware.load(elution_name, '10', 'elution plate')
tips300 = [labware.load('opentrons-tiprack-300ul', slot)
           for slot in ['7', '8', '9', '11']]
tips50 = [labware.load('opentrons-tiprack-300ul', slot) for slot in ['5', '6']]

# reagents
beads = [chan for chan in trough1.wells('A1', length=3)]
magwash1 = [chan for chan in trough1.wells('A4', length=6)]
dnase_free_water = trough1.wells('A10')
magwash2 = [chan for chan in trough2.wells('A1', length=12)]

# pipettes
m300 = instruments.P300_Multi(mount='right', tip_racks=tips300)
m50 = instruments.P50_Multi(mount='left', tip_racks=tips50)


def run_custom_protocol(
        number_of_sample_columns: int = 12
):

    if number_of_sample_columns < 1 or number_of_sample_columns > 12:
        raise Exception('Invalid number of sample columns.')
    mag_samples = mag_plate.rows('A')[:number_of_sample_columns]

    # function to remove supernatant from magnetic samples
    def remove_supernatant(vol):
        magdeck.engage(height=16)
        m300.delay(minutes=5)

        m300.transfer(
            900,
            [s.bottom() for s in mag_samples],
            m300.trash_container.top(),
            new_tip='always'
        )
        magdeck.disengage()

    # distribute mag binding buffer
    m300.pick_up_tip()
    for i, s in enumerate(mag_samples):
        bead_ind = i//4
        m300.transfer(
            600,
            beads[bead_ind],
            s.top(),
            blow_out=True,
            new_tip='never'
        )
    m300.drop_tip()

    # remove supernatant
    remove_supernatant(600)

    robot.pause('Refill tip racks in slots 7, 8, 9, and 11 before resuming.')
    m300.reset()

    # transfer magnetic wash 1
    for i, s in enumerate(mag_samples):
        wash_ind = i//6
        m300.pick_up_tip()
        m300.transfer(
            900,
            magwash1[wash_ind],
            s,
            new_tip='never'
        )
        m300.mix(10, 200, s)
        m300.blow_out(s.top())
        m300.drop_tip()

    # remove supernatant
    remove_supernatant(900)

    # 2 washes with magnetic wash 2
    for wash in range(2):
        # transfer magnetic wash 2
        if wash == 0:
            robot.pause('Refill tip racks in slots 7, 8, 9, and 11 before \
resuming.')
            m300.reset()
        for i, s in enumerate(mag_samples):
            wash_ind = i//2 + wash*6
            m300.pick_up_tip()
            m300.transfer(
                900,
                magwash2[wash_ind],
                s,
                new_tip='never'
            )
            m300.mix(10, 200, s)
            m300.blow_out(s.top())
            m300.drop_tip()

        # remove supernatant
        remove_supernatant(900)

        if wash == 0:
            robot.pause('Refill tip racks in slots 7, 8, 9, and 11 before \
resuming.')
            m300.reset()

    robot.pause('Transfer deepwell plate to tempdeck set at 65˚C. Once dry, \
place back on the magdeck.')

    # transfer DNase/RNase-free water to each sample
    for s in mag_samples:
        m50.pick_up_tip()
        m50.transfer(
            50,
            dnase_free_water,
            s,
            new_tip='never'
        )
        m50.mix(10, 40, s)
        m50.blow_out(s)
        m50.drop_tip()

    magdeck.engage(height=16)
    m50.delay(minutes=5)

    # transfer to final elution plate
    final_dests = elution_plate.rows('A')[0:number_of_sample_columns]
    for source, dest in zip(mag_samples, final_dests):
        m50.pick_up_tip()
        m50.transfer(
            50,
            source.bottom(),
            dest,
            new_tip='never'
            )
        m50.blow_out(dest)
        m50.drop_tip()

    magdeck.disengage()
