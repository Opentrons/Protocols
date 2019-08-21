from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Oxford Nanopore 16S Barcoding NGS Library Prep',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
res12_name = 'axygen_12_reservoir_290ml'
if res12_name not in labware.list():
    labware.create(
        res12_name,
        grid=(12, 1),
        spacing=(9, 0),
        diameter=8.3,
        depth=43,
        volume=22000
    )

# load modules and labware
rxn_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr', '1', 'sample plate')
barcode_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr', '2', 'barcode plate')
reagent_res = labware.load(
    res12_name, '3', 'reagent reservoir')
magdeck = modules.load('magdeck', '4')
magplate = labware.load(
    'biorad_96_wellplate_200ul_pcr',
    '4',
    'sample plate (on magnetic module)',
    share=True
)
original_sample_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr', '5', 'original samples')
reagent_rack = labware.load(
    'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '6')
tips10 = [
    labware.load('opentrons_96_tiprack_10ul', slot) for slot in ['8', '9']]
tips300 = [labware.load('opentrons_96_tiprack_300ul', slot) for slot in ['10']]

# reagents
nuc_free_water = reagent_rack.wells('A1')
longamp_mm = reagent_rack.wells('B1')
tris_hcl = reagent_rack.wells('A2')
rap = reagent_rack.wells('B2')

ampure_xp_beads = reagent_res.wells(0)
etoh = reagent_res.wells()[1:3]
liquid_trash = reagent_res.wells()[10:]


def run_custom_protocol(
        number_of_samples: int = 96,
        barcode_start_well: str = 'A1',
        p10_mount: StringSelection('right', 'left') = 'right',
        p300_mount: StringSelection('left', 'right') = 'left'
):
    # checks
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Invalid number of samples.')

    all_wells = [r + str(c) for r in 'ABCDEFGH' for c in range(1, 13)]
    if barcode_start_well not in all_wells:
        raise Exception('Invalid barcode start well (must be between A1 and \
H12)')

    if all_wells.index(barcode_start_well) + number_of_samples > 96:
        raise Exception('Invalid barcode start well with input number of \
samples')

    if p10_mount == p300_mount:
        raise Exception('Select different mounts for P10 and P300 pipettes.')

    # pipettes
    p10 = instruments.P10_Single(mount=p10_mount, tip_racks=tips10)
    p300 = instruments.P300_Single(mount=p300_mount, tip_racks=tips300)

    # setup
    original_samples = original_sample_plate.wells()[:number_of_samples]
    reactions = rxn_plate.wells()[:number_of_samples]
    barcodes = barcode_plate.wells(
        barcode_start_well, length=number_of_samples)
    mag_samples = magplate.wells()[:number_of_samples]

    tip10_count = 0
    tip10_max = 96*len(tips10)
    tip300_count = 0
    tip300_max = 96*len(tips300)

    def tip_check(pip):
        nonlocal tip10_count
        nonlocal tip300_count
        if pip == 'p10':
            if tip10_count == tip10_max:
                robot.pause('Replace 10ul tipracks before resuming.')
                tip10_count = 0
                p10.reset()
            tip10_count += 1
        elif pip == 'p300':
            if tip300_count == tip300_max:
                robot.pause('Replace 300ul tipracks before resuming.')
                tip300_count = 0
                p300.reset()
            tip300_count += 1

    robot.comment('Transfer 10ng genomic DNA into the sample plate. Adjust the \
volume to 10ul with nuclease-free water. Mix thoroughly by flicking the tube. \
Spin down briefly in a microfuge, and mount in slot 4.')

    # prepare reaction mix
    for o, r in zip(original_samples, reactions):
        tip_check('p10')
        p10.transfer(25, longamp_mm, r)
        tip_check('p10')
        p10.pick_up_tip()
        p10.transfer(5, nuc_free_water, r, new_tip='never')
        p10.transfer(10, o, r, new_tip='never')
        p10.drop_tip()

    robot.pause('Mix gently by flicking the tube, and spin down. Remove the \
foil of the barcode plate for pipette access.')

    # add barcode
    for b, r, in zip(barcodes, reactions):
        tip_check('p10')
        p10.pick_up_tip()
        p10.transfer(10, b, r, new_tip='never')
        p10.mix(5, 9, r)
        p10.blow_out(r.top())
        p10.drop_tip()

    robot.pause('Thermocycle according to parameters prescribed in kit \
manual. Replace on slot 1 when finished.')

    # transfer DNA samples, add beads, and mix
    tip_check('p300')
    p300.pick_up_tip()
    p300.mix(10, 200, ampure_xp_beads)
    p300.blow_out(ampure_xp_beads.top())
    for i, (r, m) in enumerate(zip(reactions, mag_samples)):
        if not p300.tip_attached:
            tip_check('p300')
            p300.pick_up_tip()
        p300.transfer(30, ampure_xp_beads, m, new_tip='never')
        p300.transfer(50, r, m, new_tip='never')
        p300.mix(5, 30, m)
        p300.blow_out(m.top())
        p300.drop_tip()

    robot.pause('Incubate on a Hula mixer (rotator mixer) for 5 minutes at \
RT. Then spin down the samples and place on the magnetic module.')

    robot._driver.run_flag.wait()
    magdeck.engage(height=18)

    p300.set_flow_rate(aspirate=30, dispense=60)

    # Ethanol washes
    for wash in range(2):
        for m in mag_samples:
            tip_check('p300')
            p300.pick_up_tip()
            p300.transfer(200, etoh[wash], m.top(), new_tip='never')
            p300.transfer(220, m, liquid_trash[wash], new_tip='never')
            p300.drop_tip()

    robot.pause('Spin down and place the tube back on the magnetic module. \
Allow to dry for ~30s but not to the point of the pellet cracking.')

    robot._driver.run_flag.wait()
    magdeck.disengage()

    # transfer Tris-HCl
    for m in mag_samples:
        tip_check('p10')
        p10.pick_up_tip()
        p10.transfer(10, tris_hcl, m, new_tip='never')
        p10.mix(3, 8, m)
        p10.blow_out(m)
        p10.drop_tip()

    p10.delay(minutes=2)

    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    robot._driver.run_flag.wait()
    robot.pause('Resume once the eluate is clear and colourless. Replace the \
barcode plate in slot 2 with a clean plate for elution')

    elution_samples = barcodes
    for m, e in zip(mag_samples, elution_samples):
        tip_check('p10')
        p10.pick_up_tip()
        p10.transfer(10, m, e, new_tip='never')
        p10.blow_out(e)
        p10.drop_tip()

    robot.pause('Dispose of the pelleted beads, quantify 1 μl of eluted \
sample using a Qubit fluorometer, and pool all barcoded libraries in the \
desired ratios to a total of 50-100 fmoles in 10 μl of 10 mM Tris-HCl pH 8.0 \
with 50 mM NaCl. For 16S amplicons of ~1500 bp, 50-100 fmoles equates to \
~50-100 ng. Put the pool tube in well A3 of the tuberack in slot 6.')

    pool = reagent_rack.wells('A3')

    tip_check('p10')
    p10.transfer(1, rap, pool)

    robot.comment('Flick the tube and spin down. Incubate for 5 minutes at room \
temperature. Thaw the Sequencing Buffer (SQB), Loading Beads (LB), Flush \
Tether (FLT) and one tube of Flush Buffer (FB) at RT before placing the tubes \
on ice as soon as thawing is complete. Continue manually with the SpotON \
loading as prescribed in the manual.')
