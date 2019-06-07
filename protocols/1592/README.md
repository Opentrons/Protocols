# NGS Library Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * NGS Library Prep

## Description
This protocol performs NGS library preparation using both a magnetic module and a temperature module. **Ensure the temperature module plate is mounted on the 96-well aluminum block, which is in turn mounted on the temperature module.** For reagent setup, see 'Additional Notes' below.

---

You will need:
* [P10 Multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [P300 Single-channel electronic pipette](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [P300 Multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [10µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [300µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Eppendorf twin.tec 96 Well LoBind PCR Plates, Skirted #E0030129512](https://www.fishersci.com/shop/products/eppendorf-twin-tec-96-lobind-pcr-plates-skirted-clear/e0030129512)
* [12-Channel trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [Opentrons 4-in-1 tube rack set](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* [Aluminum block set for temperature module](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set)

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
1. Select your type of P300 electronic pipette (single- or multi-channel).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The protocol waits for the temperature deck to cool to 4˚C.
8. 10ul of SPRI beads is transferred to each well of the magnetic deck plate.
9. The protocol pauses for 10 minutes for incubation.
10. The magnetic deck engages. Samples incubate for an additional 5 minutes.
11. Supernatant is removed from each sample on the magnetic plate.
12. 100ul of EtOH is transferred to each sample on the magnetic plate.
13. Supernatant is removed from each sample.
14. Steps 10-11 are repeated for a total of 2 ethanol washes.
15. The protocol pauses and the user is prompted to replace the 10ul tipracks.
16. The magnetic deck disengages. 4ul of PBS is transferred to each well of the magnetic deck plate.
17. The magnetic deck engages. Samples incubate for 1 minute.
18. Supernatant is transferred to its corresponding well on the temperature deck plate.
19. 1ul of each barcode is transferred to its corresponding well on the temperature deck plate.
20. The magnetic deck disengages, and the protocol finishes.

### Additional Notes
Reagent plate setup:
* SPRI beads: wells A1-H1
* PBS: wells A4-H4  

12-Channel trough setup:
* 80% EtOH: channel A1

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
2KCUQm4Y  
1592
