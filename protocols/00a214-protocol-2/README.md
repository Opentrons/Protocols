# DAPI Staining

### Author
[Opentrons](https://opentrons.com/)


# Opentrons has launched a new Protocol Library. This page won’t be available after March 31st, 2024. [Submit a request](https://docs.google.com/forms/d/e/1FAIpQLSdYYp9QCKow4nn0KlCVsMS3HX0eJ0N9O7-erajKvcpT0lWbSg/viewform) to add this protocol to the new library.

## Categories
* Sample Prep
	* Staining


## Description
This protocol automates DAPI staining and is part of a five protocol suite. The five protocols are:</br>
</br>
Protocol 1: [Seeding Plates with Mammalian Cells](https://develop.protocols.opentrons.com/protocol/00a214-protocol-1)</br>
Protocol 2: [DAPI Staining](https://develop.protocols.opentrons.com/protocol/00a214-protocol-2)</br>
Protocol 3: [Fix and DAPI Stain](https://develop.protocols.opentrons.com/protocol/00a214-protocol-3)</br>
Protocol 4: [Media Exchange](https://develop.protocols.opentrons.com/protocol/00a214-protocol-4)</br>
Protocol 5: [Primary Staining](https://develop.protocols.opentrons.com/protocol/00a214-protocol-5)</br>
</br>
The protocol begins with an empty reservoir for liquid waste, a 12-channel reservoir that contains what will be added to the plates, tips, eppendorf plate(s), and the P300-Multi attached to the left mount. Using up to 4 plates, the protocol will iterate through each plate, adding reagents to the plate and removing liquid.</br>
</br>
The following steps are performed to each plate:</br>
Remove 120µL of media</br>
Add 140µL of PBS</br>
Remove 140µL of PBS</br>
Add 140µL of PBS</br>
Remove 140µL of PBS</br>
Add 100µL of 2% PFA</br>
Pause</br>
Remove 100µL of 2% PFA</br>
Add 140µL of PBS+DAPI</br>
Remove 140µL of PBS+DAPI</br>
Add 140µL of PBS</br>
Remove 140µL of PBS</br>
Add 140µL of PBS</br>
</br>
If you have any questions about this protocol, please email our Applications Engineering team at [protocols@opentrons.com](mailto:protocols@opentrons.com).

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

To purchase tips, reagents, or pipettes, please visit our [online store](https://shop.opentrons.com/) or contact our sales team at [info@opentrons.com](mailto:info@opentrons.com)

* [Opentrons OT-2](https://shop.opentrons.com/collections/ot-2-robot/products/ot-2)
* [Opentrons OT-2 Run App (Version 3.19.0 or later)](https://opentrons.com/ot-app/)
* [Opentrons p300 Multi-Channel Pipette, GEN2](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [Opentrons Tips](https://shop.opentrons.com/collections/opentrons-tips)
* [NEST 12-Well Reservoir, 15mL](https://shop.opentrons.com/collections/verified-labware/products/nest-12-well-reservoir-15-ml)
* [NEST 1-Well Reservoir, 195mL](https://shop.opentrons.com/collections/verified-labware/products/nest-1-well-reservoir-195-ml)
* Eppendorf Plate
* Reagents



---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Slot 1: [Opentrons Tips](https://shop.opentrons.com/collections/opentrons-tips), note: protocol saves tip state and will prompt user to replace tips when new tips are needed.
</br>
Slot 2: Eppendorf Plate (Plate 1)
</br>
Slot 3: Eppendorf Plate (Plate 2)
</br>
Slot 5: Eppendorf Plate (Plate 3)
</br>
Slot 6: Eppendorf Plate (Plate 4)
</br>
Slot 7: [NEST 12-Well Reservoir, 15mL](https://shop.opentrons.com/collections/verified-labware/products/nest-12-well-reservoir-15-ml)
</br>
Columns 1-4: PBS</br>
Columns 5-8: PBS</br>
Columns 9-12: 2% PFA</br>
</br>
Slot 10: [NEST 12-Well Reservoir, 15mL](https://shop.opentrons.com/collections/verified-labware/products/nest-12-well-reservoir-15-ml)
</br>
Columns 1-4: PBS+DAPI</br>
Columns 5-8: PBS</br>
Columns 9-12: PBS</br>
</br>
Slot 11: [NEST 1-Well Reservoir, 195mL](https://shop.opentrons.com/collections/verified-labware/products/nest-1-well-reservoir-195-ml), for liquid waste
</br>
**Note**: When filling the 12-well reservoirs with reagents, each column corresponds to a plate (there are 4 columns allocated per reagent). For example, if running this protocol with two (2) plates, columns 1, 2, 5, and 6 would be filled with PBS in slot 7; columns 9 and 10 would be filled with 2% PFA; etc.</br>
</br>
**Using the customizations field (below), set up your protocol.**
* **Number of Plates**: Specify the number of plates (1-4) to use.
* **Aspiration/Dispense Speed**: Specify the aspiration/dispense speed of the pipette (in µL/sec). Note: default rate is 43.46µL/sec.
* **Aspiration Height**: Specify how high (in mm) from the bottom of the well the pipette should be in the plate when aspirating.
* **Dispense Height**: Specify how high (in mm) from the bottom of the well the pipette should be in the plate when dispensing.
</br>
</br>

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process

1. Download your protocol bundle.
2. Upload [custom labware definition](https://support.opentrons.com/en/articles/3136506-using-labware-in-your-protocols), if needed.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tipracks, and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
00a214-protocol-2
