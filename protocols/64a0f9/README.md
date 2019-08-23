# Swift Biosciences Swift 25 Turbo NGS Library Prep

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Molecular Biology
	* NGS Library Prep

## Description
This protocol performs NGS library prep according to the [Swift Biosciences Swift 2S Turbo DNA Library Kit](https://swiftbiosci.com/wp-content/uploads/2019/06/19-2420-2STurbo-w-PCR-Protocol-WEB.pdf). The protocol pauses and prompts the user intermittently for off-deck microfuging, vortexing, and thermocycling steps, as well as tiprack replenishing.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Bio-Rad Hard Shell 96-well PCR plates 200ul #hsp9601](http://www.bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
* [USA Scientific 12-channel reservoir 22ml #1061-8150](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [P10 Single-channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [P300 Multi-channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202489885)
* [Opentrons 10ul Pipette Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Opentrons 300ul Pipette Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Opentrons magnetic module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Opentrons temperature module with aluminum block set](https://shop.opentrons.com/products/tempdeck?_ga=2.260195210.640108062.1566160120-1245111371.1550251253)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Aluminum block 2ml screwcap tuberack (slot 3)
* A1: enzymatic mastermix
* B1-C1: ligation mastermix (C1 not needed in sample number is 48 or less)

12-Channel reservoir (slot 5)
* A1: magnetic beads
* A2-A5: 80% ethanol (A4-A5 not needed in sample number is 48 or less)
* A6: EDTA buffer
* A7: TE buffer
* A8-A12: liquid trash (loaded empty)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the number of samples to process and the mount side for your P10 single-channel and P300 multi-channel pipettes.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
64a0f9
