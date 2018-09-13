# Indirect ELISA

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Proteins & Proteomics
    * ELISA

## Description
This protocol allows the robot to perform indirect ELISA to detect anti-MOMP antibodies in serum and plasma of farm animals, and can be used for similar assays. Indirect ELISA is a two-step ELISA that involves binding process of primary antibody and labeled second antibody. Use the field labeled "Strip Number" below to define the number of strips you will be using in your experiment. You can input any number from 1-12.

### Robot
* [OT 2](https://opentrons.com/ot-2)

### Reagents
* IDvet Chlamydophila abortus Indirect Multi-species

## Process
1. Input desired number of strips to use in your experiment.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Transfer 90 uL dilution buffer to target strips.
8. Pause for 45-min incubation.
9. Empty target strips into liquid trash.
10. Wash strips with 300 uL of wash buffer 5 times.
11. Transfer 100 uL of conjugate secondary antibody to strips.
12. Pause for 30-min incubation.
13. Empty target strips into liquid trash.
14. Wash strips with 300 uL of wash buffer 5 times.
15. Transfer 100 uL of substrate to target strips.
16. Pause for 15-min incubation.
17. Transfer 100 uL stop solution to target strips.

###### Internal
ledvUIra
1055
