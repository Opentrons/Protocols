# Standard Liquid Transfer

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Basic Pipetting
    * Plate filling

## Description
This protocol performs standard liquid transfer from a 12-row trough to a user specified number of custom 96-well deep plates. The entire protocol uses the same tips throughout the process. The protocol can handle volumes from 5-300µl assuming the user has both p50 and p300 Opentrons electronic pipettes.

---

You will need:
* [p50 8-channel pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202457117)
* [p300 8-channel pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202457117)
* [Opentrons 300uL Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [12-row trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)

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
6. The protocol determines which pipette to use from the user-specified transfer volume per well.
7. The protocol loads up to 8 custom plates depending on the user-specified number of plates.
8. The pipette picks up one column of tips, and the specified volume is distributed to every well of every plate using the same tips. The volume is blown out into the wells at each transfer.
9. If more than 8 plates are specified, the program pauses and waits for the user to reload new plates in ascending slots starting at 1 (max 8 plates per deck reload).
10. The process continues until all plates have received a liquid transfer, such that the number of deck reloads.
11. The tips are dropped after the entire protocol is completed.

### Additional Notes

###### Internal
ucje75RN  
1515
