# Cherrypick Multiple Wells to Master Tube

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Cherrypicking

## Description
This protocol performs cherrypicking from a 96-well PCR plate to one master tube, according to an input CSV file. For tube setup, see 'Additional Notes' below.

To generate a `.csv` from from Excel or another spreadsheet program, try "File > Save As" and select `*.csv`

The csv for this protocol must contain rows where the first column is the name of the source well to pick (eg `A1`), and the second column is the volume in uL to aspirate (eg, `20`). Do not include headers or empty columns before transfer data in the csv file.

For example, to cherry-pick 3 wells, your CSV could look like:

```
A1, 20
A3, 10
B2, 15
```

Result:
* **20uL** will be taken from well **A1** of the source plate and added to the master tube in well A1 of the tube rack.
* **10uL** will be taken from well **A3** of the source plate and added to the master tube in well A1 of the tube rack.
* **15uL** will be taken from well **B2** of the source plate and added to the master tube in well A1 of the tube rack.

---

You will need:
* [Opentrons Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [BioRad 96-Well PCR plate](http://www.bio-rad.com/en-us/sku/mll9651-multiplate-96-well-pcr-plates-low-profile-unskirted-white?ID=MLL9651)
* [Opentrons 4-in-1 tube rack set](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [Fisherbrand 1.5ml Microcentrifuge Tubes](https://www.fishersci.com/shop/products/fisherbrand-premium-microcentrifuge-tubes-1-5ml-natural-1-5ml-o-d-x-l-10-8-x-40-6mm/05408129)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Upload your cherrypicking CSV file and select your single channel pipette type, pipette mount, and tip use strategy.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".

### Additional Notes
Tube setup in 4x6 Eppendorf tube rack (slot 2):
* Master tube: well A1

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
LYGy3LO9  
1604
