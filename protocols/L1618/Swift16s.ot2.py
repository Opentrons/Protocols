from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Swift Biosciences Swift Amplicon 16S+ ITS Panel',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# modules and labware
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load('biorad_96_wellplate_200ul_pcr', '1', share=True)
tempdeck = modules.load('tempdeck', '4')
temp_plate = labware.load('biorad_96_wellplate_200ul_pcr', '4', share=True)
elution_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr', '2', 'elution plate')
reagent_rack = labware.load(
    'opentrons_24_aluminumblock_generic_2ml_screwcap',
    '3',
    'reagent tuberack (for mastermixes)')
reagent_res = labware.load(
    'usascientific_12_reservoir_22ml', '5', 'reagent reservoir')
index_rack = labware.load('opentrons_96_aluminumblock_generic_pcr_strip_200ul',
                          '6', 'Aluminum Block with Index Solutions')
tempdeck.set_temperature(4)
tempdeck.wait_for_temp()
tips50 = [
    labware.load('opentrons_96_tiprack_300ul', slot)
    for slot in ['7', '8', '9']
]
tips300 = [
    labware.load('opentrons_96_tiprack_300ul', slot)
    for slot in ['10', '11']
]

mm1 = reagent_rack.wells('A1')
mm2 = reagent_rack.wells('A2')
irm1 = reagent_rack.wells('B1')
irm2 = reagent_rack.wells('B2')

magbeads = reagent_res.wells(0)
etoh_waste = reagent_res.wells(11)
pegnacl = reagent_res.wells(5)
PCRte = reagent_res.wells(6)


