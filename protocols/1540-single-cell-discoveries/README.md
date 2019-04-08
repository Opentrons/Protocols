# NGS Library Preparation

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * NGS Library Prep

## Description
This protocol performs NGS library preparation for up to 96 samples. The protocol allows for selected columns of a 96-well plate to undergo the preparation process.

---

You will need:
* [96-Well PCR Plates](https://www.thermofisher.com/order/catalog/product/AB2396B)
* [12-Row Trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [P10 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [P300 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

### Reagents
* [Beckman Coulter Ampure XP beads for DNA cleanup](https://www.beckman.com/reagents/genomic/cleanup-and-size-selection/pcr/a63881)

## Process
1. Edit the customizable fields for your protocol.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The Ampure beads are mixed thoroughly and transferred to each of the selected sample columns. The destination is mixed after each transfer, and a new tip is used for each transfer.
8. The samples incubate at room temperature for 15 minutes.
9. The module engages and the samples incubate for 5 minutes or until the sample liquid is clear.
10. Supernatant is carefully removed from each sample well ensuring that the pipette tip does not touch the beads.
11. The pellets are immediately washed with 200µl of 80% EtOH after the supernatant is removed. After 30 seconds, the EtOH is removed.
12. Step 11 is repeated for as many times as specified.
13. The protocol pauses for the beads to dry completely.
14. Each sample is resuspended in water and mixed thoroughly.
15. The protocol pauses for the samples to incubate at room temperature for 2 minutes.
16. The module engages and the samples incubate for 5 minutes or until the sample liquid is clear.
17. Supernatant is transferred to a new 96-well plate.

### Additional Notes
![Trough Reagent Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1540-single-cell-discoveries/trough_reagent_setup.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
Jm1695SW  
1540
