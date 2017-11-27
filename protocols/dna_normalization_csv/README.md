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

The csv must contain volumes in microliters (uL). It can be oriented either in "portrait" orientation with well A1 at the bottom left, or in "landscape" orientation with well A1 in the top left.

For example, for an 8x12 96-well plate, your CSV could look like this ("portrait" orientation):

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

**Result:** 66 uL will be added to well A1, then 60 uL to well B1, and so on.

Equivalently, you can use a CSV in a "landscape" orientation, with well A1 at the top left. This example will do the same as the above:

```
66,43,58,61,24,111,139,185,28,106,56,90
60,16,101,71,128,25,48,96,143,198,197,168
164,156,121,109,106,84,111,60,185,45,147,187
129,175,5,84,88,12,68,105,17,6,139,13
106,190,122,85,124,63,179,143,199,46,74,70
7,41,88,62,65,31,126,151,155,113,61,189
198,78,27,89,133,34,59,18,78,111,44,196
195,8,59,168,26,8,172,102,93,33,157,93
```

**Result:** This "landscape" example will produce the same result as the other "portrait" example: 66 uL will be added to well A1, then 60 uL to well B1, and so on.

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
