# Mass Spectrometry Sample Prep

### Author
[Opentrons](http://www.opentrons.com/)

### Partner


## Categories
* Proteins & Proteomics
  * Sample Prep


## Description

Part A: Get samples from variously-sized containers into a deep (2.2 mL) 96 well plate:
---
  Step A1:	Take clean pipette tip for p100 (single channel) and move to reagent 1 in the trough; ‘dunk’ the tip fully in the trough (but don’t take up anything) to remove any external particles
  Step A2:	Move to reagent 2 (also in trough) and uptake full volume of tip and dispense to waste; repeat this step three times.
  Step A3:	Take up between 20→100 uL of a sample (located in 15 or 50 mL tube rack) and dispense into the appropriate position in the 96 well plate
  Step A4:	Discard pipette tip after sample is transferred

Repeat steps 1→4 for x number of samples

Part B: Dilute each sample up to 1,900 uL using a clean tip
---
  Step B5:	Take clean pipette tips for multi-channel p300 and move to reagent 1 in the trough; ‘dunk’ fully in the trough (but don’t take up anything) to remove any external particles
  Step B6:	Move to reagent 2 (also in trough) and uptake full volume of tip and dispense to waste; repeat this step three times
  Step B7:	Move to reagent 3 in the trough, uptake 300 uL and add to each sample; repeat six times so each sample has 1,800 uL of reagent 3.

Note that, for samples that were <100 uL, the volume will be less than 1,900 uL, and so we’ll need to go back with the p100 (single channel) to dilute these samples with the correct amount of reagent 3. The exterior and interior tip cleaning procedure is the same as in steps A1 & A2.

Part C: Add 100 uL internal standard to each sample and homogenize
---
Step C8:	Using the p300 (multi-channel), clean a set of 200 uL tips as per steps B5 and B6 above (‘dunk’ in reagent 1; rinse with reagent 2)
Step C9:	Take 100 uL of internal standard (reagent 4) from a separate trough and dispense into the bottom of each sample
Step C10:	Dispense up and down a few times in each sample to mix/homogenize before withdrawing; discard pipette tips after this

Repeat steps C8→C10 for each row of the well plate that contains samples.

### Time Estimate

### Robot
* [OT PRO](https://opentrons.com/ot-one-pro)
* [OT Standard](https://opentrons.com/ot-one-standard)
* [OT Hood](http://opentrons.com/robots/ot-one-s-hood)

### Modules


### Reagents
* Samples in dilute acid
* IS Solution
* Pre-wet reagent
* Wash reagent

## Process
This protocol requires the use of 3 separate CSV files:
* Destination Volume
* Source Location
* Destination Location
---
The formats should be as follows:
* Destination Volume - the excel rows correspond to rows A, B, C...of a container
and the columns correspond to columns 1, 2, 3, 4...

```
| Vol1 | Vol2     | Vol3 |
| Vol4 | Vol5     | Vol6 |
| Vol7 | Vol8     | Vol9 |
```
* Source Location - the excel rows correspond to rows A, B, C...of a container
and the columns correspond to columns 1, 2, 3, 4...

```
| Sample 1 | Sample 2     | Sample 3 |
| Sample 4 | Sample 5     | Sample 6 |
| Sample 7 | Sample 8     | Sample 9 |
```
* Destination Location - the excel rows correspond to rows A, B, C...of a container
and the columns correspond to columns 1, 2, 3, 4...

```
| Sample 1 | Sample 2     | Sample 3 |
| Sample 2 | Sample 1     | Sample 2 |
| Sample 9 | Sample 8     | Sample 5 |
```
### Additional Notes


###### Internal
RlR2aGWc
157
