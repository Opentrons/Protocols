# Illumina DNA Prep with Enrichment: Part 2 - Clean Up and Pool Libraries, Hybridize and Capture Probes, Amplify Enriched Library, Clean Up Enriched Library

### Author
[Opentrons](https://opentrons.com/)


# Opentrons has launched a new Protocol Library. This page won’t be available after March 31st, 2024. [Submit a request](https://docs.google.com/forms/d/e/1FAIpQLSdYYp9QCKow4nn0KlCVsMS3HX0eJ0N9O7-erajKvcpT0lWbSg/viewform) to add this protocol to the new library.

## Categories
* NGS Library Prep
     * Illumina DNA Prep with Enrichment

## Description
Part 2 of 2: Clean Up and Pool Libraries, Hybridize and Capture Probes, Amplify Enriched Library, Clean Up Enriched Library

Links:
* [Part 1: Tagmentation, Clean Up, Amplify Tagmented DNA](http://protocols.opentrons.com/protocol/4ee4d6)
* [Part 2: Clean Up and Pool Libraries, Hybridize and Capture Probes, Amplify Enriched Library, Clean Up Enriched Library](http://protocols.opentrons.com/protocol/4ee4d6-part2)
* [Protocol](https://s3.amazonaws.com/pf-upload-01/u-4256/0/2021-03-24/dw03wwr/Opentron%20protocol.docx)

With this protocol, your robot can perform the Illumina DNA Prep with Enrichment protocol described by the [Illumina DNA Prep with Enrichment Reference Guide](https://support.illumina.com/sequencing/sequencing_kits/illumina-dna-prep-with-enrichment/documentation.html).

This is part 2 of the protocol, which includes the steps (1) Clean Up and Pool Libraries (2) Hybridize and Capture Probes (3) Amplify Enriched Library and (4) Clean Up Enriched Library.

The first clean up uses a double-sided bead purification for consistently narrow fragment size distribution. Up to 12 libraries with unique indexes are combined into one pool. Streptavidin magnetic beads are used to capture probes hybridized to target sequences. The enriched library is then amplified by PCR.

## Protocol Steps

Set up: Set the block temperature for the thermocycler module to 10 degrees Celsius by using settings in the OT app. Place reagents in the reservoir and aluminum block in deck slots 2 and 3 as shown [Protocol](https://s3.amazonaws.com/pf-upload-01/u-4256/0/2021-03-24/dw03wwr/Opentron%20protocol.docx).

The OT-2 will perform the steps as shown [Protocol](https://s3.amazonaws.com/pf-upload-01/u-4256/0/2021-03-24/dw03wwr/Opentron%20protocol.docx).

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

To purchase tips, reagents, or pipettes, please visit our [online store](https://shop.opentrons.com/) or contact our sales team at [info@opentrons.com](mailto:info@opentrons.com)

* [Opentrons OT-2](https://shop.opentrons.com/collections/ot-2-robot/products/ot-2)
* [Opentrons OT-2 Run App (Version 3.19.0 or later)](https://opentrons.com/ot-app/)
* [Opentrons Single-Channel p300 and p20 Pipettes](https://shop.opentrons.com/collections/ot-2-pipettes/products/single-channel-electronic-pipette)
* [Opentrons Tips for the p20 and p300 pipettes](https://shop.opentrons.com/collections/opentrons-tips)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

### Deck Setup
* Opentrons Temperature Module (Deck Slot 9)
* Opentrons Magnetic Module (Deck Slot 6)
* Opentrons p300 tips (Deck Slot 5)
* Opentrons p20 tips (Deck Slot 4)
* Opentrons Thermocycler Module (Deck Slots 7,8,10,11)
* reagents block (opentrons_24_aluminumblock_nest_2ml_snapcap) (Deck Slot 3)
* reagents reservoir (nest_12_reservoir_15ml) (Deck Slot 2)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Reagents
* [Illumina DNA Prep with Enrichment Kit](https://support.illumina.com/sequencing/sequencing_kits/illumina-dna-prep-with-enrichment/documentation.html)
* [Illumina TruSight Cardio Oligos (Ref. 20029229)]
* [Illumina DNA Prep LP with Enrichment (S) Tag) (Ref. 20025524)]

## Process
1. Input your number of samples (up to 12).
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map below.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
4ee4d6-part2
