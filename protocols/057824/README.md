# Custom Mass Spec Sample Prep

### Author
[Opentrons](https://opentrons.com/)


## Categories
* Sample Prep
	* Mass Spec

## Description
This protocol uses the heater-shaker module, magnetic module, single-channel P20, and single-channel P300 pipette to perform mass spec sample prep for up to 96 input samples. A user-input-specified volume of reducing agent is added to samples on the heater-shaker at 60 degrees C followed by shaking at 1500 rpm for 30 seconds. After a 30 minute incubation, a user-input-specified volume of alkylating agent is added followed by shaking and incubation at room temperature. A second addition of reducing agent is followed by a series of incubations, shaking, bead binding, washes, digestion and recovery of digestion products to the final plate. Run-specific user input (number of samples, sample volume, reagent source volumes, liquid transfer volumes) is provided by csv file upload (see example file below).

Links:
* [example parameter input csv](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/057824/parameters_csv.csv)</br>
* [example sample position csv](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/057824/sample_positions.csv)</br>

![parameter input csv](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/057824/screenshot-parameters.png)</br>
![sample position csv](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/057824/screenshot-samplepositions.png)</br>

Values for CSV file input:
* SAMPLE COUNT  1-96
* V(Sample)  sample volume (ul)
* ACN CONC  50 or 70 (percent ACN)
* WORKING PLATE  nest_96_wellplate_100ul_pcr_full_skirt or redefinedbiorad_96_wellplate_200ul
* FINAL PLATE  nest_96_wellplate_100ul_pcr_full_skirt or redefinedbiorad_96_wellplate_200ul
* DIG VESSEL  opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical (if vessel is a 15 mL conical tube) or opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap (if vessel is 1.5 mL eppendorf snap-cap tube)
* V(EtOH) up to 50000 (uL)
* V(ACN) up to 50000 (uL)
* V(RED first time)  transfer volume for first RED transfer (uL)
* V(ALK)  transfer volume for ALK (uL)
* V(RED second time)  transfer volume for second RED transfer (uL)
* V(Bead Mixture)  transfer volume for bead mixture (uL)
* V(DIG)  transfer volume for DIG (uL)


---


### Labware
* [Opentrons Filter Tips for the P20 and P300] (https://shop.opentrons.com)
* [Opentrons 24-Tube Rack, 10-Tube Rack] (https://shop.opentrons.com/4-in-1-tube-rack-set/)
* [Nest 1.5 mL Snap Cap Tubes] (https://shop.opentrons.com/nest-1-5-ml-microcentrifuge-tube/)
* [Nest 100 uL PCR Plate] (https://shop.opentrons.com/nest-0-1-ml-96-well-pcr-plate-full-skirt/)
* [NEST 195 mL Reservoir] (https://labware.opentrons.com/nest_1_reservoir_195ml?category=reservoir)



### Pipettes
* Opentrons single-channel P20 and single-channel P300 Gen2 Pipettes (https://shop.opentrons.com/pipettes/)



---


### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/057824/screenshot-deck.png)
</br>
</br>
**Slot 1**: Opentrons Magnetic Module with Working Plate (csv-specified 96-well PCR plate) </br>
**Slot 3**: Opentrons Heater-Shaker Module with Working Plate (csv-specified 96-well PCR plate on aluminum adapter) </br>
![heater shaker plate](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/057824/screenshot-hs.png)
</br>
</br>
**Slot 4**: Opentrons 10-Tube Rack with Falcon 50 mL and 15 mL conical tubes (EtOH, ACN and optionally DIG) </br>
![10-tube rack](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/057824/screenshot-10rack.png)
</br>
</br>
**Slot 5**: Opentrons 24-Tube Rack with Eppendorf 1.5 mL Snap Cap Tubes (Bead Mixture, ALK, RED, and optionally DIG) </br>
![eppendorf rack](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/057824/screenshot-eppendorfrack.png)
</br>
</br>
**Slot 2**: Opentrons 20 uL filter tips </br>
**Slots 6,7,11**: Opentrons 200 uL filter tips </br>
**Slot 8**: Empty Opentrons 200 uL filter tip rack (for tip parking) </br>




---

### Protocol Steps
1. The protocol will calculate and display V(ACN calculated) and V(BINDING) and will check to ensure that csv-specified volumes will not result in V(BINDING) and V(DIG) that would over-fill the working plate or final plate beyond capacity.
2. The protocol will pause and prompt the user to place the working plate on the heater-shaker.
3. The protocol will heat the heater shaker to 60 degrees C. Upon reaching the target temperature, V(RED first time) will be dispensed to the northern-side-wall of each sample-containing well of the working plate on the heater shaker by either the p20 single or p300 single followed by shaking at 1500 rpm for 30 seconds.
4. The OT-2 will wait for a 30 minute on-deck incubation (with passive cooling of the heater shaker initiated during the incubation).
5. The OT-2 will then wait for the necessary additional length of time needed for the target temperature to be reached (passive cooling).
6. V(ALK) will be dispensed to the southern-side-wall of each sample-containing well of the working plate on the heater shaker by either the p20 single or p300 single followed by shaking at 1500 rpm for 30 seconds and then another 30 minute incubation.
7. V(RED second time) will be dispensed to the eastern-side-wall of each sample-containing well of the working plate on the heater shaker by either the p20 single or p300 single followed by a 15 minute incubation.
8. V(Bead Mixture) will be dispensed to the western-side-wall of each sample-containing well of the working plate on the heater shaker by either the p20 single or p300 single followed by shaking at 1500 rpm for 30 seconds.
9. V(ACN calculated) will be dispensed to each sample-containing well of the working plate on the heater shaker by the p300 single with the tip dropped into a sample-specific location in the empty tip rack (for later reuse).
10. The heater shaker will perform nine iterations of (1500 rpm 30 sec, 100 rpm 90 sec).
11. The OT-2 will pause and prompt the user to relocate the working plate to the magnetic module.
12. After engaging magnets and waiting, the p300 single will discard bead pellet supernatants to the reservoir.
13. The p300 single and magnetic module will perform two washes of beads with 80 percent ethanol and one wash with 100 uL ACN (includes mixing and resuspension of beads in the ethanol or ACN).
14. V(DIG) will be top dispensed directly above (1 mm from side of the well) each washed bead pellet.
15. The OT-2 will pause and prompt the user to relocate the working plate back to the heater shaker.
16. The heater shaker will perform a single iteration of (1500 rpm 2 min, 1000 rpm sustained until the user signals readiness to stop heating and shaking by providing user input - by clicking "resume" in the OT app).
17. The OT-2 will pause and prompt the user to relocate the working plate back to the magnetic module.
18. After magnet engagement and waiting, the p300 single will transfer bead pellet supernatants (digestion products) to the corresponding well in the final plate.


### Process
1. Input your protocol parameters and csv files using the parameters section on this page, then download your protocol.
2. Upload your protocol file (.py extension) to the [OT App](https://opentrons.com/ot-app) in the `Protocol` tab.
3. Set up your deck and run labware position check using the OT App. For tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
4. Hit 'Run'.

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
057824
