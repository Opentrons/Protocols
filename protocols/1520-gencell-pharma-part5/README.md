# TruSight Rapid Capture Part 5/8: Second Capture

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* NGS Library Prep
    * TruSight Rapid Capture

## Description
Links:
* [Part 1/8: Tagmentation and Cleanup](./1520-gencell-pharma-part1)
* [Part 2/8: First Amplification](./1520-gencell-pharma-part2)
* [Part 3/8: Cleanup PCR1](./1520-gencell-pharma-part3)
* [Part 4/8: First Capture](./1520-gencell-pharma-part4)
* [Part 5/8: Second Capture](./1520-gencell-pharma-part5)
* [Part 6/8: Capture Cleanup](./1520-gencell-pharma-part6)
* [Part 7/8: Second Amplification](./1520-gencell-pharma-part7)
* [Part 8/8: Cleanup PCR2](./1520-gencell-pharma-part8)

This protocol performs cleanup PCR for the [TruSight Rapid Capture](https://support.illumina.com/content/dam/illumina-support/documents/documentation/chemistry_documentation/samplepreps_trusight/trusight-rapid-capture-reference-guide-15043291-01.pdf) kit and process. The protocol allows for 4, 8, 12, or 16 samples in pools of 4 each, and completes the fifth of 8 parts for the total process. For proper reagent setup, please see 'Additional Info' below.

Note that this protocol is written specifically for multi-channel pipettes--tips are iterated through from the bottom left (well H1) of the rack to ensure that the pipette only picks up one tip. In addition, the decks slot below the tip racks are intentionally left open so that the multi-channel pipette does not crash.

---

You will need:
* [P10 8-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [P50 8-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202457117)
* [P300 8-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202457117)
* [Opentrons 10µl Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Opentrons 300µl Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [4x6 2ml Tube Rack](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1)
* [Non-Skirted PCR Plates](http://www.ssibio.com/pcr/ultraflux-pcr-plates/non-skirted-pcr-plates/3400-00-detail)
* [PCR Strips](http://www.simport.com/products/pcr/pcr-strips/t320-and-t321-amplitube.html)
* [Deepwell Storage Plate](https://www.thermofisher.com/order/catalog/product/AB0859)
* [Magnetic Stand](https://www.thermofisher.com/order/catalog/product/AM10027)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck) with [Aluminum Block Set](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set)
* [Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

### Reagents
* Refer to [TruSight Rapid Capture Reference Guide](https://support.illumina.com/content/dam/illumina-support/documents/documentation/chemistry_documentation/samplepreps_trusight/trusight-rapid-capture-reference-guide-15043291-01.pdf)

## Process
1. Set the number of pools you will be processing.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The temperature module will heat to 42˚C for precise sample incubation later in the protocol.
8. Streptavidin beads are mixed and transferred to each pool in the deepwell plate, which is mixed after the transfer. A new tip is used for each transfer.
9. The protocol pauses and prompts the user to vortex the deepwell plate at 1200rpm for 5 minutes.
10. The protocol delays to incubate at room temperature for 25 minutes.
11. The protocol pauses and prompts the user to place the deepwell plate on the magnetic stand. After resuming, the pools incubate for 2 minutes.
12. Supernatant is transferred from just above the bottom of each pool to the waste rack, using a new tip for each transfer.
13. The protocol pauses and prompts the user to remove the samples from the magnetic stand.
14. Wash solution is transferred to each pool in the deepwell plate, which is mixed after the transfer. A new tip is used for each transfer.
15. Each pool is distributed to 2 new corresponding wells each on the wash rack, using a new tip for each distribution.
16. The protocol pauses and prompts the user to place the deepwell plate on the magnetic stand, as well as to place the wash rack on the temperature module.
17. The sets of 2 samples each on the wash rack are consolidated back into 1 well per pool on the deepwell plate using a new tip for each consolidation.
18. The protocol delays to incubate at room temperature for 2 minutes.
19. 200ul of each pool is transferred to a new corresponding well on the extra rack (PCR strips) using a new tip for each transfer.
20. The protocol pauses and prompts the user to remove the deepwell plate from the magnetic stand.
21. Steps 14-20 are repeated.
22. Elution buffer and HP3 are transferred to elution mix, which is mixed after the transfer. A new tip is used for each transfer.
23. Elution mix is transferred to each pool in the deepwell plate, which is mixed after the transfer. A new tip is used for each transfer.
24. The protocol delays to incubate at room temperature for 2 minutes.
25. The protocol pauses and prompts the user to place the deepwell plate on the magnetic stand. After resuming, the pools incubate for 2 minutes.
26. Supernatant is transferred from the samples to new wells on the wash rack in 2 steps, using a new tip for each transfer.
27. Target buffer is transferred to each of wells on the wash rack from step 26.

### Additional Notes
![Reagent Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1520-gencell-pharma-part4/reagent_setup_part4.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
16MQe5kh  
1520
