# Cherrypicking

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Cherrypicking

## Description
This protocol performs a custom cherrypicking sample prep from up to 9 DNA donor plates to 1 deepwell pool plate using a P10 single-channel pipette. Source slots and wells, destination well, and transfer volume are specified in an input `.csv` formatted as follows (include header line; empty lines and whitespace are ignored):

```
Deck Position,Well,Pooled Plate (Position 10),Volume (ul)
1,A7,A1,8.7
1,C12,A3,8.7
1,E4,A11,8.7
1,G2,A12,6
1,G8,B5,6
1,H8,B6,6
1,H9,B7,6
1,H4,B10,6
2,B6,B11,6
2,B12,B12,6
2,C9,H1,6
```

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Thermofisher Abgene 96-deepwell plate 800ul #AB-0765](https://www.thermofisher.com/order/catalog/product/AB0859#/AB0859)
* [Opentrons GEN1 P10 electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons 10ul tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)

---

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the mount side for your P10 single-channel pipette, upload the input `.csv` file, and input whether to touch tip on transfer.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
59f50b
