# NEBNext Direct® Genotyping Solution 2/4: Streptavidin Bead Preparation

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* NGS Library Prep
    * NEBNext Direct® Genotyping Solution Panels

## Description
Links:
* [Part 1: Sample Prep Kit and Hybridization](./1553-part1)
* [Part 2: Streptavidin Bead Preparation](./1553-part2)
* [Part 3: Bead Binding, Ligation, and Amplification](./1553-part3)
* [Part 4: Purify and Size Select Amplified Fragments](./1553-part4)

With this protocol, your robot is capable to perform the NEBNext Direct® Genotyping Solution Panels protocol, as described by the New England BioLabs Instructional Manual.

This is part 2 of the protocol, which completes (1.7.) Streptavidin Bead Preparation.

Make sure to review the instructional manual before proceeding to confirm kit contents and make sure you have the required equipment and consumables. See Additional Notes below for reagent setup and more details about this protocol.

You will need to equilibrate the Streptavidin beads to room temperature for ~15 minutes and vortex to resuspend before the start of the protocol. Once part 1 and part 2 are complete, you can safely move on to part 3 of the protocol.


---

You will need:
* P300 Single-channel Pipette
* [Magnetic Module](https://shop.opentrons.com/products/magdeck)
* FrameStar Skirted 96-well PCR Plate
* [4-in-1 Tube Rack Set](https://shop.opentrons.com/products/tube-rack-set-1)
* Opentrons 300 uL Tip Racks

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the desired engage height for your Magnetic Module. (see Additional Notes below)
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".


### Additional Notes
Reagent Setup:

![reagents](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1553/part2-reagent.png)

---

Deck Setup:

* Follow Deck Config 1 to set up your deck before the start of the protocol. Throughout the protocol, the deck configurations may change when protocol is paused. Make sure to read the instructions on the OT App to see which configuration to follow.

![deck](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1553/part2-deck.png)

---

Engage Height:

* You might need to modify the Magnetic Module engage height based on the labware you are placing on top. To find the right engage height for your labware, plug the Magnetic Module in the robot, and place the labware on the module. [Download](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1553/test_mag_module_engage_height.py) and run this script. You can skip calibration and go directly to "RUN". If the engage height (default: 14.94 mm) is too high or too low, feel free to adjust the number in line 8 in the script. Re-run the script with thew new engage height until you find the perfect height for your labware. You can then modify the Magnetic Module engage height for your protocol in the input field above before downloading your protocol.

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
eTlJ11jO
1553
