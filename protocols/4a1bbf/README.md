# Cherrypicking from CSV

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Cherrypicking

## Description
This protocol performs cherrypicking based on an input .csv file. The sources are 50ml conical tubes contained in up to 9 tube racks. The destination is a single 96-deepwell block. The user is prompted to replace the tiprack as necessary in the protocol. Tips are only changed between source tubes (the same tip is used for each source tube). The .csv formatting is as follows:

```
Source_Well,Source_position,Source_position_name,Destination_position,Destination_Well,Destination_labware,Volume
A1,10,compounds1,8,A1,array1,1000
A1,10,compounds1,9,A1,array2,1000
A1,10,compounds1,5,A1,array3,1000
A1,10,compounds1,6,A1,array4,1000
A1,10,compounds1,2,A1,array5,1000
A1,10,compounds1,3,A1,array6,1000
A2,10,compounds1,8,B1,array1,1000
A2,10,compounds1,9,B1,array2,1000
A2,10,compounds1,5,B1,array3,1000
A2,10,compounds1,6,B1,array4,1000
A2,10,compounds1,2,B1,array5,1000
A2,10,compounds1,3,B1,array6,1000
```

**Note: Ensure the header is included in the .csv file. The first line of the file will be ignored during the run.**

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* Corning Costar 96-deepwell block 2ml #3680
* [Opentrons 4-in-1 tuberack set with 2x3 50ml conical tube inserts](https://shop.opentrons.com/collections/verified-labware/products/tube-rack-set-1)
* [Nest 50ml conical tubes](https://shop.opentrons.com/collections/verified-consumables/products/nest-50-ml-centrifuge-tube) or equivalent
* [Opentrons P1000 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549142557)
* [Opentrons 1000ul tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the mount side for your P1000 single-channel pipette, your transfer .csv file, the starting tip well.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
4a1bbf
