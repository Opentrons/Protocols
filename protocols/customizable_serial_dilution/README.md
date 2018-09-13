# Customizable Serial Dilution

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Basic Pipetting
	* Dilution
		* Customizable Serial Dilution

## Description
With this protocol, you can do a simple serial dilution in a 96-well plate using either a single-channel or multichannel pipette on the left mount of your OT-2. This can be useful for everything from creating a simple standard curve to a concentration-limiting dilution.

Using the fields below, you can define your pipette, dilution factor, final volume (max: 200uL), and number of dilutions (maximum of 11 dilutions allowed). You can also define your tip reuse strategy. We set this protocol to reuse one set of tips through the dilution series, but you can change tip between each dilution if you prefer.

This protocol assumes that you have already loaded the samples/reagents that you wish to dilute in column 1 of a 96-well plate. You must also use a [12-row automation-friendly trough](http://www.eandkscientific.com/12-Column-Reservoir-Deep-Well-Divided-V-Bottom-252ml.html) as the source of your diluent for this protocol. We plan to expand this in the future. Please chat with us and let us know if you need more functionality/flexibility in this protocol, and we'll work with you to get it done!


### Time Estimate
* 2-5 minutes depending on pipette model chosen


### Reagents
* Diluent (Pre-loaded in row 1 of trough)
* Samples/Standards (Pre-loaded in Column 1 of 96-well plate)

## Process
1. Choose the pipette you want to use from the dropdown menu above. Note: Your pipette should be installed on the **left** mount of your OT-2.
2. Set your dilution factor.
3. Set your number of dilutions (max = 11)
4. Set your final volume (max = 200uL)
5. Set your tip reuse strategy (defaults to no tip changes; adjust if you want to change tips between each well.)
6. Place your 12-row trough on the deck as indicated in the deckmap. Make sure to add diluent to the first row of your 12-row trough.
7. Place your 96-well plate on the deck as indicated in the deckmap. Make sure to load your desired samples/standards into column 1 of your plate.
8. Download your customized OT-2 Serial Dilution protocol using the blue "Download" button.
2. Upload into the Opentrons Run App and hit run!

###### Internal
Customizable Serial Dilution, v1

### Additional Notes
We understand that there are limitations to the use of this protocol! We plan to make improvements soon. In the meantime, if you'd like to request a more complex dilution workflow, please use our [Protocol Development Request Form](https://opentrons-protocol-dev.paperform.co/). You can also download this Python file and modify it using our [API Documentation](https://docs.opentrons.com/). For questions about this protocol, please email support@opentrons.com.
