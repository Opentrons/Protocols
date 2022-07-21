# Next Advance Checkit Go

### Author
[Opentrons](https://opentrons.com/)

### Partner
[Next Advance](https://www.nextadvance.com/)

## Categories
* Featured
	* Next Advance Checkit Go

## Description

This protocol performs [Next Advance Checkit Go](https://www.nextadvance.com/checkit-go/) volume accuracy testing for Opentrons electronic pipettes on the OT-2. The user can select which model Checkit Go cartridge with which to test their pipette accuracy (2, 5, 10, 20, or 50ul).

---

### Labware
* [Next Advance Checkit Go Cartridge](https://www.nextadvance.com/checkit-go/)
* [Opentrons 20/300ul Tiprack](https://shop.opentrons.com/universal-filter-tips/)

### Pipettes
* [Opentrons P20/P300 Single-/8-Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/pipettes/)

### Reagents
* [Next Advance red dye pellet](https://www.nextadvance.com/product/checkit-go-dye-pellet-6-pack/) reconstituted in water

---

### Deck Setup
![deck](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/checkit/deckv2.png)

---

### Protocol Steps
1. The pipette picks up tips and aspirates the Checkit Go-specific volume from the cartridge reservoir.
2. The pipette dispenses the entire liquid volume into the wells of the cartridge and drops the tip.
3. The user is prompted to flip the cartridge and record the measurement.
4. Steps 1-3 are repeated a total of 8 times for all wells if the selected pipette is single-channel.

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
checkit
