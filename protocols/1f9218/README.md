# Capsule Filling

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Basic Pipetting
	* Plate Filling


## Description
This protocol performs capsule filling with CBD oil on capsules mounted in a custom 10x10 rack. Oil volume and height is tracked throughout the protocol for accurate transfers. The user is prompted to refill the capsule racks if the input number of capsules to fill is greater than 200, and to refill the oil reservoir if necessary. **Be sure to calibrate precisely to the first capsule to ensure no oil spills.**

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [Agilent single-channel reservoir 290ml #201252-100](https://www.agilent.com/store/en_US/Prod-201252-100/201252-100)
* [Milimoli 100-capsule rack](https://www.amazon.com/dp/B078NWV1J4/ref=cm_sw_r_cp_api_i_1mBuDb03DZDK0)
* [Capsules for oil filling]
* [Opentrons P1000 single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549142557)
* [Opentrons 1000ul pipette tips](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5984549142557)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

2x Capsule racks (spanning slots 4, 5, 1, 2 and 10, 11, 7, 8, respectively); only first rack is needed if number of capsules to fill is less than 100

Oil reservoir (slot 3)
* filled to approximately 1cm below the opening of the reservoir

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Input the mount side for your P1000 single-channel pipette, the number of capsules to fill, and the volume to fill each capsule (in ul).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".
7. The protocol transfers the input volume of oil to each capsule.

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
1f9218
