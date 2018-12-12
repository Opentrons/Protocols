# MDA Sample Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * PCR

## Description
Using this protocol, your robot can transfer solutions from 1.7 mL tubes from the Temperature Module as well as the [4-in-1 Tube Rack Set] to PCR strips. You could change the aspirate and dispense speed during mixing, so to not disturb the DNA samples. This protocol requires a P10 single-channel and P10 multi-channel pipette, [Temperature Module](https://shop.opentrons.com/products/tempdeck), [4-in-1 Tube Rack Set](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1), and [Aluminum Block Set](https://shop.opentrons.com/products/aluminum-block-set).

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Temperature Module](https://shop.opentrons.com/products/tempdeck)

### Reagents

## Process
1. Input your desired aspirate and dispense speed (UNIT: uL/sec; DEFAULT: aspirate=5, dispense=10).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer and mix 5 uL Exo-Res random primers from Temperature Module to samples using P10 single-channel pipette.
8. Robot will pause for 5 minutes.
9. Robot will transfer samples to reaction tubes using P10 multi-channel pipette.
10. Robot will transfer and mix 2 uL D1 from tube rack to reaction tubes using P10 single-channel pipette.
11. Robot will pause for 3 minutes 30 seconds.
12. Robot will transfer and mix 4 uL neutralization buffer from Temperature Module to reaction tubes using P10 single-channel pipette.
13. Robot will transfer and mix 6 uL master mix to reaction tubes using P10 single-channel pipette.

### Additional Notes
2 mL Tube Rack (slot 1):
* D1: A1

---

PCR Strips + 96-well Aluminum Block (slot 2):
* Samples: column 1
* Reaction Tubes: column 2

---

Temperature Module + 2 mL Aluminum Block (slot 4):
* Master Mix: A1
* Exo-Res Random Primers: B1
* Neutralization Buffer: C1

---
We recommend placing water between aluminum thermal blocks and plastic tubes to allow for more consistent heating and cooling. Read more on our Temperature Module white paper [here](https://s3.amazonaws.com/opentrons-landing-img/modules/temperature/Opentrons.Temperature.Module.White.Paper.pdf).

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
xzUCIClg
1440
