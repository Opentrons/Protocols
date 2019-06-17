from opentrons import labware, instruments, modules

metadata = {
    'protocolName': 'PCR Preparation',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load labware and modules
tempdeck = modules.load('tempdeck', '1')
temp_plate = labware.load(
    'opentrons-aluminum-block-96-PCR-plate',
    '1',
    share=True
    )
tempdeck.set_temperature(4)
tempdeck.wait_for_temp()
pcr_plates = [labware.load(
                'biorad-hardshell-96-PCR',
                slot,
                'PCR plate ' + str(ind+1)
                )
              for ind, slot in enumerate(['2', '3', '5', '6'])]
trough = labware.load('trough-12row', '4')
tips50 = labware.load('opentrons-tiprack-300ul', '7')
tips10 = [labware.load('tiprack-10ul', slot)
          for slot in ['8', '9', '10', '11']]

# instruments
m10 = instruments.P10_Multi(mount='right', tip_racks=tips10)
m50 = instruments.P50_Multi(mount='left', tip_racks=[tips50])

# reagent setup
mastermixes = [chan for chan in trough.wells()[0:4]]


def run_custom_protocol(
    number_of_sample_columns: int = 12
):
    # column check
    if number_of_sample_columns > 12 or number_of_sample_columns < 1:
        raise Exception('Please specify between 1 and 12 sample columns.')

    # distribute mastermix
    for mm, plate in zip(mastermixes, pcr_plates):
        m50.distribute(
            22,
            mm,
            plate.columns()[0:number_of_sample_columns],
            disposal_vol=0
        )

    for plate in pcr_plates:
        for s, d in zip(temp_plate.columns()[0:number_of_sample_columns],
                        plate.columns()[0:number_of_sample_columns]):
            m10.pick_up_tip()
            m10.transfer(3, s, d, new_tip='never')
            m10.mix(5, 10, d)
            m10.blow_out(d)
            m10.drop_tip()
