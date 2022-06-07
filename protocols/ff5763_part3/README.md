# Illumina DNA Prep Part 3, Amplify Tagmented DNA

### Author
[Opentrons](https://opentrons.com/)

## Categories
* NGS Library Prep
  * Illumina DNA Prep

## Description
This is part three of a five part protocol for the [Illumina DNA Prep kit](https://www.illumina.com/products/by-type/sequencing-kits/library-prep-kits/nextera-dna-flex.html)

[Part 1](https://develop.protocols.opentrons.com/protocol/ff5763)

[Part 2](https://develop.protocols.opentrons.com/protocol/ff5763_part2)

[Part 4](https://develop.protocols.opentrons.com/protocol/ff5763_part4)

[Part 5](https://develop.protocols.opentrons.com/protocol/ff5763_part5)

Part 3: Amplify Tagmented DNA
Supernatant is discarded from the sample plate on the magnetic module into the liquid trash in slot 6

40ul of PCR Master Mix is added to the samples from slot 5 well 2

Samples are moved from magnetic module deep well plate to thermocycler plate in slot 2 before being centrifuged. Index adapters are added to the samples and mixed. The sample plate in slot 2 is moved to an off-deck thermocycler for a pre-programed PCR cycle as outlined in the Illumina DNA Prep reference material.

Explanation of complex parameters below:
* `Number of Samples`: Total number of samples from 1 to 48

---

### Modules
* [Temperature Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/tempdeck)
* [Magnetic Module (GEN2)](https://shop.opentrons.com/collections/hardware-modules/products/magdeck)

### Labware
* Custom 96 Well Plate with AB Gene and NEST 96 well plate with samples, slot 2
* [NEST 2ml Deep Well Plate](https://shop.opentrons.com/nest-2-ml-96-well-deep-well-plate-v-bottom/) on Magnetic Module in slot 4
* [NEST 12-Well 15ml Reservoir](https://shop.opentrons.com/nest-12-well-reservoirs-15-ml/) in slot 5
* [NEST 195ml Reservoir](https://shop.opentrons.com/nest-1-well-reservoirs-195-ml/) in slot 6


### Pipettes
* [P300 Multi Channel](https://shop.opentrons.com/8-channel-electronic-pipette/)
* [P20 Multi Channel](https://shop.opentrons.com/8-channel-electronic-pipette/)

### Reagents
* PCR Master Mix in slot 5 well 2, 40ul per sample
* Index Adapters in slot 5 well 3, 10ul per sample

---

### Protocol Steps
1. Supernatant is removed from samples on magnetic module and disposed off in liquid trash in slot 6
2. 40ul PCR Master Mix from slot 5 well 2 is added to samples on magnetic module
3. Samples are moved to thermocycler compatible plate in slot 2
4. Samples are centrifuged for 3 seconds at 280 x g
5. 10ul index adapters from slot 5 well 3 is added to sample plate in slot 2 and mixed (10x with 40ul)


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
ff5763
