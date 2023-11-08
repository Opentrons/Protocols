# Protocol Title (#2 Making Calibrator levels in 20 ml Scintillation vials)

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* Standard Curve

## Description
This section of the README (especially the first paragraph) should grip a prospective user with the overarching purpose/flow of the protocol, but should not include fine details of the protocol steps themselves.
 
### Labware
* [OT-2 Filter Tips, 1000µL (999-00082)](https://shop.opentrons.com/opentrons-1000ul-filter-tips-1000-racks/)
* [Chemglass 11-Position Block for 28 mm 20mL Scintillation Flat Bottom Vials](https://chemglass.com/blocks-for-centrifugal-vacuum-evaporators-optichem?sku=OP-6600-11)

### Pipettes
* [P1000 GEN2 Single Channel Pipette](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)

### Reagents
* [Methanol](link to product not available)

---

### Deck Setup
* If the deck layout of a particular protocol is more or less static, it is often helpful to attach a preview of the deck layout, most descriptively generated with Labware Creator. Example:
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/bc-rnadvance-viral/Screen+Shot+2021-02-23+at+2.47.23+PM.png)

### Reagent Setup
* This section can contain finer detail and images describing reagent volumes and positioning in their respective labware. Examples:
* Reservoir 1: slot 5
![reservoir 1](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1ccd23/res1_v2.png)


---

### Protocol Steps
1. Transfer diluent volume of MeOH into empty scintillation vials in A2 - C3.
2. Perform dilutional series starting with Working Stock in A1 through C2 creating specified calibrator levels.


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
0bc358-2
