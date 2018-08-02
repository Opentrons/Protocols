from opentrons import containers, instruments
import math

# labware setup
tiprack_10ul = containers.load('tiprack-10ul', 'A2')
tiprack_200ul = containers.load('tiprack-200ul', 'C2')

# 8 tubes are arranged in A1, B1, C1... D2
sample_tubes = containers.load('tube-rack-2ml', 'A3')
trough = containers.load('trough-12row', 'E1')
plate = containers.load('96-flat', 'B2')

tsb_media = trough.wells('A1')

trash = containers.load('trash-box', 'B1')

# Pipette setup
m300 = instruments.Pipette(
    axis='a',
    max_volume=300,
    channels=8,
    tip_racks=[tiprack_200ul])

p10 = instruments.Pipette(
    axis='b',
    max_volume=10,
    channels=1,
    tip_racks=[tiprack_10ul])


def run_custom_protocol(diameter: int=60):

    # Create new labware depending on diameter input
    subdiameter = round(math.sqrt(diameter**2/2)/4, 1)
    if 'petri-dish-4x4grid' not in containers.list():
        containers.create('petri-dish-4x4grid',
                          grid=(4, 4),
                          spacing=(subdiameter, subdiameter),
                          diameter=subdiameter,
                          depth=10)

    petri_1 = containers.load('petri-dish-4x4grid', 'C1')
    petri_2 = containers.load('petri-dish-4x4grid', 'D1')

    """
    1. Serial Dilutions
    """
    # Transfer TSB media to A1-H2
    m300.transfer(297, tsb_media, plate.rows('1', to='2'))

    # Transfer TSB media to A3-H6
    m300.transfer(90, tsb_media, plate.rows('3', to='6'))

    # Transfer samples 1-8 to row A1-H1
    p10.transfer(3, sample_tubes.wells('A1', length=8), plate.rows('1'),
                 mix_after=(3, 10))

    # Serial dilute row 1->2, 2->3, 3->4, 4->5, and 5->6
    m300.transfer(10, plate.rows('1', to='5'), plate.rows('2', to='6'),
                  mix_after=(3, 10))

    """
    2. Titration on Agar Plates
    """
    # Define petri_1_source as C1-F4
    petri_1_source = [
        well for col in plate.cols('A', to='D') for well in col('3', to='6')
        ]
    p10.transfer(10, petri_1_source, petri_1)

    # Define petri_2_source as C5-F8
    petri_2_source = [
        well for col in plate.cols('A', to='D') for well in col('5', to='8')
        ]
    p10.transfer(10, petri_2_source, petri_2)
