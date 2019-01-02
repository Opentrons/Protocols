# PCR Prep Using CSV Input

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * PCR

## Description
With this protocol, your robot can consolidate samples from 5 source plates into a single 96-well output plate based on a CSV input. Two master mixes located in the last two columns of the output plate will be distributed to all of the wells. See Additional Notes for information on the CSV layout.

---

For this protocol, you will need:
* P10 Single-channel Pipette
* P10 Multi-channel Pipette
* 96-well Plates
* [Temperature Module](https://shop.opentrons.com/products/tempdeck)
* 10 uL Tip Racks


### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the desired temperature of the Temperature Module throughout the protocol.
2. Input the volume of each sample to be transferred.
3. Input the volume of the master mix to be transferred into each well.
4. Upload your CSV file.
5. Download your protocol.
6. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
7. Set up your deck according to the deck map.
8. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
9. Hit "Run".
10. Temperature Module will be set to and maintained at desired temperature.
11. Robot will consolidate to samples from source plates to output plate on Temperature Module using the single-channel pipette.
12. Robot will distribute master mixes to all of the consolidated wells using the multi-channel pipette.


### Additional Notes
CSV Layout

![csv_layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1441-cellectis/csv_layout.png)

* Keep headers
* Destination wells must be within A1 - H10
* Plate_1: source plate in slot 1
* Plate_2: source plate in slot 2
* Plate_3: source plate in slot 3
* Plate_4: source plate in slot 4
* Plate_5: source plate in slot 5

---

Master Mix Setup in Plate in slot 6
* Master Mix 1: column 11 (A11-H11)
* Master Mix 2: column 12 (A12-H12)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
Z5h9YbPk
1441
