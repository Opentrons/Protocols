from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
from opentrons.legacy_api.modules import tempdeck

metadata = {
    'protocolName': 'Enzymatic Assay',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

"""Controlling two of the same module in the protocol:
1. SSH into robot
2. run $ls /dev/tty*
   you are looking for two values with the format /dev/ttyACM*
   you will use those values in line 27 and 28.
If you need to know which magdeck is hooked up to which port:
1. unplug one of the modules
2. run $ls /dev/tty* : the results correlates to the module that is plugged in
3. plug the other module in and run ls /dev/tty* again, you will be able to
   know the value of the second module
"""

# defining two Temperature Modules
tempdeck1 = tempdeck.TempDeck()
tempdeck2 = tempdeck.TempDeck()

tempdeck1._port = '/dev/ttyACM1'
tempdeck2._port = '/dev/ttyACM2'

if not robot.is_simulating():
    tempdeck1.connect()
    tempdeck2.connect()

tempdeck1.set_temperature(37)
tempdeck2.set_temperature(4)
tempdeck2.wait_for_temp()
tempdeck1.wait_for_temp()

# create custom labware
pcr_name = 'eppendorf_96_wellplate_pcr_150ul'
if pcr_name not in labware.list():
    labware.create(
        pcr_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=4,
        depth=14,
        volume=150
    )

deep_name = 'beckmancoulter_96_wellplate_deep_2ml'
if deep_name not in labware.list():
    labware.create(
        deep_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=39,
        volume=2000
    )

# load modules and labware
[modules.load('tempdeck', slot) for slot in ['1', '4']]
deep_plate = labware.load(deep_name, '1', 'deepwell plate', share=True)
pcr_plate = labware.load(pcr_name, '4', 'PCR plate', share=True)
res12 = labware.load(
    'usascientific_12_reservoir_22ml', '2', 'reagent reservoir')
tuberack = labware.load(
    'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
    '5',
    'enzyme rack'
)
tips300 = labware.load('opentrons_96_tiprack_300ul', '3', 'P300 tiprack')
tips50 = [
    labware.load('opentrons_96_tiprack_300ul', str(slot), 'P50 tiprack')
    for slot in range(6, 12)
]

# reagents
buffer = res12.wells(0)
quenching_sol = res12.wells(1)

substrates = tuberack.wells()[:16]
enzyme = tuberack.wells()[16]


def run_custom_protocol(
    P300_single_mount: StringSelection('right', 'left') = 'right',
    P50_multi_mount: StringSelection('left', 'right') = 'left'
):
    # check
    if P300_single_mount == P50_multi_mount:
        raise Exception('Pipette mounts cannot be the same.')

    # pipettes
    p300 = instruments.P300_Single(
        mount=P300_single_mount, tip_racks=[tips300])
    m50 = instruments.P50_Multi(mount=P50_multi_mount, tip_racks=tips50)

    # transfer buffer to deepwell plate
    p300.transfer(320, buffer, [s.top() for s in deep_plate.wells()[:16]])

    # transfer quenching solution to each well of PCR plate
    m50.distribute(
        20, quenching_sol, pcr_plate.rows('A'), blow_out=True, disposal_vol=0)

    # transfer substrate to corresponding deepwell plate sample
    for s, d in zip(substrates, deep_plate.wells()[:16]):
        p300.pick_up_tip()
        p300.transfer(40, s, d, new_tip='never')
        p300.blow_out()
        p300.drop_tip()

    delay_time_set = [14, 14, 29, 59, 119]
    for set in range(6):
        for t in range(2):
            index = 2*set+t

            # transfer enzyme to first column of deepwell plate
            if set == 0:
                p300.distribute(
                    40, enzyme, [s.top() for s in deep_plate.columns()[t]])

            # mix and transfer to PCR plate
            m50.pick_up_tip()
            if set == 0:
                m50.mix(10, 40, deep_plate.rows('A')[t])
                m50.blow_out(deep_plate.rows('A')[t].top())
                robot.comment('Note time-'+str(t+1))

            m50.transfer(
                50,
                deep_plate.rows('A')[t],
                pcr_plate.rows('A')[index],
                new_tip='never'
            )
            m50.mix(3, 40, pcr_plate.rows('A')[index])
            robot.comment('Note time-'+str(t+1)+'-'+str(set))
            m50.drop_tip()

        # delay
        if set < 5:
            delay_t = delay_time_set[set]
            robot.comment('Delaying ' + str(delay_t) + ' minutes.')
            m50.delay(minutes=delay_t)
