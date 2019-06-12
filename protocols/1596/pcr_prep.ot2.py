from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'PCR Preparation',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
pcr_plate_name = 'MicroAmp-96-PCR'
if pcr_plate_name not in labware.list():
    labware.create(
        pcr_plate_name,
        grid=(12, 8),
        spacing=(9.025, 9.025),
        diameter=5.5,
        depth=22.5,
        volume=200
    )

deepwell_plate_name = 'KingFisher-96-deepwell'
if deepwell_plate_name not in labware.list():
    labware.create(
        deepwell_plate_name,
        grid=(12, 9),
        spacing=(9, 9),
        diameter=8,
        depth=38,
        volume=1000
    )

tips_name = 'TipOne-tiprack-200ul'
if tips_name not in labware.list():
    labware.create(
        tips_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=3.5,
        depth=60
    )

# load labware and modules
tempdeck = modules.load('tempdeck', '1')
temp_plate = labware.load(pcr_plate_name, '1', share=True)
tempdeck.set_temperature(4)
tempdeck.wait_for_temp()
deep_plate = labware.load(deepwell_plate_name, '2')
block = labware.load(
    'opentrons-aluminum-block-2ml-eppendorf',
    '3',
    'block for reagents and master mix'
    )
tips_single = labware.load(tips_name, '4')
tips_multi = [labware.load(tips_name, slot) for slot in ['5', '6']]

# pipettes
p50 = instruments.P50_Single(mount='right', tip_racks=[tips_single])
m50 = instruments.P50_Multi(mount='left', tip_racks=tips_multi)

# reagent setup
primer1 = block.wells(0)
primer2 = block.wells(1)
dNTP = block.wells(2)
h2o = block.wells(3)
buffer_5x = block.wells(4)
dtt = block.wells(5)
rnase_out = block.wells(6)
superscript_iii = block.wells(7)
mm = block.wells(8)


def run_custom_protocol(
        number_of_sample_columns: int = 12
):

    # sample setup
    if number_of_sample_columns > 12:
        raise Exception('Please specify 12 or fewer sample columns.')

    sample_cols = temp_plate.columns()[0:number_of_sample_columns]
    samples = [well for col in sample_cols for well in col]
    num_samples = len(samples)

    # create and distribute mastermix
    p50.transfer(2.5 * num_samples, primer1, mm, blow_out=True)
    p50.transfer(
        2.5 * num_samples,
        dNTP,
        mm,
        mix_after=(10, 50),
        blow_out=True
        )
    p50.pick_up_tip()
    for well in temp_plate.columns('1'):
        p50.transfer(
            5 * number_of_sample_columns,
            mm,
            well,
            blow_out=True,
            new_tip='never'
            )
    p50.drop_tip()
    if number_of_sample_columns > 1:
        m50.pick_up_tip()
        for col in temp_plate.columns('2', length=number_of_sample_columns-1):
            m50.transfer(
                5,
                temp_plate.columns('1'),
                temp_plate.columns('2', length=number_of_sample_columns-1),
                blow_out=True,
                new_tip='never'
                )
        m50.drop_tip()

    robot.pause('Please place 96-deepwell plate in slot 2 before resuming.')

    # transfer corresponding RNA
    for source, dest in zip(deep_plate.columns()[0:number_of_sample_columns],
                            temp_plate.columns()[0:number_of_sample_columns]):
        m50.pick_up_tip()
        m50.transfer(
            25,
            source,
            dest,
            new_tip='never'
        )
        m50.mix(10, 25, dest)
        m50.blow_out(dest)
        m50.drop_tip()

    robot.pause('Please replace mastermix tube in block well A3 with a '
                'fresh tube before resuming.')

    # create new mastermix
    p50.transfer(10 * num_samples, buffer_5x, mm, blow_out=True)
    p50.transfer(8 * num_samples, h2o, mm, blow_out=True)
    p50.transfer(0.5 * num_samples, dtt, mm, blow_out=True)
    p50.transfer(0.5 * num_samples, rnase_out, mm, blow_out=True)
    p50.pick_up_tip()
    p50.transfer(
        1 * num_samples,
        superscript_iii,
        mm,
        new_tip='never',
        blow_out=True
        )
    p50.mix(20, 50, mm)
    p50.blow_out(mm)
    p50.drop_tip()

    robot.pause('Please place the reaction plate back on the tempdeck.')

    p50.pick_up_tip()
    for s in samples:
        p50.transfer(20, mm, s.top(), blow_out=True, new_tip='never')
    p50.drop_tip()
