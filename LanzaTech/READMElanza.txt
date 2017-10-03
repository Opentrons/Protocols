README

In a code text editor, such as Sublime Text (https://www.sublimetext.com/3), open the .py file for your protocol. 

Near the top of the file, locate the variable(s):

# primer set 1 and 2 or 3 and 4: 
# for primers 1 and 2, set to True, for primers 3 and 4, set to False
firstset = True  # can change here

# for filling half plate set to True, for filling a full plate for each primer set to False
halfplate = True  # can change here

# ingredient volumes
primervol = 1  # can change here
watervol = 7  # can change here
mixvol = 10  # can change here
tempvol = 2  # can change here

# source of reagents
reagents = containers.load('tube-rack-2ml', 'A3')
templates = containers.load('96-PCR-flat', 'D1')

# ingredient locations
water_loc = reagents.wells('A1')  # can change here
primer1_loc = reagents.wells('B1')  # can change here
primer2_loc = reagents.wells('C1')  # can change here
primer3_loc = reagents.wells('D1')  # can change here
primer4_loc = reagents.wells('A2')  # can change here
premix_loc = reagents.wells('B2')  # can change here
template_loc = templates.rows(0)  # can change here

 and change the variable(s) to the desired value(s) where there is some variation of "#change here", making sure to follow any specific directions if applicable.

Once you have changed all the necessary values, save the file and you will be ready to run your protocol per Opentrons' instructions.

