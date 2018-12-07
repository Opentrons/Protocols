# Fractional Factorial Designs

### Author
[Opentrons](http://www.opentrons.com/)

## Categories
* Sample Prep
    * Distribution

## Description
This protocol allows your robot to add up to 192 compounds from 96-deep well compound plates to a single 96-deep well experiment plate. The volume and destination location of each compound are defined in a CSV file input. See Additional Notes for more details on the CSV setup. Only two volumes will be accepted in the form of `1` and `-1`, each represents a volume you define in the custom fields below. In the protocol, `volume_positive_value` is the `-1` volume, and `volume_negative_value` is the `1` volume.

### Robot
* [OT-2](https://opentrons.com/ot-2)

### Modules

### Reagents

## Process
1. Input the volume represented by `1` (RANGE: 30-300 uL)
2. Input the volume represented by `-1` (RANGE: 1-10 uL)
3. Upload your CSV file.
4. Download your protocol.
5. Upload your protocol into the [OT App](https://opentrons.com/ot-app).
6. Set up your deck according to the deck map.
7. Calibrate your labware, tiprack and pipette using the OT App. For calibration tips, check out our [support article](https://support.opentrons.com/ot-2/getting-started-software-setup/deck-calibration).
8. Hit "Run".
9. Robot will distribute the `1` volume of compound 1 from well A1 of the deep well plate in slot 1 to the designated wells in output plate using the P300 single-channel pipette.
10. Robot will distribute the `-1` volume of compound 1 to the designed wells in output plate using the P10 single-channel.
11. Robot will repeat step 9-10 until the rest of the compounds defined are all distributed into the output plate.

### Additional Notes
![csv_layout](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/1360-dtu-biosustain/csv_example.png)

* Keep the headers

---

Placement of the compounds in the compound plates:  
(from the example above)    
1\. Adenine: well A1 in slot 1  
2\. Alanine: well A2 in slot 1  
3\. Ammonium sulfate: well A3 in slot 1     
...     
13\. Ferric Chloride: well B1 in slot 1
14\. Folic Acid: well in B2 in slot 1   
...     
repeat above for slot 2 starting at compound number 97

If you wish to skip a well in the compound plates, leave the corresponding row empty.

---

If you have any questions about this protocol, please contact protocols@opentrons.com.

###### Internal
8Sa3mm7H
1360
