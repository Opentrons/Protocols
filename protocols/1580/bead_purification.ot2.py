from opentrons import labware, instruments, modules, robot
import math

metadata = {
    'protocolName': 'Bead Purification',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

pcr_plate_name = 'framestar-break-way-96-pcr-plate-low-profile'
if pcr_plate_name not in labware.list():
    labware.create(
        pcr_plate_name,
        grid=(12, 9),
        spacing=(9, 9),
        diameter=5.5,
        depth=15.1,
        volume=200)

# labware setup
reg_plate = labware.load(pcr_plate_name, '1')
mag_module = modules.load('magdeck', '4')
mag_plate = labware.load(pcr_plate_name, '4', share=True)
tuberack = labware.load('opentrons-tuberack-1.5ml-eppendorf', '5')
trough = labware.load('trough-12row', '7')

tiprack_50 = labware.load('opentrons-tiprack-300ul', '2')
tipracks_300 = [labware.load('opentrons-tiprack-300ul', slot)
                for slot in ['3', '6', '8', '9', '10', '11']]

# instrument setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack_50])
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks_300)


def run_custom_protocol(number_of_samples: int=96):
    # check for too many samples
    if number_of_samples > 96:
        raise Exception('Number of samples cannot exceed 96.')

    # reagent setup
    samples = mag_plate.wells('A1', length=number_of_samples)
    sample_cols = mag_plate.cols('1', length=math.ceil(number_of_samples/8))
    spri_beads = tuberack.wells('A1')
    ethanol = trough.wells('A1', length=2)
    elution_buffer = trough.wells('A3', length=2)

    if mag_module.status == 'engaged':
        mag_module.disengage()

    for run_num in range(2):
        robot.comment(f'This is the beginning of Bead Purification \
{run_num+1}.')

        # transfer beads to sample_cols
        p50.pick_up_tip(tipracks_300[0].wells('A1'))
        for sample in samples:
            if p50.current_volume < 15:
                if p50.current_volume > 0:
                    p50.blow_out(spri_beads.top())
                p50.mix(5, 50, spri_beads)
                p50.blow_out(spri_beads.top())
                p50.aspirate(50, spri_beads)
            p50.dispense(15, sample.top())
            p50.delay(seconds=0.3)
        p50.blow_out(spri_beads.top())
        p50.drop_tip()

        # mix sample + beads
        m300.start_at_tip(tipracks_300[0].cols('2'))
        for col in sample_cols:
            m300.pick_up_tip()
            m300.mix(10, 30, col)
            m300.blow_out(col[0].top())
            m300.drop_tip()

        m300.delay(minutes=5)
        robot._driver.run_flag.wait()
        mag_module.engage(height=18)
        m300.delay(minutes=5)

        # remove supernatant
        m300.set_flow_rate(aspirate=30)  # slow down aspiration speed
        for col in sample_cols:
            m300.transfer(34, col, m300.trash_container.top())
        m300.set_flow_rate(aspirate=150)  # set speed back to default

        # wash with 80% ethanol twice
        m300.pick_up_tip()
        reuse_tip = m300.current_tip
        for index in range(2):
            if not m300.tip_attached:
                m300.start_at_tip(reuse_tip)
                m300.pick_up_tip()
            args = {'trash': False if index == 0 else True}
            m300.transfer(
                200, ethanol[index], [col[0].top() for col in sample_cols],
                )
            m300.delay(seconds=30)
            for col in sample_cols:
                m300.transfer(250, col, m300.trash_container.top(), **args)

        mag_module.disengage()
        m300.delay(minutes=5)

        # resuspend beads in elution buffer
        for col in sample_cols:
            m300.pick_up_tip()
            m300.transfer(30, elution_buffer[run_num], col, new_tip='never')
            m300.mix(10, 25, col)
            m300.blow_out(col[0].top())
            m300.drop_tip()

        m300.delay(minutes=3)
        robot._driver.run_flag.wait()
        mag_module.engage(height=18)
        m300.delay(minutes=1)

        # transfer supernatant to new plate
        sample_dests = reg_plate.wells('A1', length=number_of_samples)
        for sample, dest in zip(samples, sample_dests):
            p50.pick_up_tip()
            p50.transfer(25, sample, dest, new_tip='never')
            p50.mix(10, 20, dest)
            p50.blow_out(dest.top())
            p50.drop_tip()

        robot.comment(f'This is the end of Bead Purification {run_num + 1}.')

        if run_num == 0:

            robot.pause("Place STRIPs PCR2 in slot 1 in a Thermocycler to \
perform PCR2. While waiting, discard all the tubes on the Magnetic Module. \
Replenish all tipracks. Refill 80% Ethanol in wells A1 and A2 of the trough. \
Once PCR2 is finished, place STRIPs PCR2 on the Magnetic Module. Place clean \
tubes in slot 1 before resuming the protocol.")

            p50.reset()
            m300.reset()
