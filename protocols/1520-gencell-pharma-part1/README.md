# TruSight Rapid Capture Part 1/8: Tagmentation and Cleanup

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * NGS Library Prep

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

This protocol performs tagmentation and cleanup for the [TruSight Rapid Capture](https://support.illumina.com/content/dam/illumina-support/documents/documentation/chemistry_documentation/samplepreps_trusight/trusight-rapid-capture-reference-guide-15043291-01.pdf) kit and process. The protocol allows for 3, 4, 6, 8, 9, 12, or 16 samples, and completes the first of 8 parts for the total process. For proper reagent setup, please see 'Additional Info' below.  

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

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck) with [Aluminum Block Set](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set)
* [Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

### Reagents
* Refer to [TruSight Rapid Capture Reference Guide](https://support.illumina.com/content/dam/illumina-support/documents/documentation/chemistry_documentation/samplepreps_trusight/trusight-rapid-capture-reference-guide-15043291-01.pdf)

## Process
1. Set the number of samples you will be processing.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The temperature module will heat to 58˚C for precise sample incubation later in the protocol.
8. Tagbuffer and tagenzyme are transferred to each sample, which is mixed after the transfer. A new tip is used for each transfer.
9. The protocol pauses and prompts the user to place the samples rack on the temperature module before resuming. After resuming, the samples incubate at 58˚C for 10 minutes.
10. Stopbuffer is transferred to each sample on the temperature module using a new tip each time. Each sample is mixed after the transfer.
11. The protocol pauses and prompts the user to remove the samples rack from the temperature module before resuming. After resuming, the samples incubate at room temperature for 4 minutes.
12. Purification beads are mixed and transferred to each sample, which is mixed after the transfer. A new tip is used for each transfer.
13. The protocol delays for the samples to incubate at room temperature for 8 minutes.
14. The protocol pauses and prompts the user to place the samples rack on the magnetic module before resuming. After resuming, the samples incubate for 2 minutes.
15. Supernatant is transferred from just above the bottom of each sample well to the waste rack, using a new tip for each transfer.
16. Ethanol1 is distributed to each sample.
17. The protocol delays for the samples to incubate for 30 seconds.
18. Supernatant is transferred from just above the bottom of each sample well to the waste rack, using a new tip for each transfer.
19. Steps 16-18 are repeated with ethanol2.
20. The protocol delays for the samples to incubate for 10 minutes at room temperature.
21. The protocol pauses and prompts the user to remove the samples rack from the magnetic module before resuming.
22. Stopbuffer is transferred to each sample using a new tip each time. Each sample is mixed after the transfer.
23. The protocol delays for the samples to incubate for 2 minutes at room temperature.
24. The protocol pauses and prompts the user to place the samples rack on the magnetic module before resuming. After resuming, the samples incubate for 2 minutes.
25. Supernatant is transferred from the samples to different wells on sample rack in 2 steps, using a new tip for each transfer.

### Additional Notes
![Reagent Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1520-gencell-pharma-part1/part1_setup.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
16MQe5kh  
1520
