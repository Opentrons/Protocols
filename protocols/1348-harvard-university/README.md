# Automated Inorganic/Organic Chemical Reactions with Scheduled Addition of Reactants

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Chemistry
    * Scheduled Reaction

## Description
With this protocol, your robot can add reactants from a 6-well stock plate to 3 different wells (reactors) in another 6-well reactor plate on a controlled schedule.

### Robot
* [OT 2](https://opentrons.com/ot-2)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run
6. Robot will transfer 1000 uL from stock 1 to reactor 1.
7. Robot will pause for 2 minutes.
8. Robot will transfer 1000 uL from stock 2 to reactor 1.
9. Robot will pause for 2 minutes.
10. Robot will repeat steps 8-9 four more times.
11. Robot will transfer 250 uL from stock 3 to reactor 1.
12. Robot will pause for 2 minutes.
13. Robot will repeat 11-12 four more times.
14. Robot will transfer 250  uL from stock 4 to reactor 1.
15. Robot will pause for 2 minutes.
16. Robot will repeat steps 14-15 four more times.
17. Robot will transfer 1000 uL from stock 1 to reactor 1.
18. Robot will repeat steps 6-17 for reactor 2.
19. Robot will repeat steps 6-17 for reactor 3, but reducing the time interval between additions to 1 minute.

### Additional Notes
![setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1348-harvard-university/custom_6_well_plate.png)
* Stock Solution Plate: Slot 1
* Reactor Plate: Slot 2  

Notes: These plates are 65 mm in height, taller than the generic 6-well plate.

###### Internal
pQza41RB
1348
