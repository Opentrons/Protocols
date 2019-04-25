# NGS Library Prep - BP Post Index 1

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * NGS Library Prep

## Description
This protocol performs BP Post Index 1 on a ThermoFisher 96-well MicroAmp EnduraPlate mounted on a magnetic deck. The user can select parameters such that this protocol fulfills parts 5uL D700 1, 5uL D700 2, and 5uL D700 3 (parts 6, 7, and 8, respectively) of the NGS prep.

---

You will need:
* [P300 8-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [P300 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)
* [TipOne 200ul Filter Tips #1120-8810](https://www.usascientific.com/200ul-tipone-filtertip.aspx)
* [ThermoFisher 96-Well MicroAmp EnduraPlate #4483348](https://www.thermofisher.com/order/catalog/product/4483348)
* [Opentrons 4-in-1 Tube Rack Set](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* 2ml Eppendorf Tube
* 15ml Falcon Tube
* 96 200µl PCR Strips

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

## Process
1. Input the beads strip column and the empty strip start column for elution (2 adjacent columns total). Ensure the PCR plate is mounted on the magnetic deck before running.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. 40.6ul of beads in a specified PCR strip are transferred to each of the first 3 columns of a PCR plate mounted on the magnetic deck (already containing samples). The contents of each destination well are mixed 8x after each transfer, and new tips are used for each transfer.
8. The first pooling is performed by transferring 91.4ul of one well to its corresponding pooling well. See 'Additional Notes' below for the transfer scheme. New tips used for each transfer, and tips are returned for future use.
9. Pools 7-12 are moved to the wells directly after pool 6 as shown in 'Additional Notes' below.
10. Samples incubate for 5 minutes.
11. The magnetic deck engages, and the protocol delays 10 minutes for beads separate out.
10. 182.8ul of supernatant is removed to the trash from each pool using its corresponding tip from step 8. Tips are returned for future use.
11. 200ul of ethanol is transferred from the 15ml tube to to each of the 12 pools. A height tracker is used to ensure the pipette does not submerge in the ethanol. The tip is returned for future use.
12. The protocol delays 30 seconds for the pools to incubate
13. 200ul of ethanol is removed to the trash from each pool using its corresponding tip from step 8. Tips are returned for future use.
14. Steps 11-13 are repeated 2x more for a total of 3 ethanol washes.
15. The protocol delays 8 minutes for the pellets to dry.
16. The magnetic deck disengages, and 50.5ul of TE is distributed to the top of each pool to avoid contamination.
17. The protocol delays 2 minutes for the samples to incubate.
18. The magnetic deck engages, and the protocol delays 5 minutes for the beads to separate out.
19. 50ul of elution from pools 1-8 are transferred to the specified first elution strip. 50ul of elution from pools 9-12 are transferred to the first 4 wells of the next elution strip. Corresponding tips from step 8 are used and discarded after each transfer.

### Additional Notes
If you have any questions about this protocol, please contact protocols@opentrons.com.

Original plate Setup
![Original Plate Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1549-wu-lab-univerity-of-pennsylvania-bp-post-index-1/initial_setup.png)

Initial Pooling Result
![Initial Pooling Result](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1549-wu-lab-univerity-of-pennsylvania-bp-post-index-1/first_pool.png)

Final Pooling Result
![Final Pooling Result 1](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1549-wu-lab-univerity-of-pennsylvania-bp-post-index-1/second_pool_1.jpeg)
![Final Pooling Result 1](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1549-wu-lab-univerity-of-pennsylvania-bp-post-index-1/second_pool_2.jpeg)

###### Internal
Yp5gMvur  
1549
