# Luciferase Reporter Assay for NF-kB Activation (up to 4 plates) - Protocol 4: Luciferase Activity Measurement


### Author
[Opentrons](https://opentrons.com/)



# Opentrons has launched a new Protocol Library. This page won’t be available after January 31st, 2024. [Submit a request](https://docs.google.com/forms/d/e/1FAIpQLSdYYp9QCKow4nn0KlCVsMS3HX0eJ0N9O7-erajKvcpT0lWbSg/viewform) to add this protocol to the new library.

## Categories
* Sample Prep
	* Plate Filling


## Description
The protocol performs liquid handling for reporter cell lysis and luciferase-catalyzed chemical reaction in 96-well plates, ready for bioluminescence measurement by a microplate reader.

The luciferase reporter assay is used to investigate the regulation of expression of a gene of interest. This method relies on reporter cells created by stable or transient transfection of a promoter-driven, luciferase-expressing DNA. The bioluminescence proportional to luciferase expression can be quantified to assess the functional connection between the expression of the target gene which is controlled by this promoter, and the factor to be studied which may exhibit a regulatory effect on the cell behaviors at the transcription level. In this particular example, HeLa cells are stably or transiently transfected with an NF-kB promoter-driven, luciferase reporter construct, treated with an NF-kB activator phorbol 12-myristate 13-acetate (PMA), and activation of NF-kB assessed by measuring the luciferase enzymatic activity.

Reagent preparation:
The luciferase assay kit purchased from Promega (Madison, WI, USA) contains all reagents for cell lysis and luminescent signal development. To prepare luciferase assay reagent, the lyophilized luciferase assay substrate is dissolved in luciferase assay buffer per manufacturer’s instructions. Cell culture lysis reagent (5X) provided in the assay kit is diluted to working concentration. For a full 96-well plate, 11 mL luciferase assay reagent (100 μL per sample) and 4.6 mL lysis reagent (30 μL per sample) are recommended. These 2 reagents are filled in a NEST 12 Well Reservoir, and PBS for washing (50 μL per sample, 30 mL sufficient for up to four 96-well plates) filled in a NEST 1 Well Reservoir.  


### Labware
* [Opentrons 96 Tip Rack 300 µL](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [Corning 96 Well Plate 360 µL Flat #3650](https://ecatalog.corning.com/life-sciences/b2c/US/en/Microplates/Assay-Microplates/96-Well-Microplates/Corning%C2%AE-96-well-Solid-Black-and-White-Polystyrene-Microplates/p/corning96WellSolidBlackAndWhitePolystyreneMicroplates)
* [NEST 12 Well Reservoir 15 mL #360102](http://www.cell-nest.com/page94?_l=en&product_id=102)
* [NEST 1 Well Reservoir 195 mL #360103](http://www.cell-nest.com/page94?_l=en&product_id=102)
* [Opentrons HEPA Filter Module](https://opentrons.com/products/modules/hepa/)


### Pipettes
* [Opentrons P300 8 Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/8-channel-electronic-pipette/)


### Deck Setup
![deck](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/sci-lucif-assay4-for4/deck.png)


### Reagent Setup

1. A NEST 12 Well Reservoir 15 mL, filled with lysis reagent in Well 1, and luciferase assay reagent in Well 7 to Well 10 (for up to 96-well plates), loaded on Slot 4 (LYSIS BUFFER, LUCIFERASE REAGENT)
2. A NEST 1 Well Reservoir 195 mL filled with PBS loaded on Slot 9 (PBS)
3. Reporter cell culture (up to four Corning 96 Well Plate 360 µL Flat) loaded on Slot 2, 5, 8 and 11
4. A NEST 1 Well Reservoir 195 mL for liquid waste loaded on Slot 6
5. Opentrons 96 Tip Rack 300 µL loaded on Slot 1 and 3


### Protocol Steps
1. Remove supernatant in reporter cell culture on Slot 2
2. Transfer PBS from Slot 9 (PBS) to reporter cell culture on Slot 2 (50 μL per well) and then remove supernatant in reporter cell culture on Slot 2
3. Transfer lysis reagent from Slot 4 (LYSIS BUFFER, Well 1) to reporter cell culture on Slot 2 (30 μL per well) and incubate 3 minutes at room temperature
4. Transfer luciferase assay reagent from Slot 4 (LUCIFERASE REAGENT, Well 7) to reporter cell culture on Slot 2
5. Measure luminescence in reporter cell culture on a microplate reader (off deck)
6. Replenish 300 µL tips on Slot 3 (manually)
7. Repeat Step 1 to 6 for reporter cell culture on Slot 5, 8 and 11 with PBS on Slot 9 (PBS), lysis reagent on Slot 4 (LYSIS BUFFER, Well 1), and luciferase assay reagent on Slot 4 (LUCIFERASE REAGENT, Well 8, 9 and 10) 


### Process
1. Input your protocol parameters above.
2. Download your protocol and unzip if needed.
3. Upload your custom labware to the [OT App](https://opentrons.com/ot-app) by navigating to `More` > `Custom Labware` > `Add Labware`, and selecting your labware files (.json extensions) if needed.
4. Upload your protocol file (.py extension) to the [OT App](https://opentrons.com/ot-app) in the `Protocol` tab.
5. Set up your deck according to the deck map.
6. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
7. Hit "Run".


### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).


###### Internal
sci-lucif-assay4-for4
