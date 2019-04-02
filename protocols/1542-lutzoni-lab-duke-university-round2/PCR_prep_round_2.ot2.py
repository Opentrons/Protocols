from opentrons import labware, instruments, robot

metadata = {
    'protocolName': 'PCR Preparation Round 2/2',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = 'Olympus-96-plate'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6,
        depth=20,
        volume=200
    )

rack_name = '4x6-custom-tube-rack'
if rack_name not in labware.list():
    labware.create(
        rack_name,
        grid=(6, 4),
        spacing=(20, 19),
        diameter=5,
        depth=42,
        volume=1700
    )

# load labware
PCR_round_2 = labware.load('Olympus-96-plate', '1')
PCR_round_1 = labware.load('Olympus-96-plate', '2')
primers = labware.load('Olympus-96-plate', '3')
tubes = labware.load('4x6-custom-tube-rack', '4')
tips10 = [labware.load('tiprack-10ul', slot) for slot in ['5', '6']]
tips50 = labware.load('opentrons-tiprack-300ul', '7')

# pipettes
m10 = instruments.P10_Multi(
    mount='right',
    tip_racks=tips10
)

p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tips50]
)


def run_custom_protocol(number_of_plates: int = 1):

    # reagent setup
    buffer = tubes.wells('A1')
    dNTP = tubes.wells('B1')
    taq_pol = tubes.wells('C1')
    BSA = tubes.wells('D1')
    H2O = tubes.wells('A2')
    mm = tubes.wells('B2', length=2)

    for plate in range(number_of_plates):
        if plate > 0:
            robot.pause('Please replace all reagents and plates in their '
                        'respective defined positions before resuming.')
        # volume setup for each sample
        vol_buffer = 5
        vol_dNTP = 0.5
        vol_taq_pol = 0.2
        vol_BSA = 0.25
        vol_H2O = 16.05

        # create second master mix
        p50.transfer(vol_buffer*50, buffer, [tube.top() for tube in mm])
        p50.distribute(vol_dNTP*50, dNTP, [tube.top() for tube in mm])
        p50.distribute(vol_taq_pol*50, taq_pol, [tube.top() for tube in mm])
        p50.distribute(vol_BSA*50, BSA, [tube.top() for tube in mm])
        p50.transfer(vol_H2O*50,
                     H2O,
                     [tube.top() for tube in mm],
                     mix_after=(5, 50))

        # evenly distribute master mix to all plate wells
        p50.distribute(23, mm[0], PCR_round_2.wells('A1', length=48))
        p50.distribute(23, mm[1], PCR_round_2.wells('A7', length=48))

        # transfer PacBio Primers to corresponding well
        m10.transfer(2,
                     [s.bottom(1) for s in primers.rows('A')],
                     PCR_round_2.rows('A'),
                     blow_out=True,
                     new_tip='always')

        # transfer PCR product from previous round to corresponding well
        m10.transfer(1,
                     [s.bottom(1) for s in PCR_round_1.rows('A')],
                     PCR_round_2.rows('A'),
                     blow_out=True,
                     new_tip='always')
