# NGS Library Prep Part 3/4: M5 PCR Amplification

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * NGS Library Prep

## Description
This protocol performs NGS library preparation part 3/4 for up to 96 samples. For reagent setup for the protocol, please see 'Additional Notes' below.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Bio-Rad Hard Shell 96-Well PCR Plate 200uL # HSP9601](http://www.bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
* [Abgene 96-Deepwell 0.8mL Polypropylene Storage Plate # AB-0765](https://www.thermofisher.com/order/catalog/product/AB0765?SID=srch-hj-AB-0765)
* [USA Scientific 12-channel reservoir # 1061-8150](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [Opentrons P10 Multi-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [Opentrons P50 Multi-Channel Electronic Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [10ul Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [300ul Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Opentrons Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck) with [96-well aluminum blocks](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set)
* [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Reagent plate order (consecutive columns starting with user-input column):
* FS2E1: first column (wells A:H)
* FS1: second column (wells A:H)
* RS: third column (wells A:H)
* SS1: fourth column (wells A:H)
* SS2E2: fifth column (wells A:H)
* PCRE3: sixth column (wells A:H)

12-Channel reagent reservoir:
* PB: channel 1
* EB: channel 2
* PS: channel 3
* EtOH: channels 4-7
* liquid waste: channels 8-12 (loaded empty)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the number of samples to be processed, pipette mount sides, and reagent starting column.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
0cb5e5
