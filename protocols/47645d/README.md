# Protein Crystallization Screen

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Basic Pipetting
	* Plate Filling


## Description
This protocol transfers a varying volume (500ul, 375ul, 250ul, 125ul) from six different tubes of solution to 24-vial rack (each column). The protocol then distributes 500ul of solution from two sources to each vial in the rack. This protocol calls for the P1000-Single for easy, 1:1 transfers. Here, you can select which mount (left or right) for the P1000 and the deck layout can be found below.

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* [P1000 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)
* [1000uL Opentrons Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)
* [Opentrons 6-Tube Rack (50mL)](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* [Opentrons 10-Tube Rack (15mL + 50mL)](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* [24-Well Plate with 4mL Vials, Analytical Sales](https://www.analytical-sales.com/Aluminum-Reaction-Plates.html)


---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Slot 1: [Opentrons 6-Tube Rack (50mL)](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1); Set-Up:
* A1: Transfers to A1 - D1 in 24-Well Plate
* B1: Transfers to A2 - D2 in 24-Well Plate
* A2: Transfers to A3 - D3 in 24-Well Plate
* B2: Transfers to A4 - D4 in 24-Well Plate
* A3: Transfers to A5 - D5 in 24-Well Plate
* B3: Transfers to A6 - D6 in 24-Well Plate

Slot 2: [Opentrons 10-Tube Rack (15mL + 50mL)](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1); Set-Up:
* A3: Transfers to all wells in 24-Well Plate
* B3: Transfers to all wells in 24-Well Plate

Slot 3: [24-Well Plate with 4mL Vials, Analytical Sales](https://www.analytical-sales.com/Aluminum-Reaction-Plates.html)

Slot 4: [1000uL Opentrons Tiprack](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-1000ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process

1. Input your protocol parameter.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit "Run".

### Additional Notes
An "Air Gap" has been added to each transfer to account for liquid properties.

If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
47645d
