# Master Mix and DNA Distribution

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * PCR

## Description
With this protocol, your robot can perform PCR prep by (1) distribute master mixes from 2 mL tubes to a 96-well output plate, (2) distribute samples from a 96-well source plate to master mixes, (3) transfer master mix and sample mixture in duplicate in output plate.

---

For this protoc0l, you will need:
* P300 Single-channel Pipette
* P10 Multi-channel Pipette
* [Opentrons 4-in-1 Tube Rack Set](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* 96-well PCR plates
* [Opentrons 300 uL Tip Racks](https://shop.opentrons.com/collections/opentrons-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Select the tube rack type you are using.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will distribute 90 uL master mix 1 to column 1 and 4 of master plate using P300 single-channel pipette.
8. Robot will distribute 90 uL master mix 2 to column 7 and 10 of master plate using P300 single-channel pipette.
9. Robot will distribute 2 uL DNA from column 1 of source plate to column 1 of master plate using P10 multi-channel pipette.
10. Robot will distribute 2 uL DNA from column 2 of source plate to column 4 of master plate using P10 multi-channel pipette.
11. Robot will distribute 2 uL DNA from column 3 of source plate to column 7 of master plate using P10 multi-channel pipette.
12. Robot will distribute 2 uL DNA from column 4 of source plate to column 10 of master plate using P10 multi-channel pipette.
13. Robot will transfer 10 uL master mix and DNA mixture from column 1 to column 2, and 3 using P10 multi-channel pipette.
14. Robot will transfer 10 uL master mix and DNA mixture from column 4 to column 5, and 6 using P10 multi-channel pipette.
15. Robot will transfer 10 uL master mix and DNA mixture from column 7 to column 8, and 9 using P10 multi-channel pipette.
16. Robot will transfer 10 uL master mix and DNA mixture from column 10 to column 11, and 12 using P10 mulit-channel pipette.

### Additional Notes

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
YZc22RRe
1456
