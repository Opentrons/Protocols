# PCR For NGS Library Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * PCR

## Description
With this protocol, your robot can generate a 96-well plate for library prep PCR. Your robot will distribute master mix to a clean 96 well plate. Your robot will then copy the forward primer (96 wells), reverse primer (96 wells), and DNA (96 well) plates to the plate containing the master mix. User can adjust the volume of each reagent in the fields below.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Adjust the volume of your master mix, forward primers, reverse primers, and DNA.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will distribute the master mix to all wells of clean output plate.
8. Robot will copy the forward primer plate to the new plate.
9. Robot will copy the reverse primer plate to the new plate.
10. Robot will copy and mix the DNA plate to the new plate.

### Additional Notes
Deck Setup:
* Forward Primer Pllate: slot 1
* Output Plate: slot 2
* Reverse Primer Pllate: slot 3
* Opentrons 2 mL Tube Rack: slot 4
* DNA Plate: slot 5

** Notes: Put your master mix in well A1 of the 2 mL tube rack. If you would like to change the location, you could change it in line 8 of the protocol.

###### Internal
xIJGibjA
1350
