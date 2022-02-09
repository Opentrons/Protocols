# Automated GenFind V3 Blood/serum DNA extraction

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Nucleic Acid Extraction & Purification
	* Blood Sample

## Description
This protocol automates the GenFind V3 protocol from Beckman Coulter for [DNA isolation from whole blood or serum with magnetic particles](https://s3.amazonaws.com/pf-upload-01/u-4256/0/2022-01-24/kz234fm/C36038AB.pdf). This protocol utilizes a P300-Multi Channel pipette and gives the user the option to select a variable number of samples (Should be a multiple of 8) and whether to dispense liquid waste in a reservoir in slot 6 or in the fixed trash container. This protocol is designed for holding the samples on the [USA Scientific PlateOne® Deep 96-Well 2 mL Polypropylene Plate (P/N 1896-2800)](https://www.usascientific.com/plateone-96-deep-well-2ml/p/PlateOne-96-Deep-Well-2mL) on a 2nd generation magnetic module. The purified samples are transferred to a [Abgene™ 96 Well 0.8mL Polypropylene Deepwell Storage Plate (Thermo AB-0859)](https://www.thermofisher.com/order/catalog/product/AB0859) in the final step. The protocol uses the [NEST 12 Well Reservoir 15 mL](https://shop.opentrons.com/nest-12-well-reservoirs-15-ml/) and the [NEST 1 Well Reservoir 195 mL](https://shop.opentrons.com/nest-1-well-reservoirs-195-ml/) as sources of reagents


The protocol is broken down into 5 main parts:
* Lysis buffer is added to the samples and proteinase K is added to the samples. The samples are incubated until the lysis reaction has completed
* Binding buffer containing paramagnetic particles are added and the samples are incubated in order to bind DNA
* The supernatant is discarded and the beads are washed two times with Wash WBB and two times with Wash WBC buffers.
* Elution buffer is added to the samples which are incubated.
* Finally the eluted purified samples are transferred to the target plate

Explanation of parameters below:
* `Number of samples`:  How many samples to run, it should ideally be a multiple of 8 for efficient use of resources.
* `Blood cells or serum?`: Choose what kind of samples to use for the protocol. This parameter will set the sample volume to 200 uL for blood cells, and 400 for serum samples. It will also set the elution volume to 200 uL for blood cell samples, and 40 uL for serum samples.
This setting will affect the volume requirements for all other reagents
* `X offset for bead aspiration`: How many millimeters away from the center of the sample wells to aspirate bead supernatant from, the default is 1 mm.
* `Magnet extension (mm)`: How far from the base of the sample plate to extend the magnets of the magnet deck (default is 4.7 mm)
* `Proteinase K location`:  Choose whether the proteinase K is located in tube 1 of the tube rack, or well 1 of the 12 well reservoir
* `Elution buffer location`:  Choose whether the elution buffer is located in tube 2 to 8 of the tube rack, or well 6 and 7 of the 12 well reservoir
* `Liquid waste reservoir?`: If set to `yes` the protocol will use a NEST 1 well 195 mL reservoir as a target of liquid waste, otherwise it will empty liquid waste into the regular trash bin.  

---

### Modules
* [Magnetic Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

### Labware
* [NEST 1 Well Reservoir 195 mL](https://labware.opentrons.com/nest_1_reservoir_195ml)
* [NEST 12 Well Reservoir 15 mL](https://shop.opentrons.com/nest-12-well-reservoirs-15-ml/)
* [USA Scientific PlateOne® Deep 96-Well 2 mL Polypropylene Plate (P/N 1896-2800)](https://www.usascientific.com/plateone-96-deep-well-2ml/p/PlateOne-96-Deep-Well-2mL)
* [Abgene™ 96 Well 0.8mL Polypropylene Deepwell Storage Plate (Thermo AB-0859)](https://www.thermofisher.com/order/catalog/product/AB0859)

### Pipettes
* [P300 Multichannel GEN2 Pipette](https://shop.opentrons.com/collections/ot-2-robot/products/8-channel-electronic-pipette?variant=5984202489885)

**Tips**
* [Opentrons 96 Filter Tip Rack 200 µL](https://labware.opentrons.com/opentrons_96_filtertiprack_200ul/)

### Reagents
* [GenFind V3 Reagent Kit](https://www.beckman.com/reagents/genomic/dna-isolation/from-blood)

---

### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/0f5985/deck.jpg)

### Reagent Setup
* 12-well reservoir: slot 4
![reservoir 1](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/0f5985/12_well_resv.jpg)
* Reagent tuberack: slot 7  
![reservoir 2](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/0f5985/tuberack.jpg)

---

### Protocol Steps
1. Add Lysis LBB to samples
2. Add Proteinase K to samples and mix
3. Incubate the samples with buffer and enzyme, 10 minutes at 37 degrees C, or 30 minutes at room temperature
4. Add Bind BBB and mix the samples gently
5. Incubate the samples for 5 minutes
6. Engage the magnets for 15 minutes
7. Aspirate the supernatant and dump it in the chosen waste receptacle
8. Wash the beads 2 times with Wash WBB and dump the supernatant
9. Wash the beads 2 times with Wash WBC and dump the supernatant
10. Add elution buffer and mix
11. Incubate the samples for 2 minutes and mix again
12. Engage the magnets for 5 minutes and transfer the supernatant containing purified DNA to the target plate

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
0f5985
