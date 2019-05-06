# ProA ELISA 1/2: Sample Dilution

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * ELISA

## Description
Links:
* [Part 1: Sample Dilution](./1556-part1)
* [Part 2: ELISA Assay](./1556-part2)

This the first part of the ProA ELISA protocol: Sample Dilution. The robot will perform serial dilutions on samples located in the Opentrons 2 mL Eppendorf tube rack in a 2 mL deep well plate. User will need to upload a CSV specifying the desired concentration of each sample to be transferred to the 96-well STP plate. See more information on the CSV requirement in Additional Notes below.

---

You will need:
* P300 Single-channel Pipette
* P1000 Single-channel Pipette
* [Opentrons Tube Racks (2 mL Eppendorf)](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [Opentrons Tube Rack (15 + 50 mL)](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [2 mL 96-deep well Plate](https://www.usascientific.com/2ml-deep96-well-plateone-bulk.aspx)
* 96-well Plate
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
Tube Rack Setup: (slot 4)
* DI Water: A1
* Diluent: A2
* Standards: A3-B2 if number of standards is 6, A3-B4 if 8
* Samples: B3-(D6) if number of standards is 6, B5-(D6) if 8 You will need to shift the locations of the samples based on the number of standards you have each run. This configuration must be consistent of that of part 2.

---

CSV Layout:
![csv layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1556/csv_layout.png)

* No headers
* Each row represents each sample
* Each column represents the dilution factor of that sample to be transferred to the STP plate
* Robot will determine the dilution scheme of each sample based on the concentrations in the CSV

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
cSWp6GcV
1556
