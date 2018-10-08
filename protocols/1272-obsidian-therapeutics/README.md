# Meso Scale Discovery Proinflammatory Panel 1 (human) Kit Assay

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
With this protocol, your robot can perform the [MSD cytokine](https://www.mesoscale.com/~/media/files/product%20inserts/proinflammatory%20panel%201%20human%20insert.pdf) assays and other similar assays using a p300 multi-channel and p50 single-channel pipettes.

### Robot
* [OT 2](https://opentrons.com/ot-2)

### Reagents
* [V-PLEX Human IL-12p70 Kit](https://www.mesoscale.com/products/v-plex-human-il-12p70-kit-k151qvd/)

## Process
1. Input your desired reagent container type.
2. Input your desired number of samples (max = 37).
3. Download your protocol.
4. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "Run".
8. Robot will wash plate 3 times with 150 uL/well of wash buffer.
9. Robot will add 50 uL samples, calibrators, and controls to the plate.
10. Robot will pause for user to seal plate and place on shaker.
11. Robot will wash plate 3 times with 150 uL/well of wash buffer.
12. Robot will add 25 uL of detection antibody to each well.
13. Robot will pause for user to seal plate and plate on shaker.
14. Robot will wash plate 3 times with 150 uL/well of wash buffer.
15. Robot will add 150 uL of 2X read buffer T to each well.

### Additional Notes
* Reagent container setup (slot 1):
    * Wash Buffer: column 1-9
    * Buffer T: column 12


* Source plate layout (slot 5):  
    * ![source plate layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1272-obsidian-therapeutics/source_plate_layout.png)


* Output plate layout (slot 2):  
    * ![output plate layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1272-obsidian-therapeutics/output_plate_layout.png)

* Refer to the [kit manual](https://www.mesoscale.com/~/media/files/product%20inserts/proinflammatory%20panel%201%20human%20insert.pdf) to make sure you have all the equipment and consumables needed for this protocol.

###### Internal
aGygEBof
1272
