# Reverse Transcriptase Preparation

### Author
[Opentrons](https://opentrons.com/)

## Categories
* PCR Prep
	* Reverse Transcriptase

## Description
This is a plate filling protocol for a reverse transcriptase procedure. Up to 95 samples can be prepped using 4-in-1 tube racks filled with barcode primer mixes and a prepared enzyme mix in the final tube.

Explanation of complex parameters below:
* `Number of samples`: Specify the number of samples this run (1-95)
* `Reagent Volume to Add`: Specify the volume of RT mix to add. Default is 4.7 uL
* `Well Plate Type`: Change between the BioRad plate in the OT-2 default labware library and the custom definition for Greiner 96 well plates with a circular well
* `P20 Mount`: Specify which side the single-channel P20 is mounted to

---

### Labware
* [Opentrons 20uL Filter Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-200ul-filter-tips)
* [Opentrons 4-in-1 Tube Rack](https://shop.opentrons.com/4-in-1-tube-rack-set/)
* [BioRad 96 Well Plate](https://www.bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
* [Greiner Microplate, 96 Well, PP, V-Bottom](https://shop.gbo.com/en/usa/products/bioscience/microplates/96-well-microplates/96-well-polypropylene-microplates/651201.html)

### Pipettes
* [P20 Single Channel Pipette](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)

---

### Deck Setup

* Tube racks in slots 1, 2, 4, and 5 map directly to the 96 well plate. I.e. if 95 samples are specified all four tube racks will load in, RT mix will be in the bottom right well, C4, for slot 2. Well G12 will have primers added from slot 2, tube C3. If 13 samples are specified, the tube racks in slot 4 and 1 will load in, RT mix will be in well B2 in slot 1 (the 14th tube). Slot 1 A1's primer will add to well E1 in slot 3's well plate

![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/e54ada/deck_layout.png)

### Reagent Setup

* Liquid Color Code:

![Color Code](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/e54ada/liquids.png)

* Reservoir 1: Slot 3

![reservoir 1](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/e54ada/resv.png)

* NOTE ON REAGENT LOADING:
  Ethanol should be loaded into slots 1-4 in deck slot 3. Ethanol will be aspirated equally from all 4 wells. The minimum volume for the NEST reservoir is 1.5 mL. E.g. if 4 mL of ethanol is needed in total it should be split between the four wells with an extra 500 uL added to reach 1.5 mL per well.

  Additionally, the ethanol wash volume varies depending on the well plate being used. 200 uL per wash per sample will be used for the Greiner plate while 120 uL per wash per sample will be used for the BioRad plate.

* NOTE ON SAMPLE NUMBERS:
  This protocol is very flexible in sample numbers but with one caveat. Multiples of 8 to run full columns is recommended for efficiency. Running 15 samples will take much longer than 16 samples as 7 samples in the second column will utilize the single-channel pipette. This is a trade off of total run time for reagent efficiency. If you want to run 15 samples and are willing to use extra reagent, enter 16 samples and leave the 16th well empty in column 2.

* NOTE ON SLOT 2's EMPTY TIP BOX
  This protocol uses an empty 300uL tip box in slot 2 for tip parking and reuse across steps. This allows easy tip re-use for supernatant removal and wash steps. Proper tip rack calibration is still necessary for good results

---

### Protocol Steps
1. Beads are added to the sample plate according to the supplied bead ratio parameter. The sample/bead mixture is mixed. The beads are re-mixed every 3 samples to ensure homogeneity in the reagent well.
2. The beads are incubated for 10 minutes in the samples before the magnetic module is engaged for 7 minutes
3. The supernatant is removed and deposited in the waste container in slot 11
4. Ethanol is added to the wells to wash beads. 200 uL is added for the Greiner plates and 120 uL for BioRad plates
5. A 2 minute delay occurs to allow beads to re-pellet after ethanol wash
6. Ethanol is removed from samples and deposited in the waste container in slot 11
7. Steps 4-6 are repeated for a second ethanol wash
8. Water is added to the samples to elute according to the set parameters below and mixed
9. A 5 minute delay occurs to allow elution to occur followed by the magnetic module being engaged for 7 minutes
10. The elution solution, now separated from the beads, is aspirated and dispensed in the awaiting plate in slot 10

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
e54ada
