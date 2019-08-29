# Nucleic Acid Purification: Part 2/2

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Molecular Biology
	* Nucleic Acid Purification


## Description
This protocol performs part 2/2 of a custom nucleic acid purification protocol. The user is prompted to place/replace labware on the deck as necessary.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [QIAGEN 12x 8-well collection microtube strips, racked 1.2 ml #19560](https://www.qiagen.com/us/products/discovery-and-translational-research/lab-essentials/plastics/collection-microtubes/#orderinginformation)
* [Thermo Fisher Scientific Abgene 96-deepwell plate 2.2ml #AB0661](https://www.thermofisher.com/order/catalog/product/AB0661)
* [Thermo Fisher Scientific MicroAmp optical 96-Well reaction plate 200ul #4316813](https://www.thermofisher.com/order/catalog/product/4316813)
* [Biomek 4-channel reservoirs 40ml #372790](https://us.vwr.com/store/product/4694729/biomek-modular-reservoirs-beckman-coulter) in [Biomek reservoir stand #372795](https://www.beckman.com/supplies/reservoirs/)
* [P300 Multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202489885)
* [Opentrons 300ul tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Opentrons magnetic module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

4-channel Biomek reagent reservoir (slot 2)
* channels 1-2: bead buffer
* channels 3-4: CSPW1 buffer

4-channel Biomek reagent reservoir (slot 3)
* channels 1-2: CSP2 buffer
* channels 3-4: SPM buffer

4-channel Biomek reagent reservoir (slot 3) **User is prompted to load this reservoir only at the end of the protocol, because the elution buffer must be heated to 65C until use.**
* channel 1: elution buffer

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the mount for your P300 multi-channel pipette, the number of samples to process, and the volume of elution buffer to transfer (in ul).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
569d34
