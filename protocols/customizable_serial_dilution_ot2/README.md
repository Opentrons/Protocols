# Customizable Serial Dilution for OT-2

### Author
[Opentrons](https://opentrons.com/)

## Categories
* Basic Pipetting
    * Dilution

## Description
With this protocol, you can do a simple serial dilution across a 96-well plate using either a single-channel or multichannel pipette. This can be useful for everything from creating a simple standard curve to a concentration-limiting dilution. For more information (including data from the Opentrons Lab and other considerations), please see our [Technical Note](https://s3.amazonaws.com/opentrons-protocol-library-website/Technical+Notes/Serial+Dilution+OT2+Technical+Note.pdf).

---

---

![serial dilution](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/customizable-serial-dilution/Customizable+Serial+Dilution+Illustration+LATEST+VERSION.jpg)

***Example Setup***

This protocol uses the inputs you define for "***Dilution Factor***" and "***Total Mixing Volume***" to automatically infer the necessary transfer volume for each dilution across your plate. For a 1 in 3 dilution series across an entire plate, as seen above:

-- Start with your samples/reagents in Column 1 of your plate. In this example, you would pre-add 150 uL of concentrated sample to the first column of your 96-well plate.

-- Define a ***Total Mixing Volume*** of 100uL, a ***Dilution Factor*** of 3, and set ***Number of Dilutions*** = 11.

-- Your OT-2 will add 100uL of diluent to each empty well in your plate. Then it will transfer 50uL from Column 1 between each well/column in the plate. 

-- "***Total mixing volume***" = transfer volume + diluent volume.

---

---


![Materials Needed](https://s3.amazonaws.com/opentrons-protocol-library-website/custom-README-images/customizable-serial-dilution/materials.png)

-- [Opentrons OT-2](http://opentrons.com/ot-2)

-- [Opentrons OT-2 Run App (Version 3.1.2 or later)](http://opentrons.com/ot-app)

-- 200uL or 300 uL Tiprack ([Opentrons tips suggested](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-300ul-tips-racks-9-600-tips))

-- [12-row automation-friendly trough](https://www.usascientific.com/12-channel-automation-reservoir.aspx)

-- Clear flat-bottom 96-well polystyrene 96-well plate

-- Diluent (Pre-loaded in row 1 of trough)

-- Samples/Standards (Pre-loaded in Column 1 of a standard flat-bottom 96-well plate)

---

---

### Time Estimate
* Varies. 2-5 minutes depending on pipette model chosen

## Process
1. Choose the pipette you want to use from the dropdown menu above. ***Note:*** Your pipette should be installed on the ***left mount*** of your OT-2.
2. Set your dilution factor.***Example:*** If you want a 1:2 ratio of sample to total reaction volume, you would set your dilution factor to 2.
3. Set your number of dilutions (max = 11)
4. Set your total mixing volume. (Total mixing volume = transfer volume + diluent volume). Be careful to make sure this number does not exceed the volume capacity of your plate. To see how this number is used, scroll to the example above.
5. Set your tip reuse strategy. ***Note:*** This defaults to no tip changes; adjust only if you want to change tips between each well.
6. Download your customized OT-2 Serial Dilution protocol using the blue "Download" button.
7. Upload into the Opentrons Run App and follow the instructions there to set up your deck and proceed to run!
8. Make sure to add diluent to the first row of your 12-row trough and load your desired samples/standards into column 1 of your plate before running your protocol in the run app!

###### Internal
Customizable Serial Dilution, v1

### Additional Notes
Please reference our [Technical Note](https://s3.amazonaws.com/opentrons-protocol-library-website/Technical+Notes/Serial+Dilution+OT2+Technical+Note.pdf) for more information about the expected output of this protocol, in addition to expanded sample data from the Opentrons lab. 

We understand that there are limitations to the use of this protocol, and we plan to make improvements soon. In the meantime, if you'd like to request a more complex dilution workflow, please use our [Protocol Development Request Form](https://opentrons-protocol-dev.paperform.co/). You can also download this Python file and modify it using our [API Documentation](https://docs.opentrons.com/). For additional questions about this protocol, please email support@opentrons.com.
