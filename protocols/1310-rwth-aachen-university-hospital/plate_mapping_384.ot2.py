from opentrons import labware, instruments

# labware setup
master_plate = labware.load('384-plate', '5')
tipracks = [labware.load('tiprack-10ul', slot)
            for slot in ['7', '9', '10', '11']]

# instrument setup
p10 = instruments.P10_Multi(
    mount='left',
    tip_racks=tipracks)


def run_custom_protocol(
        number_of_destination_plates: int=6,
        transfer_volume: float=1):

    dest_plates = [labware.load('384-plate', slot)
                   for slot in ['1', '2', '3', '4', '6', '8']][
                   :number_of_destination_plates]

    sources = [well
               for col in master_plate.cols()
               for well in col.wells('A', 'B')]

    for source_well in sources:
        name = source_well.get_name()
        dests = [plate.wells(name) for plate in dest_plates]
        p10.distribute(transfer_volume, source_well, dests)
