from opentrons import labware, instruments, robot

microplate_name = 'greiner-384-square-1'
if microplate_name not in labware.list():
    labware.create(
        microplate_name,
        grid=(24, 16),
        spacing=(4.5, 4.5),
        diameter=3.7,
        depth=11.5)

reservoir_name = 'biotix-reservoir'
if reservoir_name not in labware.list():
    labware.create(
        reservoir_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=72,
        depth=23)

# labware setup
destination = labware.load(microplate_name, '2', 'Destination')
destination.properties['height'] = 14.5

liquid_trash = labware.load(reservoir_name, '1', 'Liquid Trash').wells('A1')
water = labware.load(reservoir_name, '3', 'Water').wells('A1').bottom(-4)
dye = labware.load(reservoir_name, '4', 'dye').wells('A1').bottom(-4)
tipracks = [labware.load('opentrons-tiprack-300ul', str(slot))
            for slot in range(5, 12)]

# instruments setup
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks)

tip_count = 0

dests = [col[well_index]
         for well_index in range(2)
         for col in destination.cols('2', to='23')]

dispense_dests = [[col[well_index].top(-4)
                  for col in destination.cols('2', to='23')]
                  for well_index in range(2)]


def dispense_solution(volume, reagent, destinations, dispense_flow_rate):
    m300.set_flow_rate(dispense=dispense_flow_rate)
    for dest in destinations:
        m300.pick_up_tip()
        m300.distribute(volume, reagent, dest, disposal_vol=0, new_tip='never')
        m300.drop_tip()


def remove_solution(volume, sources, trash_location):
    m300.start_at_tip(tipracks[0].cols('1'))
    m300.set_flow_rate(dispense=300)
    for index, source in enumerate(sources):
        if index == 22:
            m300.start_at_tip(tipracks[2].cols('1'))
        m300.transfer(volume, source.bottom(0.5), trash_location)


def run_custom_protocol(
        dispense_flow_rate: float=100,
        supernatant_volume: float=50,
        water_volume: float=50,
        dye_volume: float=30):

    remove_solution(supernatant_volume, dests, liquid_trash)

    m300.start_at_tip(tipracks[4].cols('1'))

    dispense_solution(water_volume, water, dispense_dests, dispense_flow_rate)

    robot.pause("Refill tip racks in slot 5, 6, 7, and 8 before resuming. \
Remove the first row of tips in slot 5, and 6, remove the last row in slot 7, \
and 8.")

    remove_solution(water_volume, dests, liquid_trash)

    m300.start_at_tip(tipracks[4].cols('3'))
    dispense_solution(dye_volume, dye, dispense_dests, dispense_flow_rate)
