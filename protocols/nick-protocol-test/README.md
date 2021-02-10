# Nick's Protocol

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Plate Filling

## Description
This protocol moves 100µl of sample from odd numbered columns to their corresponding wells directly to their right.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

To purchase tips, reagents, or pipettes, please visit our [online store](https://shop.opentrons.com/) or contact our sales team at [info@opentrons.com](mailto:info@opentrons.com)

* [Opentrons OT-2](https://shop.opentrons.com/collections/ot-2-robot/products/ot-2)
* [Opentrons OT-2 Run App (Version 3.15.0 or later)](https://opentrons.com/ot-app/)
* [Opentrons Single-Channel Pipette](https://shop.opentrons.com/collections/ot-2-pipettes) and corresponding [Tips](https://shop.opentrons.com/collections/opentrons-tips)
* [Microplates (96-well or 384-well)](https://labware.opentrons.com/?category=wellPlate)

For more detailed information on compatible labware, please visit our [Labware Library](https://labware.opentrons.com/).



---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

[Tipracks](https://shop.opentrons.com/collections/opentrons-tips) should be loaded in **Slot 1** (if using more than 96 tips, Slots 4, 7, and 10 can be loaded as well).

The Source Plate should be loaded in **Slot 1**.

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process

1. Download your customized OT-2 protocol using the blue “Download” button, located above the deckmap.
4. Upload your protocol into the Opentrons App and follow the instructions there to set up your deck, calibrate your labware, and proceed to run.
5. Make sure to add samples to your labware before placing them on the deck! Your source plate should contain the samples you want to pick.

### Additional Notes

If you’d like to request a protocol supporting multiple destination plates or require other changes to this script, please fill out our [Protocol Request Form](https://opentrons-protocol-dev.paperform.co/). You can also modify the Python file directly by following our [API Documentation](https://docs.opentrons.com/v2/). If you’d like to chat with an automation engineer about changes, please contact us at [protocols@opentrons.com](mailto:protocols@opentrons.com).

###### Internal
nick-protocol-test
