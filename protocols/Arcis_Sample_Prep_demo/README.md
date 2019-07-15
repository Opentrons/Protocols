# Arcis Sample Prep Demo Kit (12rxn)

### Author
[Opentrons](http://www.opentrons.com/)

### Partner:
[Arcis Biotechnology](http://www.arcisbio.com/arcis-biotechnology-revolution/)

## Categories
* Sample Prep
    * Arcis

## Description
With this protocol, you can perform sample prep on any DNA or RNA-containing samples. This protocol follows the [Arcis Sample Prep Kit Instructions](http://www.arcisbio.com/wp-content/uploads/2019/04/Arcis-Sample-Prep-50-rxn-UFL002-Bulk-Kit-Rev-8.-12.18.pdf).

---
![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/materials.png)

* Arcis Sample Prep Demo Kit
* Opentrons OT-2
* Opentrons OT-2 Run App (Version 3.9.0 or later)
* Opentrons P300 Single-Channel Pipette
* Opentrons P10 or P50 Single-Channel Pipette
* Opentrons 4-in-1 Tube Rack Set
* 2-mL
* 300 uL and/or 10 uL Tiprack (Opentrons tips recommended)

---
![Setup](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/001-General+Headings/Setup.png)

Using the customization fields below, set up your protocol as follows:

* Left Pipette: A P300 single-channel pipette is required to be attached to the right mount. Select a second pipette, either a P10 (working volume: 1-10 uL) or P50 (5-50 uL) based on your extract volume if it is smaller than 30 uL.
* Sample Number: Customize the number of samples to run per protocol (max: 12 for this demo kit)
* Sample Container: Select the container type for your sample source
* Stage 1 Container: Select the container type for your Stage 1 reaction
* Stage 2 Container: Select the container type for your Stage 2 reaction
* Extract Volume: Specify the volume from Stage 1 reaction to be extracted for Stage 2 reaction
* Extract/Reagent 2 Ratio: Specify the Stage 1 Reaction to Reagent 2 volume ratio for Stage 2 reaction


Make sure to add reagents to your labware before placing it on the deck! You can see where to place your reagents below.


![Setup](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/Arcis_Sample_Prep/reagent_setup.png)

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Reagents

## Process
1. Select all desired settings according to the "Setup" section above to create your customized protocol.
2. Download your customized OT-2 protocol using the blue "Download" button.
3. Upload your protocol file into the [OT App](https://opentrons.com/ot-app) and follow the instructions there to set up your deck and proceed to run.
4. Make sure to add reagents to your labware before placing it on the deck! You can see where to place your reagents in the "Setup" section above.
5. Robot will transfer 150 uL of Reagent 1 to each well in the Stage 1 Plate in slot 2.
6. Robot will transfer (Extract volume x Reagent 2 Ratio) uL of Reagent 2 to each well in the Stage 2 Plate in slot 3.
7. Robot will transfer 90 uL of sample from Sample Plate in slot 1 to Stage 1 Plate and incubate for one minute.
8. Robot will transfer (Extract volume) uL of Stage 1 reaction to Stage 2 Plate.



### Additional Notes
Please reference the [Arcis instructions](http://www.arcisbio.com/wp-content/uploads/2019/04/Arcis-Sample-Prep-50-rxn-UFL002-Bulk-Kit-Rev-8.-12.18.pdf) for more information about this protocol.

If you have any questions about this protocol, please contact protocols@opentrons.com.
