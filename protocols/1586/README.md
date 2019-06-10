# CSV Cherrypicking

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Cherrypicking

## Description
This protocol performs cherrypicking from source to target plates as specified in an input CSV file. The protocol parses the CSV for slots to load the source and target plates. Only non-zero volume transfers are carried out for efficiency, and the user is prompted to refill tipracks if necessary.

---

You will need:
* [P10 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5978967113757)
* [10µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Axygen 96-eep well plates](https://ecatalog.corning.com/life-sciences/b2c/US/en/Genomics-&-Molecular-Biology/Automation-Consumables/Deep-Well-Plate/Axygen%C2%AE-Deep-Well-and-Assay-Plates/p/P-96-450V-C-S)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Reagents
* DNA oligos stored in 10x TBE

## Process
1. Upload your CSV and select your pipette mount side.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. A transfer is performed for each set of source plate and well, target plate and well, and volume. New tips are used for each transfer, and the user is prompted to replace tip racks once they are used. 0µl transfers are skipped for efficiency.

### Additional Notes
If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
S9XO3IPF  
1586
