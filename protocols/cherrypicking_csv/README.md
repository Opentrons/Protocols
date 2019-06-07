# Cherrypicking CSV Spreadsheet

### Author
[Opentrons](https://opentrons.com/)

### Partner

## Categories
* Basic Pipetting
	* Plate Consolidation

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

### Time Estimate

### Robot
* [OT PRO](https://opentrons.com/ot-one-pro)
* [OT Standard](https://opentrons.com/ot-one-standard)
* [OT Hood](https://opentrons.com/ot-one-hood)

### Modules

### Reagents

## Process

### Additional Notes

###### Internal
