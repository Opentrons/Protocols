from opentrons import labware, instruments, modules

metadata = {
    'protocolName': 'NEBNext Direct Genotyping Solution Panels Part 2',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

pcr_plate_type = 'framestar-96-PCR-skirted'
if pcr_plate_type not in labware.list():
    labware.create(
        pcr_plate_type,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.5,
        depth=15.1)

# labware Setup
mag_module = modules.load('magdeck', '1')
bead_plate = labware.load(pcr_plate_type, '1', share=True)
tuberack = labware.load('opentrons-tuberack-2ml-screwcap', '2')
tiprack_300 = labware.load('opentrons-tiprack-300ul', '11')

# reagent Setup
beads = tuberack.wells('A1')
hyb_wash = tuberack.wells('B1')
bead_prep_buffer = tuberack.wells('C1')

# instrument Setup
p300 = instruments.P300_Single(
    mount='right',
    tip_racks=[tiprack_300])


def run_custom_protocol(engage_height: float=18):

    dests = bead_plate.wells('A1', length=4)

    # transfer beads to new tubes
    p300.pick_up_tip()
    p300.mix(5, 300, beads)
    p300.blow_out(beads)
    for dest in dests:
        p300.transfer(82.5, beads, dest, new_tip='never')
    p300.drop_tip()

    mag_module.engage(height=engage_height)
    p300.delay(minutes=1)

    # remove supernatant
    p300.consolidate(100, dests, p300.trash_container.top())

    mag_module.disengage()

    # wash beads with Hybridization Wash
    for _ in range(2):
        p300.pick_up_tip()
        p300.transfer(
            165, hyb_wash, [dest.top(-5) for dest in dests], new_tip='never')
        for dest in dests:
            p300.mix(5, 120, dest)
            p300.blow_out(dest)
        p300.retract()
        mag_module.engage(height=engage_height)
        p300.delay(minutes=1)
        for dest in dests:
            p300.transfer(
                200, dest, p300.trash_container.top(), new_tip='never')
        p300.drop_tip()
        mag_module.disengage()

    # resuspend beads in Bead Prep Buffer
    p300.pick_up_tip()
    p300.distribute(
        33, bead_prep_buffer, [dest.top(-3) for dest in dests],
        blow_out=bead_prep_buffer, new_tip='never')
    for dest in dests:
        p300.mix(5, 30, dest)
        p300.blow_out(dest)
    p300.drop_tip()
