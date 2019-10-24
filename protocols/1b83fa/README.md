# Updated Cherrypicking with CSV

### Author
[Opentrons](https://opentrons.com/)

### Partner

## Categories
* Basic Pipetting
	* Plate Consolidation

## Description

This protocol is a modified version of this [Cherrypicking Protocol](https://protocols.opentrons.com/protocol/cherrypicking_csv). This protocol uses two pipettes, has expanded labware capabilities, and allows the user to customize which destination well will be chosen. This protocol requires a CSV to be uploaded below.

To generate a `.csv` from from Excel or another spreadsheet program, try "File > Save As" and select `*.csv`

The CSV for this protocol must contain rows where the first column is the name of the source well to pick (eg `A1`), the second column is the volume in uL to aspirate (eg, `20`), and the third column is the name of the destination well (eg `A2`).

For example, to cherry-pick 3 wells, your CSV could look like:

```
A1, 20, A1
A2, 10, A2
B2, 15, B1
```

Result:
* **20uL** will be taken from well **A1** of the source plate and added to the **first** well (A1) on the destination plate
* **10uL** will be taken from well **A3** of the source plate and added to the **second** well (A2) on the destination plate
* **15uL** will be taken from well **B2** of the source plate and added to the **third** well (B1) on the destination plate

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [P10/P50/P300 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)
* [P10/P50/P300 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)
* [50/300uL Opentrons tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [10uL Opentrons tipracks, if using P10](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Fisherbrand 200uL PCR Plate, 05-408-210](https://www.fishersci.com/shop/products/fisherbrand-96-well-ultra-pcr-plate-96-well-ultra-pcr-plate/05408210)
* [Fisherbrand 300uL PCR Plate, 14-230-23X](https://www.fishersci.com/shop/products/fisherbrand-96-well-nonskirted-pcr-plates-natural/14230232)
* [ThermoScientific 300uL PCR Plate, AB-0600-L](https://www.thermofisher.com/order/catalog/product/AB0600L)
* [Axygen Plate Rack, R96PCRFSP](https://us.vwr.com/store/product/4907380/pcr-tube-storage-racks-axygen-scientific)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Slot 1: [50/300uL Opentrons tipracks](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)

Slot 2: Source Plate (select from dropdown below before downloading)

Slot 3: Destination Plate (select from dropdown below before downloading)

Slot 4 (optional): [10uL Opentrons tipracks, if using P10](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)


### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process

1. Input your protocol parameters and upload CSV.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes

If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
1b83fa
