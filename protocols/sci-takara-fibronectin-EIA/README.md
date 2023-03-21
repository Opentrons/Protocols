# Takara Fibronectin EIA w/ Heater Shaker


### Author
Boren Lin


## Categories
* Proteins
	* Proteins


## Description
The human Fibronectin (FN) EIA kit (Cat. #: MK115, Takara Bio, San Jose, CA, USA) is an in vitro assay kit for quantitative determination of soluble human FN in serum, urine, cell culture supernatants, and other biological fluids. The assay utilizes two mouse monoclonal anti-human FN antibodies allowing an antibody-antigen-antibody sandwich to form: the capture antibody pre-coated on 8-well strips, and the detection antibody conjugated with peroxidase (POD). The photometric signal can be developed by exposing this complex to a substrate of peroxidase, with the absorbance proportional to the amount of target (i.e., human FN) present in the sample.
The protocol performs transferring of the samples into the EIA plate to allow the capture antibody to bind to FN. After washing, the detection antibody is added into the EIA plate. After another round of washing, the substrate for POD is transferred into the EIA plate to develop photometric signal which can be measured on a microplate reader at 450 nm. The on-deck Heater-Shaker Module provides set temperature at 37°C for sample incubation to promote antigen-antibody interaction.

Materials provided in the kit:
1.	Anti-human FN monoclonal antibody coated microtiter plate (8-well strip x12)
2.	POD-labeled anti-human FN monoclonal antibody (Antibody-POD Conjugate)
3.	Lyophilized human FN (for standards)
4.	Sample Diluent
5.	Substrate Solution (TMBZ)

Other materials required:
1.	Wash and Stop Solution for ELISA (Takara Bio, San Jose, CA, USA)
2.	Slit seal (BioChromato, Fujisawa, Japan)
3.	NEST 1 Well Reservoir 195 mL 
4.	NEST 96 Deep Well Plate 2mL
5.	Opentrons Tip Rack, 300 µL
6.	Nunc 96-Well Polypropylene Storage Microplates (Cat. #: 249947, Thermo Fisher, Waltham, MA, USA) or compatible 
7.	Microplate Reader

Pipettes and Modules
1.	Opentrons P300 8-Channel Pipette (GEN2)
2.	Heater Shaker Module (GEN1) with Aluminum Adaptor for 96-well Flat Plate

Deck setup:
Please see the deck layout as the general guideline for labware setup. 
1.	The EIA plate is sealed with a slit seal and placed on the Heater Shaker Module (Slot 3). 
2.	Samples or sample dilutions are pre-loaded in the Nunc 96-Well Polypropylene Storage Microplates, the SAMPLES plate (Slot 1).
3.	The REAGENTS plate (Slot 4) is filled with Antibody-POD Conjugate in Column 1, Substrate Solution in Column 2, and Stop Solution in Column 3.
Note: see Reagent Step for reagent plate preparation
4.	For WASH1 (Slot 5), sufficient wash buffer is filled in each well for 3 washes of 250 μL, and 4 washes for WASH2 (Slot 8)
5.	Three boxes of Opentrons 96 tips (Slot 7, 10, and 11) are sufficient to run a full 96-well EIA plate (12 8-well strips).  
6.	The WASTE plate is loaded at Slot 9.



### Labware
* Takara EIA 96-well on Heater Shaker #468667
* Thermo Scientific 96 Well Plate V Bottom 450 uL #249944/249946
* [NEST 96 Deepwell Plate 2mL #503001](http://www.cell-nest.com/page94?product_id=101&_l=en)
* [Opentrons 96 Tip Rack 300 µL](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [NEST 1 Well Reservoir 195 mL #360103](http://www.cell-nest.com/page94?_l=en&product_id=102)


### Pipettes
* [Opentrons P300 8 Channel Electronic Pipette (GEN2)](https://shop.opentrons.com/8-channel-electronic-pipette/)


### Deck Setup
[deck](https://drive.google.com/open?id=1g8Y6ouV1dMw2Opn_LFsKhEVBxVTCLLrI)


### Reagent Setup
[reagents](https://drive.google.com/open?id=10jOo7iZ7eAduNUCFqefaOp9MmcRgPhH0)


### Protocol Steps

1.	User is prompted to place the EIA plate on the Heater Shaker Module, which is then secured when the latches close.
2.	The samples (100 μL per sample) are transferred into the EIA plate
3.	After a brief shaking, the temperature increases to 37°C, maintained for 60 min
4.	The supernatant in each well is discarded.
5.	The wash buffer (250 μL per well) is added into the EIA plate. 
6.	The supernatant in each well is discarded.
7.	For 2 more washes, Step 4 and 5 are repeated.
8.	Antibody-POD Conjugate (100 μL per well) is added into the EIA plate
9.	After a brief shaking, the temperature increases to 37°C, maintained for 60 min
10.	The supernatant in each well is discarded.
11.	The wash buffer (250 μL per well) is added into the EIA plate. 
12.	The supernatant in each well is discarded.
13.	For 3 more washes, Step 11 and 12 are repeated.
14.	Substrate Solution (100 μL per well) is added into the EIA plate.
15.	After a brief shaking, the protocol pauses for 15 min for the photometric signal to develop.
16.	Stop Solution (100 μL per well) is added into the EIA plate.
17.	The latches of the Heater Shaker Module open, and user is prompted to move the EIA plate to a microplate reader.



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
sci-takara-fibronectin-EIA
