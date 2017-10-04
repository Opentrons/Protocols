# Serial Dilution HC

### Author
[Opentrons](https://opentrons.com/)

### Partner
[Hampton Creek](www.hamptoncreek.com)

## Categories
* Basic Pipetting

### Sub Categories
* Dilution


## Description
Performs 2 separate serial dilutions in one 96-well plate. Dilute column A to D, and dilute column H to E. Optionally, add diluent to all wells as a last step.

### Time Estimate
1 hour and 6 minutes

### Robot
* [OT PRO](https://opentrons.com/ot-one-pro)
* [OT Standard](https://opentrons.com/ot-one-standard)
* [OT Hood](https://opentrons.com/ot-one-hood)

### Modules


### Reagents
* Samples
* Diluent

## Process
1. Distribute specified volume of buffer to columns B,C,D,F,G,H.
2. Distribute samples at specified volume in duplicate to columns A and E (1 tube to two wells).
3. Dilute 2X down rows, from A to D, and then E to H.
4. Dispense specified volume of diluent to every even row (if Diluent Volume is 0, this step will be omitted).


### Additional Notes
