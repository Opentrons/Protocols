# High-Throughput Synthesis

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Cherrypicking


## Description
This protocol performs a custom cherrypicked high-throughput synthesis. It requires a CSV input for the mapping of the wells and vials on the tube racks. It also requires a CSV for high-throughput synthesis which contains the dispending volumes from each reservoir.

---

![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [P1000 single-channel GEN2 electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [P300 single-channel GEN2 electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons Tube Racks](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

* [Vial Map CSV Example](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/5191b6/vial_map.csv)
* [High-Throughput CSV Example](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/5191b6/htp.csv)

Deck Setup
* P1000 Tips (Slot 1)
* P300 Tips (Slot 2)
* NEST 12-well 15 mL reservoir (Slot 3)
* Opentrons Tube Racks (Use Vial Map CSV)

Example of the Vial Map CSV [Download Example](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/5191b6/vial_map.csv):
```
Well Number,Labware,Slot,Well Position
1,opentrons_24_tuberack_nest_2ml_screwcap,4,A1
2,opentrons_24_tuberack_nest_2ml_screwcap,4,A2
3,opentrons_24_tuberack_nest_2ml_screwcap,4,A3
...
96,opentrons_24_tuberack_nest_2ml_screwcap,7,D6
```

The Vial Map CSV can be used to place custom labware and different tube racks from the labware library. It also allows mapping of the well positions of each vial on a tube rack corresponding to the well number in the high-throughput synthesis protocol.

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Upload Vial Map CSV and High-Throughput Synthesis Protocol CSVs. Choose pipette tips, pipette mounts, and reservoir.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
5191b6
