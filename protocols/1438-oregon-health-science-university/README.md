# Drug Distribution in Triplicate

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Basic Pipetting
    * Distribution

## Description
This protocol allows your robot to distribute drug from a 2 mL Eppendorf tube in triplicate to a 96-well plate. See Additional Notes for tube rack and plate layout. You will need our [4-in-1 Tube Rack Set](https://shop.opentrons.com/collections/opentrons-tips/products/tube-rack-set-1) and the P50 single-channel pipette.

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Input your desired volume in the field above.
2. Download your protocol.
3. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
4. Set up your deck according to the deck map.
5. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
6. Hit "Run".
7. Robot will transfer drug from tube rack well A1 to plate well A1-A3.
8. Robot will transfer drug from tube rack well A2 to plate well A4-A6.
9. Robot will transfer drug from tube rack well A3 to plate well A7-A9.
10. Robot will transfer drug from tube rack well A4 to plate well B1-B3.
11. Robot will repeat step 7-11 until all the drugs in the tube rack have been distributed.


### Additional Notes
![layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1438-oregon-health-science-university/layouts.png)

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
6zZMhc4I
1438
