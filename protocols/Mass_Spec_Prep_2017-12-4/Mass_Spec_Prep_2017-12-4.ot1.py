from opentrons import containers, instruments
from collections import defaultdict
from otcustomizers import FileInput, StringSelection

"""
Column A
"""
trough = containers.load('trough-12row', 'A1')
single_tip = containers.load('tiprack-200ul', 'A2', 'Single Tips')
"""
Column B
"""
multi_tip = containers.load('tiprack-200ul', 'B1', 'Multi Tips')
"""
Column C
"""
plate96 = containers.load('96-deep-well', 'C1')
plate384 = containers.load('384-plate', 'C1')

tuberack = containers.load('tube-rack-15_50ml', 'C2')

"""
Column D
"""
liquid_trash = containers.load('trash-box', 'D2', 'Liquid Trash')
trash = containers.load('trash-box', 'D1', 'Tip Trash')
"""
Instruments
"""
p300multi = instruments.Pipette(
    axis='a',
    name='p300multi',
    max_volume=300,
    min_volume=50,
    channels=8,
    tip_racks=[multi_tip])

p100single = instruments.Pipette(
    axis='b',
    name='p100single',
    max_volume=100,
    min_volume=10,
    channels=1,
    tip_racks=[single_tip])

"""
Reagents/variable initialization
"""
reagent1 = trough.wells('A1')
reagent2 = trough.wells('A2')
reagent3 = trough.wells('A3')
reagent4 = trough.wells('A4')


"""
Sample Number (Range) for customization: 96-384 (Handled within CSV)
"""
volume_example = """
    50,50,50,50,50,50,50,50
    50,50,50,50,50,50,50,50
    50,50,50,50,50,50,50,50
    50,50,50,50,50,50,50,50
    50,50,50,50,50,50,50,50
    50,50,50,50,50,50,50,50
    50,50,50,50,50,50,50,50
    50,50,50,50,50,50,50,50
    50,50,50,50,50,50,50,50
    50,50,50,50,50,50,50,50
    50,50,50,50,50,50,50,50
    50,50,50,50,50,50,50,50
    """

source_example = """
    A,B,C
    D,E,F
    G,H,
    I,J,
    """
destination_example = """
    A,,,,,H,
    ,A,,,,H,
    ,,,,,H,E
    ,,,A,,,,
    ,,,,,,,,
    ,A,,,,,E
    ,,G,,,,,
    ,A,G,E,E
    ,,,,,,,,
    ,,G,,,,,
    ,,G,,,,,
    ,,,,,,H,
"""


