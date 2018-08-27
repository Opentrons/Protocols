# DNA Isolation with Magnetic Nanoparticles

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Molecular Biology
	* DNA

## Description
DNA isolation with magnetic nanoparticles in 96-well plate on a magnetic plate. Uses p10 multi and p300 multi channel pipettes. Process any number of columns in a single plate. Adjust height of aspiration and mixing so as to not disturb nanoparticles.

### Robot
* OT-2

### Reagents
* Fetal bovine serum (FBS)
* Magnetic nanoparticles

## Process
1. Input number of columns of the 96-well plate you want to process.
2. Input height (in mm) above the bottom of the well you want to aspirate.
3. Download your protocol.
4. Upload your protocol into the [OT App](http://opentrons.com/ot-app).
5. Set up your desk according to the deck map.
6. Calibrate your trough, 96-well plate, and tipracks using OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
7. Hit "run".
8. Robot will transfer 261 uL of water from trough row 1 to all designated columns of the 96-well plate.
9. Robot will transfer 30 uL of FBS from trough row 8 to all designated columns of the 96-well plate.
10. Robot will transfer 9 uL of nanoparticles from trough row 9 to all designated columns of the 96-well plate.
11. Robot will mix contents of all designated columns.
12. Robot will delay for 30 minutes.
13. Robot will aspirate 250 uL from each well with the pipette at the designated height above the well and discard it into liquid trash container.
14. Robot will add 250 uL of water back to each well, dispensing at top of the well. Tips will be returned to tip rack.
15. Robot will delay for 15 minutes.
16. Robot will aspirate 250 uL from each well with the pipette at the designated height above the well and discard it into liquid trash container. Tips will be the same as the ones in step 14, and will be discarded after this step.
17. Robot will repeat steps 14-16 three additional times.

### Additional Notes
* Fill trough A1-A6 with water, A8 with FBS, and A9 with nanoparticles. Make sure to slightly overfill the water reservoirs.
* Liquid trash can be any [container](https://docs.opentrons.com/ot1/containers.html#point) with one position.

###### Internal
7WWI3gWl
719
