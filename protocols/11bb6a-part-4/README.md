# Quarter Volume Library Prep Step 4: Adapter Ligation

### Author
[Opentrons](https://opentrons.com/)



# Opentrons has launched a new Protocol Library. This page won’t be available after March 31st, 2024. [Submit a request](https://docs.google.com/forms/d/e/1FAIpQLSdYYp9QCKow4nn0KlCVsMS3HX0eJ0N9O7-erajKvcpT0lWbSg/viewform) to add this protocol to the new library.

## Categories
* NGS Library Prep
	* NEBNext

## Description
This protocol uses multi-channel P20 and P300 pipettes to perform adapter ligation steps on 48-96 input samples. User-determined parameters are available for selection of the labware for the library prep plate, the reagent plate, and the labware for reagent tubes on the temperature module.

Links:
* [Part 1: Enzymatic Fragmentation and End Prep](http://protocols.opentrons.com/protocol/11bb6a)
* [Part 2: Sample Cleanup for Covaris Samples](http://protocols.opentrons.com/protocol/11bb6a-part-2)
* [Part 3: End Prep](http://protocols.opentrons.com/protocol/11bb6a-part-3)
* [Part 4: Adapter Ligation](http://protocols.opentrons.com/protocol/11bb6a-part-4)
* [Part 5: Size Selection](http://protocols.opentrons.com/protocol/11bb6a-part-5)
* [Part 6: Clean Up](http://protocols.opentrons.com/protocol/11bb6a-part-6)
* [Part 7: PCR Enrichment](http://protocols.opentrons.com/protocol/11bb6a-part-7)
* [Part 8: Sample Clean Up](http://protocols.opentrons.com/protocol/11bb6a-part-8)
* [Part 9: Fragment Analyzer](http://protocols.opentrons.com/protocol/11bb6a-part-9)
* [Part 10: Pooling According to Concentration](http://protocols.opentrons.com/protocol/11bb6a-part-10)

---


### Labware
* [Opentrons Filter Tips for the P20 and P300] (https://shop.opentrons.com)
* [Opentrons Temperature Module] (https://shop.opentrons.com/modules/)
* [Selected 96-well PCR plate] ([see parameter dropdown list below] https://labware.opentrons.com/)
* [Selected aluminum block and tube combination] ([see parameter dropdown list below] https://labware.opentrons.com/)


### Pipettes
* Opentrons 8-channel P20 and P300 Gen2 Pipettes (https://shop.opentrons.com/pipettes/)

### Reagents
* [NEBNext® Ultra™ II DNA Library Prep Kit for Illumina, Catalog # E7645S / E7645L] (https://international.neb.com/products/e7645-nebnext-ultra-ii-dna-library-prep-kit-for-illumina#Product%20Information)
* [NEBNext® Ultra™ II FS DNA Library Prep Kit for Illumina, Catalog # E7805S / E7805L] (https://international.neb.com/products/e7805-nebnext-ultra-ii-fs-dna-library-prep-kit-for-illumina#Product%20Information)

---

### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/11bb6a/screenshot4-deck.png)
</br>
</br>
**Slot 1**: Opentrons Temperature Module with dropdown-selected aluminum block and tube combination </br>
![tempmod layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/11bb6a/screenshot4-tempmod.png)
</br>
</br>
**Slot 3**: Library Prep Plate (dropdown-selected 96-well PCR plate) </br>
**Slot 6**: Reagent Plate (dropdown-selected 96-well PCR plate) </br>
**Slot 9**: Magnetic Module empty </br>
**Slot 8**: Opentrons 200 uL filter tips </br>
**Slots 7, 10, 11**: Opentrons 20 uL filter tips </br>


---

### Protocol Steps
1. Set up - be sure to pre-cool the Temperature Module to 4 degrees C using settings in the OT app prior to running this protocol.
2. The protocol will alert the user to ensure reagents are present on deck in sufficient volume.
3. The p300 multi will use a single tip on the rear-most channel to pre-mix the ligation mix, deliver ligation mix to the mix tube, then deliver enhancer to the mix tube, mix, and deliver the mixture to the second column of the reagent plate.
4. The p20 multi will deliver adapter to wells of the library prep plate.
5. Using the second column of the reagent plate as source, the p20 multi will deliver the mixture to wells of the library prep plate, then mix.
6. The OT-2 will pause for incubation steps in an off-deck thermocycler.
6. The p20 multi will deliver User dilution to wells of the library prep plate followed by a mix.
6. Proceed with incubation on off-deck thermocycler, then either part-5 or part-6.

### Process
1. Input your protocol parameters using the parameters section on this page, then download your protocol.
2. Upload your protocol file (.py extension) to the [OT App](https://opentrons.com/ot-app) in the `Protocol` tab.
3. Set up your deck and run labware position check using the OT App. For tips, check out our [support articles](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2).
4. Hit 'Run'.

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
11bb6a-part-4
