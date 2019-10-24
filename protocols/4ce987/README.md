# Nucleic Acid Polymerization Validation

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Distribution


## Description
This protocol aids in nucleic acid polymerization validation by creating dilution plates and transferring the necessary solutions. The protocol begins by creating a dilution plate. The protocol then moves on to specific mixes and mastermix. The protocol finalizes with an ortho reaction. This protocol requires the [P10 Single](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette) and the [P300 Single](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette). Additionally, specific labware is needed (as described below).

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [P10 Single-channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)
* [P300 Single-channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)
* [Opentrons 4-in-1 Tube Rack Set](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1), (x3)
* Eppendorf DNA LoBind 1.5mL tubes
* Eppendorf DNA LoBind 50mL tubes
* Eppendorf DNA LoBind Microplate 96-Well, V-Shaped, Polypropylene
* USA Scientific 300uL TipOne Tips
* USA Scientific 10uL TipOne Tips
* Samples/Solutions/Reagents

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Slot 1: [Opentrons Tube Rack Set (1.5/2mL)](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1) with 1.5mL LoBind Tubes

Slot 2: [Opentrons Tube Rack Set (1.5/2mL)](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1) with 1.5mL LoBind Tubes

Slot 3: Eppendorf DNA LoBind Microplate (Final Ortho Reaction)

Slot 4: Eppendorf DNA LoBind Microplate (Initiator Stock 9uM)

Slot 5: Eppendorf DNA LoBind Microplate (Initiator 0.45uM)

Slot 6: Eppendorf DNA LoBind Microplate (Snap Cooled HP)

Slot 7: TipOne Tips, 10uL

Slot 8: TipOne Tips, 10uL

Slot 9: [Opentrons Tube Rack Set (50mL)](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1) with 50mL LoBind Tubes

Slot 10: TipOne Tips, 300uL

Slot 11: TipOne Tips, 10uL

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process

1. Input your protocol parameters.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
This protocol requires user intervention. Whenever user intervention is required (primarily for off-robot mixing/vortexing), the robot will stop and a prompt with more instructions will appear in the OT app. This protocol also requires the use of multiple tipracks. Similarly, the robot will pause function when it runs out of tips and prompt the user to replace the tiprack(s).

If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
4ce987
