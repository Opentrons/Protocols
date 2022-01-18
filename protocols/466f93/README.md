# LifeCell NIPT 35Plex HV Part I

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Sample Prep
	* DNA Library prep

## Description
This protocol performs the preparation of samples from tubes to plates. It takes in a CSV file and uses the it to load the labware and make the necessary liquid transfers. It can support up to 2 sample plates.

Explanation of parameters below:
* `Number of samples`: The number of DNA samples on your sample plate. Should be between 7 and 36.

---

### Labware
* [Bio-Rad 96 well 200 µL PCR plate](https://labware.opentrons.com/biorad_96_wellplate_200ul_pcr?category=wellPlate)

### Pipettes
* [P300 Single Channel GEN2](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)
* [P20 Single Channel GEN2](https://shop.opentrons.com/single-channel-electronic-pipette-p20/)

---

### Deck Setup

![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/459cc2/459cc2-layout.png)

### Reagent Setup
* Slot 1 Destination plate - This is where DNA sample gets mixed with end repair buffer and enzyme
* Slot 3 Magnetic module (Not used in part 1)
* Slot 4 DNA sample plate  - DNA samples
* Slot 5 200 µL Opentrons filter tips
* 12-well reservoir (not used in part 1)
* Slot 7 Yourgene cfDNA Library Prep Kit Library Preparation Plate I
* Slot 8 200 µL Opentrons filter tips
* Slot 10 20 µL Opentrons filter tips
* Slot 11 20 µL Opentrons filter tips

---

### Protocol Steps
1. Create a mastermix of End Repair buffer I and End Repair Enzyme 1 and dispense it into the unusued well B2 of Reagent Plate I (RP-I). The buffer and enzyme is mixed ten times each before the transfer.
2. 12.75 µL of each DNA sample is transferred to the Destination Plate in Slot 1
3. Transfer 2.25 µL of Mastermix from well B2 of RP-I to each sample well on the Destination Plate
4. Mix the sample and Mastermix on the Destination plate 10 times
5. Ask the user to pulse spin the destination plate and perform the repair reaction incubation in the thermocycler

### Process
1. Input your protocol parameters above.
2. Download your protocol and unzip if needed.
3. Upload your protocol file (.py extension) to the [OT App](https://opentrons.com/ot-app) in the `Protocol` tab.
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
6. Hit 'Run'.

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
466f93
