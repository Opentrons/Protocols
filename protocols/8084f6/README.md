# Drug Screening

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Plate Filling

## Description
This protocol performs a one-to-one transfer from 4 96-well source PCR plates to 1 384-well destination plate using a multi-channel pipette. Mastermix is distributed from a PCR strip to each well of the destination plate before sample transfers.

---

You will need:
* [Biostrategy 96-well PCR plates # 26194](https://www.bio-strategy.com/)
* [Biostrategy 384-well NX plate # 39694](https://www.bio-strategy.com/)
* [SSI 0.2ml 8 strip PCR tubes, flat caps # 313500 (seated)](https://www.ssibio.com/pcr/strip-pcr-tubes-and-caps)
* [Opentrons P10 multi-channel electronic pipette](https://shop.opentrons.com/collections/ot-2-pipettes/products/8-channel-electronic-pipette)
* [Opentrons 10ul pipette tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-10ul-tips)

### Robot
* [OT-2](https://opentrons.com/ot-2)

## Process
1. Upload your protocol parameters.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Mastermix is distributed from the PCR to each well of the 384-well destination plate.
8. Source plate 1, column 1 rows A-H is transferred to destination plate column 1 rows A, C, E, G, I, K, M, O using multi channel pipette (spacing on 384-well plate is exactly have the spacing on 96-well plate).
9. Step 8 is repeated for source plate 1, columns 2-12 and destination plate, columns 2-12. New tips are used for each transfer.
10. Source plate 2, column 1 rows A-H is transferred to destination plate column 1 rows B, D, F, H, J, L, N, P using multi channel pipette.
11. Step 10 is repeated for source plate 2, columns 2-12 and destination plate, columns 2-12. New tips are used for each transfer.
12. Source plate 3, column 1 rows A-H is transferred to destination plate column 13 rows A, C, E, G, I, K, M, O using multi channel pipette (spacing on 384-well plate is exactly have the spacing on 96-well plate).
13. Step 12 is repeated for source plate 3, columns 2-12 and destination plate, columns 14-24. New tips are used for each transfer.
14. Source plate 4, column 1 rows A-H is transferred to destination plate column 13 rows B, D, F, H, J, L, N, P using multi channel pipette.
15. Step 14 is repeated for source plate 4, columns 2-12 and destination plate, columns 14-24. New tips are used for each transfer.

### Additional Notes
If you have any questions about this protocol, please contact the Protocol Development Team by filling out the [Troubleshooting Survey](https://protocol-troubleshooting.paperform.co/).

###### Internal
8084f6
