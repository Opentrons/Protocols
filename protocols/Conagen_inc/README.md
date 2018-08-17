# Sample Extraction

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
With this protocol, the robot can perform sample extraction in up to three 96-deep well plates and load the samples into a 24-position tube rack that are filled with Gas Chromatography tubes. If only one plate is used, the plate is placed on the Temp Deck in slot 1.

### Robot
* [OT 2](https://opentrons.com/ot-2)

### Modules
* Temp Deck

### Reagents
* Sulfuric acid-methanol
* Hexane

## Process
1. Download your protocol.
2. Open the protocol, adjust the number of 96-well plates and columns to fill in your experiment.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. (Temp Deck is set to 65 degree if only one plate is present.)
8. Transfer 200 uL sulfuric acid-methanol to the columns.
9. Pause for incubation, prompt user to resume the run.
10. (Temp Deck is deactivated.)
11. Transfer 400 uL water to the columns.
12. Transfer 200 uL hexane to the columns, mix 3 times.
13. Transfer 100 uL hexane layer in the columns to a tube in the 24-well tube rack. Rinse tip in hexane twice between each transfer. Pause after every time all tubes have been filled, prompt the user to replace tube rack and resume the run.

### Additional Information
* You can adjust the heights (from the bottom of the well/tube) from which the pipette aspirate and dispense at the top of the protocol.

###### Internal
issNaqUF
1041
