def run(ctx):

    plate = ctx.load_labware('biorad_96_wellplate_200ul_pcr', '1')
    tiprack300 = [ctx.load_labware('opentrons_96_tiprack_300ul','3')]

    #loop w/append
    plate.wells ()
    wells_row_order= []
    for row in plate.rows():
        for well in row:
            wells_row_order.append(well)
    print(wells_row_order)

    
   # list comprehension: comprehensive way of simplifying above code. Moving from outer into inner loop. No colons in list comprehension

   wells_row_order = [well for row in plate.rows() for well in row]
print(wells_row_order)



#list comprehensive example:
#
single_line_string = "FAS"
#
#multi line string via """ 3 quotes to open and close

ex_csv = """well,vol
A1,2.0
B4, 10.0

"""

#loop w/ append 2nd example
data = []
lines = ex_csv.split()
for line in lines:
    data.append(line.split(','))


#list comprehensive of 2nd example
data = [line.split(',') for line in ex_csv_splitline()]



