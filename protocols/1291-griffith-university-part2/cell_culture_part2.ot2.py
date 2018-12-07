from opentrons import labware, instruments, robot

microplate_name = 'greiner-384-square-1'
if microplate_name not in labware.list():
    labware.create(
        microplate_name,
        grid=(24, 16),
        spacing=(4.5, 4.5),
        diameter=3.7,
        depth=11.5)

# labware setup
destination = labware.load(microplate_name, '2', 'Destination')
destination.properties['height'] = 14.5

master = labware.load(microplate_name, '1', 'Master')
master.properties['height'] = 14.5

control_1 = labware.load(microplate_name, '3', 'Control 1')
control_1.properties['height'] = 14.5

control_2 = labware.load(microplate_name, '5', 'Control 2')
control_2.properties['height'] = 14.5

tipracks = [labware.load('tiprack-10ul', str(slot))
            for slot in ['4', '6', '7', '8']]

# instruments setup
m10 = instruments.P10_Multi(
    mount='left',
    tip_racks=tipracks)


def run_custom_protocol(
        sample_volume: float=5,
        control_volume: float=5,
        control_column: str=1,
        number_of_destination_plates: int=4):

    for plate_num in range(number_of_destination_plates):
        # transfer samples
        sample_cols = [col for col in master.cols(plate_num*6, length=6)]
        for index, sample in enumerate(sample_cols, 1):
            for well_index in range(2):
                source = sample[well_index].bottom(0.5)
                dest = [col[well_index]
                        for col in destination.cols(index*3, length=3)]
                for well in dest:
                    well_edge = well.from_center(x=0.8, y=-0.8, z=0)
                    m10.transfer(
                        sample_volume,
                        source,
                        (well, well_edge),
                        blow_out=True)

        # transfer controls
        ctrl_1 = [well for well in control_1.cols(control_column)[:2]]
        ctrl_2 = [well for well in control_2.cols(control_column)[:2]]
        ctrl_1_dest = [destination.cols(col_num)[:2]
                       for col_num in ['2', '22']]
        ctrl_2_dest = [destination.cols(col_num)[:2]
                       for col_num in ['3', '23']]

        for dest in ctrl_1_dest:
            for source, well in zip(ctrl_1, dest):
                well_edge = well.from_center(x=0.8, y=-0.8, z=0)
                m10.transfer(control_volume, source, (well, well_edge))

        for dest in ctrl_2_dest:
            for source, well in zip(ctrl_2, dest):
                well_edge = well.from_center(x=0.8, y=-0.8, z=0)
                m10.transfer(control_volume, source, (well, well_edge))

        if not plate_num == (number_of_destination_plates-1):
            robot.pause("Put a new plate in slot 2 and refill all of the \
            tipracks.")
            m10.reset_tip_tracking()
