# Generic protein purification protocol

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Broader Category
	* Subcategory (can be the name of a kit when applicable)

## Description

The generic protein purification is a flexible protocol that starts from bacterial
media ready for lysis on a well plate. From there the protocol adds lysis buffer
and then proceeds to bind the target his-tagged proteins with nickel linked paramagnetic beads. After a variable amount of washes the user may choose to
elute the proteins using elution buffer, or with SDS buffer if the purpose is to
run the samples on a gel.

The user is given extensive control of the protocol from the parameters. Pipettes, labware, modules (i.e. temperature and magnetic modules), protocol steps, and volumes are examples of things that can be customized to the users specifications.

The protocol is based on Promega's MagneHis™ system, but should work for any other similar system.

---

### Modules
* [Temperature Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* [Magnetic Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

### Labware
* [Labware Library](https://labware.opentrons.com/)

### Pipettes
* [Opentrons Pipettes](https://opentrons.com/pipettes/)

### Reagents
* [MagneHis™ Protein Purification System](https://www.promega.com/products/protein-purification/protein-purification-kits/magnehis-protein-purification-system/?catNum=V8500#protocols)

---

### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/generic_protein_purification/deck.jpg)

### Reagent Setup
![Reagent reservoir](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/generic_protein_purification/deck.jpg)

---

### Protocol Steps
The protocol is based on [MagneHis protein purification protocol](https://www.promega.com/-/media/files/resources/protocols/technical-manuals/0/magnehis-protein-purification-system-protocol.pdf?rev=cbf49f7cf6fa4696b965c92c1f8e9c72&sc_lang=en)
1. Bacterial lysis: Lysis buffer is added to all the sample wells. If the DNAse step is activated DNAse will be added to each well as well. If it's not activated DNAse I should be added to the lysis buffer by the user before running the protocol (1 µL per mL of bacterial media)
2. The protocol is paused to allow the user to shake the sample plate for 10-20 minutes at room temperature for the lysis reaction to complete
3. Binding: The paramagnetic beads are added to the samples, along with sodium chloride, if desired. The user has an option to pause the protocol before this step in order to vortex the beads in order to resuspend them. The user may also specify a number of mixes with the pipettes to help homogenize the solution.
4. The beads are washed with wash buffer (and optionally NaCl) and the supernatant is removed while the magnets on the magnetic module are engaged. This is repeated as many times as the user wants.
5. Elution: Finally the wash supernatant is removed while the magnets are engaged and elution buffer (or optionally: SDS buffer replaces the EB if the user desires to run the samples on a gel) is added. The bead supernatant is transferred to the target plate.

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
generic_protein_purification
