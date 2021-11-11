# Sample Prep MALDI spotting - Serial Dilution

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Serial Dilution

## Description
This protocol serially dilutes stock from tube A1 of the stock tube rack (slot 1) to up to 15 tubes in the dilution rack (see diagram below). The `initial volume of stock for tube 1` and `initial volume of dilution for tube 1` volumes are added to A1 of the tuberack in slot 2, and from there the `Initial volume of stock for the rest of the tubes (mL)` and `Initial volume of dilution for the rest of the tubes (mL)` volume parameters are used to step down up from tube A2 to the number of tubes specified by the user. Mix steps are also included at full pipette tip volume.

Explanation of complex parameters below:
* `Number of dilution tubes (1-15)`: Specify the number of dilution tubes to step down in slot 2.
* `Initial volume of stock for tube 1 (ul)`: Specify the volume of stock for the initial tube.
* `Initial volume of dilution for tube 1 (mL)`: Specify the volume of dilution for the initial tube.
* `Initial volume of stock for the rest of the tubes (mL)`: Specify the volume of stock for all other tubes.
* `Initial volume of dilution for the rest of the tubes (mL)`: Specify the volume of stock for all other tubes.
* `P1000 Single-Channel Mount`: Specify which mount (left or right) to host the P1000 single-channel pipette.


---

### Labware
* [Opentrons 4-in-1 tube rack](https://shop.opentrons.com/collections/racks-and-adapters/products/tube-rack-set-1)
* [Opentrons 1000ul Tips](https://shop.opentrons.com/collections/opentrons-tips)
* [Nest 1-well Reservoir 195mL](https://shop.opentrons.com/collections/reservoirs/products/nest-1-well-reservoir-195-ml)



### Pipettes
* [P1000 Single-Channel Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/single-channel-electronic-pipette)

---

### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/469c70/Screen+Shot+2021-11-11+at+12.59.57+PM.png)

---

### Protocol Steps
1. Transfer 230µl of stock solution from 2 mL Eppendorf tube (9.6x 4.7mm) or 15 mL Falcon tube (17.5 mm Diameter) → 15 mL Falcon tube (17.5 mm Diameter)
2. Transfer 9.770 mL of diluent from Source. 500mL or 1000mL media storage bottle (100 x 400mm or 100 x 900mm) → above 15 mL Falcon tube (17.5 mm Diameter)
3. Mix 5 times (Aspiration) (Sample ID. STD 8)
4. Transfer 1.2 mL of STD 8 from 15 mL Falcon tube (17.5 mm Diameter) → 15 mL Falcon tube (17.5 mm Diameter).
5. Transfer 8.8 mL of diluent from Source. 500mL or 1000mL media storage bottle (100 x 400mm or 100 x 900mm) → above 15 mL Falcon tube (17.5 mm Diameter)
6. Mix 5 times (Aspiration) (Sample ID. STD 7)
7. (Likewise, the serial dilutions shall be prepared as STD6, STD5, STD4, STD3, STD2 & STD1).

### Process
1. Input your protocol parameters above.
2. Download your protocol and unzip if needed.
3. Upload your custom labware to the [OT App](https://opentrons.com/ot-app) by navigating to `More` > `Custom Labware` > `Add Labware`, and selecting your labware files (.json extensions) if needed.
4. Upload your protocol file (.py extension) to the [OT App](https://opentrons.com/ot-app) in the `Protocol` tab.
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
7. Hit 'Run'.

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
469c70
