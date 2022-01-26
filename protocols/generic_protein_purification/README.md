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
* If the deck layout of a particular protocol is more or less static, it is often helpful to attach a preview of the deck layout, most descriptively generated with Labware Creator. Example:
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/bc-rnadvance-viral/Screen+Shot+2021-02-23+at+2.47.23+PM.png)

### Reagent Setup
* This section can contain finer detail and images describing reagent volumes and positioning in their respective labware. Examples:
* Reservoir 1: slot 5
![reservoir 1](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1ccd23/res1_v2.png)
* Reservoir 2: slot 2  
![reservoir 2](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/1ccd23/res2.png)

---

### Protocol Steps
1. This section should consist of a numerical outline of the protocol steps, somewhat analogous to the steps outlined by the user in their custom protocol submission.
2. example step: Samples are transferred from the source tuberacks on slots 1-2 to the PCR plate on slot 3, down columns and then across rows.
3. example step: Waste is removed from each sample on the magnetic module, ensuring the bead pellets are not contacted by the pipette tips.

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
