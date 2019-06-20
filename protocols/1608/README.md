# Bead Purification

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * Nucleic Acid Purification

## Description
This protocol performs nucleic acid purification on deepwell plate mounted on a magnetic module. The protocol allows for the user to select the number of sample columns to be processed, and purified samples are transferred to a new fresh plate at the end of the protocol. For reagent setup, see Additional Notes below.

---

You will need:
* [Abgene 96-deepwell plate # AB0859](https://www.thermofisher.com/order/catalog/product/AB0859)
* [USA Scientific 12-Channel reservoir # 1061-8150](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [Opentrons P10 Multi-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [Opentrons P300 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202489885)
* [Opentrons 10ul pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Opentrons 300ul pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

## Process
1. Input the number of sample columns to be processed (1-12).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. 8ul of sample is transferred from the sample plate to its corresponding well on the magnetic module plate. New tips are used for each transfer.
8. 2ul of MQ is transferred from the trough to each well of the magnetic module plate (now 10ul total). Contents are mixed 10x after the transfer, and new tips are used for each transfer/mix sequence.
9. The protocol delays 5 minutes for the samples to incubate at room temperature.
10. The magnetic module engages, and the protocol delays 2 minutes for the samples to incubate on the magnet.
11. Supernatant is transferred out to the trash. New tips are used for each supernatant removal.
12. 200ul of ethanol is transferred form the ethanol plate to its corresponding  sample well on the magnetic module plate. The same tip is used, and ethanol is dispensed at the top of each well to avoid contamination.
13. The protocol delays 30 seconds for the samples to incubate.
14. Supernatant is transferred out to the trash. New tips are used for each supernatant removal.
15. Steps 12-14 are repeated for a total of 2 ethanol washes.
16. The magnetic module disengages.
17. 20ul of IDTE is transferred from the trough to each well of the magnetic module plate. Contents are mixed 10x after the transfer, and new tips are used for each transfer/mix sequence.
18. The protocol delays 2 minutes for the samples to incubate at room temperature.
19. The magnetic module engages, and the protocol delays 2 minutes for the samples to incubate on the magnet.
20. 20ul of sample is transferred from each well on the magnetic module plate its corresponding well on a new plate. New tips are used for each transfer.

### Additional Notes
Reagent setup for 12-channel trough:  
MQ: channel 1
IDTE: channel 2

Ethanol plate setup:  
minimum 400ul of ethanol in each column corresponding to sample columns to be processed

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
ViKOxOBi  
1608
