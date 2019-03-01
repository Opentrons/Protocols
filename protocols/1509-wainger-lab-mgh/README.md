# Protein Quantification Preparation

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Proteins & Proteomics
    * PCR preparation

## Description
This protocol performs a series of liquid transfers and disposals on a 12-row trough and 96-well flat PCR plate using an 8-channel p300 pipette. The program pauses for a manual step in the middle of the protocol and prompts the user to reload the labware and resume after the manual step is completed. Note that this protocol uses a large number of 300µl tips throughout the transfers, and 6 tip racks will need to be loaded to run. Note that all liquid disposals will go to the default trash in slot 12.

---

You will need:
* [p300 Multi-channel pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette?variant=5984202457117)
* [Opentrons 300µl Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips)
* [12-row trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)
* Standard 96-well flat PCR plate

### Time Estimate
30 minutes

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents
* 1x HBSS
* 0.1% Triton X-100

## Process
1. Download your protocol.
2. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
3. Set up your deck according to the deck map.
4. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
5. Hit "Run".
6. 180µl are removed from each sample well in the 96-well plate and disposed.
7. 60µl are added from trough column 1 to all wells.
8. The program pauses for the user to perform a manual step. The user is prompted to resume whenever the labware is reloaded on the deck.
9. 70µl are removed from all wells and disposed.
10. 60µl are added from trough column 1 to all wells.
11. 140µl are added from trough column 4 to all wells. This is repeated for trough columns 5-12.
12. 150µl are removed from all wells and disposed.
13. Steps 11 and 12 are repeated once.
14. 60µl are added from trough column 3 to all wells.

### Additional Notes
For further questions or inquiries, please reach out to protocols@opentrons.com.

###### Internal
jh40dqpv  
1509
