# DNA Normalization

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * DNA Normalization

## Description
This protocol performs the first of two steps for DNA normalization in a custom 96 flat-well plate. For reagent setup, see 'Additional Notes' below.

---

You will need:
* [FrameStar 96 Well Semi-Skirted PCR Plate](https://www.4ti.co.uk/new-products/framestar-96-well-roche-style-plates-high-sensitivity)
* [4titude 96-Well Flat-Bottom Black Plates](https://www.4ti.co.uk/microplates/Black-Assay-Plates/96-well)
* [12-Row Trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [P10 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5978967113757)
* [P300 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549109789)
* [10µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [300µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Reagents
* [Quant-iT PicoGreen dsDNA Assay Kit](https://www.thermofisher.com/order/catalog/product/P7589)

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. Working solution is distributed to each well of the flat plate using the same tip.
7. The contents of each well in columns 2-12 of the PCR plate are transferred to their corresponding well in the flat plate. A new tip is used for each transfer.
8. The contents of wells F1, G1, and H1 of the PCR plate are transferred to their corresponding wells in the flat plate. A new tip is used for each transfer.
9. The protocol pauses and prompts the user to replace the flat plate with a new empty flat plate.
10. Working solution is distributed to wells 1 and 2 of columns A-E (10 wells total) of the flat plate using the same tip.
11. The contents of wells A2, B2, C2, D2, and E2 of the PCR plate are transferred to their corresponding wells in the flat plate. A new tip is used for each transfer.

### Additional Notes
![Trough Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1546-cytena-gmbh-part1/trough_setup.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
XHv5s7Rn  
1546
