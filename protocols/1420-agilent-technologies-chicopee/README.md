# Liquid Transfer on Custom Cartridges

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
With this protocol, your robot can fill custom Seahorse cartridges using a P50 and P300 multi-channel pipette. You will need XFe96 Sensor Cartridges, XFe24 Sensor Cartridges, XFp Sensor Cartridges, a 1-well trough and a 2-well trough.


### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Robot will fill 384 injection ports in XFe96 Sensor Cartridge in slot 1 with colored water from 1-well trough.
7. Robot will fill 96 ports in XFe24 Sensor Cartridge in slot 2 with colored water from 1-well trough.
8. Robot will fill each port A in XFe24 Sensor Cartridge in slot 6 with colored water from 1-well trough.
9. Robot will fill each port B in XFe24 Sensor Cartridge in slot 9 with colored water from 1-well trough.
10. Robot will fill each port B in XFe96 Sensor Cartridge in slot 5 with colored water from 1-well trough.
11. Robot will fill each port A in XFe96 Sensor Cartridge in slot 4 with colored water from 1-well trough.
12. Wash Pipette tips
13. Robot will fill all ports in XFp Sensor Cartridge in slot 3 with colored water from 1-well trough.

### Additional Notes
Manual Tip Removal prior to running the protocol
* Remove tip 2, 4, 6, 8  from column 3 for step 8
* Remove tip 1, 3, 5, 7 from column 4 for step 9
* Remove tip 1, 3, 5, 6 from column 5 for step 10
* Remove tip 2, 4, 5, 6 from column 6 for step 11

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
qvPIJ0Cg
1420
