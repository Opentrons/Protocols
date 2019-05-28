# NGS Library Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * NGS Library Prep

## Description
This protocol performs NGS library preparation using both a magnetic module and a temperature module. **Please fill the 50ml EtOH tube to the 50ml mark to ensure accurate height tracking throughout ethanol washes. Also, ensure the temperature module plate is mounted on the 96-well aluminum block, which is in turn mounted on the temperature module.** For reagent setup, see 'Additional Notes' below.

---

You will need:
* [P10 Multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [10µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [P300 Single-channel electronic pipette](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [300µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Eppendorf twin.tec 96 Well LoBind PCR Plates, Skirted #E0030129512](https://www.fishersci.com/shop/products/eppendorf-twin-tec-96-lobind-pcr-plates-skirted-clear/e0030129512)
* [12-Channel trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [Opentrons 4-in-1 tube rack set](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* [Aluminum block set for temperature module](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set)
* 50ml Falcon Tubes

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

### Reagents
* Beckman SPRI beads
* 80% EtOH
* Custom oligo barcodes

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. The protocol waits for the temperature deck to cool to 4˚C.
7. 10ul of SPRI beads is transferred to each well of the magnetic deck plate.
8. The protocol pauses for 10 minutes for incubation.
9. The magnetic deck engages. Samples incubate for an additional 5 minutes.
10. Supernatant is removed from each sample on the magnetic plate.
11. 100ul of EtOH is transferred to each sample on the magnetic plate.
12. Supernatant is removed from each sample.
13. Steps 10-11 are repeated for a total of 2 ethanol washes.
14. The protocol pauses and the user is prompted to replace the 10ul tipracks.
15. The magnetic deck disengages. 4ul of PBS is transferred to each well of the magnetic deck plate.
16. The magnetic deck engages. Samples incubate for 1 minute.
17. Supernatant is transferred to its corresponding well on the temperature deck plate.
18. 1ul of each barcode is transferred to its corresponding well on the temperature deck plate.
19. The magnetic deck disengages, and the protocol finishes.

### Additional Notes
Reagent plate setup:
* SPRI beads: wells A1-H1
* PBS: wells A4-H4

50ml Tube rack setup:
* 80% EtOH (filled to ~50ml): well A1

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
2KCUQm4Y  
1592
