from opentrons import protocol_api
metadata = {
    'protocolName': 'Combo IC',
    'author': 'Abel.Tesfaslassie@opentrons.com',
    'description': 'Sterile Workflows',
    'apiLevel': '2.11'
}
def run(ctx):

    magdeck = ctx.load_module('magnetic module gen2', '1')
    plate = magdeck.load_labware('nest_96_wellplate_1000ul_pcr_full_skirt', 'my plate')
    tipracks = ctx.load_labware('opentrons_96_tiprack_300ul', '2')
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', '4', 'my reservoir')

    m300 = ctx.load_instrument ('p300_multi_gen2', 'left', tip_racks=[tipracks])

    #variable time!

    #accessing well a1, since all wells are identical we will evaluate the dimensions of it
    test_well = plate.wells()[0]
    radius = test_well.diameter/2
    buffer = reservoir.wells()[0]
    number_of_samples = 48
    number_columns = math.ceil(number_of_samples/8)

    #accessing samples in plate.wells through all number of samples, moving along column. helpful since we have multi channel 
    samples = plate.rows()[:number_of_columnsop]
    resuspend_volume = 150
    magdeck.engage(height=6.8)

    def wick(pip, well):
            #well.bottom() moves to bottom, move applies offset. Defines location
            move_location = well.bottom().move(Point(x=radius, y=0, z=3))
            #executes the movement 
            pip.move_to(move_location)

#to slow down the head speed of both pipettes. In a well slowing down and when moving out any excess liquid will adhere to liquid level
    def slow_withdraw(pip,well):
            
            #both A & Z denote two z axises 
            ctx.max_speed['A'] = 25
            ctx.max_speed['Z'] = 25
            Pip.move_to(well.top())

            #del deletes those speeds defined
            del ctx.max_speeds['A']
            del ctx.max_speeds['Z']
# Enumerate- index iterating over samples. Ex: i=0 sample =A1 , i=1 sample=A2, i=2 sample=A3.....
#code below outlines accessing wells over bead location (mag module)
        for i,s in enumerate(sample):
            print(i, s)
            #%
            if i % 2 == 0:
                    slide = 1

        #goes through sides 
            print(i,s)

            m300.pick_up_tip()
            m300.aspirate(resuspend_volume, buffer.center())
           #calls slow withdraw function
            slow_withdraw(m300, buffer)

            #definiting accessing bead location
            bead_location = s.bottom().move(Point(x=side*radius, z=1))
           #accessing locaiton
            m300.move_to(bead_location)
            m300.dispense(m300.current_volume, buffer.bottom(5))
            m300.mix(10, 0.8*resuspend_volume, bead_location)
            wick(m300, s)
            m300.blow_out(s.top(-1))
            m300.air_gap(20)
            m300.drop_tip()
 