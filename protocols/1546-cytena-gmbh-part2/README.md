# DNA Normalization

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Molecular Biology
    * DNA Normalization

## Description
This protocol performs the second of two steps for DNA normalization in a custom 96 flat-well plate. The protocol takes input from a CSV containing well-specific transfer information for water and DNA to the flat plate.. For reagent setup, see 'Additional Notes' below.

---

You will need:
* [FrameStar 96 Well Semi-Skirted PCR Plate](https://www.4ti.co.uk/new-products/framestar-96-well-roche-style-plates-high-sensitivity)
* [4titude 96-Well Flat-Bottom Black Plates](https://www.4ti.co.uk/microplates/Black-Assay-Plates/96-well)
* [12-Row Trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [P50 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549077021)
* [300µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Reagents
* [Quant-iT PicoGreen dsDNA Assay Kit](https://www.thermofisher.com/order/catalog/product/P7589)

## Process
1. Upload your CSV to be run in the protocol.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The input CSV is parsed for the proper volumes and locations of each water and DNA transfer.
8. The input volume of water is transferred from the trough to the top of each well of the flat plate using the same tip.
9. The input volume of DNA is transferred from each well of the PCR plate to the corresponding well of the flat plate.

### Additional Notes
![Trough Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1546-cytena-gmbh-part2/trough_setup.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
XHv5s7Rn  
1546
