# Protein crystallization screens: Tubes to Blocks

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * Protein Crystallography

## Description
This protocol allows your robot to transfer 96 tubes containing screen solution to six deep-well blocks.

---

You will need:
* P1000 Single-channel Pipette
* 13 mL Tubes
* Custom 13 mL Tube Racks
* Starlab Deep Well Blocks
* 1000 uL Tip Rack

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
6. Robot will transfer 750 uL of solution from well A1 tube rack in slot 10 to A1 of all of the deep well blocks.
7. Robot will repeat step 6 so that 1500 uL solution is transferred to each destination well.
8. Robot will follow steps 6-7 for each tube so that each 96-well block will contain 1500 uL from each tube.


### Additional Notes
Tube Racks Setup:

![layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1525-university-of-manchester/tuberack_layout.png)

---


If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
Lda5mQV1
1525
