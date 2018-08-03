# Nucleic Acid Purification

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * DNA

## Description
This protocol allows to robot to perform nucleic acid purification using isopropanol precipitation, and can be used for similar assays. Extraction buffer is used to breakdown cell component to initiate the process of DNA extraction. With the addition of isopropanol and followed by centrifugation, alcohol-insoluble DNA precipitates in the solution and forms a pellet. The pellet is then washed in ethanol, dried and resuspended in TE buffer.

### Robot
* [OT-One](https://opentrons.com/robots)

### Reagents
* Isopropanol
* Ethanol

## Process
1. Download your protocols.
2. Upload Part 1 onto the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your tiprack, pipette, plate, and petri dishes using the OT App. For calibration tips, check out our support articles:
 * [Calibrating the Deck](https://support.opentrons.com/ot-one/getting-started-software-setup/calibrating-the-deck)
 * [Calibrating the Pipettes](https://support.opentrons.com/ot-one/getting-started-software-setup/calibrating-the-pipettes)
5. Hit "Run Job".
6. Transfer 250 uL of DNA extraction buffer to the 96-well plate.
7. Pause for incubation and await for user to resume.
8. Transfer supernatant from 96-well plate to a new well plate, using new tip each time.
9. Transfer isopropanol to the new 96-well plate.
10. Upload Part 2 after spinning to pellet DNA.
11. Set up your deck according to the deck map.
12. Aspirate 199 uL of supernatant to liquid trash.
13. Transfer 200 uL of 70% ethanol.
14. Aspirate 199 uL of supernatant to liquid trash.
15. Pause to let dry, await for user to resume.
16. Transfer 50 uL of TE buffer to pellets.

### Additional Information
* The height from which the pipette aspirates from the tubes can be modified, check out our support article for [adjusting default dispense height](https://support.opentrons.com/ot-one/ot-one-defaults/adjusting-default-dispense-height).
###### Internal
TIuqUJUw
1043
