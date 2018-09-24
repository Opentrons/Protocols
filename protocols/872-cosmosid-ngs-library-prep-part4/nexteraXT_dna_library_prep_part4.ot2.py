from opentrons import labware, instruments

"""
Pool Libraries
"""
# labware setup
in_plate = labware.load('96-PCR-flat', '1')
tuberack = labware.load('tube-rack-2ml', '2')



def run_custom_protocol(
        number_of_samples: int=24,
        number_of_pools: int=1,
        pool_volume: int=5
        ):

    total_tips = number_of_samples * number_of_pools
    total_tiprack = total_tips // 96 + (1 if total_tips % 96 > 0 else 0)
    tipracks10 = [labware.load('tiprack-10ul', slot)
                  for slot in ['3', '4', '5', '6', '7', '8', '9', '10', '11'][
                  :total_tiprack]]

    p10 = instruments.P10_Single(
        mount='right',
        tip_racks=tipracks10)

    if number_of_samples <= 24:
        input = [well
                 for col in in_plate.cols('1', to='6')
                 for well in col.wells('A', to='D')][:number_of_samples]
    else:
        input = [well for well in in_plate.wells()][:number_of_samples]

    # Transfer each library to pooling tube(s)
    for tube in tuberack.wells(0, length=number_of_pools):
        p10.transfer(pool_volume, input, tube, new_tip='always')

run_custom_protocol(**{'number_of_samples': 96, 'number_of_pools': 3})
