# Multiple Sample Transfer

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Distribution

## Description
Your robot can transfer 32 samples from two 24-well plates in triplicate in a 96-well U-bottom plate. Three reagents will be distributed to each well of the 96-well plate between incubations. Lastly, a diluent from a 50 mL conical tube will be added to each well to complete the protocol.

---

You will need:
* P10 Single-channel Pipette
* P300 Single-channel Pipette
* 24-well Plates
* [Greiner Bio-One 96-well U-bottom Plate](https://shop.gbo.com/en/usa/products/bioscience/cell-culture-products/cellstar-cell-culture-microplates/96-well-cell-culture-microplates-clear/650185.html)
* [4-in-1 Tube Rack Set](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* 50 mL Conical Tube
* Opentrons Tips

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Robot transfer 2.5 uL of 32 samples from the 24-well plates in slot 4 and 5 to the 96-well plate.
7. Robot will add 3 uL of reagent 1 to each well.
8. Robot will pause for 10-minute incubation.
9. Robot will add 3 uL of reagent 2 to each well.
10. Robot will pause for 10-minute incubation.
11. Robot will add 3 uL of reagent 3 to each well.
12. Robot will pause for 30-minute incubation.
13. Robot will add 238.5 uL of diluent to each well.


### Additional Notes
![96-well plate layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1477-university-of-alberta/layout.png)

---

2 mL Tube Rack Setup:
* Reagent 1: A1
* Reagent 2: A2
* Reagent 3: A3

---

50 mL Tube Rack Setup:
* Buffer: A1

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
NM3RqA8O
1477
