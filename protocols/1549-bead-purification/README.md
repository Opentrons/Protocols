# NGS Library Prep - Bead Purification

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * NGS Library Prep

## Description
This protocol performs a mix distribution from 200ul PCR strips to a ThermoFisher 96-well MicroAmp EnduraPlate mounted on a temperature deck set at 4˚C. The user can select parameters such that this protocol fullfills the 10uL Random Priming Mix, 3uL Exo rSAP MM, 10.5uL Adaptase, and 25.3uL Indexing D500 (parts 1, 2, 4, and 5, respectively) of the NGS prep. The multi-channel pipette that is needed is automatically determined by the protocol after the user inputs the desired transfer volume.

---

You will need:
* [P10 8-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [P300 Single-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)
* [10µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [200µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [ThermoFisher 96-Well MicroAmp EnduraPlates #4483348](https://www.thermofisher.com/order/catalog/product/4483348)
* 96 200µl PCR strips
* [Opentrons 4-in-1 Tube Rack Set](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* 15ml Falcon Tubes
* 2ml Eppendorf Tubes

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

## Process
1. Input the beads strip column. Ensure the PCR plate is mounted on the temperature deck before running.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. 18.4ul of beads are transferred to each well of each of the 2 sample plates. The contents of each well are mixed 8x after each transfer. New tips are used for each transfer and mix.
8. The protocol pauses and prompts the user to replace the 10ul tiprack in slot 10 before resuming.
9. The contents of each column of each plate are consolidated to well A for that column (H to A, G to A, F to A, ..., B to A). Tips are changed between each column consolidation.
10. The protocol delays for 5 minutes for the samples to incubate.
11. The protocol pauses and prompts the user to place the first plate on the magnetic module before resuming.
12. The magnetic deck engages, and the plate incubates for 10 minutes for the beads to separate out.
13. Supernatant is removed from each well of the plate on the magnetic deck with magnet engaged to the trash container. A new tip is used for each well.
14. 200ul of ethanol is distributed from a 15ml tube to each well of the plate on the magnetic deck (occupying row A after the consolidation in step 9). A height tracker is enabled so that the pipette does not submerge in the ethanol tube.
15. The protocol delays for 30 seconds for the samples to incubate.
16. The ethanol is removed from each well of the plate on the magnetic deck with magnet engaged to the trash container. A new tip is used for each well.
17. Steps 14-16 are repeated 2x more for a total of 3 ethanol washes.
18. The height tracker is reset to the second ethanol tube for the second plate later in the protocol.
19. The protocol delays for 8 minutes for the pellets to dry.
20. The magnetic deck disengages.
21. 10.5ul of TE is added to each sample of the magnetic plate (occupying row A). The wells are mixed 10x after each transfer, and 10ul is immediately transferred to the the corresponding spot a new plate. See 'Additional Notes' for transfer order.
22. The protocol pauses and prompts the user to replace the 200the plate in its original slot on the deck.
23. The protocol pauses and prompts the user to place the second plate on the magnetic module before resuming.
23. Steps 12-21 are repeated with the second plate.

### Additional Notes
![Deck Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1549-university-of-pennsylvania-bead-purification/deck_setup_2.png)

![2ml Tube Rack Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1549-university-of-pennsylvania-bead-purification/2ml_rack_setup.png)

![15ml Tube Rack Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1549-university-of-pennsylvania-bead-purification/15ml-rack-setup.png)

![Elute Order](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1549-university-of-pennsylvania-bead-purification/elute_order.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
Yp5gMvur  
1549