def run_custom_protocol(volumes_csv: FileInput=volume_example,
                        source_csv: FileInput=source_example,
                        destination_csv: FileInput=destination_example,
                        plate_type:
                            StringSelection('96-flat', '384-flat')='96-flat'):

    """
    Helper Functions
    """

    def prewet_tip(pipette):
        pipette.move_to((reagent1, reagent1.from_center(x=0, y=0, z=-1)))

    def wash(pipette):
        for _ in range(3):
            pipette.transfer(
                pipette.max_volume,
                reagent2,
                liquid_trash,
                new_tip='never')

    """
    Check which plate you are using
    """
    plate = plate384
    if plate_type == '96-flat':
        plate = plate96

    """
    Turns files into dictionaries for volume,
    sources, destinations respectively

    Create vols dict mapping well number on the destination plate to volume
    to transfer to that well. The vols dict is of the form:
    {well_number: volume}
    """
    vols = dict()
    temp_lines = []
    for row in volumes_csv.split('\n'):
        # parse through each row of the CSV
        if row:
            # check if that row is not empty
            temp_lines.append(row.split(','))
    for col in range(len(temp_lines)):
        # Starting with the column
        row_len = len(temp_lines[col])
        for well in range(len(temp_lines[col])):
            # Now loop through each invidiual cell
            try:
                # Add a key based on the cell in excel
                # Each cell row corresponds to a row on the
                vols[col + well*row_len] = float(temp_lines[col][well])
            except (ValueError, TypeError):
                vols[col + well*row_len] = 0

    """
    Create source dict mapping well number on the source plate to location
    of sample. The source dict is of the form:
    {sample: well_number}
    """
    sources = defaultdict(list)
    temp_lines = []
    for row in source_csv.split('\n'):
        if row:
            temp_lines.append(row.split(','))
    for col in range(len(temp_lines)):
        row_len = len(temp_lines[col])
        for well in range(len(temp_lines[col])):

            sources[temp_lines[col][well].strip()].append(well + col*row_len)

    """
    Create destination dict mapping well number on the destination plate to
    which sample is in that well. The destination dict is of the form:
    {sample: [well_number1, well_number2 etc...]}
    """
    dest_keys = []
    dest = defaultdict(list)
    temp_lines = []
    for row in destination_csv.split('\n'):
        if row:
            temp_lines.append(row.split(','))

    for col in range(len(temp_lines)):
        for well in range(len(temp_lines[col])):
            dest_keys = dest_keys + list(temp_lines[col][well].strip())
            row_len = len(temp_lines[col])
            dest[temp_lines[col][well].strip()].append(col + well*row_len)

    dest_keys = list(set(dest_keys))  # This grabs only unique keys
    if not '' not in dest_keys:
        dest_keys.remove('')  # gets rid of whitespace key

    """
    Part A: Get samples from variously-sized containers
    into a deep (2.2 mL) 96 well plate:
    Step A1:	Take clean pipette tip for p100 (single channel)
    and move to reagent 1 in the trough; ‘dunk’
    the tip fully in the trough (but don’t take up anything)
    to remove any external particles
    Step A2:	Move to reagent 2 (also in trough) and
    uptake full volume of tip and dispense
    to waste; repeat this step three times.
    Step A3:	Take up between 20→100 uL of a sample
    (located in 15 or 50 mL tube rack)
    and dispense into the appropriate position in the 96 well plate
    Step A4:	Discard pipette tip after sample is transferred
    """
    for sample in dest_keys:
        p100single.pick_up_tip()

        prewet_tip(p100single)

        wash(p100single)

        destination = dest[sample]

        volumes = [vols[i] for i in destination]

        p100single.distribute(
            volumes,
            tuberack.wells(sources[sample]),
            plate.wells(destination),
            new_tip='never')

        p100single.drop_tip()

    """
    Part B: Dilute each sample up to 1,900 uL using a clean tip
    Step B5:	Take clean pipette tips for multi-channel
    p300 and move to reagent 1 in the trough;
    ‘dunk’ fully in the trough (but don’t take up anything)
    to remove any external particles
    Step B6:	Move to reagent 2 (also in trough) and
    uptake full volume of tip and dispense to waste;
    repeat this step three times
    Step B7:	Move to reagent 3 in the trough,
    uptake 300 uL and add to each sample;
    repeat six times so each sample has 1,800 uL of reagent 3.

    Note that, for samples that were <100 uL,
    the volume will be less than 1,900 uL,
    and so we’ll need to go back with the
    p100 (single channel) to dilute these
    samples with the correct amount of reagent 3.
    The exterior and interior tip cleaning
    procedure is the same as in steps A1 & A2.
    """
    for sample in dest_keys:
        p300multi.pick_up_tip()

        prewet_tip(p300multi)

        wash(p300multi)

        destination = dest[sample]
        for well in destination:
            volume = 0
            if vols[well] > 0:
                volume = 1900-vols[well]

            p300multi.distribute(
                volume,
                reagent3,
                plate.wells(well),
                new_tip='never')
            if volume > 1800:
                p100single.pick_up_tip()
                prewet_tip(p100single)
                wash(p100single)

                p100single.transfer(volume-1800, reagent3, plate.wells(well))
                p100single.drop_tip()

        p300multi.drop_tip()

    """
    Part C: Add 100 uL internal standard to each sample and homogenize
    Step C8:	Using the p300 (multi-channel),
    clean a set of 200 uL tips as per steps B5
    and B6 above (‘dunk’ in reagent 1; rinse with reagent 2)
    Step C9:	Take 100 uL of internal standard (reagent 4)
    from a separate trough and dispense into the bottom of each sample
    Step C10:	Dispense up and down a few times in each sample
    to mix/homogenize before withdrawing; discard pipette tips after this

    Repeat steps C8→C10 for each row of the well plate that contains samples.
    """
    for row in range(len(dest_keys)):

        p300multi.pick_up_tip()
        prewet_tip(p300multi)

        wash(p300multi)

        destination = dest[sample]
        p300multi.transfer(100, reagent4, plate.rows(row), new_tip='never')

        p300multi.drop_tip()
