from opentrons import containers, instruments

# Creating BioRad PCR plate
containers.create(
                 'BioRad_HSS9601',  # name of plate
                 grid=(8, 12),      # grid 8 columns x 12 rows, remember
                                    # the robot sees the plate in portrait
                 spacing=(9, 9),    # Distance between center of each well
                 diameter=5.5,      # Diameter at the top of teh well
                 depth=19.85)       # Internal depth of the well
"""
    Below are variables representing which primers to use and how much to use.
    @primer_set_1 Set to True if using primers 1 and 2
    @primer_set_2 Set to True if using primers 3 and 4
    @halfplate Set to True if you wish to have a half plate of primers
"""

primer_set_1 = True
primer_set_2 = True

halfplate = True

# ingredient volumes
primervol = 1  # can change here
watervol = 7  # can change here
mixvol = 10  # can change here
tempvol = 2  # can change here

# source of reagents
reagents = containers.load('tube-rack-2ml', 'A3')
templates = containers.load('BioRad_HSS9601', 'D1')

# ingredient locations
water_loc = reagents.wells('A1')  # can change here
primer1_loc = reagents.wells('B1')  # can change here
primer2_loc = reagents.wells('C1')  # can change here
primer3_loc = reagents.wells('D1')  # can change here
primer4_loc = reagents.wells('A2')  # can change here
premix_loc = reagents.wells('B2')  # can change here
template_loc = templates.rows(0)  # can change here

"""
    Below, plates are loaded on an as needed basis
    (whether or not you wish to do half or whole plates of primer combos)
    @wells_plate1_single Calls all wells in a plate to
    touch the bottom of the well for plate 1
    @wells_plate1_multi Calls all rows in a plate
    to touch the bottom for plate 1
    @wells_plate2_single Calls all wells in a plate to
    touch the bottom of the well for plate 2
    @wells_plate2_multi Calls all rows in a plate to touch
    the bottom for plate 2

    Do not change these variables. We will fix it
    for you if the pipette still doesn't touch the bottom
"""

plate1 = containers.load('BioRad_HSS9601', 'B1')
wells_plate1_single = [well.bottom() for row in plate1.rows() for well in row]

wells_plate1_multi = [well.bottom() for well in plate1.cols(0)]

if not halfplate:
    plate2 = containers.load('BioRad_HSS9601', 'C1')
    wells_plate2_single = [well.bottom()
                           for row in plate2.rows() for well in row]

    wells_plate2_multi = [well.bottom() for well in plate2.cols(0)]

# tip rack for p50 pipette
m200rack = containers.load('tiprack-200ul', 'C3')

# tip rack for p10 pipette
m10rack = containers.load('tiprack-10ul', 'E3')

# trash location
trash = containers.load('trash-box', 'B2')

p10multi = instruments.Pipette(
    trash_container=trash,
    name='p10multi',
    tip_racks=[m10rack],
    min_volume=1,
    max_volume=10,
    axis="a",
    channels=8
)

p50single = instruments.Pipette(
    trash_container=trash,
    name='p50single',
    tip_racks=[m200rack],
    min_volume=5,
    max_volume=50,
    axis="b",
    channels=1
)

"""
 PCR protocol. Steps:
 1. First fill plate 1 with water and pre-mixer to specified volumes
 2. Check if you want to fill both PCR plates with primer combos 1+2, 3+4
 3. If so, fill plate 2 with water and pre-mixer and
 check if using primer set 1 and/or 2
 4. If only doing half plate, skip filling plate 2
 and check if using primer set 1 and/or 2
 5. Distribute template to specified volume
"""

p50single.distribute(watervol, water_loc,
                     wells_plate1_single, disposal_vol=0, blowout=True)
p50single.distribute(mixvol, premix_loc,
                     wells_plate1_single, disposal_vol=0, blowout=True)

if not halfplate:
    p50single.distribute(watervol, water_loc,
                         wells_plate2_single, disposal_vol=0, blowout=True)
    p50single.distribute(mixvol, premix_loc,
                         wells_plate2_single, disposal_vol=0, blowout=True)
    if primer_set_1:
        p50single.distribute(primervol, primer1_loc,
                             wells_plate1_single, disposal_vol=0, blowout=True)
        p50single.distribute(primervol, primer2_loc,
                             wells_plate1_single, disposal_vol=0, blowout=True)
    if primer_set_2:
        p50single.distribute(primervol, primer3_loc,
                             wells_plate2_single, disposal_vol=0, blowout=True)
        p50single.distribute(primervol, primer4_loc,
                             wells_plate2_single, disposal_vol=0, blowout=True)

    p10multi.distribute(tempvol, template_loc,
                        wells_plate2_multi, disposal_vol=0, blowout=True)

if primer_set_1:
        p50single.distribute(primervol, primer1_loc,
                             wells_plate1_single[
                                                0:len(wells_plate1_single)//2],
                             disposal_vol=0, blowout=True)
        p50single.distribute(primervol, primer2_loc,
                             wells_plate1_single[
                                                0:len(wells_plate1_single)//2],
                             disposal_vol=0, blowout=True)

if primer_set_2:
        p50single.distribute(primervol, primer3_loc,
                             wells_plate1_single[
                                                len(wells_plate1_single) //
                                                2:len(wells_plate1_single)],
                             disposal_vol=0, blowout=True)
        p50single.distribute(primervol, primer4_loc,
                             wells_plate1_single[
                                                len(wells_plate1_single) //
                                                2:len(wells_plate1_single)],
                             disposal_vol=0, blowout=True)

p10multi.distribute(tempvol, template_loc, wells_plate1_multi,
                    disposal_vol=0, blowout=True)
