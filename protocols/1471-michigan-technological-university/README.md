# NGS Library Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * NGS Library Prep

## Description
With this protocol, your robot can perform NGS Library Prep using [Axyprep Magnetic Beads](https://www.fishersci.com/shop/products/axygen-axyprep-mag-pcr-clean-up-kits-3/p-4265673#?keyword=axyprep).

---

With this protocol, you will need:
* P50 Multi-channel Pipette
* P300 Multi-channel Pipette
* [Opentrons Magnetic Module](https://shop.opentrons.com/products/magdeck)
* [Biorad Hardshell 96-well PCR Plates](https://www.bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
* 12-well Trough
* 200 uL Tip Racks

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Magnetic Module](https://shop.opentrons.com/products/magdeck)

### Reagents
* [Axygen Axyprep Magnetic Beads](https://www.fishersci.com/shop/products/axygen-axyprep-mag-pcr-clean-up-kits-3/p-4265673#?keyword=axyprep)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Robot will transfer and mix 20 uL magnetic beads to each wells of the 96-well plate on the magnetic module.
7. After 5 minutes of incubation, robot will activate the magnet for 2 minutes.
8. Robot will transfer 200 uL 80% ethanol to each sample and let mixture incubate for 30 seconds.
9. Robot will remove and discard supernatant from each well.
10. Robot will repeat step 8-9.
11. Robot will pause to allow the plate to air dry for 15 minutes. Magnetic Module will then be deactivated.
12. Robot will transfer and mix 52.5 uL of 10 mM Tris to each sample.
13. After 2 minutes of incubation, robot will activate the magnet for 2 minutes.
14. Robot will transfer 50 uL supernatant to a new PCR plate. Robot will disengage the magnetic module.

### Additional Notes
Trough Setup:
* Magnetic Beads: A1
* 80% Ethanol: A2-A3
* 10 mM Tris: A4

---


If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
yAeSnQcF
1471