def run_custom_protocol(
        p50_single_mount: StringSelection('left', 'right') = 'left',
        p300_multi_mount: StringSelection('right', 'left') = 'right',
        number_of_samples: StringSelection('96', '48') = '48'
):

    # create pipettes and values based on number of samples
    s50 = instruments.P50_Single(mount=p50_single_mount, tip_racks=tips50)
    m300 = instruments.P300_Multi(mount=p300_multi_mount, tip_racks=tips300)
    temp1 = temp_plate.wells()[:48]
    mag1 = mag_plate.wells()[:48]

    if number_of_samples == '96':
        temp2 = temp_plate.wells()[48:]
        mag2 = mag_plate.wells()[48:]
        # temptotal = temp1 + temp2
        magtotal = mag_plate
        magcol = mag_plate.rows('A')
        elutes = elution_plate
    else:
        # temptotal = temp1
        magtotal = mag1
        magcol = mag_plate.rows('A')[:6]
        elutes = elution_plate.wells()[:48]
    # pipette tip function
    tip50_count = 0
    tip300_count = 0
    tip50_max = len(tips50)*96
    tip300_max = len(tips300)*12

    def pick_up(pip):
        nonlocal tip50_count
        nonlocal tip300_count

        if pip == s50:
            if tip50_count == tip50_max:
                robot.pause('Replace 50/300ul tipracks in slots 7, 8, 9 \
                before resuming.')
                s50.reset()
                tip50_count = 0
            s50.pick_up_tip()
            tip50_count += 1
        else:
            if tip300_count == tip300_max:
                robot.pause('Replace 50/300ul tipracks in slots 10 and 11 \
                before resuming.')
                m300.reset()
                tip300_count = 0
            m300.pick_up_tip()
            tip300_count += 1

    # wash function

    wash_count = 1

    def wash(wvol, rvol):
        nonlocal wash_count
        m300.set_flow_rate(aspirate=50, dispense=50)

        # add wash
        pick_up(m300)
        for samples in magcol:
            m300.transfer(wvol, reagent_res.wells(wash_count), samples.top(-1),
                          air_gap=20, new_tip='never')
            m300.blow_out(samples.top(-1))
        m300.delay(seconds=30)

        m300.set_flow_rate(dispense=300)
        for samples in magcol:
            if not m300.tip_attached:
                pick_up(m300)
            m300.transfer(rvol, samples, etoh_waste.top(-1), air_gap=20,
                          new_tip='never')
            m300.blow_out(etoh_waste.top(-1))
            m300.drop_tip()
        m300.set_flow_rate(aspirate=150)
        wash_count += 1

    """ Multiplex PCR """
    pick_up(s50)
    s50.mix(10, 45, mm1)
    s50.blow_out(mm1.top())
    for sample in temp1:
        if not s50.tip_attached:
            pick_up(s50)
        s50.transfer(20, mm1, sample, new_tip='never')
        s50.blow_out(sample.top())
        s50.drop_tip()

    if number_of_samples == '96':
        pick_up(s50)
        s50.mix(10, 45, mm2)
        s50.blow_out(mm2.top())
        for sample in temp2:
            if not s50.tip_attached:
                pick_up(s50)
            s50.transfer(20, mm2, sample, new_tip='never')
            s50.blow_out(sample.top())
            s50.drop_tip()

    robot.pause('Please remove plate from the temperature module and place in \
    thermocycler for PCR run. When nearing completion of PCR run, place the \
    Index Reaction Mix in tube slots A3 (and A4 if doing 96 samples) in deck \
    slot 3. After completion of PCR run, place sample on the magnetic module \
    in deck slot 1 and click RESUME in OT App.')

    """ Size Selection and Clean-Up Step 1 """
    pick_up(m300)
    m300.mix(5, 100, magbeads)
    m300.blow_out(magbeads.top(-1))
    magdeck.disengage()

    for sample in magcol:
        if not m300.tip_attached:
            pick_up(m300)
        m300.transfer(36, magbeads, sample, new_tip='never')
        m300.blow_out(sample.top())
        m300.drop_tip()

    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage()
    m300.delay(minutes=5)

    for sample in magcol:
        pick_up(m300)
        m300.transfer(60, sample, etoh_waste, new_tip='never')
        m300.drop_tip()

    wash(200, 200)

    wash(200, 200)

    magdeck.disengage()
    robot.pause('Pulse-Spin samples in microfuge and place back on Magnetic \
    Module. Before beginning Indexing Step, be sure Index D50X and D7XX are \
    placed in the positions specified in the protocol documentation. Place \
    the plate back on the Magnetic Module when ready and click RESUME.')

    """ Indexing Step """

    Index5 = range(8)
    Index5rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    Index7 = range(8, 20)
    Index7s = [8, 14, 9, 15, 10, 16, 11, 17, 12, 18, 13, 19]

    if number_of_samples == '48':
        idx_range = range(0, 41, 8)
        for i in Index5:
            pick_up(s50)
            for j in idx_range:
                s50.transfer(5, index_rack.wells(i),
                             magtotal.wells(i+j).top(-1), new_tip='never')
                s50.blow_out(magtotal.wells(i+j).top())
            s50.drop_tip()

        startno = 1
        for q in range(48):
            i7 = q//4
            if not s50.tip_attached:
                pick_up(s50)
            s50.transfer(10, index_rack.wells(Index7s[i7]),
                         magtotal.wells(q).top(-1), new_tip='never')
            s50.blow_out(magtotal.wells(q).top())
            startno += 1
            if startno > 4:
                s50.drop_tip()
                startno = 1
    else:
        for i, j in zip(Index5, Index5rows):
            pick_up(s50)
            for k in magtotal.rows(j):
                s50.transfer(5, index_rack.wells(i),
                             k.top(-1), new_tip='never')
                s50.blow_out(k.top())
            s50.drop_tip()

        startno = 1
        for q in range(96):
            i7 = (q//8)
            if not s50.tip_attached:
                pick_up(s50)
            s50.transfer(10, index_rack.wells(Index7[i7]),
                         magtotal.wells(q).top(-1), new_tip='never')
            s50.blow_out(magtotal.wells(q).top())
            startno += 1
            if startno > 8:
                s50.drop_tip()
                startno = 1

    if not s50.tip_attached:
        pick_up(s50)

    for dest in mag1:
        s50.transfer(35, irm1, dest.top(-1), new_tip='never')
        s50.blow_out(dest.top())

    if number_of_samples == '96':
        for dest in mag2:
            s50.transfer(35, irm2, dest.top(-1), new_tip='never')
            s50.blow_out(dest.top())

    s50.drop_tip()

    robot.pause('Remove plate from OT-2 and place in thermocycler for \
    20 minutes at 37C. Before resuming, briefly vortex the PEG NaCl solution \
    before adding it Column 6 in the 12-Channel Reservoir in slot 5. When \
    ready, replace plate on Magnetic Module and click RESUME.')

    """ Size Selection and Clean-Up Step 2 """
    pick_up(m300)
    for dest in magcol:
        m300.transfer(42.5, pegnacl, dest.top(-1), new_tip='never')
        m300.blow_out(dest.top())

    robot.pause('Incubate the sample for 5 minutes and then pulse-spin the \
    samples with a microfuge. After spinning, replace the plate on the \
    Magnetic Module and click RESUME.')

    magdeck.engage()
    m300.delay(minutes=5)

    m300.set_flow_rate(aspirate=50)
    for samps in magcol:
        if not m300.tip_attached:
            pick_up(m300)
        m300.transfer(88, samps, etoh_waste, new_tip='never')
        m300.drop_tip()

    wash(180, 180)

    wash(180, 180)

    magdeck.disengage()

    for sample in magtotal:
        pick_up(s50)
        s50.transfer(20, PCRte, sample, new_tip='never')
        s50.mix(5, 20, sample)
        s50.blow_out(sample.top())
        s50.drop_tip()

    s50.delay(minutes=2)
    robot._driver.run_flag.wait()

    magdeck.engage()
    s50.delay(minutes=2)

    for m, e in zip(magtotal, elutes):
        pick_up(s50)
        s50.transfer(20, m, e, new_tip='never')
        s50.blow_out(e.top())
        s50.drop_tip()

    robot.comment('Congratulations, the protocol is now complete. Please move \
    samples from slot 2 to next stage and properly dispose of waste.')
