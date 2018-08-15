from opentrons import labware, instruments

# reagent rack setup
liquid1 = labware.load('tube-rack-15_50ml', '6')
liquid2 = labware.load('tube-rack-15_50ml', '9')

# capsule plates
plates = [
    labware.load('96-PCR-flat', '1'),
    labware.load('96-PCR-flat', '2'),
    labware.load('96-PCR-flat', '3'),
    labware.load('96-PCR-flat', '4'),
    labware.load('96-PCR-flat', '5'),
    labware.load('96-PCR-flat', '7'),
    labware.load('96-PCR-flat', '8'),
    labware.load('96-PCR-flat', '11')
]

# tip rack
tiprack = labware.load('tiprack-1000ul', '10')

# pipette setup
p1000 = instruments.P1000_Single(
    mount='right',
    tip_racks=[tiprack])

# locates all eight 50 mL tubes in reagents racks
tubes_50ml = [well for well in liquid1.wells('A3', 'A4', 'B3', 'B4')] + \
    [well for well in liquid2.wells('A3', 'A4', 'B3', 'B4')]


def run_custom_protocol(fill_volume: float=500):
    """
    Fill each plate of capsules with reagent in each 50 mL tube
    """
    p1000.pick_up_tip()

    for each_tube, each_plate in zip(tubes_50ml, plates):
        p1000.transfer(
            fill_volume,
            each_tube,
            each_plate.wells(),
            air_gap=int(1000-fill_volume),  # air gap to prevent dripping
            new_tip='never')

    p1000.drop_tip()
