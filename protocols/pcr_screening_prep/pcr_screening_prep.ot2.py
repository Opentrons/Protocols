from opentrons import containers, instruments

# primer set 1 and 2 or 3 and 4:
# for primers 1 and 2, set to True, for primers 3 and 4, set to False
firstset = True  # can change here

# For filling half plate set to True,
# for filling a full plate for each primer set to False
halfplate = True  # can change here

# ingredient volumes
primervol = 1  # can change here
watervol = 7  # can change here
mixvol = 10  # can change here
tempvol = 2  # can change here

# source of reagents
reagents = containers.load('tube-rack-2ml', '3')
templates = containers.load('96-PCR-flat', '4')

# ingredient locations
water_loc = reagents.wells('A1')  # can change here
primer1_loc = reagents.wells('B1')  # can change here
primer2_loc = reagents.wells('C1')  # can change here
primer3_loc = reagents.wells('D1')  # can change here
primer4_loc = reagents.wells('A2')  # can change here
premix_loc = reagents.wells('B2')  # can change here
template_loc = templates.rows(0)  # can change here

# plate(s) setup will happen in
plate1 = containers.load('96-PCR-flat', '5')
plate2 = containers.load('96-PCR-flat', '6')

# tip rack for p50 pipette
m200rack = containers.load('tiprack-200ul', '1')

# tip rack for p10 pipette
m10rack = containers.load('tiprack-10ul', '2')

p10multi = instruments.P10_Multi(
    tip_racks=[m10rack],
    mount='right'
)

p50single = instruments.Pipette(
    name='p50single',
    tip_racks=[m200rack],
    min_volume=5,
    max_volume=50,
    mount='left',
    channels=1
)

# We need a protocol to set up for PCR screening of a large number of colonies
# in 96 well PCR plates.
# Work flow after picking colonies into 5-10 uL H2O would be,
# make master mix for either half plate of primer 1 and 2 with H2O and
# 2x KAPA HotStart do teh same with primers 3 and 4, dispense into
# the PCR plate. Add 2 ul of template from an other PCR plate.
# Same template from each half of the plates
# (so same templeate in A1 and A7 etc).
# If we could also have the option to expand this to filling a full plate with
# each primer set that would be great.
# Final volume would be 20ul (18 mix 2 template)

p50single.distribute(
    watervol,
    water_loc,
    plate1.cols(),
    disposal_vol=0,
    blowout=True)
if not halfplate:
    p50single.distribute(
        watervol,
        water_loc,
        plate2.cols(),
        disposal_vol=0,
        blowout=True)

p50single.distribute(
    mixvol,
    premix_loc,
    plate1.cols(),
    disposal_vol=0,
    blowout=True)
if not halfplate:
    p50single.distribute(
        mixvol,
        premix_loc,
        plate2.cols(),
        disposal_vol=0,
        blowout=True)

if firstset:
    if halfplate:
        p50single.distribute(
            primervol,
            primer1_loc,
            plate1.cols(0, to=6),
            disposal_vol=0,
            blowout=True)
        p50single.distribute(
            primervol,
            primer2_loc,
            plate1.cols(6, to=12),
            disposal_vol=0,
            blowout=True)
    else:
        p50single.distribute(
            primervol,
            primer1_loc,
            plate1.cols(),
            disposal_vol=0,
            blowout=True)
        p50single.distribute(
            primervol,
            primer2_loc,
            plate2.cols(),
            disposal_vol=0,
            blowout=True)
else:
    if halfplate:
        p50single.distribute(
            primervol,
            primer3_loc,
            plate1.cols(0, to=6),
            disposal_vol=0,
            blowout=True)
        p50single.distribute(
            primervol,
            primer4_loc,
            plate1.cols(6, to=12),
            disposal_vol=0,
            blowout=True)
    else:
        p50single.distribute(
            primervol,
            primer3_loc,
            plate1.cols(),
            disposal_vol=0,
            blowout=True)
        p50single.distribute(
            primervol,
            primer4_loc,
            plate2.cols(),
            disposal_vol=0,
            blowout=True)

p10multi.distribute(
    tempvol,
    template_loc,
    plate1.cols(),
    disposal_vol=0,
    blowout=True)
if not halfplate:
    p10multi.distribute(
        tempvol,
        template_loc,
        plate2.cols(),
        disposal_vol=0,
        blowout=True)
