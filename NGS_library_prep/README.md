# NGS Library Prep

### Author
 * Opentrons

### Date
 * October 11th, 2017

## Categories
 * Molecular Biology
** DNA

## Description
This NGS prep uses Opentrons' MagDeck module to cut down and create sequencing
library.

### Robot
* OT PRO
* OT Standard

### Instruments
* 300 ul single channel Pipette
* 200 ul multi channel Pipette
* Mag Deck

### Reagents
* EtOH
* TE
* H20
* KAPA beads

## Time Estimate
* Depends on the amount of samples

## Process
1. Choose values for TE volume as well as number of samples. Note the allocated
range are TE [20, 200] and number of samples [8,96] <- (multiples of 8!)
2. Place plates, tip-racks and troughs in their designated locations found below in the commands
containers.load() or in the deck image generated on the library.
2. Upload to OT app and connect to the robot
3. Calibrate each container as specified in the app
4. Hit run and watch your robot go!

#### Internal
MP3h4TXU
350
