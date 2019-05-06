# ProA ELISA 2/2: ELISA Assay

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * ELISA

## Description
Links:
* [Part 1: Sample Dilution](./1556-part1)
* [Part 2: ELISA Assay](./1556-part2)

This the second part of the ProA ELISA protocol: ELISA Assay. The robot will add denaturing buffer to the STP plate created in part 1. After 10 minutes of incubation, robot will add Enzyme Conjugate Reagent to an output plate in slot 9. Robot will transfer contents in the STP plate to the output plate. User will cover the output plate with parafilm and transfer the plate to a shaker and incubate for 1 hours at room temperature. After the plate has been washed for 4 time, user will replace the plate in slot 9. Robot will then add TMB substrate and stop solution before ending the protocol.

---

You will need:
* P300 Single-channel Pipette
* P1000 Single-channel Pipette
* 96-well Plate
* Trough 12-row
* 1000 uL Tip Rack
* 300 uL Tip Rack


### Robot
* [OT-2](https://opentrons.com/ot-2)


## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".


### Additional Notes
Trough Setup: (slot 8)
* Denaturing Buffer: A1
* Enzyme Conjugated Antibody: A2
* TMB Subtrate: A3
* Stop Solution: A4

---
96-well Plate Layout:
![layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1556/plate_layout.png)

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
cSWp6GcV
1556
