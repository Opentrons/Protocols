from opentrons import labware, instruments, modules
# from otcustomizers import StringSelection
import math

# labware setup
mag_deck = modules.load('magdeck', '1')
plate = labware.load('biorad-hardshell-96-PCR', '1', share=True)
new_plate = labware.load('biorad-hardshell-96-PCR', '2')
trough = labware.load('trough-12row', '5')
tipracks = [labware.load('tiprack-200ul', slot)
            for slot in ['6', '7', '8', '9', '10', '11']]

# pipette setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=tipracks[:3])

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks[3:])

# reagent setup
ethanol = trough.wells('A1')


def run_custom_protocol(
        number_of_samples: int=24,
        beads_container: 'StringSelection'(
            'opentrons-tuberack-2ml-eppendorf',
            'opentrons-aluminum-block-2ml-screwcap',
            'trough-12row')='opentrons-tuberack-2ml-eppendorf',
        beads_location: str='A1',
        bead_volume: float=50,
        elution_buffer_container: 'StringSelection'(
            'opentrons-tuberack-2ml-eppendorf',
            'opentrons-aluminum-block-2ml-screwcap',
            'trough-12row')='opentrons-tuberack-2ml-eppendorf',
        elution_buffer_location: str='B1',
        elution_buffer_volume: float=12):

    if beads_container == 'trough-12row':
        beads = trough.wells(beads_location)
    else:
        beads_labware = labware.load(beads_container, '3')
        beads = beads_labware.wells(beads_location)
    if elution_buffer_container == 'trough-12row':
        elution_buffer = trough.wells(elution_buffer_location)
    elif elution_buffer_container == beads_container:
        elution_buffer = beads_labware.wells(elution_buffer_location)
    else:
        elution_buffer_labware = labware.load('elution_buffer_container', '4')
        elution_buffer = elution_buffer_labware.wells(elution_buffer_location)

    cols = math.ceil(number_of_samples/8)
    samples = [well for well in plate.wells()[:number_of_samples]]
    sample_cols = [well for well in plate.rows(0).wells()[:cols]]
    new_samples = [well for well in new_plate.wells()[:number_of_samples]]

    # mix bead stock and add 50 uL beads to each well
    p50.pick_up_tip()
    p50.mix(20, 50, beads)
    for sample in samples:
        if not p50.tip_attached:
            p50.pick_up_tip()
        p50.transfer(
            bead_volume, beads, sample,
            mix_before=(5, 50), mix_after=(5, 50), new_tip='never')
        p50.drop_tip()

    p50.delay(minutes=5)
    mag_deck.engage()
    p50.delay(minutes=5)

    # remove supernatant
    for col in sample_cols:
        m300.transfer(bead_volume, col, m300.trash_container.top())

    # wash beads with 200 uL 80% ethanol
    m300.pick_up_tip()
    start_tip = m300.current_tip()
    for wash_cycle in range(2):
        if wash_cycle == 0:
            trash = False
        else:
            trash = True
        if not m300.tip_attached:
            m300.start_at_tip(start_tip)
            m300.pick_up_tip()
        m300.transfer(200, ethanol, [well.top() for well in sample_cols],
                      trash=trash)
        for col in sample_cols:
            m300.transfer(200, col, m300.trash_container.top(), trash=trash)

    # dry beads for 5 min
    m300.delay(minutes=5)
    mag_deck.disengage()

    # elute DNA in elution buffer and transfer to new plate
    for source, dest in zip(samples, new_samples):
        p50.pick_up_tip()
        p50.transfer(elution_buffer_volume, elution_buffer, source,
                     mix_after=(10, 12), new_tip='never')
        p50.transfer(elution_buffer_volume, source, dest, blow_out=True,
                     new_tip='never')
        p50.drop_tip()
