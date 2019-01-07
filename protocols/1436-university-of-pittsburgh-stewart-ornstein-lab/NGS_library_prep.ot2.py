from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'NGS Library Prep',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware setup
mag_module = modules.load('magdeck', '1')
plate_A = labware.load('biorad-hardshell-96-PCR', '1', share=True)
plate_B = labware.load('biorad-hardshell-96-PCR', '2')
plate_C = labware.load('biorad-hardshell-96-PCR', '3')
plate_D = labware.load('96-deep-well', '4')
liquid_waste = labware.load('trough-12row', '5', 'LIQUID WASTE').wells('A1')
tipracks_10 = [labware.load('tiprack-10ul', slot)
               for slot in ['6', '7', '8']]
tipracks_300 = [labware.load('opentrons-tiprack-300ul', slot)
                for slot in ['9', '10', '11']]

# instrument setup
m10 = instruments.P10_Multi(
    mount='left',
    tip_racks=tipracks_10)
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks_300)


# reagent setup
beads = plate_B.cols('1')
TAE = plate_B.cols('3')
binding_buffer = plate_B.cols('5')
primer_mix = plate_B.cols('7')
RT_mix = plate_B.cols('9')
wash_buffer = plate_D.cols('1', to='2')

m10_tip_num = 0
m300_tip_num = 0


def update_m10_tip_tracking(num):
    global m10_tip_num
    m10_tip_num += num
    if m10_tip_num == len(m10.tip_racks) * 12:
        robot.pause("Your 10 uL tips have run out. Refill all of the tipracks \
before resuming.")
        m10.reset_tip_tracking()
        m10_tip_num = 0


def update_m300_tip_tracking(num):
    global m300_tip_num
    m300_tip_num += num
    if m300_tip_num == len(m300.tip_racks) * 12:
        robot.pause("Your 300 uL tips have run out. Refill all of the tipracks \
before resuming.")
        m300.reset_tip_tracking()
        m300_tip_num = 0


def run_custom_protocol(
        bead_volume: float= 10,
        wash_buffer_volume: float=60,
        TAE_volume: float=10,
        binding_buffer_volume: float=10,
        primer_mix_volume: float=4,
        RT_mix_volume: float=1,
        RNA_volume: float=3):

    # add beads to plate A
    for col in plate_A.cols():
        m10.pick_up_tip()
        m10.transfer(bead_volume, beads, col, new_tip='never')
        m10.mix(3, bead_volume, col)
        m10.blow_out(col)
        m10.drop_tip()
        update_m10_tip_tracking(1)

    robot.pause("Run the plate on a Thermocycler. Place it back in slot 1.")

    # mix mixture in plate A
    for col in plate_A.cols():
        m10.pick_up_tip()
        m10.mix(3, bead_volume, col)
        m10.blow_out(col)
        m10.drop_tip()
        update_m10_tip_tracking(1)

    m10.delay(minutes=5)
    mag_module.engage()
    m10.delay(minutes=1)

    # remove supernatant in plate A
    m300.pick_up_tip()
    m300.transfer(
        2.5 * bead_volume, plate_A.cols(), liquid_waste, new_tip='never')
    m300.drop_tip()
    update_m300_tip_tracking(1)

    # add wash buffer to plate A
    m300.distribute(
        wash_buffer_volume,
        wash_buffer[0],
        [col[0].top() for col in plate_A.cols()])
    update_m300_tip_tracking(1)

    # remove supernatant in plate A
    m300.consolidate(
        wash_buffer_volume + 10,
        [col for col in plate_A.cols()],
        liquid_waste)
    update_m300_tip_tracking(1)

    mag_module.disengage()

    # add TAE to plate A
    for col in plate_A.cols():
        m10.pick_up_tip()
        m10.transfer(TAE_volume, TAE, col, new_tip='never')
        m10.mix(3, 10, col)
        m10.drop_tip()
        update_m10_tip_tracking(1)

    robot.pause("Run the plate on a Thermocycler. Place it back in slot 1.")

    # add binding buffer in plate A
    for col in plate_A.cols():
        m10.pick_up_tip()
        m10.transfer(
            binding_buffer_volume, binding_buffer, col, new_tip='never')
        m10.mix(3, 10, col)
        m10.drop_tip()
        update_m10_tip_tracking(1)

    m300.delay(minutes=5)
    mag_module.engage()
    m300.delay(minutes=1)

    m300.consolidate(
        TAE_volume + binding_buffer_volume,
        [col for col in plate_A.cols()],
        liquid_waste)
    update_m300_tip_tracking(1)

    # add wash buffer to plate A
    m300.distribute(
        wash_buffer_volume,
        wash_buffer[1],
        [col[0].top() for col in plate_A.cols()])
    update_m300_tip_tracking(1)

    # remove supernatant in plate A
    m300.consolidate(
        wash_buffer_volume + 10,
        [col for col in plate_A.cols()],
        liquid_waste)
    update_m300_tip_tracking(1)

    mag_module.disengage()

    for col in plate_A.cols():
        m10.pick_up_tip()
        m10.transfer(primer_mix_volume, primer_mix, col, new_tip='never')
        if primer_mix_volume > m10.max_volume:
            mix_vol = m10.max_volume
        else:
            mix_vol = primer_mix_volume
        m10.mix(3, mix_vol, col)
        m10.drop_tip()
        update_m10_tip_tracking(1)

    robot.pause("Run the plate on a Thermocycler. Place it back in slot 1.")

    m10.transfer(
        RT_mix_volume,
        RT_mix,
        [col for col in plate_C.cols()])
    update_m10_tip_tracking(1)

    mag_module.engage()

    for source, dest in zip(plate_A.cols(), plate_C.cols()):
        m10.pick_up_tip()
        m10.transfer(RNA_volume, source, dest, new_tip='never')
        if RNA_volume > m10.max_volume:
            mix_vol = m10.max_volume
        else:
            mix_vol = RNA_volume
        m10.mix(3, mix_vol)
        m10.drop_tip()
        update_m10_tip_tracking(1)
