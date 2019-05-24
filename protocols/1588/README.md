# Mass Spec Sample Prep

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * Sample Prep

## Description
This protocol performs a mass spec sample preparation on 3 Falcon 96-well round-bottom plates, with the second (intermediate) plate mounted on a temperature module. The protocol allows for the user to select start and end temperatures. Each sample preparation increments the temperature module temperature by 1˚C. For reagent setup, see 'Additional Notes' below.

---

You will need:
* [P10 Single-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette?variant=5978967113757)
* [10µl Pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)
* [Aluminum block set](https://shop.opentrons.com/collections/hardware-modules/products/aluminum-block-set)
* [12-Channel trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* [4-in-1 Tuberack Set](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* 2ml Eppendorf tubes

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules
* [Temperature Module](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)

## Process
1. Input your start and stop temperature in degrees Celsius (note that both temperatures are inclusive).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. The temperature deck sets to the specified start temperature and waits to reach the temperature.
8. With a fresh tip, 10ul of liquid from the tube is transferred to plate 1 well A1.
9. With a fresh tip, 90ul of liquid from the trough is transferred to plate 1 well A1. Contents of the well are mixed 5x after the transfer.
10. With the same tip from step 9, 100ul of plate 1 well A1 are transferred to the corresponding well in plate 2 mounted on the temperature module.
11. The protocol delays for 2 minutes, and contents of the corresponding well on plate 2 mixed 5x with the same tip from steps 9-10.
12. Step 11 is repeated for a total of 2 delays and mixes.
13. With the same tip from steps 9-12, 100ul of the well in plate 2 are transferred to the corresponding well in plate 3.
14. The temperature module increments up 1˚C.
15. Steps 8-14 are repeated across the row and then down the column (i.e.- A2, A3, A4, ... A12, B1, B2...) until the specified stop temperature is reached.

### Additional Notes
Reagent setup:
* 1ml Liquid in tube in well A1 of 4x6 2ml Eppendorf tuberack
* 10ml Liquid in channel A1 of 12-channel trough

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
LjRwD9GL
1588
