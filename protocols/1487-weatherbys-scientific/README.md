# NGS Library Prep: Plate Mapping

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * NGS Library Prep

## Description
With this protocol, your robot can transfer four 96-well plates to a single 384-well plate. Layout can be found in Additional Notes.

---

You will need:
* P50 Multi-channel Pipette
* 96-well Plates
* 384-well Plate
* [TipOne Starlab 100 uL Filter Tip Racks](https://www.starlabgroup.com/en/consumables/pipette-tips_WebPSub-155853/100-l-ultrapoint-graduated-filter-tip-sterile-refill_SLS1123-1740-C.html)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Set volume to be transferred to each well.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer each column in plate 1 to 384-well plate.
8. Robot will transfer each column in plate 2 to 384-well plate.
9. Robot will transfer each column in plate 3 to 384-well plate.
10. Robot will transfer each column in plate 4 to 384-well plate.

### Additional Notes
Plate Layout:

![layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1487-weatherbys-scientific/plate_layout.png)

* Plate 1: slot 1
* Plate 2: slot 3
* Plate 3: slot 4
* Plate 4: slot 6

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
4i4t04yK
1487
