# Cherrypicking CSV Spreadsheet

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
    * Cherrypicking

## Description
Cherry picking is used to take the contents of selected wells on a source plate, and arrange them on a destination plate. It is useful for doing **limiting dilutions**.

This protocol currently only allows the use of a single-channel pipette -- multi-channel is not supported.

To generate a `.csv` from from Excel or another spreadsheet program, try "File > Save As" and select `*.csv`

The csv for this protocol must contain rows where the first column is the name of the source well to pick (eg `A1`), and the second column is the volume in uL to aspirate (eg, `20`).

For example, to cherry-pick 3 wells, your CSV could look like:

```
A1, 20
A3, 10
B2, 15
```

Result:
* **20uL** will be taken from well **A1** of the source plate and added to the **first** well (A1) on the destination plate
* **10uL** will be taken from well **A3** of the source plate and added to the **second** well (B1) on the destination plate
* **15uL** will be taken from well **B2** of the source plate and added to the **third** well (C1) on the destination plate

Note that well A3 is not transferred to A3 on the destination plate. Instead, it is transferred to the 3rd well on the plate, because it's on row 3 of the spreadsheet.

### Robot
* [OT PRO](https://opentrons.com/ot-one-pro)
* [OT Standard](https://opentrons.com/ot-one-standard)
* [OT Hood](https://opentrons.com/ot-one-hood)

## Process
1. Upload your CSV file and input your pipette axis, pipette model, whether to reuse tips, and whether to blow out at destination.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
gn0k1kuY  
1581
