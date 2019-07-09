from opentrons import labware, instruments, robot
from otcustomizers import StringSelection, FileInput

metadata = {
    'protocolName': 'Cell Culture Assay Part 1: Overnight Culture Prep',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
culture_plate_24_name = 'Costar-culture-plate-24'
if culture_plate_24_name not in labware.list():
    labware.create(
        culture_plate_24_name,
        grid=(6, 4),
        spacing=(19.3, 19.3),
        diameter=16.26,
        depth=17.4,
        volume=3400
    )

reservoir_name = 'Axygen-290ml-reservoir'
if reservoir_name not in labware.list():
    labware.create(
        reservoir_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=8,
        depth=37,
        volume=290000
    )

# load labware
source_plate = labware.load(culture_plate_24_name, '1', 'source plate')
media_res = labware.load(reservoir_name, '2', 'media')
tips1000 = labware.load('tiprack-1000ul', '5')

# reagent setup
media = media_res.wells('A1')

# csv defaults
example1 = """,1,2,3,4
A,ycEW000_b3_ct in SC-URA,ycEW000_b4_ct in SC-URA,ycEW000_b3_rt in SC-URA,ycEW\
000_b4_rt in SC-URA
B,ycEW163_b3_ct in SC-URA,ycEW163_b4_ct in SC-URA,ycEW163_b3_rt in SC-URA,ycEW\
163_b4_rt in SC-URA
C,ycEW081_b3_ct in SC-URA,ycEW081_b4_ct in SC-URA,ycEW081_b3_rt in SC-URA,ycEW\
081_b4_rt in SC-URA
D,media,,,
,,,,
"""


def run_custom_protocol(
        overnight_contents_in_24_well_plate_csv: FileInput = example1,
        P1000_mount: StringSelection('right', 'left') = 'right'
):

    # instruments
    p1000 = instruments.P1000_Single(mount=P1000_mount, tip_racks=[tips1000])

    # initialize data storage dictionary
    all_data = {}
    row_names = 'ABCDEFGH'

    # parse overnight contents CSV
    overnight_data = [line.split(',')[1:]
                      for line in
                      overnight_contents_in_24_well_plate_csv.splitlines()
                      if line][1:]
    for r_ind, row in enumerate(overnight_data):
        for c_ind, culture in enumerate(row):
            if culture:
                well_name = row_names[r_ind] + str(c_ind+1)
                well = source_plate.wells(well_name)
                all_data[culture.strip()] = well

    # distribute media to specified wells of 24-well source plate
    p1000.pick_up_tip()
    for key in all_data:
        p1000.transfer(
            1000,
            media,
            all_data[key].top(),
            blow_out=True,
            new_tip='never'
        )
    p1000.drop_tip()

    robot.comment('Use sterile tips to pick 1 colony from the agar plate contain\
ing the strains and inoculate in the liquid media on the 24 well plate. Repeat\
 this step for all strains and biological replicates. Grow the strains on the \
24 well culture plates overnight at 30˚C on a shaking incubator set at 180 rpm\
. Resume to finish first protocol.')
