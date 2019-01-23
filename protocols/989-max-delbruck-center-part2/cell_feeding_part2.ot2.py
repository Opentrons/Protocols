from opentrons import labware, instruments
from otcustomizers import StringSelection

"""
Step 2: Adding Trypsin and Transferring to Eppendorf Tube
"""

tiprack_dict = {'p10': 'tiprack-10ul',
                'p50': 'tiprack-200ul',
                'p300': 'opentrons-tiprack-300ul'}

pipette_m = None
pipette_s = None


def pipette_setup(pipette_model, pipette_mount, tipracks):
    if pipette_model == 'p10-Single':
        pipette = instruments.P10_Single(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_model == 'p50-Single':
        pipette = instruments.P50_Single(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_model == 'p300-Single':
        pipette = instruments.P300_Single(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_model == 'p10-Multi':
        pipette = instruments.P10_Multi(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_model == 'p50-Multi':
        pipette = instruments.P50_Multi(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_model == 'p300-Multi':
        pipette = instruments.P300_Multi(
            mount=pipette_mount,
            tip_racks=tipracks)
    return pipette


def run_custom_protocol(
        cell_container: StringSelection(
            '24-well-plate', '96-flat')='96-flat',
        multi_pipette_model: StringSelection(
            'p10-Multi', 'p50-Multi', 'p300-Multi')='p300-Multi',
        multi_pipette_mount: StringSelection(
            'left', 'right')='left',
        single_pipette_model: StringSelection(
            'p10-Single', 'p50-Single', 'p300-Single')='p300-Single',
        single_pipette_mount: StringSelection(
            'left', 'right')='right',
        sample_num: int=96,
        old_media_volume: float=200,
        trypsin_volume: float=200,
        trypsin_wait_time: int=5,
        wash_volume: float=200,
        mix_times: int=3,
        new_media_volume: float=200):

    global pipette_m, pipette_s

    # labware setup
    old_plates = [labware.load(cell_container, '1')]
    new_plates = [labware.load(cell_container, '2')]
    tuberack_2ml = labware.load('opentrons-tuberack-2ml-eppendorf', '3')
    trough = labware.load('trough-12row', '4')
    tuberack_15ml = labware.load('opentrons-tuberack-15ml', '5')

    # reagent setup
    trypsin = tuberack_15ml.wells('A1')
    PBS = trough.wells('A1')
    media = trough.wells('A10')
    liquid_trash = trough.wells('A12')

    s_name = single_pipette_model.split('-')[0]
    m_name = multi_pipette_model.split('-')[0]

    # if using 24-well plate, only single channel pipette is loaded
    if cell_container == '24-well-plate':
        s_slots = ['6', '7', '8', '9', '10', '11']
    else:
        s_slots = ['10', '11']
        m_slots = ['6', '7', '8', '9']
        tipracks_m = [labware.load(tiprack_dict[m_name], slot)
                      for slot in m_slots]
        pipette_m = pipette_setup(
            multi_pipette_model, multi_pipette_mount, tipracks_m)
    tipracks_s = [labware.load(tiprack_dict[s_name], slot)
                  for slot in s_slots]
    pipette_s = pipette_setup(
        single_pipette_model, single_pipette_mount, tipracks_s)

    # define single-channel pipette loc
    s_old_locs = [well for plate in old_plates for well in plate.wells()][
        :sample_num]
    s_new_locs = [well for plate in new_plates for well in plate.wells()][
        :sample_num]
    dest = s_old_locs
    pipette = pipette_s

    # define multi-channel pipette loc if pipette_m is loaded
    if pipette_m:
        col_num = sample_num // 8 + (1 if sample_num % 8 > 0 else 0)
        m_old_locs = [col for plate in old_plates for col in plate.cols()][
            :col_num]
        dest = m_old_locs
        pipette = pipette_m

    # discard media from wells
    pipette.pick_up_tip()
    for loc in dest:
        pipette.transfer(old_media_volume, loc, liquid_trash, new_tip='never')
    pipette.drop_tip()

    # add trypsin to old plate
    pipette_s.pick_up_tip()
    for loc in s_old_locs:
        pipette_s.transfer(trypsin_volume, trypsin, loc.top(), new_tip='never')
    pipette_s.drop_tip()

    pipette_s.delay(minutes=trypsin_wait_time)

    # discard trypsin from old plate
    for loc in dest:
        pipette.transfer(trypsin_volume, loc.bottom(3), liquid_trash)

    # wash with PBS 3 times
    pipette.pick_up_tip()
    aspirate_tip_loc = pipette.current_tip()
    for cycle in range(3):
        # dispensing PBS
        if not pipette.tip_attached:
            pipette.pick_up_tip(aspirate_tip_loc)
        pipette.transfer(wash_volume, PBS, dest, new_tip='never')
        pipette.return_tip()
        if cycle == 0:
            pipette.pick_up_tip()
            dispense_tip_loc = pipette.current_tip()
        else:
            pipette.start_at_tip(dispense_tip_loc)
            pipette.pick_up_tip()
        # discarding PBS from wells
        for index, loc in enumerate(dest):
            pipette.transfer(wash_volume, loc, liquid_trash,
                             trash=False)

    # add more media
    # pipette moves in a circular motion in the well
    # mix with custom number of times
    for loc in dest:
        pipette.pick_up_tip()
        pipette.aspirate(new_media_volume, media)
        theta = 0.0
        while pipette.current_volume > 0:
            well_edge = loc.from_center(r=1.0, theta=theta, h=0.9)
            destination = (loc, well_edge)
            pipette.move_to(destination, strategy='direct')
            pipette.dispense(new_media_volume/10)
            theta += 0.314
        pipette.mix(mix_times, pipette.max_volume/2, loc)
        pipette.drop_tip()

    # transfer half of the dissociated colony to a 96-well plate and rest of it
    # goes to an eppendorf tube
    for source, dest in zip(s_old_locs, s_new_locs):
        pipette_s.transfer(
            new_media_volume/2, source, [dest, tuberack_2ml.wells('A1')])
