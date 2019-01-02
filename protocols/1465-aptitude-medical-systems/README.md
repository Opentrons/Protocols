# Nucleic Acid Purification

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * Nucleic Acid Purification

## Description
With this protocol, you can perform nucleic acid purification using the [Opentrons Magnetic Module](https://shop.opentrons.com/products/magdeck).

---

You will need:
* P300 Multi-channel Pipette
* 12-well Trough
* [Bio-rad Hardshell 96-well PCR plate, low profile](https://www.bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
* [Magnetic Module](https://shop.opentrons.com/products/magdeck)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Magnetic Module](https://shop.opentrons.com/products/magdeck)

### Reagents

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Robot will discard 95 uL solution from samples in column 1-4 of DNA plate to the trash container in slot 12.
7. Robot will distribute 30 uL Butanol from trough to column 1-4 of DNA plate.
8. Robot will mix Butanol and sample mixture in column 1-4 of DNA plate using the same tip.
9. Robot will consolidate column 1-4 of the DNA plate to column 1 of Out plate (~240 uL/well).
10. Robot will pause for user to inspect the plate, and will prompt user to resume after incubating the plate for 10 minutes.
11. Robot will discard 100 uL solution from column 1 of Out plate before transferring 100 uL solution from the column 1 to the plate on the Magnetic Module.

### Additional Notes
DNA Plate Setup:
* 125 uL Sample/well: column 1-4
* Slot 1

---

Out Plate Setup:
* Slot 2

---

Trough Setup:
* Butanol: A1

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
fUTASFAY
1465
