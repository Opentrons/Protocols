from opentrons import labware, instruments, robot

metadata = {
    'protocolName': 'Cell Culture',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

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
water = labware.load(reservoir_name, '3', 'Water').wells('A1')
dye = labware.load(reservoir_name, '4', 'dye').wells('A1')
tipracks = [labware.load('opentrons-tiprack-300ul', str(slot))
            for slot in range(5, 12)]

# instruments setup
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks)

tip_count = 0

dests = [[col[well_index] for col in destination.cols('4', to='21')]
         for well_index in range(2)]


def update_tip_count(num):
    global tip_count
    tip_count += num
    if tip_count == (len(tipracks) * 12):
        robot.pause("Tips have run out. Resume protocol after the tips have \
        been refilled.")
        print('refill')
        m300.reset_tip_tracking()
        tip_count = 0


def dispense_solution(volume, reagent, destinations):
    m300.set_flow_rate(dispense=150)
    for dest in destinations:
        m300.pick_up_tip()
        m300.aspirate(300, reagent)
        for well in dest:
            if m300.current_volume < volume:
                m300.aspirate(300, reagent)
            m300.dispense(volume, well.top(-6))
        m300.drop_tip()
    update_tip_count(1)


def remove_solution(volume, sources, trash_location):
    m300.set_flow_rate(dispense=300)
    for source in sources:
        for well in source:
            m300.transfer(volume, well.bottom(0.5), trash_location)
            update_tip_count(1)


def run_custom_protocol(
        supernatant_volume: float=50,
        water_volume: float=50,
        dye_volume: float=30,
        incubation_time: float=15):

    m300.start_at_tip(tipracks[0].cols('5'))
    remove_solution(supernatant_volume, dests, liquid_trash)
    new_tip = m300.get_next_tip()

    m300.start_at_tip(tipracks[0].cols('1'))
    dispense_solution(water_volume, water, dests)

    m300.start_at_tip(new_tip)
    remove_solution(water_volume, dests, liquid_trash)

    m300.start_at_tip(tipracks[0].cols('3'))
    dispense_solution(dye_volume, dye, dests)
