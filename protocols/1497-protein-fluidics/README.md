# Low Volume ELISA

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * ELISA

## Description
With this protocol, your robot can perform low volume ELISA prep on microfluidic chips that are in 384-well plate format. The source and volume in each well will be provided as a CSV input. See Additional Notes for more details on the required CSV format.

---

You will need:
* P50 Single-channel Pipette
* 96-well V-bottom Plate
* [4-in-1 Tube Rack Set](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* Microfluidic Chips
* 200 uL Tip Racks

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Upload your CSV file.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer reagents from either tube rack or 96-well plate to the microfluidic chip based on the CSV file. Same tip will be used to transfer the same reagent.


### Additional Notes
CSV Setup (24 columns x 16 rows):

![csv_layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1497-protein-fluidics/csv_layout.png)

* MUST be in this format: `SourceType-SourceWell;Volume`
* Source Type:
    * R: Tube Rack in slot 4
    * P: 96-well plate in slot 1
* Each cell represent each well in the 384-well plate format
* If you leave a cell empty, no reagent will be transferred to the corresponding well

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
nztfeFd5
1497
