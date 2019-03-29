# TruSight Rapid Capture Part 6/8: Capture Cleanup

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

This protocol performs cleanup PCR for the [TruSight Rapid Capture](https://support.illumina.com/content/dam/illumina-support/documents/documentation/chemistry_documentation/samplepreps_trusight/trusight-rapid-capture-reference-guide-15043291-01.pdf) kit and process. The protocol allows for 4, 8, 12, or 16 samples in pools of 4 each, and completes the sixth of 8 parts for the total process. For proper reagent setup, please see 'Additional Info' below.

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
7. Purification beads are mixed and transferred to each pool in the deepwell plate, which is mixed after the transfer. A new tip is used for each transfer.
8. The protocol delays to incubate at room temperature for 10 minutes.
9. The protocol pauses and prompts the user to place the sample pools in the deepwell plate on the magnetic stand. After resuming, the pools incubate for 2 minutes.
10. Supernatant is transferred from just above the bottom of each pool well to new corresponding wells of the waste rack, using a new tip for each transfer.
11. Ethanol is distributed to each sample.
12. The protocol delays for the samples to incubate for 30 seconds.
13. Supernatant is transferred from just above the bottom of each pool well to the new corresponding wells of the waste rack, using a new tip for each transfer.
14. Steps 11-13 are repeated.
15. The protocol delays to incubate at room temperature for 10 minutes.
16. The protocol pauses and prompts the user to remove the deepwell plate from the magnetic module before resuming.
17. Resuspension buffer is transferred to each sample using a new tip each time. Each pool is mixed after the transfer.
18. The protocol delays for the pools to incubate for 2 minutes at room temperature.
19. The protocol pauses and prompts the user to place the deepwell plate on the magnetic module before resuming. After resuming, the pools incubate for 2 minutes.
20. Supernatant is transferred from the pools to different wells on sample rack in 2 steps, using a new tip for each transfer.

### Additional Notes
![Reagent Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1520-gencell-pharma-part6/reagent_setup_part6.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
16MQe5kh  
1520
