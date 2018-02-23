from opentrons import containers, instruments

bead_plate = containers.load('96-PCR-flat', '4', 'bead_plate')
spin_plate = containers.load('96-PCR-flat', '5', 'spin_plate')
collection1mL_1 = containers.load('96-PCR-flat', '6', 'collection1mL_1')
collection1mL_2 = containers.load('96-PCR-flat', '7', 'collection1mL_2')
collection1mL_3 = containers.load('96-PCR-flat', '8', 'collection1mL_3')
collection1mL_4 = containers.load('96-PCR-flat', '9', 'collection1mL_4')
collection2mL_1 = containers.load('96-PCR-flat', '10', 'collection2mL_1')

trough = containers.load('trough-12row', '11', 'trough')

m300rack1 = containers.load('tiprack-200ul', '1', 'm300rack1')
m300rack2 = containers.load('tiprack-200ul', '2', 'm300rack2')
m300rack3 = containers.load('tiprack-200ul', '3', 'm300rack3')

m300 = instruments.P300_Multi(
    tip_racks=[m300rack1, m300rack2, m300rack3],
    mount='left',
)

ethanol = trough.cols('1')
bead_solution = trough.cols('2')
C1 = trough.cols('3')
C2 = trough.cols('4')
C3 = trough.cols('5')
C4 = trough.cols('6')
C5_D = trough.cols('7')
C6 = trough.cols('8')

supernatantvol = 100

# VACUUM & CENTRIFUGATION:

# Prepare C5-D by adding equal amounts of ehtanol and mix.
m300.transfer(120, ethanol, C5_D, mix_after=(3, 120))

# Remove mat from bead plate and add 0.25 grams of soil sample to bead plate.

# Transfer 750uL of bead solution to bead plate
m300.transfer(750, bead_solution, bead_plate.cols('1', to='12'))

# Transfer 60uL of C1 to bead plate and secure with mat.
m300.transfer(60, C1, bead_plate.cols('1', to='12'))

# Place bead plate between adapter plates and place on shaker.
# Shake at speed 20 for 10 minutes, turn and repeat.
# Centrifuge at room temperature for 6 minutes at 4500 x g.
# Remove bead plate from centrifuge and remove mat.

# Transfer supernatant to clean 1mL collection plate.
m300.transfer(
    supernatantvol,
    bead_plate.cols('1', to='12'),
    collection1mL_1.cols('1', to='12'))

# Transfer 250uL of C2 to each well and apply sealing tape.
# Vortex for 5 seconds.
m300.transfer(250, C2, collection1mL_1.cols('1', to='12'))

# Incubate at 4C for 10 minutes.
# Centrifuge collection1mL_1 at room temperature for 6 mins at 4500 x g.
# Remove and discard sealing tape.

# Transfer supernatant from collection1mL_1 to new collection1mL_2.
# Apply sealing tape.
m300.transfer(
    supernatantvol,
    collection1mL_1.cols('1', to='12'),
    collection1mL_2.cols('1', to='12'))

# Centrifuge at room temperature for 6 minutes at 4500 x g.

# Transfer supernatant from collection1mL_2 to new collection1mL_3.
m300.transfer(
    supernatantvol,
    collection1mL_2.cols('1', to='12'),
    collection1mL_3.cols('1', to='12'))

# Transfer 200uL of C3 and apply sealing tape to collection1mL_3.
# Vortex for 5 seconds.
m300.transfer(200, C3, collection1mL_3.cols('1', to='12'))

# Incubate at 4C for 10 minutes.
# Centrifuge collection1mL_3 at room temperature for 6 minutes at 4500 x g.
# Remove and discard sealing tape.

# Transfer supernatant from collection1mL_3 to new collection1mL_4.
m300.transfer(
    supernatantvol,
    collection1mL_3.cols('1', to='12'),
    collection1mL_4.cols('1', to='12'))

# Apply sealing tape and centrifuge at room temperature
# for 6 minutes at 4500 x g.

# Transfer no more than 650uL of supernatant to new 2mL collection plate.
m300.transfer(
    650,
    collection1mL_4.cols('1', to='12'),
    collection2mL_1.cols('1', to='12'))

# Transfer 650uL of C4 to collection2mL_1
# and add a second 650uL of C4 to collection2mL_1.
for _ in range(2):
    m300.transfer(650, C4, collection2mL_1.cols('1', to='12'))

# Remove top portion of vacuum manifold and place new 2mL collection plate
# in bottom of vacuum manifold.
# Replace top of manifold and place spin plate on top of manifold.
# Turn vacuum on. Make sure there is a good seal with manifold and spin plate.

# Mix collection2mL_1.
m300.pick_up_tip()
for i in range(12):
    m300.mix(5, 300, collection2mL_1.cols(i))
m300.drop_tip()

# Load 650uL of samples into wells of spin plate
# until entire volume of each sample is processed.
for i in range(6):
    m300.transfer(650, trough.cols(i + 2), spin_plate.cols('1', to='12'))

# Turn off vacuum.

# Remove spin plate from manifold and set aside.
# Discard flow through from 2mL collection plate in bottom
# and place it back in manifold.
# Reassemble manifold with spin plate on top and turn vacuum on. Test seal.

# Add 500uL of C5 to each well of spin plate. Turn off vacuum
# after entire volume has passed.
m300.transfer(500, C5_D, spin_plate.cols('1', to='12'))

# Apply centrifuge tape to spin plate to cover all wells.
# Place 0.5 collection plate under spin plate.
# Centrifuge at room temperature for 6 minutes at 4500 x g.
# Place spin plate on microplate. Remove centrifuge tape and discard.
# Air dry for 10 minutes at room temperature.

# Add 100uL of C6 to center of each well of spin plate
# and apply centrifuge tape.
m300.transfer(100, C6, spin_plate.cols('1', to='12'))

# Centrifuge at room temperature for 3 minutes at 4500 x g.
# Remove tape and discard.
# Cover wells of microplate with elution sealing mat.
# Store DNA fozen (-20 to -80 C).
