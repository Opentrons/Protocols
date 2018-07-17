from opentrons import labware, instruments

trough = labware.load('trough-12row', 10)
liquid_waste = labware.load('trough-12row', 6)
source_plate = labware.load('96-flat', 11)
target_plate = labware.load('96-flat', 9)
tuberack = labware.load('tube-rack-15_50ml', 4)
tiprack_200 = labware.load('tiprack-200ul', 7)
tiprack_10 = labware.load('tiprack-10ul', 8)

p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack_10])

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack_200])


def reverse_pipette(pipette, volume, source, target, liquid_trash):
    pipette.pick_up_tip()
    for i in target:
        pipette.aspirate(source)
        pipette.dispense(volume, i)
    pipette.blow_out(liquid_trash)
    pipette.drop_tip()


def run_custom_protocol(
    drug_volume: int=1,
    final_volume: int=250,
    media_DMSO_volume: int=107,
        ):
    
    dilution_volume = final_volume - media_DMSO_volume

    reverse_pipette(m300, 100, trough['A1'], source_plate.cols(),
                    liquid_waste[0])
    reverse_pipette(m300, 100, trough['A2'], source_plate.cols(1, length=10),
                    liquid_waste[0])

    m300.delay(minutes=2)

    p10.transfer(drug_volume,
                 tuberack.wells('A1', 'A2'),
                 tuberack.wells('A3', 'A4'),
                 mix_after=(10, 10), new_tip='always')

    p10.transfer(media_DMSO_volume, tuberack.wells('A3'),
                 source_plate.cols[11:1:-1])
    p10.transfer(media_DMSO_volume, tuberack.wells('A4'),
                 source_plate.cols('1'))
    p10.transfer(final_volume, tuberack.wells('A4'),
                 source_plate.cols('2'))

    m300.pick_up_tip()
    for i in range(1, 10):
        if i == 9:
            m300.transfer(dilution_volume, source_plate.cols(i),
                          liquid_waste[0], new_tip='never')
            m300.drop_tip()
        else:
            m300.transfer(dilution_volume, source_plate.cols(i),
                          source_plate.cols(i+1),
                          mix_after=(5, dilution_volume), new_tip='never')

    m300.delay(minutes=2)

    # Aspirate media from all wells of the target plate
    m300.transfer(200, target_plate.cols(), liquid_waste)

    m300.transfer(100, source_plate.cols(), target_plate.cols())

    m300.delay(minutes=4)
    m300.delay(minuates=24.5*60)

    reverse_pipette(m300, 100, trough['A3'], target_plate.cols(),
                    liquid_waste[0])
