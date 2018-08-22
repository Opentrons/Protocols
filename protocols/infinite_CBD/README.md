# Capsule Filling

### Author
[Opentrons](https://opentrons.com/)

### Partner

## Categories
* Industry
    * Capsule Filling


## Description
With this protocol, your robot can fill 96 well plates with "00" capsules, with reagent stored in 50mL tubes using a single pipette tip.

### Robot
* [OT 2](https://opentrons.com/ot-2)

### Reagents
* ["00" Capsules](https://www.capsuline.com/empty-capsule-size-chart/)

## Process
Off Robot
1. Load the plates of empty capsules into the plates to be filled.
2. Slightly overfill eight 50 mL tubes with reagents and place them in the 15-50 mL tube racks.

Download and Run
1. Input your desired fill volume in the field above.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Transfer desired volume of reagent from 50 mL tubes to each capsule, until all eight plates of capsules are filled.


### Additional Notes
* After every run of the protocol, you will have to replace all the capsule plates with new plates and refill all of the tubes in the 2 tube racks.
* Overfill the 50 mL tubes slightly, each tube needs about 51 ml for the protocol to work correctly for every capsule.
* The protocol runs on 8 plates at a time.
* Make sure the tip rack is reset every time as the robot starts over on the tip rack each time the protocol is run.
* An air gap is performed after every aspirate to prevent reagent from dripping.

###### Internal
vN6FbPq8
1123
