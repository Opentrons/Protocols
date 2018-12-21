# Nucleic Acid Purification

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * Nucleic Acid Purification

## Description
With this protocol, your robot can perform nucleic acid purification on 8 samples in [1.2 mL tubes](https://www.usascientific.com/1.2ml-tube-individual-racked.aspx).

---

You will need:
* P50 Multi-channel Pipette
* P300 Multi-channel Pipette
* [1.2 Tubes in a 96-deep well plate](https://www.usascientific.com/1.2ml-tube-individual-racked.aspx)
* 12-well Trough
* [0.2 mL 96-well Plate](https://www.bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
* [Magnetic Module](https://shop.opentrons.com/products/magdeck)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Magnetic Module](https://shop.opentrons.com/products/magdeck)

### Reagents

## Process
1. Input the height of the 1.2 mL tubes.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer and mix 500 uL Buffer A to samples in column 1 of the deep-well plate, pause for 5 minutes, mix again. Robot will then incubates the samples for another 5 minutes.
8. Robot will transfer and mix 500 uL Buffer B to samples.
9. Robot will transfer and mix 1100 uL samples to column 2 of the of the deep-well plate, pause for 5 minutes, and mix again. Robot will then incubates the samples for another 5 minutes.
10. Robot will engage the magnetic module, and remove supernatant from column 2. Robot will disengage the magnetic module.
11. Robot will transfer and mix 250 uL Buffer C to column 2, engage the magnetic module and wait 30 seconds. Robot will then remove the supernatant and disengage the magnetic module.
12.  Robot will repeat step 11.
13. Robot will transfer and mix 250 uL Buffer D to column 2, engage the magnetic module and wait 30 seconds. Robot will then remove the supernatant and disengage the magnetic module.
14. Robot will repeat step 13.
15. Robot will transfer and mix 50 uL Buffer E to column 2, engage the magnetic module and wait 30 seconds. Robot will then transfer the supernatant to column 1 of the Bio-rad Hardshell PCR plate. Robot will disengage the magnetic module.


### Additional Notes
96-deep Well Plate Setup
* Samples: Column 1
* Beads: Column 2

---

12-well Trough:
* Buffer A: A1
* Buffer B: A2
* Buffer C: A3
* Buffer D: A4
* Buffer E: A5

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
17D6BBzc
1470
