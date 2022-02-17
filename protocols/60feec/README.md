# DNA Dilution with CSV File

### Author
[Opentrons](https://opentrons.com/)

### Partner
[Partner Name](partner website link)

## Categories
* Sample Prep
	* Normalization

## Description
This protocol preps a 96 well plate with DNA and water to normalize concentration of all DNA samples. DNA concentration of sample will adjust the parameters of each sample's dilution requirements to meet the 0.8ng/uL target. Additionally, some samples may be low DNA concentration, meaning that some samples will not require to be diluted by the water - in this case we would then want to transfer only DNA to the dilution plate destination well.


Explanation of complex parameters below:
* `.CSV File`: Here, you should upload a .csv file formatted in the following way, being sure to include the header line:
![csv](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/60feec/Screen+Shot+2022-02-17+at+2.14.42+PM.png)
* `P20/P300 Mount`: Specify which mount (left or right) to host your P20 and P300 pipettes, respectively.

---


### Labware
* [NEST 12 Well Reservoir 195mL](https://shop.opentrons.com/nest-12-well-reservoirs-15-ml/)
* [NEST 0.1 mL 96-Well PCR Plate, Full Skirt](https://shop.opentrons.com/nest-0-1-ml-96-well-pcr-plate-full-skirt/)
* [Opentrons 20ul Filter tips](https://shop.opentrons.com/universal-filter-tips/)
* [Opentrons 200ul Filter tips](https://shop.opentrons.com/universal-filter-tips/)

### Pipettes
* [Opentrons P20 Single-Channel Pipette](https://shop.opentrons.com/pipettes/)
* [Opentrons P300 Single-Channel Pipette](https://shop.opentrons.com/pipettes/)

---

### Deck Setup
![deck layout](https://opentrons-protocol-library-website.s3.amazonaws.com/custom-README-images/60feec/Screen+Shot+2022-02-17+at+2.23.27+PM.png)

---

### Protocol Steps
1. Water is added to plate per csv input (same tip)
2. DNA is transferred to plate per csv input (change tip)

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
60feec
