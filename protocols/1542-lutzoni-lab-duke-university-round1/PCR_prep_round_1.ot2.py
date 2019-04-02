from opentrons import labware, instruments

metadata = {
    'protocolName': 'PCR Preparation Round 1/2',
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
PCR = labware.load('Olympus-96-plate', '1')
DNA = labware.load('Olympus-96-plate', '2')
tubes = labware.load('4x6-custom-tube-rack', '3')
tips10 = labware.load('tiprack-10ul', '4')
tips50 = labware.load('opentrons-tiprack-300ul', '5')

# pipettes
m10 = instruments.P10_Multi(
    mount='right',
    tip_racks=[tips10]
)

p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tips50]
)


def run_custom_protocol(number_of_primers: int = 2):
    # handle too many primers
    if number_of_primers > 2:
        raise Exception("Too many primers. Please specify 0, 1, or 2 primers.")

    # reagent setup
    buffer = tubes.wells('A1')
    dNTP = tubes.wells('B1')
    taq_pol = tubes.wells('C1')
    BSA = tubes.wells('D1')
    H2O = tubes.wells('A2')
    primers = tubes.wells('B2', length=2)
    mm = tubes.wells('A3', length=2)

    # volume setup for each sample
    vol_buffer = 5
    vol_dNTP = 0.5
    vol_primer = 0.5
    vol_taq_pol = 0.2
    vol_BSA = 0.25
    vol_H2O = 17.55-0.5*number_of_primers

    # create 100x master mix in 2 separate mix_tubes (500x each)
    p50.transfer(vol_buffer*50, buffer, [tube.top() for tube in mm])
    p50.distribute(vol_dNTP*50, dNTP, [tube.top() for tube in mm])
    for primer in primers:
        p50.distribute(vol_primer*50, primer, [tube.top() for tube in mm])
    p50.distribute(vol_taq_pol*50, taq_pol, [tube.top() for tube in mm])
    p50.distribute(vol_BSA*50, BSA, [tube.top() for tube in mm])
    p50.transfer(vol_H2O*50,
                 H2O,
                 [tube.top() for tube in mm],
                 mix_after=(5, 50))

    # evenly distribute master mix to all plate wells
    p50.distribute(23, mm[0], PCR.wells('A1', length=48))
    p50.distribute(23, mm[1], PCR.wells('A7', length=48))

    # transfer Extract-N-Amp DNA to corresponding well
    m10.transfer(2,
                 [s.bottom(4) for s in DNA.rows('A')],
                 PCR.rows('A'),
                 blow_out=True,
                 new_tip='always')
