from opentrons import labware, instruments

def create_container_instance(name, grid, spacing, diameter, depth, height,
                              volume=0, slot=None, label=None):
    from opentrons import robot
    from opentrons.containers.placeable import Container, Well
    from opentrons.data_storage import database

    if slot is None:
        raise RuntimeError('"slot" argument is required.')
    if label is None:
        label = name
    columns, rows = grid
    col_spacing, row_spacing = spacing
    custom_container = Container()
    well_properties = {
        'type': 'custom',
        'diameter': diameter,
        'height': depth,
        'total-liquid-volume': volume
    }

    for c in range(columns):
        for r in range(rows):
            well = Well(properties=well_properties)
            well_name = chr(r + ord('A')) + str(1 + c)
            coordinates = (c * col_spacing, r * row_spacing, 0)
            custom_container.add(well, well_name, coordinates)
            
    custom_container.properties['type'] = name
    custom_container.properties['height'] = height
    custom_container.get_name = lambda: label

    # add to robot deck
    if not in database.list_all_containers():
    	database.save_new_container(custom_container, name)
    robot.deck[slot].add(custom_container, label)

    return custom_container

## FIX AND DOUBLE CHECK DIMS
glassVials = create_container_instance(
    'solidBlue_5x10',                    # name of you container
    grid=(5, 10),                    # specify amount of (columns, rows)
    spacing=(18.4, 18.4),               # distances (mm) between each (column, row)
    diameter=11,                     # diameter (mm) of each well on the plate
    depth=50,                       # depth of tube
    height=70,                      # total height of container
    slot='2')                       # depth (mm) of each well on the plate

cuvetteTray = create_container_instance(
    'clearBlue_8x12',                    # name of you container
    grid=(8, 12),                    # specify amount of (columns, rows)
    spacing=(12, 15),               # distances (mm) between each (column, row)
    diameter=9,                     # diameter (mm) of each well on the plate
    depth=40,
    height=63.5,
    slot='3')                       # depth (mm) of each well on the plate

tiprack1 = labware.load('opentrons-tiprack-300ul', '1')
tiprack2 = labware.load('opentrons-tiprack-300ul', '2')

p50 = instruments.P50_Single(mount='left', tip_racks=[tiprack1, tiprack2])

# Clear Blue Set-up Locations
QC = cuvetteTray.wells('A1')
BuffA = cuvetteTray.wells('A2')
urine1 = cuvetteTray.wells('A3')
urine2 = cuvetteTray.wells('A4')
intstd1 = cuvetteTray.wells('A5')
intstd2 = cuvetteTray.wells('A6')
intstd3 = cuvetteTray.wells('A7')

conc_1000 = cuvetteTray.wells('C1')
conc_200 = cuvetteTray.wells('C2')
conc_20 = cuvetteTray.wells('C3')

# Solid blue set up
QChigh1 = glassVials.wells('A1')
QChigh2 = glassVials.wells('A2')
QClow1 = glassVials.wells('C1')
QClow2 = glassVials.wells('C2')


def run_custom_protocol(QC_Conc1000: float=100.0,
						BuffA_Conc1000: float=100.0,
						urine_Conc1000: float=100.0,
						urine_Conc200: float=800.0,
						urine_Conc20: float=800.0,
						dilute_Conc200by1000: float=200.0,
						dilute_Conc20by200: float=100.0,
						QC_highvol: float=800.0,
						QC_lowvol: float=800.0,
						std3_vol: float=50.0,
						add_Conc200: float=400.0,
						add_Conc20: float=400.0):
    p50.transfer(QC_Conc1000, QC, conc_1000, new_tip='once')
    p50.transfer(BuffA_Conc1000, BuffA, conc_1000, new_tip='always')
    p50.transfer(urine_Conc1000, urine1, conc_1000, new_tip='always')
    p50.pick_up_tip()
    p50.transfer(urine_Conc200, urine1, conc_200, new_tip='never')
    p50.transfer(urine_Conc20, urine2, conc_20, new_tip='never')
    p50.drop_tip()
    p50.transfer(dilute_Conc200by1000, conc_1000, conc_200, new_tip='always')
    p50.transfer(dilute_Conc20by200, conc_200, conc_20, new_tip='always')

    p50.pick_up_tip()
    p50.transfer(QC_highvol, intstd1, QChigh1, new_tip='never')
    p50.transfer(QC_highvol, intstd1, QChigh2, new_tip='never')
    p50.transfer(QC_lowvol, intstd2, QClow1, new_tip='never')
    p50.transfer(QC_lowvol, intstd2, QClow2, new_tip='never')
    p50.drop_tip()

    p50.pick_up_tip()
    QCs = [QChigh1, QChigh2, QClow1, QClow2]
    p50.transfer(std3_vol, intstd3, QCs, new_tip='never')
    p50.drop_tip()

    p50.transfer(add_Conc200, conc_200, QChigh1, new_tip='always')
    p50.transfer(add_Conc200, conc_200, QChigh2, new_tip='always')
    p50.transfer(add_Conc20, conc_20, QClow1, new_tip='always')
    p50.transfer(add_Conc20, conc_20, QClow2, new_tip='always')
