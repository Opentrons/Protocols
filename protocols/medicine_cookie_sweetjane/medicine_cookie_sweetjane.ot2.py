from opentrons import instruments, labware
from opentrons.data_storage import database

# CUSTOMIZATION
volume = 300  # medicine per cookie in microliters (uL) (5 to 300 uL)
# this will also determine whether you need to use the p300 or p50 pipette
number_cookies = 18  # number of cookies you want to process (1 to 18 cookies)
height_below_top = 20  # height below top of container that...
# ...you want to aspirate liquid from (in millimeters)

# LABWARE SETUP
tips = labware.load('tiprack-200ul', '10')
medicine = labware.load('trough-1row-25ml', '11')  # on temperature module
# get all remaining empty containers
empty_slots = [slot.get_name() for slot in
               robot.deck if len(slot.children_by_name) == 0]
# create custom cookie holder container
if 'cookie-holder-1' not in database.list_all_containers():
    labware.create('cookie-holder-1',
                   grid=(1, 2),
                   spacing=(0, 63),
                   diameter=53,
                   depth=1)
# make a list of all the cookie holder containers
holders = [labware.load('cookie-holder-1', slot) for slot in empty_slots]

# INSTRUMENT SETUP
if volume <= 50:
    pip = instruments.P50_Single(
        mount='right',
        tip_racks=[tips])
else:
    pip = instruments.P300_Single(
        mount='right',
        tip_racks=[tips])

# VARIABLES AND REAGENTS SETUP
# for every cookie in every cookie holder, add designated volume of medicine
total = 0
pip.pick_up_tip()
for cookie_holder in holders:
    for cookie in cookie_holder:
        if total < number_cookies:
            pip.transfer(volume, medicine.wells(0),
                         cookie.top(-height_below_top), new_tip='never')
            total = total + 1
        else:
            break
pip.drop_tip()
