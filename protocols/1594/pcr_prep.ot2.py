from opentrons import labware, instruments

metadata = {
    'protocolName': 'PCR Preparation',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# create custom labware
tips10_name = 'Starlab-10ul-tiprack'
if tips10_name not in labware.list():
    labware.create(
        tips10_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5,
        depth=60)

tips50_name = 'Starlab-50ul-tiprack'
if tips50_name not in labware.list():
    labware.create(
        tips50_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5,
        depth=60)


trough_name = 'Starlab-trough-12row'
if trough_name not in labware.list():
    labware.create(
        trough_name,
        grid=(12, 1),
        spacing=(9, 0),
        diameter=8.1,
        depth=39.1,
        volume=7000
    )

plate_name = 'Starlab-96-PCR'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(8.9, 8.9),
        diameter=5.6,
        depth=15,
        volume=200
    )

# load labware
trough = labware.load('trough-12row', '1', 'reagent trough')
forward_primer = labware.load(plate_name, '2', 'foward primer plate')
reverse_primer = labware.load(plate_name, '3', 'reverse primer plate')

# reagent setup
mineral_oil = trough.wells('A1')
master_mix = trough.wells('A3')


def run_custom_protocol(
        number_of_destination_plates: int = 5,
        volume_of_mineral_oil_in_ul: float = 15,
        distance_from_oil_surface_to_opening_of_trough_in_mm: float = 10
        ):

    # check for labware space
    if number_of_destination_plates > 5:
        raise Exception('Please specify 5 or fewer destination plates.')

    # remaining labware
    dest_plates = [labware.load(plate_name, str(slot))
                   for slot in range(4, 4+number_of_destination_plates)]
    tips50 = labware.load(tips50_name, str(4+number_of_destination_plates))
    tips10 = [labware.load(tips10_name, str(slot))
              for slot in range(5+number_of_destination_plates, 12)]

    # pipettes
    m10 = instruments.P10_Multi(mount='right', tip_racks=tips10)
    m50 = instruments.P50_Multi(mount='left', tip_racks=[tips50])

    all_dests = [well for plate in dest_plates for well in plate.rows('A')]

    # variables for mineral oil height track
    h_oil = -(distance_from_oil_surface_to_opening_of_trough_in_mm + 5)
    length = 71.4
    width = dest_plates[0].wells(0).properties['diameter']

    def oil_height_track():
        nonlocal h_oil
        dh = volume_of_mineral_oil_in_ul/(length*width)
        h_oil -= dh

    # transfer mineral oil
    m50.set_flow_rate(aspirate=5, dispense=10)
    t_count = 0
    m50.pick_up_tip()
    for d in all_dests:
        # prevent oil buildup in the same tip (replace after each plate fill)
        if t_count == 12:
            m50.drop_tip()
            m50.pick_up_tip()
            t_count = 1

        oil_height_track()
        m50.aspirate(volume_of_mineral_oil_in_ul, mineral_oil.top(h_oil))
        m50.delay(seconds=5)
        m50.dispense(d.bottom(5))
        t_count += 1
        m50.blow_out()
    m50.drop_tip()

    # distribute PCR master mix
    m50.set_flow_rate(aspirate=25, dispense=50)
    m50.pick_up_tip()
    for d in all_dests:
        m50.transfer(18, master_mix, d.top(), blow_out=True, new_tip='never')
    m50.drop_tip()

    # forward primer distribution
    for ind, primer in enumerate(forward_primer.rows('A')):
        dests = [plate.rows('A')[ind] for plate in dest_plates]
        m10.distribute(1, primer, dests)

    # reverse primer distribution
    for ind, primer in enumerate(reverse_primer.rows('A')):
        dests = [plate.rows('A')[ind] for plate in dest_plates]
        m10.distribute(1, primer, dests)
