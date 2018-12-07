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
water = labware.load(reservoir_name, '3', 'Water').wells('A1')
dye = labware.load(reservoir_name, '4', 'dye').wells('A1')
tipracks = [labware.load('opentrons-tiprack-300ul', str(slot))
            for slot in range(5, 12)]

# instruments setup
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks)

tip_count = 0

dests = [col[well_index]
         for col in destination.cols()
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
    m300.pick_up_tip()
    for dest in destinations:
        well_edge = dest.center()
        m300.transfer(volume, reagent, (dest, well_edge), new_tip='never')
        m300.blow_out((dest, well_edge))
    m300.drop_tip()
    update_tip_count(1)


def remove_solution(volume, sources, trash_location):
    m300.set_flow_rate(dispense=300)
    for source in sources:
        well_edge = source.from_center(x=0.8, y=-0.8, z=-0.9)
        m300.transfer(volume, (source, well_edge), trash_location)
        update_tip_count(1)


def remove_solution_using_same_tip(volume, sources, trash_location):
    m300.set_flow_rate(dispense=300)
    consolidate_dest = [(source, source.from_center(x=0.8, y=-0.8, z=-0.9))
                        for source in sources]
    m300.consolidate(volume, consolidate_dest, trash_location)
    update_tip_count(1)


def run_custom_protocol(
        supernatant_volume: float=50,
        water_volume: float=50,
        dye_volume: float=30,
        incubation_time: float=15):

    remove_solution(supernatant_volume, dests, liquid_trash)

    dispense_solution(water_volume, water, dests)

    remove_solution(water_volume, dests, liquid_trash)

    dispense_solution(dye_volume, dye, dests)

    m300.delay(minutes=incubation_time)

    remove_solution(dye_volume, dests, liquid_trash)

    dispense_solution(water_volume, water, dests)

    remove_solution_using_same_tip(water_volume, dests, liquid_trash)

    dispense_solution(water_volume, water, dests)
