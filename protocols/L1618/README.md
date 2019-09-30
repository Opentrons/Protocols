# Swift Biosciences Swift Amplicon 16S+ ITS Panel

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Molecular Biology
	* NGS Library Prep


## Description
This protocol performs amplicon prep according to the [Swift Amplicon 16S+ ITS Panel Kit](http://t7fuu3u4kioyf7ep21k6b916.wpengine.netdna-cdn.com/wp-content/uploads/2019/02/18-2328_Swift-Amplicon-16SITS-Panel_Protocol.pdf). The protocol pauses and prompts the user intermittently for off-deck microfuging, vortexing, and thermocyclying steps, as well as, tiprack replenishing. Users have the option of running either 48-samples (half plate) or 96-samples (full plate).

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [P50 Single-channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)
* [P300 Multi-channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [50/300uL Opentrons tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-3000ul-tips)
* [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)
* [Opentrons Temperature Module with Aluminum Block Set](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* [Bio-Rad Hard Shell 96-Well PCR Plate](http://www.bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
* [USA Scientific 12-Channel Reservoir](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* 8-Well PCR Strips, x3
* 2mL Tubes (preferably screwcap), for [Aluminum Tube Rack](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

* [Protocol Reagents](http://t7fuu3u4kioyf7ep21k6b916.wpengine.netdna-cdn.com/wp-content/uploads/2019/02/18-2328_Swift-Amplicon-16SITS-Panel_Protocol.pdf)
	* Multiplex PCR Reaction Mix
	* Indexing Reaction Mix
	* Magnetic Beads
	* Ethanol Solution, freshly prepared
	* Index D50X & D7XX
	* PEG NaCl Solution
	* Post-PCR TE Buffer



---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Slot 1: [Opentrons Magnetic Module](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

Slot 2: Bio-Rad 96-Well Plate, clean and empty (used for final elution)

Slot 3: [Opentrons Aluminum Tube Rack](https://shop.opentrons.com/collections/racks-and-adapters/products/aluminum-block-set), chilled
	* A1: Multiplex PCR Reaction Mix
	* A2: Multiplex PCR Reaction Mix (if running 96 samples)
	* B1: Indexing Reaction Mix
	* B2: Indexing Reaction Mix (if running 96 samples)

Slot 4: [Opentrons Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck) loaded with [Opentrons 96-Well Aluminum Block](https://shop.opentrons.com/collections/racks-and-adapters/products/aluminum-block-set/) and Bio-Rad 96-Well Plate, loaded with 10 ul of samples (either half or full plate)

Slot 5: [USA Scientific 12-Channel Reservoir](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
	* Column 1: Magnetic Beads
	* Column 2: Ethanol Solution, Freshly Prepared
	* Column 3: Ethanol Solution, Freshly Prepared
	* Column 4: Ethanol Solution, Freshly Prepared
	* Column 5: Ethanol Solution, Freshly Prepared
	* Column 6: PEG NaCl Solution
	* Column 7: Post-PCR TE Buffer

Slot 6: [Opentrons 96-Well Aluminum Block](https://shop.opentrons.com/collections/racks-and-adapters/products/aluminum-block-set/), after Multiplex PCR Step, with 8-Well PCR Strips filled with Indexing Solution
	* A1: D501
	* B1: D502
	* C1: D503
	* D1: D504
	* E1: D505
	* F1: D506
	* G1: D507
	* H1: D508

	* A2: D701
	* B2: D702
	* C2: D703
	* D2: D704
	* E2: D705
	* F2: D706
	* G2: D707
	* H2: D708

	* A3: D709
	* B3: D710
	* C3: D711
	* D3: D712
	* E3: empty
	* F3: empty
	* G3: empty
	* H3: empty

Slot 7: [50/300uL Opentrons Tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-3000ul-tips)

Slot 8: [50/300uL Opentrons Tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-3000ul-tips)

Slot 9: [50/300uL Opentrons Tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-3000ul-tips)

Slot 10: [50/300uL Opentrons Tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-3000ul-tips)

Slot 11: [50/300uL Opentrons Tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-3000ul-tips)


### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process

1. Mount P50-Single and P300-Multi pipettes to OT-2, then input number of samples (48 or 96) and specify where the pipettes are attached.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
This protocol is based on the [Swift Amplicon 16S+ ITS Panel Kit](http://t7fuu3u4kioyf7ep21k6b916.wpengine.netdna-cdn.com/wp-content/uploads/2019/02/18-2328_Swift-Amplicon-16SITS-Panel_Protocol.pdf). Please review this document for more details regarding this protocol.

If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
L1618
