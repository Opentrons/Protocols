# DNA Normalization with CSV Spreadsheet

### Author
[Opentrons](https://opentrons.com/)

### Partner

## Categories
* Molecular Biology
	* DNA

## Description
Dilute samples in a 96 or 384 well plate, using volumes from a CSV file.

To generate a `.csv` from from Excel or another spreadsheet program, try "File > Save As" and select `*.csv`

The csv must contain volumes in microliters (uL), and be oriented like plate on the deck of the Opentrons robot -- well A1 should be on the bottom left.

For example, for an 8x12 96-well plate, your CSV would look like:

```
90,168,187,13,70,189,196,93
56,197,147,139,74,61,44,157
106,198,45,6,46,113,111,33
28,143,185,17,199,155,78,93
185,96,60,105,143,151,18,102
139,48,111,68,179,126,59,172
111,25,84,12,63,31,34,8
24,128,106,88,124,65,133,26
61,71,109,84,85,62,89,168
58,101,121,5,122,88,27,59
43,16,156,175,190,41,78,8
66,60,164,129,106,7,198,195
```

66 uL will be added to well A1, 60 uL to well B1, and so on.

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
