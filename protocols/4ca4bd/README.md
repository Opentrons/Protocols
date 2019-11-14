# Cherrypicking

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Cherrypicking

## Description
This protocol performs a custom cherrypicking sample prep from up to 7 96-tube racks to a custom 96-well plate (maximum 96 cherrypicks). The destination plate first receives 198ul of DMSO from a 12-channel reservoir using a multi-channel pipette, before receiving 2ul of the corresponding sample from the tube rack. The plate is filled sequentially down the columns then across the rows. The transfer scheme should be input in a `.csv` file formatted as follows (including headers):

```
Source Well,Source Slot,Pos,Tube BC
A01,2,1,0357024553
B01,3,13,0357024554
H01,3,25,0357024555
D01,5,37,0357024556
E01,4,49,0357024557
F01,2,61,0357024558
G01,3,73,0357024559
H01,6,85,0357024560
A02,2,2,0357024561
B02,7,14,0357024562
C02,1,26,0357024563
D02,2,38,0357024564
E02,3,50,0357024565
F02,1,62,0357024566
G02,2,74,0357024567
H02,3,86,0357024568
A03,1,3,0357024569
B03,1,15,0357024570

```

In this example, all wells in columns 1, 2, and 3 of the destination plate will receive 198ul each of DMSO from the reservoir using a P300 multi-channel pipette. Then, 2ul of sample from tube A1 will be transferred to well A1 in the plate, 2ul of sample from tube B1 will be transferred to well B1 in the plate, etc. The P10 single-channel pipette is used for these one-to-one sample transfers, and tips are changed between each transfer.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Greiner Bio-one 96-well v-bottom plate 340ul #651201](https://shop.gbo.com/en/usa/products/bioscience/microplates/96-well-microplates/96-well-polypropylene-microplates/651201.html)
* [Thermo Fisher 96-matrix tube rack 500ul #3743](https://www.thermofisher.com/order/catalog/product/3743?SID=srch-srp-3743)
* [Opentrons P300 multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202489885)
* [Opentrons P10 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons 300ul tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Opentrons 10ul tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

12-channel reservoir (slot 4):
* channel 1: DMSO

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the respective mount sides for your P300 multi-channel and P10 single-channel pipettes, and your input `.csv` containing transfer information.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
4ca4bd
